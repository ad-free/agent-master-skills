---
name: api-versioning
description: API version management with deprecation policies, migration guides, and backward compatibility patterns.
metadata:
  origin: agent-master-skills
---

# API Versioning Plugin

## Overview

Manages API version lifecycle: introduction, deprecation, sunset. Ensures breaking changes are communicated and migrated smoothly.

## When to Use

- Public-facing APIs
- Breaking changes to existing endpoints
- Multiple client versions in production
- API contract changes

## Versioning Strategies

| Strategy | When to Use |
|----------|-------------|
| URL path (`/v1/`, `/v2/`) | Simple, explicit. Best for major breaking changes. |
| Header (`Accept: application/vnd.api+json;version=2`) | Cleaner URLs, harder to discover. |
| Query param (`?v=2`) | Easy to test. Can be forgotten by clients. |

## Deprecation Policy

```
1. ANNOUNCE — Add `Deprecation` header + docs update
2. SUNSET — Set `Sunset` header with date
3. MIGRATE — Guide clients with migration docs
4. REMOVE — Remove endpoint after sunset date
```

## Integration

Registered in `state.json`:
```json
{
  "plugins": ["api-versioning"]
}
```
