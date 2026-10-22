---
name: database-migrations
description: Use when you need safe migration patterns for schema changes with rollback, data backfill, and zero-downtime deployment.
version: 1.0.0
preamble-tier: 1
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "database migration"
  - "schema change"
  - "data migration"
  - "rollback"
  - "zero downtime migration"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
---

<!-- TOKEN CEILING: ~2K -->

# Database Migrations Plugin

## Overview

Safe, reversible database migration workflows. Every migration has a forward and backward path.

## When to Use

- Schema changes in production databases
- Data backfill and transformation
- Column type changes that require locking consideration
- Adding indexes to large tables

## Core Rules

1. **Every migration is reversible** — `up` and `down` always
2. **One logical change per migration** — no mixing schema + data
3. **Test migration on staging first** — never straight to production
4. **No locking migrations on live tables** — use `CONCURRENTLY` for indexes
5. **Data migrations before schema migrations** — move data, then change structure

## Classify before writing

| Change | Risk | Strategy |
|---|---|---|
| Additive (new table, nullable column, index) | low | Expand-contract: add, deploy code, remove old later |
| Modifying but backward-compatible | medium | Online change; app works with old and new schema during deploy |
| Destructive (drop, narrow type) or data transform | high | Dual-write + batched backfill, then cutover |
| Production data with no rollback path | critical | Stop: user review, staged rollout behind a flag |

## Authoring rules

- Follow the repo's migration tool and naming; otherwise `YYYYMMDDHHMM_<description>`.
- Idempotent where the tool allows; wrap in a transaction where the database supports it.
- Note every lock taken and how long it holds; large tables need `CREATE INDEX CONCURRENTLY` (outside a
  transaction in PostgreSQL).
- Backfills run separately, in batches, with a stated batch size.
- State deploy order: does the migration run before or after the app, and does each app version work with both
  schemas during the window?

## Proof

Upgrade, downgrade, upgrade again on a disposable database; constraints and row counts checked after each step.
Never run against a shared or production database without approval (`AGENTS.md`). For non-schema migrations
(API, protocol, config, dependency): `references/folded-migration.md`.

## Pattern Reference

### Safe Column Addition

```sql
-- 1. Add column as nullable
ALTER TABLE users ADD COLUMN timezone TEXT;

-- 2. Backfill data
UPDATE users SET timezone = 'UTC' WHERE timezone IS NULL;

-- 3. Add NOT NULL constraint (only after backfill)
ALTER TABLE users ALTER COLUMN timezone SET NOT NULL;
```

### Zero-Downtime Column Rename

```
1. Add new column
2. Dual-write to both columns (app layer)
3. Backfill old data to new column
4. Change reads to new column
5. Remove old column
```

## Integration

Registered in `state.json`:
```json
{
  "plugins": ["database-migrations"],
  "pluginConfig": {
    "database-migrations": {
      "autoGenerate": true,
      "requireDownMigration": true
    }
  }
}
```