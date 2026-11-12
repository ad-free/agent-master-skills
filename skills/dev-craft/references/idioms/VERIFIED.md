# Idioms verification log

Maintainer record; not loaded by the skill. Update when a file is re-checked.

Verification status of these files (2026-10-19), checked against official docs via context7 or the docs site:
Tailwind v4 `@theme`, Pydantic v2 names and `pydantic-settings`, FastAPI `dependency_overrides` and `Annotated`
dependencies, SQLAlchemy 2.0 `Mapped`/`mapped_column`/`selectinload`, Alembic autogenerate limits, naming
conventions, `autocommit_block` and `postgresql_concurrently`, MUI `createTheme`/`sx` and MUI X DataGrid license
tiers, shadcn `components.json` and `npx shadcn@latest add`, TanStack Query v5 keys and `invalidateQueries`,
TanStack Table manual pagination/sorting, React Hook Form `zodResolver`, httpx `ASGITransport`, pytest-asyncio
modes, Playwright viewport and `toHaveScreenshot`, MSW v2 handlers, Postgres `CREATE INDEX CONCURRENTLY`,
`lock_timeout`, GIN/BRIN.
Also checked 2026-10-20 via context7 (TanStack Router, Recharts, ECharts, Tremor, PostgreSQL 17 docs, shadcn/ui):
TanStack Router `autoCodeSplitting` and `errorComponent`, Recharts v3 `accessibilityLayer` default and
`ResponsiveContainer`, ECharts heatmap progressive rendering, `@tremor/react` bundling Recharts, `pg_trgm` GIN and
operators, RLS owner/`BYPASSRLS` rules, shadcn Radix vs Base UI (changed: Base UI is now the default).
Not checked: the Radix component APIs themselves, React Router specifics, the Recharts v2 to v3 migration details,
Postgres versions other than 17. Treat these as defaults and read the installed version's docs.

Last verified: `charts.md`, `postgres.md`, `shadcn-ui.md`, `frontend-data.md` on 2026-10-20 (edited above); the other
idioms files carry the 2026-10-19 verification listed above (not re-checked today). Re-verify a file when a major
version of its library changes in the repo, or every 3 months, whichever comes first.
