---
name: database-migrations
description: |
  Safe migration patterns for schema changes with rollback, data backfill,
  and zero-downtime deployment. Use for any database schema change,
  data migration, or migration strategy decision. Do NOT use for general
  database design (see dev-craft) or for reviewing existing migration quality
  after the fact (see dev-craft's security-audit plugin).
  
model: big-pickle
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "database migration"
  - "schema change"
  - "migrate database"
  - "zero-downtime migration"
  - "data backfill"
  - "rollback migration"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: specialized-engineering
  integrates-with: [dev-craft, planning-and-task-breakdown]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~3K tokens. If skill exceeds, extract sections to references/.

# database-migrations

## Relationship to existing skills

- dev-craft: Provides the overall engineering pipeline; database-migrations is invoked as a specialized phase within dev-craft when schema changes are needed.
- security-audit: Validates migration safety post-execution; database-migrations focuses on the migration process itself.
- dev-craft/plugins/database-migrations: The plugin version handles migrations within the dev-craft pipeline; this standalone skill handles migrations as a standalone workflow.

## When to Use

- Adding, modifying, or removing database columns, tables, indexes, or constraints
- Migrating data between schemas or storage engines
- Planning zero-downtime deployment strategies for database changes
- Deciding migration ordering, rollback strategy, or backfill approach
- Reviewing a proposed migration before execution

## When NOT to Use

- General database schema design without a migration context (see dev-craft)
- Writing application-level queries or ORM models (see dev-craft)
- Performance tuning database queries (see dev-craft/plugins/performance-profiling)
- Reviewing an existing migration for security vulnerabilities after the fact (see dev-craft/plugins/security-audit)

## Workflow

### Phase 1: Migration Assessment

Analyze the proposed schema change and classify it:

1. **Identify the change type**: additive (new column/table), modifying (alter column), destructive (drop column/table), or data transformation
2. **Assess blast radius**: which services, tables, and queries are affected
3. **Classify risk level**:
   - `low`: additive changes with no data transformation
   - `medium`: modifying changes that are backward-compatible
   - `high`: destructive changes or data transformations
   - `critical`: changes affecting production data with no rollback path
4. **Determine migration strategy** based on risk:
   - `low` → expand-contract pattern (add column, deploy code, remove old column)
   - `medium` → online schema change with shadow writes
   - `high` → dual-write with backfill, then cutover
   - `critical` → manual review required, staged rollout with feature flags

### Phase 2: Migration Authoring

Write the migration following these rules:

1. **Naming**: `YYYYMMDDHHMM_<description>.sql` (e.g., `202607311200_add_user_email_idx.sql`)
2. **Forward migration**: the `up` or `do` script that applies the change
3. **Backward migration**: the `down` or `undo` script that reverts the change
4. **Idempotency**: every migration must be safe to re-run without side effects
5. **Transaction wrapping**: wrap in a transaction where the database supports it
6. **Lock awareness**: note any table locks acquired and their duration
7. **Data backfill**: if data transformation is needed, include a separate backfill step with batch size and rate limiting
8. **Index management**: create indexes concurrently where supported (PostgreSQL `CREATE INDEX CONCURRENTLY`)

### Phase 3: Safety Review

Before executing, validate:

1. **Rollback feasibility**: can the `down` script run in under the rollback time budget?
2. **Data integrity**: are foreign keys, constraints, and triggers handled correctly?
3. **Deployment order**: will the migration run before or after the application deploy? Is the app backward-compatible with both old and new schema during the deploy window?
4. **Lock contention**: will the migration block production queries? If so, is the maintenance window approved?
5. **Backup verification**: has a recent backup been verified and is it accessible?

### Phase 4: Execution

Execute the migration with these safeguards:

1. **Dry run**: execute the migration on a staging/clone environment first
2. **Progress monitoring**: track migration progress (rows affected, lock wait times)
3. **Abort threshold**: define a maximum acceptable duration; abort if exceeded
4. **Post-migration validation**: run integrity checks (row counts, sample queries, constraint validation)
5. **Deployment gate**: do not proceed to application deploy until migration is verified

### Phase 5: Post-Migration Verification

1. Run integrity checks against production
2. Monitor error rates and latency for 15 minutes post-migration
3. Verify rollback script works on a clone if any anomaly is detected
4. Archive the migration with execution timestamp and result

## Context Management

- Persist migration state in `.dev-craft/migrations/<project>/state.json` with fields: `migration_id`, `status` (pending/applied/rolled-back), `executed_at`, `rollback_script_path`
- On session resume, check state.json for any pending or failed migrations
- Track migration history across sessions; never re-apply a migration marked `applied`

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read existing migration files, state.json, schema dumps | Only read from `migrations/` and `.dev-craft/` directories |
| Write | Create new migration files and state updates | Migration files must follow naming convention; never overwrite existing applied migrations |
| Edit | Modify migration scripts during review | Only edit `pending` migrations; never edit `applied` migrations |
| Bash | Execute migration dry-runs, integrity checks, backup verification | Must use `--dry-run` or `--preview` flags first; never execute destructive DDL without explicit user confirmation |
| Grep | Search migration files for table/column references | Search only within `migrations/` directory |
| Glob | Find migration files by pattern | Pattern: `migrations/**/*.sql` |

## Output Contract

On completion, the skill must produce:

1. A migration file pair (`up` + `down`) in the project's `migrations/` directory
2. An updated `state.json` entry with the migration status
3. A migration summary including: change type, risk level, strategy, estimated duration, rollback time, and lock impact
4. A verification checklist confirming all safety gates passed

## Quality Gates

- [ ] Migration is idempotent (safe to re-run)
- [ ] Backward migration exists and is tested on a clone
- [ ] No destructive DDL without explicit user confirmation
- [ ] Backup verified before execution
- [ ] Dry run passed on staging environment
- [ ] Rollback script executes in under the rollback time budget
- [ ] Application code is backward-compatible with both old and new schema during deploy window

## Error Handling

- **Migration timeout**: abort and trigger rollback; alert the user with the current state
- **Lock contention detected**: pause migration, suggest maintenance window, do not force execution
- **Data integrity check failure**: halt, do not proceed to application deploy, preserve the migration state for investigation
- **Rollback failure**: escalate immediately; the database may be in an inconsistent state requiring manual intervention
- **Backup not found**: halt migration until a verified backup is confirmed