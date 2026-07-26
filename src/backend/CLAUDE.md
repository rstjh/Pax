# CLAUDE.md

This file provides guidance to Claude Code when working with code in `src/backend/`.

## Stack

Django 2.2 + Django REST Framework, using **mongoengine** for models and raw **pymongo** (`MongoClient`) in several views/services for direct MongoDB access — the app largely bypasses Django's own ORM (`DATABASES` in `Pax/settings.py` is unconfigured).

- `Pax/` — Django project (settings, urls, wsgi, `api_config.py`)
- `api/` — DRF app: `models/` (mongoengine), `serializers/`, `services/`, `views/`, `database_options.py`
- `analytics/` — plain-Python risk/game-theory modules (`Risk.py`, `RiskAnalysis.py`, `AttackDefenceGame.py`, `NetworkRisk.py`, `MissionAnalysis.py`, etc.) with no Django dependency; uses numpy/pandas/networkx/matplotlib
- `utils/` — `MongoDataLoader.py`, `SystemConfig.py`, `Exceptions.py`
- `tests/` — mirrors `analytics/` and `views/`, plus `mocks/` and JSON fixtures in `data/`

## Running tests

`python manage.py test` (or `./build.sh test` from the repo root, which `cd`s here first).

## Linting

`ruff check .` (config in `ruff.toml`). Install with `pip install -r requirements-dev.txt`.

## Env vars

`DB_HOSTNAME`, `DB_PORT`, `DB_NAME` — read via `os.environ.get(...)` throughout `api/database_options.py` and several `api/views/*.py` for direct pymongo connections.
`C2_REST` — external C2 API endpoint used in `api/services/system_data.py`, undocumented elsewhere.

## Gotchas

- Importing `Pax/settings.py` calls `reset_app_data()` as a side effect of import — this can trigger a DB reset/reload just from running `manage.py`, a shell, or tests.
- `DEBUG = os.environ.get('DEBUG', True)` doesn't cast to bool — setting `DEBUG=False` in the environment still evaluates truthy.
- `SECRET_KEY` is hardcoded in `settings.py`; don't add further hardcoded secrets alongside it.
