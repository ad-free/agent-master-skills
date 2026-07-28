# Test Transcript: Out-of-Scope Detection (04-out-of-scope.md)

## Scenario
During BUILD phase of auth feature, agent discovers legacy password hashing uses MD5.

## Expected Flow

### During BUILD Phase (Slice 2: Login)
```
Agent working on login slice
Discovers: getUser() uses MD5 for password hashing
Not in current PLAN (PLAN.md only covers JWT auth)
```

### Agent Action: Out-of-Scope Detection
1. Creates `.dev-craft/out-of-scope/2026-07-28-legacy-md5.md`:

```markdown
# Out-of-Scope Issue: Legacy MD5 Password Hashing

## Discovered During
- Phase: BUILD
- Slice: 2 (Login)
- File: src/auth/password.ts

## Issue Description
Legacy password hashing uses MD5 (cryptographically broken).
Current PLAN only covers JWT auth, not password migration.

## Impact Assessment
- Priority: High (cryptographically broken)
- Related to current PLAN: No (different module)
- Effort estimate: 2 days (migration + re-hash)
- Risk if deferred: Credential stuffing, rainbow table attacks

## Options
1. Add to current PLAN — scope creep, extends timeline
2. Create follow-up ticket — separate PR, own lifecycle (recommended)
3. Defer to retro/learn — track for later, continue current work
```

2. Asks: "Create follow-up ticket? [y/n]"

### Human Response: `y`

### Agent Action
- Creates GitHub Issue (if `gh` available) or local markdown ticket
- Records in `state.json.outOfScope`
- Continues current slice

### State Update
```json
{
  "outOfScope": [
    {
      "file": ".dev-craft/out-of-scope/2026-07-28-legacy-md5.md",
      "issue": "Legacy MD5 password hashing",
      "action": "ticket_created",
      "ticketUrl": "https://github.com/org/repo/issues/456"
    }
  ]
}
```

### Continues Current Slice
- Completes login slice with JWT
- Does NOT migrate passwords in this PR