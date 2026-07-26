# CLAUDE.md

This file provides guidance to Claude Code when working with code in `src/webserver/`.

## Stack

Angular 10 SPA, lives in `gui/app/` (not at this directory's root): `gui/index.html` + `gui/app/` component tree (home, actions, cvi, risk-graph, survey, navbar, not-found, shared, services, assets).

## Commands

`package.json` scripts (run from `gui/app/`):
- `npm start` — `concurrently "npm run tsc:w" "npm run lite" ...` (dev watch + serve)
- `npm run lite` — serves via `lite-server`
- `npm run tsc` / `tsc:w` — compile / watch-compile TypeScript
- No `build` script is defined.
- `npm run lint` (ESLint, config in `.eslintrc.json`) and `npm run format` (Prettier, config in `.prettierrc`) — run `npm install` first to pull in the added devDependencies.

## Known state — verify before assuming this runs cleanly

- Code uses deprecated Angular APIs (e.g. `HTTP_PROVIDERS` from `@angular/http`, removed in Angular 5+) despite `package.json` declaring Angular 10 — this suggests the code hasn't been fully migrated and may not compile as-is.
- `Dockerfile`'s `CMD` is effectively disabled: the real serve command (`npm run lite`) is commented out, replaced with no-op/diagnostic commands (`npm view package.json`, `npm audit fix`, etc.). Building/running this Dockerfile as committed will not actually serve the app.
- Both `package-lock.json` and `yarn.lock` are committed (mixed package-manager history), plus a stray `package.json.original` backup file.
- No lint/format tooling is configured.
