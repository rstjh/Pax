# Pax — Design Document

Pax ("peace" in Latin) is a web application for planning and evaluating courses of
action in combined cyber–physical military missions. It scores the risk of assigning
effects (DESTROY, DISRUPT, SEIZE, …) to mission assets, models how a hostile force is
likely to respond, and recommends courses of action using game-theoretic analysis.
It is designed to sit alongside an external Command-and-Control (C2) system that owns
the authoritative mission/unit/system data.

---

## 1. Architecture Overview

Pax is two independently-built applications plus a database, run as three containers
via Docker Compose, with an optional fourth party — the external C2 REST API — that
several backend features depend on.

```
                 browser
                    │
        ┌───────────▼──────────────┐
        │  pax-gui  (port 3000)    │   Angular 10 SPA, served by lite-server.
        │  src/webserver/          │   No bundler: TypeScript is compiled by plain
        └───────────┬──────────────┘   tsc and modules load in-browser via SystemJS.
                    │  XHR (CORS, absolute http://localhost:8200 URLs)
        ┌───────────▼──────────────┐
        │  pax  (port 8200)        │   Django 2.2 + Django REST Framework API.
        │  src/backend/            │   Swagger docs at /swagger/ (drf-yasg).
        │   ├─ api/       (REST)   │
        │   └─ analytics/ (engine) │
        └─────┬───────────────┬────┘
              │ pymongo       │ requests (env var C2_REST)
   ┌──────────▼─────────┐   ┌─▼──────────────────────────┐
   │ pax-db (port 8210) │   │ external C2 REST API       │
   │ MongoDB, database  │   │ missions, entity/Unit,     │
   │ "PaxDB"            │   │ system/{id}, coa/…/task    │
   └────────────────────┘   └────────────────────────────┘
```

Key structural facts:

- **The two stacks share nothing at build time.** There is no monorepo tooling; the
  root `build.sh` is the only cross-cutting script (`up`/`down`/`stop`/`test`/`all`).
- **Frontend and backend are separate origins** (`:3000` vs `:8200`). The frontend
  builds absolute API URLs from `environment.API_BASE_URL` and the backend allows
  the GUI origin via `django-cors-headers` (`CORS_ALLOWED_ORIGINS` in `settings.py`).
- **Source is volume-mounted into the containers** (`docker-compose.yml` mounts
  `./backend/` → `/Pax/` and `./webserver/gui/` → `/gui/`), so code edits are live;
  Django's autoreloader restarts on backend changes.
- **MongoDB runs on the non-default port 8210** (`mongod --port 8210`), addressed by
  the env vars `DB_HOSTNAME`/`DB_PORT`/`DB_NAME`.

---

## 2. Key Components

### 2.1 Backend: REST API layer (`src/backend/api/`, `src/backend/Pax/`)

`Pax/urls.py` maps all routes under `/api/v1/` (version from `Pax/api_config.py`).
The main resources:

| Route (under `/api/v1/`) | View | Backing store |
|---|---|---|
| `risk_analysis/network/<systemId>/` | `NetworkRiskAnalysis` | request payload + `deviceNetwork` |
| `risk_analysis/system/<systemId>/` | `SystemRiskAnalysis` | C2 system data + Mongo |
| `risk_analysis/task_dependency/<systemId>/` | `TaskDependencyRiskAnalysis` | C2 + Mongo |
| `risk_analysis/compare_system/<systemId>/` | `CompareSystemRiskAnalysis` | C2 + Mongo |
| `effects/` | `EffectsView` | `effects` collection |
| `hostile_response/`, `hostile_response/<effect>/` | `HostileResponsesView`, `HostileResponseDetailView` | `hostile_response` collection |
| `action_list/all/<force>/`, `action_list/type/<force>/<effect>/<type>/` | `ActionListForceDetail`, `ActionListForceEffectDetail` | `action_list` collection |
| `action_templates/`, `action_instances/` | template/instance views | `actionTemplates`, `actionInstances` |
| `course_of_action/generate/` | `GenerateCoursesOfAction` | `action_list` + C2 |
| `system/mission_time/<systemId>/` | `SystemMissionTime` | C2 + analytics |
| `cvi/`, `cvi/<systemId>/` | `CVIView`, `CVISystemView` | `cviSystems` collection |
| `missions/`, `missions/<missionId>/` | `MissionsView`, `MissionIdView` | `missions` collection |
| `risk_appetite/<missionId>/` | `RiskAppetiteDetail` | `riskAppetite` collection |
| `reset/` | `ResetData` | drops/reseeds everything |

Two catch-alls close the URL conf: `/swagger/` + `/redoc/` (drf-yasg API docs) and a
SPA-fallback `IndexView` that serves an `index.html` template for any other path
(a leftover from a combined-deployment mode; in the split container setup the real
GUI is served by `pax-gui`, so this fallback just 500s — see §7).

**How the API talks to data.** Despite mongoengine being installed and `api/models/`
existing, the ORM is barely used: most views open a raw `pymongo.MongoClient` in
`__init__` and query collections directly. The classes in `api/models/` are DRF
`Serializer`s used for *request validation and Swagger schema generation only* —
they are never persisted through. Django's own `DATABASES` setting is intentionally
left unconfigured; the relational ORM is unused.

**External C2 integration.** `api/services/system_data.py`,
`api/views/c2_data_requestor.py`, `api/views/courses_of_action.py`, and several
analytics modules call the external C2 REST API via `requests`, with the host coming
from the `C2_REST` env var. Endpoints Pax expects a C2 system to serve:
`system/{systemId}`, `missions`, `missions/{missionId}`, `entity/Unit`,
`entity/Unit/{unitId}`, and `coa/mission/{missionId}/coa/{coaId}[/task[/{taskId}]]`.
Without a live C2, those code paths fail at runtime; the GUI degrades to
"No system data found on C2…".

### 2.2 Backend: analytics engine (`src/backend/analytics/`)

A plain-Python package (~27 modules, no Django dependency) implementing the risk
mathematics. Entry points called from `api/views/`:

- **`RiskAnalysis.py`** — orchestrates system-level analysis:
  `perform_system_risk_analysis` scores every asset, and the course-of-action
  comparison pipeline (`calculate_comparative_statics` →
  `remove_unattainable_strategies` → `calculate_dominated_strategies` →
  `calculate_recommended_strategy`) is a textbook game-theory reduction: enumerate
  strategies, drop unattainable/dominated ones, recommend what survives.
- **`SystemRisk.py` / `Risk.py`** — per-asset risk scoring. Combines vulnerability
  counts, threat levels, asset criticality/impact (`Criticality.py`), task-dependency
  success probabilities, unit capability, and time feasibility into risk/likelihood
  scores with human-readable labels (`Config.py` maps scores → labels).
- **`HostileResponses.py` + `AttackDefenceGame.py`** — the adversarial model. For a
  friendly action it computes the hostile side's *most likely* and *most dangerous*
  counter-responses (lookup via the `hostile_response` collection) and the payoff
  values of the resulting attack/defence game.
- **`NetworkRisk.py` / `NetworkAnalysis.py` / `NetworkStatistics.py` /
  `NetworkVulnerabilities.py`** — device-network risk: graph-topological risk
  (networkx) over the `deviceNetwork` collection plus CVE-style vulnerability data
  (`utils/data/NetworkData.py` embeds a large CVE dataset).
- **`CourseOfActionGeneration.py` / `CoursesOfAction.py`** — builds candidate task
  trees (dependency-ordered) for a mission.
- **`Geolocation.py` / `UnitAnalysis.py` / `TimeTaken.py`** — physical feasibility:
  unit-to-asset distance, travel time, whether a task fits the mission window
  (`SystemAnalysis.exceeds_mission_time`).
- **`RiskAppetite.py`** — scores the questionnaire submitted from the Risk Appetite
  survey page.

Internally the modules share helpers (`SystemAnalysis.asset_from_id`,
`UnitAnalysis.get_unit_data`, `Config` label maps). Several modules query Mongo
and the C2 API directly rather than receiving data as arguments — the engine is
*not* a pure-function library.

### 2.3 Backend: data layer and seeding (`src/backend/utils/`)

MongoDB database `PaxDB` holds all state. Collections and their seed sources:

| Collection | Seed (in `utils/data/`) | Consumers |
|---|---|---|
| `effects` | `EffectData.py` | EffectsView, asset-info modal, `ActionAnalysis.action_force` |
| `hostile_response` | `HostileResponseData.py` (derived from `EffectData`) | Actions page CRUD, `HostileResponses.get_counter_effects` |
| `action_list` | `ActionListData.py` (derived from `EffectData`; 8 effects × 3 asset types) | Actions page tables/properties, `get_counter_actions`, `get_effect_likeliness`, COA generation |
| `cviSystems` | `CVISystemData.py` | CVI page, risk-graph system data |
| `deviceNetwork` | `NetworkData.py` (incl. embedded CVE data) | network risk analysis |
| `missions` | `MissionData.py` | mission dropdown, risk-graph |
| `units` | `UnitData.py` | unit lookups, hostile-unit modeling |
| `riskAppetite` | `RiskAppetite.py` | risk-appetite survey |
| `actionTemplates`, `actionInstances` | `ActionTemplateData.py` / none | action templates, staged actions |

`utils/MongoDataLoader.reset_app_data()` **drops and reseeds every collection above
and runs at Django settings import time** — every server start, every `manage.py`
command, every autoreloader cycle. This makes the app self-initializing for demos
and development at the cost of persistence across restarts (see §5). The explicit
`/api/v1/reset/` endpoint triggers the same reload on demand.

### 2.4 Frontend (`src/webserver/gui/`)

An Angular 10 SPA with an unusual, CLI-less toolchain (see §5). Routes
(`app/app.routing.ts`) and their components:

| Route | Component | Backend endpoints used |
|---|---|---|
| `/` and `/risk-graph/:systemId` | `RiskGraphComponent` | `missions/`, `cvi/<id>`, `risk_analysis/*`, C2 (via config) |
| `/actions` | `ActionsComponent` | `hostile_response/*`, `action_list/*`, static JSON |
| `/cvi` | `CVIComponent` | static question JSON, `application/system/` (legacy path) |
| `/risk-appetite` | `SurveyComponent` | static question JSON, `risk-appetite-data` (legacy path) |
| `**` | `NotFoundComponent` | — |

- **`RiskGraphComponent`** is the heart of the UI (~2,600 lines): mission/system
  selection, a d3 force-graph of assets colored by risk, a Leaflet map of asset
  geolocation, chart.js/nvd3 risk visuals, and drill-down modals — Asset Info,
  Threat Info, Group Info, and the Action (course-of-action) window.
- **Modals** use `ngx-bootstrap`'s `BsModalService.show(Component, {initialState})`;
  each window has a `…WindowData` class whose fields are copied onto the component
  instance before `ngOnInit` (this replaced the dead `angular2-modal` library).
- **Services** (`*.service.ts` per feature) wrap `HttpClient` and build URLs from
  `environment/environment.ts` (`API_BASE_URL`, `API_VERSION`, `C2_REST_API`).
- **`survey-angular` (SurveyJS)** renders the CVI and Risk Appetite questionnaires
  from static JSON definitions shipped in `app/cvi/data/` and `app/survey/data/`.
- **Dead code**: `app/home/` is a complete feature (component/service/data) that is
  neither routed nor declared; `shared/` pagination/spinner components are declared
  in an unused `SharedModule`.

---

## 3. Data Flow

**Startup.** `docker-compose up` starts Mongo → backend → GUI. Importing Django
settings fires `reset_app_data()`, which drops/reseeds all collections from
`utils/data/*.py`. The GUI is served statically; the browser loads `index.html`,
which loads zone.js, SystemJS, and `systemjs.config.js`, then `System.import('app')`
boots Angular from per-file compiled JS.

**Primary flow — risk analysis of a system:**

1. `RiskGraphComponent` loads `/api/v1/missions/` and populates the mission picker.
2. Selecting a mission/system fetches system data (`/api/v1/cvi/<systemId>` or via
   C2 passthrough) — assets, threats, vulnerabilities, geolocation.
3. The component POSTs to `/api/v1/risk_analysis/system/<systemId>/`. The view
   (a `C2DataRequestor` subclass) assembles system data, then
   `analytics.RiskAnalysis.perform_system_risk_analysis` scores every asset:
   criticality × threat × vulnerability × (for tasked assets) action success
   likelihood, with `HostileResponses` computing the enemy's most-likely and
   most-dangerous counter-moves for each friendly task.
4. The response drives the d3 graph coloring; clicking a node opens the Asset Info
   modal, which pulls per-asset threats/vulnerabilities/actions and lets the user
   stage courses of action (POST/DELETE against C2 `coa/…/task` endpoints, risk
   deltas recomputed via `risk_analysis/task_dependency/`).
5. Comparing courses of action calls `risk_analysis/compare_system/`, which runs the
   comparative-statics → dominated-strategy elimination pipeline and returns a
   recommended strategy.

**Actions page (effect administration).** CRUD over the effect/response/action
triple: list effect names from `hostile_response`; per effect, edit the most-likely/
most-dangerous hostile responses (PATCH `hostile_response/<effect>/`), the action
tables per asset type, and time/likeliness properties (PATCH
`action_list/type/<force>/<effect>/<type>/`). These properties feed directly into
the analytics likelihood calculations.

**CVI and Risk Appetite.** SurveyJS questionnaires; CVI submissions post a system
definition, and risk-appetite submissions are scored by `RiskAppetiteAnalysis` into
the `riskAppetite` collection. Separately, the course-of-action comparison accepts
optional `restrictions` (mission time, personnel, minimum success probability) in
its request body; `get_unattainable_strategies` eliminates strategies that violate
them before dominance analysis.

---

## 4. Major Design Decisions

1. **MongoDB-direct instead of Django ORM.** Django's relational layer is bypassed
   entirely (`DATABASES` unconfigured); views and analytics open `pymongo` clients
   directly, and DRF serializers exist only to validate payloads and generate
   Swagger schemas. Consequence: schema lives in seed files and consumer code, with
   no migrations; collections are free-form documents.

2. **Reset-on-start data model.** All collections are dropped and reseeded at every
   settings import. This trades persistence for a guaranteed-consistent demo state
   and makes tests/dev environments self-initializing. Any data a user creates at
   runtime survives only until the next restart.

3. **External C2 as the source of truth for missions/units.** Pax deliberately does
   not own operational data — mission structure, units, and course-of-action task
   assignment live in a separate C2 system reached over REST (`C2_REST`). Pax caches
   or mirrors some of it in Mongo (`missions`, `units` seeds) for standalone demos.

4. **Analytics as a separate plain-Python package.** The risk engine has no Django
   imports and mirrors an external research codebase (`O1sims/NetworkDefence`, per
   the README). It is unit-tested independently (`tests/analytics/`). It is not
   fully pure, however: modules reach into Mongo and C2 themselves.

5. **No-bundler frontend toolchain.** The GUI predates Angular CLI adoption: plain
   `tsc` compiles each `.ts` to a sibling `.js` (gitignored), and SystemJS 0.21
   resolves module specifiers in the browser at runtime via a hand-maintained map in
   `assets/systemjs.config.js`. Every npm dependency must be manually mapped there,
   and CJS/UMD packages consumed via `import * as X` need `.default`-unwrapping
   shims. This is the single largest source of frontend fragility.

6. **Split-origin deployment with CORS** (rather than same-origin reverse proxying).
   The GUI calls the backend by absolute URL (`environment.API_BASE_URL`) and the
   backend whitelists the GUI origin. The backend still carries a vestigial
   SPA-fallback route from an earlier combined-deployment design.

7. **Matched-pair effect data.** An "effect" spans three collections: `effects`
   (rich per-asset-type definition), `hostile_response` (counter-response pair per
   effect), and `action_list` (concrete actions + time/likeliness per effect × asset
   type). The seeds derive the latter two from `EffectData.py` to keep them in sync;
   at runtime the API can mutate them independently (a known integrity gap — §7).

---

## 5. Directory Structure

```
Pax/
├── build.sh                    # task runner: up / down / stop / test / all
├── CLAUDE.md                   # AI-assistant guidance (root, + per-stack copies)
├── docs/DESIGN.md              # this document
└── src/
    ├── docker-compose.yml      # pax (8200) + pax-gui (3000) + pax-db (8210)
    ├── backend/                # Django 2.2 + DRF API  (image: pax:latest)
    │   ├── Dockerfile          # python:3.5 base, apt via archived Debian mirror
    │   ├── manage.py, requirements.txt, requirements-dev.txt, ruff.toml
    │   ├── Pax/                # Django project: settings, urls, wsgi, api_config
    │   ├── api/
    │   │   ├── views/          # one module per resource; raw pymongo access
    │   │   ├── models/         # DRF serializers (validation + swagger only)
    │   │   ├── serializers/    # additional mongoengine-flavored serializers
    │   │   └── services/       # C2 data fetch helpers
    │   ├── analytics/          # game-theoretic risk engine (no Django deps)
    │   ├── utils/              # MongoDataLoader (reset/seed), SystemConfig
    │   │   └── data/           # seed modules per collection (+ CVE dataset)
    │   └── tests/              # unittest suite: analytics/, views/, mocks/, data/
    └── webserver/              # Angular 10 SPA      (image: pax-gui:latest)
        ├── Dockerfile          # node base; serves via lite-server
        └── gui/
            ├── index.html      # script-tag bootstrap: zone.js → SystemJS → app
            └── app/
                ├── package.json, tsconfig.json, .eslintrc.json, .prettierrc
                ├── main.ts, app.module.ts, app.routing.ts
                ├── environment/           # API_BASE_URL, API_VERSION, C2_REST_API
                ├── assets/                # systemjs.config.js, css, js libs, images
                ├── risk-graph/            # main view + modals/ (asset/threat/group/action)
                ├── actions/  cvi/  survey/  navbar/  not-found/
                ├── home/  shared/         # dead code (unrouted / unused module)
                └── */data/                # static JSON consumed by components
```

---

## 6. Testing & Tooling

- **Backend tests**: `python manage.py test` (or `./build.sh test`) runs a
  `unittest`+`mock` suite focused on the analytics engine (`tests/analytics/`) with
  JSON fixtures in `tests/data/` and a C2 `requests` stub in `tests/mocks/`.
- **Linting**: `ruff` for the backend (`ruff.toml`, via `requirements-dev.txt`);
  ESLint + Prettier for the frontend (`npm run lint` / `npm run format`).
- **API docs**: live Swagger UI at `http://localhost:8200/swagger/` (and `/redoc/`),
  generated by drf-yasg from the serializer classes and `@swagger_auto_schema`
  annotations.
- **No CI** is configured; `build.sh test` is the only defined check.

---

## 7. Known Quirks & Current State

Recorded here because they shape day-to-day work (see also `CLAUDE.md` files):

- `reset_app_data()` runs on *import* of settings — any `manage.py` invocation
  resets the database.
- The backend base image is EOL `python:3.5`; its Dockerfile pins Debian's archived
  snapshot mirror to keep `apt` working. The dependency set is 2017–2020 era
  (Django 2.2, DRF 3.11.2, drf-yasg 1.17.1 — a mutually-pinned trio; see
  `requirements.txt` history before upgrading any of them).
- The backend's SPA-fallback `IndexView` 500s (`TemplateDoesNotExist`) in the split
  deployment — harmless, but it means unknown backend paths return HTML errors, not
  404 JSON.
- Effect CRUD can break the `effects`/`hostile_response`/`action_list` pairing:
  creating an effect via the Actions page seeds no `action_list` docs, and deleting
  one leaves dangling counter-response references that the analytics engine indexes
  without guards.
- Several legacy frontend paths (`application/...` in the CVI/survey/home services)
  point at backend routes that no longer exist; the corresponding features silently
  no-op or 500 until reimplemented.
- The C2 integration is unauthenticated plain HTTP and required for full
  functionality; without it, mission/unit-dependent features degrade.
- `SECRET_KEY` is hardcoded in `settings.py`, and `DEBUG` defaults truthy (the env
  string `"False"` is still truthy) — both fine for the lab/demo context, both
  blockers for any production deployment.
