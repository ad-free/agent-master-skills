---
name: database-migrations
description: Use when you need the database-migrations skill (plugin).

---

---
name: database-migrations
description: Use when safe migration patterns for schema changes with rollback, data backfill, and zero-downtime deployment.
metadata:
  origin: agent-master-skills---

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