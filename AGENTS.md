# Repository Guidelines

## Project Structure & Module Organization
`app/` hosts the FastAPI backend; `main.py` wires `api/v1` routers that depend on services (`app/services`) and repositories (`app/repositories`) layered over SQLAlchemy models in `app/models`. Shared configuration, DB sessions, and telemetry helpers live in `app/core` and `app/infrastructure`. Alembic metadata and revision scripts are stored in `alembic/` (see `alembic/versions`). Architecture diagrams stay under `architecture/` (keep the PlantUML sources and rendered assets in sync). The React/Vite UI resides in `gui/`, with generated API clients under `gui/src/api`, feature modules in `gui/src/app`, and static assets in `gui/public`.

## Build, Test, and Development Commands
- `python -m venv .mlv1sion && source .mlv1sion/bin/activate` — create the repo-local Python 3.12 environment.
- `pip install -r requirements.txt` — install backend dependencies maintained via `pip freeze`.
- `uvicorn app.main:app --reload` — run the API locally.
- `alembic upgrade head` — apply migrations to the Postgres instance defined in `.env`.
- `alembic revision --autogenerate -m "message"` — record schema changes reflected in `app/models/orm`.
- `cd gui && npm install` — install Node dependencies.
- `npm run dev` / `npm run build` — start the Vite dev server or produce the production bundle.
- `npm run lint` — run ESLint/TypeScript checks.
- `npx kubb generate --config kubb.config.ts` — regenerate the OpenAPI client (supersedes the legacy `generate:api` script).

## Coding Style & Naming Conventions
Use Python 3.12, four-space indentation, type hints throughout, `snake_case` modules, and `PascalCase` classes; inject repositories/services via constructors. Keep SQLAlchemy columns typed and aligned with DB field names. Format with Black (79 columns) and lint with Ruff. On the frontend, rely on strict TypeScript, React function components, `PascalCase` component files, `camelCase` hooks/utilities, and reuse `@mui` primitives plus the generated client instead of bespoke fetches.

## Testing Guidelines
House backend tests under `app/tests`, mirroring API/service/repository layers, and run them with `pytest -q`. Configure `.env` (or `DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/mlv1sion_dev`) so tests hit the same Postgres engine used in development; leverage transaction rollbacks or dedicated schemas instead of SQLite. Once Vitest/Testing Library scaffolding is added, frontend features should include component or hook coverage; until then, `npm run lint` plus manual verification is the minimum gate. Target roughly 80% coverage on modules you modify and document any gaps in the PR.

## Commit & Pull Request Guidelines
Follow the current history’s short, imperative subjects (`add alembic`, `init gui with heyapi`) and keep them ≤72 characters. Each PR should describe the change, link to issues, list migrations executed (`alembic upgrade head`, etc.), and enumerate the commands run (`pytest -q`, `npm run lint`, manual GUI steps or screenshots for visual tweaks). Address review feedback with follow-up commits rather than force pushes.

## Security & Configuration Tips
All runtime settings come from `app/core/config.Settings`, which reads `.env`; never commit actual secrets (`jwt_secret_key`, Postgres credentials, S3 keys). Provide sanitized example values whenever introducing new settings, rotate JWT material after auth changes, and store production credentials in your secrets manager.
