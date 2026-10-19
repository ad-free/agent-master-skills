# Postgres

Detect the version (features differ). See `data-modeling.md` for the review process.
- Types: `numeric` or integer cents for money, `timestamptz`, `uuid` or `bigint` identity with a reason, `jsonb`
  for truly schemaless extras (not for relations you query or constrain), `text` over `varchar(n)` unless a limit is a rule.
- Constraints in the database: PK, FK, UNIQUE, NOT NULL, CHECK.
- Indexes: B-tree default; GIN for `jsonb`/arrays/full-text; partial for hot subsets; BRIN for huge append-only
  tables; index foreign keys. Index to the real query, then verify with `EXPLAIN (ANALYZE, BUFFERS)`: look for
  sequential scans on big tables, row-estimate gaps, sorts spilling to disk.
- Search: full-text (`tsvector`) or `pg_trgm` for fuzzy matching. Reporting: materialized views with a refresh plan.
- Multi-tenancy: tenant column, with row-level security where the tenant boundary must be enforced by the DB.
- Safe migrations: `CREATE INDEX CONCURRENTLY`, add columns nullable then backfill in batches then enforce,
  avoid table rewrites and long locks, set `lock_timeout`.
- Operations: connection pooling (pgbouncer or the app pool), partition only past a measured need.
