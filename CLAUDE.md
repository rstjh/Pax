# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project structure

Pax is two independent stacks under `src/`, with no top-level monorepo manifest:
- `src/backend/` — Django + MongoDB API. See `src/backend/CLAUDE.md`.
- `src/webserver/` — Angular frontend. See `src/webserver/CLAUDE.md`.
- `src/docker-compose.yml` wires both together plus a `pax-db` (MongoDB) service.

## Running the project

Use `build.sh` at the repo root (dev workflow is Docker Compose-based):
- `./build.sh up` / `down` / `stop` — `docker-compose up/down/stop` from `src/`
- `./build.sh all` — builds both Docker images (`pax:latest`, `pax-gui:latest`)
- `./build.sh test` — runs `cd src/backend && python manage.py test` (backend only; there is no frontend test script)

## Env vars and ports

`src/docker-compose.yml` is the source of truth for env vars actually used at runtime — it disagrees with the README in places (e.g. `UI_PORT=3000` in compose vs `UI_PORT=8200` documented in the README). When in doubt, check `docker-compose.yml` and the code, not the README.

The backend also reads `C2_REST` (an external C2 API endpoint, used in `api/services/system_data.py`) which isn't documented anywhere — ask before assuming its value or removing code that depends on it.

## Gotchas

- `src/backend/Pax/settings.py` calls `reset_app_data()` at **import time**. Simply importing Django settings (e.g. via `manage.py`, a test run, or a shell) can trigger a database reset/reload as a side effect. Be careful when running one-off management commands.
- The backend mostly bypasses Django's ORM: `DATABASES` in `settings.py` is unconfigured, and code talks to MongoDB directly via `pymongo`/`mongoengine` instead.

## Tooling

- No linter or formatter is configured for either stack (no `.eslintrc`, `.prettierrc`, `ruff`/`flake8`, `.editorconfig`). Don't assume a house style beyond what's already in the surrounding file.
- No CI is configured. `./build.sh test` is the only defined check.
- No branch/PR conventions — direct commits to `master` are the norm.
