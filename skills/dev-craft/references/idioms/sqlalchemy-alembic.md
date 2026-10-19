# SQLAlchemy and Alembic

Detect SQLAlchemy 1.x vs 2.x; for 2.x use 2.0 style.
- `select()` with `session.execute/scalars`, typed `Mapped[...]` / `mapped_column`, not `session.query`.
- One session per request via dependency; commit at the service boundary; no sessions in module globals.
- Avoid N+1: `selectinload`/`joinedload` where lists render related rows.
- Alembic: every schema change is a migration with a working `downgrade`; review autogenerate output (it cannot see table or
  column renames, which come out as drop+add and must be hand-edited into a rename, nor anonymous constraints,
  so name every constraint; it also guesses wrong on types like `Enum` on backends without native ENUM); data migrations separate from schema steps; set a naming
  convention for constraints and indexes; add NOT NULL in steps (nullable -> backfill -> NOT NULL) on big tables;
  build indexes concurrently on large Postgres tables: `op.create_index(..., postgresql_concurrently=True)` inside
  `with op.get_context().autocommit_block():` (it cannot run in a transaction), and set
  `transaction_per_migration=True` so the commit that block forces does not split a multi-migration run.
- Test: upgrade, downgrade, upgrade on a copy (`data-modeling.md`).
