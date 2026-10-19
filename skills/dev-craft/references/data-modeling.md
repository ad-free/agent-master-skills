# Data modeling (schema or query changes only)

Agents treat a given schema as fixed. Bad schema decisions are cheap now and expensive later, so a schema
change gets a review inside Challenge. Findings are options with a cost, never orders. Stack specifics:
`idioms/postgres.md`, `idioms/sqlalchemy-alembic.md`; migration safety: `plugins/database-migrations`.

## Checklist

- **Entities and relations:** right cardinality; many-to-many through a join table; no comma-separated values
  or JSON blobs hiding relations.
- **Normalization:** repeated data that will drift (department name copied into rows); or over-normalization
  hurting the common queries.
- **Keys and constraints:** primary and foreign keys, UNIQUE, NOT NULL, CHECK. The database enforces rules, not
  only the app.
- **Types:** money as numeric or integer cents, never float; timestamps with time zone; enum vs lookup table;
  UUID vs bigint with a stated reason.
- **Consistency** with existing naming and key types.
- **History and audit:** soft delete, `created_at/updated_at/created_by`, audit trail for sensitive data (HR
  data needs one), effective-dated records (salary, position) instead of overwriting.
- **Tenancy and permissions:** tenant column or schema decision made explicit; who may read sensitive fields.
- **Indexes:** matched to real queries (list screens, filters, search) and foreign keys.
- **Migrations:** reversible, safe on existing data, no long locks on big tables, backfill plan.
- **Privacy:** minimization, encryption for sensitive fields, retention.
- **Scale:** flag only what is likely to matter, not hypothetical growth.

## Check against reality

1. Read the existing schema and migrations. List the 5 most important queries the planned screens need; each
   gets a sensible plan and index.
2. Run `EXPLAIN (ANALYZE)` on realistic volume or generated sample data. Findings from Run beat opinions. No
   database available: "Not verified", with the exact command.
3. Migration up, down, up on a copy with sample data (disposable database; never the user's dev database
   without approval).

## Output

```markdown
## Schema findings
1. [Gap | Logic] `employees.department` is free text, so typos split reports. Propose a `departments` table
   with FK. Cost: one migration + backfill.
2. [Risk | Code] Salary is overwritten on update (employees.py:73), so history is lost. Propose a
   `compensation` table with effective dates.
Decision needed: apply 1? apply 2?
```
Existing production data is a hard constraint: every change ships with a migration, a rollback, and the stated
effect on existing rows.
