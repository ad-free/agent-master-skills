# Postgres

Detect the version (features differ). See `data-modeling.md` for the review process.
- Types: `numeric` or integer cents for money, `timestamptz`, `uuid` or `bigint` identity with a reason, `jsonb`
  for truly schemaless extras (not for relations you query or constrain), `text` over `varchar(n)` unless a limit is a rule.
- Constraints in the database: PK, FK, UNIQUE, NOT NULL, CHECK.
- Indexes: B-tree default; GIN for `jsonb`/arrays/full-text (multi-valued columns); partial for hot subsets; BRIN for huge tables whose
  column correlates with physical row order (for example append-only timestamps); index foreign keys. Index to the real query, then verify with `EXPLAIN (ANALYZE, BUFFERS)`: look for
  sequential scans on big tables, row-estimate gaps, sorts spilling to disk.
- Search: full-text (`tsvector`) or `pg_trgm` for fuzzy matching. Reporting: materialized views with a refresh plan.
- Multi-tenancy: tenant column, with row-level security where the tenant boundary must be enforced by the DB.
- Safe migrations: `CREATE INDEX CONCURRENTLY` (not allowed inside a transaction block; only one concurrent
  build per table at a time; a failed build leaves an INVALID index: drop it and retry, or `REINDEX INDEX
  CONCURRENTLY`), add columns nullable then backfill in batches then enforce,
  avoid table rewrites and long locks, set `lock_timeout` per session inside the migration (the docs advise
  against putting it in `postgresql.conf`; it also fires only while waiting for locks, unlike `statement_timeout`).
- Operations: connection pooling (pgbouncer or the app pool), partition only past a measured need.
