# Idioms

Do not trust remembered versions. Detect what the project uses, match it, load only the file(s) that apply.

| Look at | Tells you |
|---|---|
| `pyproject.toml` (`requires-python`), `uv.lock`, `requirements*.txt` | Python version, tooling, FastAPI/Pydantic/SQLAlchemy versions |
| `package.json`, lockfile, `tsconfig.json` | Node, TypeScript strictness, React, Tailwind, UI library, data libs |
| `alembic.ini`, migrations dir, `docker-compose*`, `DATABASE_URL` shape | Postgres version and migration tool |
| eslint/prettier/ruff/mypy config | Rules the repo already enforces; do not fight them |

For anything version-sensitive, read the installed version's docs (context7 or the official site) before using
an API. If an idiom here conflicts with the repo's convention, the repo wins.

| Task touches | Load |
|---|---|
| Python backend | `python.md`; plus `fastapi.md`, `pydantic.md`, `sqlalchemy-alembic.md`, `testing-python.md` as used |
| Postgres | `postgres.md` |
| React + TypeScript | `react-typescript.md`; plus `tailwind.md`, one of `shadcn-ui.md` / `material-ui.md` (detected, never both), `frontend-data.md`, `testing-frontend.md`, `charts.md` as used |
| Language not listed | Detect conventions from the repo and `clean-code-defaults.md`; do not invent a house style |

Verification status of these files (2026-10-19), checked against official docs via context7 or the docs site:
Tailwind v4 `@theme`, Pydantic v2 names and `pydantic-settings`, FastAPI `dependency_overrides` and `Annotated`
dependencies, SQLAlchemy 2.0 `Mapped`/`mapped_column`/`selectinload`, Alembic autogenerate limits, naming
conventions, `autocommit_block` and `postgresql_concurrently`, MUI `createTheme`/`sx`, shadcn `components.json`
and `npx shadcn@latest add`, TanStack Query v5 keys and `invalidateQueries`, Postgres `CREATE INDEX CONCURRENTLY`.
Not checked: MUI X DataGrid license tiers, `lock_timeout` details, BRIN/GIN guidance, httpx `ASGITransport`,
pytest-asyncio vs anyio, Playwright, MSW, React Hook Form + Zod, TanStack Table/Router, Recharts/ECharts/Tremor.
Treat the unchecked ones as defaults and read the installed version's docs for anything version-sensitive.
