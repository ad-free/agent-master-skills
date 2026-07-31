---
name: handoff
description: |
  Agent-to-agent and session-to-session context transfer protocol. Structured handoff documents
  with task context, file changes, decisions, blockers, and resume instructions.
  Use when rotating context, switching agents, or resuming after break.
  (from mattpocock handoff skill)
  
model: gpt-5-nano
version: 2.0.0
preamble-tier: 1
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - "handoff to"
  - "transfer context"
  - "resume session"
  - "context rotation"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 2.0.0
  domain: context-memory
  integrates-with: [context-engineering, agent-orchestration]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Handoff Protocol

Standardized context transfer between agents and across sessions. Prevents context loss, drift, and re-work.

## When to Handoff

| Trigger | Action |
|---------|--------|
| Context > 60% | `context-guard` generates handoff, suggests new session |
| Agent completes slice | Agent writes handoff for next agent |
| Switching pipelines (dev-craft → ui-craft) | Pipeline handoff document |
| End of work session | Session handoff for next day |
| `orchestrator` delegates to sub-agent | Task-specific handoff |

---

## Handoff Document Format

```markdown
# Handoff: <from> → <to>

## Metadata
- **From**: <agent-name> / <session-slug>
- **To**: <agent-name> / <session-slug>
- **Timestamp**: 2026-07-28T15:30:00Z
- **Feature**: <feature-name>
- **Slice**: <N of M>

## Task Context
**What was being done:** <one paragraph summary>
**Current state:** <what's complete, what's next>
**Immediate next action:** <specific, actionable>

## Key Files Modified
| File | Change Description | Verification |
|------|-------------------|--------------|
| `src/auth/login.ts` | Added OAuth2 PKCE flow | Tests pass, lint clean |
| `src/auth/types.ts` | New `PKCEChallenge` type | Typecheck clean |

## Decisions Made
| Decision | Rationale | ADR / Reference |
|----------|-----------|-----------------|
| Use PKCE over implicit flow | Mobile app security requirement | ADR-017 |
| Store code_verifier in memory only | Prevent token theft via XSS | Security review 2026-07-15 |

## Blockers / Open Questions
| Blocker | Owner | Status |
|---------|-------|--------|
| Need Apple Developer cert for SIWA | @mobile-lead | BLOCKED - waiting on cert |
| Stripe test mode webhook URL | @backend-lead | RESOLVED - ngrok configured |

## Fresh Evidence (Verification Gates)
- `npm test` → 47 passed, 0 failed (as of 2026-07-28T15:25:00Z)
- `npm run lint` → 0 errors
- `npm run typecheck` → 0 errors
- `npm run build` → success

## State Reference
- **state.json**: `.dev-craft/runs/auth-slice-3/state.json`
- **Current slice**: 3 (of 5)
- **Next slice**: 4 — Token Refresh & Rotation

## Resume Instructions
1. Load `skill("context-engineering")`
2. Read `state.json` for `auth-slice-3`
3. Continue from slice 4: Token Refresh & Rotation
4. Run verification gates before starting

## Learnings Captured
- `learn-048`: "Stripe webhook idempotency requires sorting events by created timestamp"
- `learn-049`: "React Query cache TTL must match backend TTL to avoid stale reads"
```

---

## Agent-to-Agent Handoff (Skill Chain)

When agent A invokes agent B:

```markdown
## Handoff: planner → implementer

### Task
Implement slice 2: User Registration API

### Inputs
- **Spec**: `PLAN.md#slice-2` — POST /api/auth/register with email verification
- **Contract**: `api-contract.md#auth-register` — OpenAPI spec
- **Types**: `src/auth/types.ts` — `RegisterRequest`, `RegisterResponse`

### Constraints
- **Must follow**: Existing auth patterns in `src/auth/login.ts`
- **Must not**: Direct database access — use `UserRepository` interface
- **Token budget**: standard (see `token-budget` skill)

### Expected Output
- **Files**: `src/auth/register.ts`, `src/auth/register.test.ts`
- **Tests**: Unit (repository), Integration (API), Contract (Pact)
- **Verification**: `npm test -- register.test.ts`

### Context from Planner
- Priority: G1 (blocks login slice)
- Dependencies: Email service (mock in tests)
- Risk: R-03 (team unfamiliar with React Query) — not applicable to backend
```

---

## Session-to-Session Handoff (Context Rotation)

When context > 60% or explicit rotation:

1. **Context Guard** generates handoff document
2. **Saves** to `.dev-craft/runs/<slug>/handoff-<timestamp>.md`
3. **Updates** `state.json`:
   ```json
   {
     "lastHandoff": ".dev-craft/runs/auth-slice-3/handoff-2026-07-28T15:30:00Z.md",
     "contextUsageAtHandoff": 67
   }
   ```
4. **Next session** loads via `context-engineering`:
   ```markdown
   # Resume Session: auth-slice-3
   
   ## Load Order
   1. `skill("context-engineering")`
   2. Read handoff: `.dev-craft/runs/auth-slice-3/handoff-2026-07-28T15:30:00Z.md`
   3. Read state: `.dev-craft/runs/auth-slice-3/state.json`
   4. Continue from slice 4
   ```

---

## Handoff Validation Checklist

Before considering handoff complete:

- [ ] Task context is unambiguous (next agent knows exactly what to do)
- [ ] All modified files listed with descriptions
- [ ] Decisions have rationale and references
- [ ] Blockers have owners and status
- [ ] Fresh evidence included (tests, lint, typecheck from THIS session)
- [ ] State reference points to correct `state.json`
- [ ] Resume instructions are executable (copy-paste runnable)
- [ ] Learnings captured via `learn` skill

---

## Reference

- `skills/references/handoff-protocol.md` — Standardized agent-to-agent and session-to-session context transfer format

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| "See the code" | Forces next agent to reverse-engineer | Document what/why |
| Missing evidence | Next agent can't verify state | Always run gates before handoff |
| No blockers listed | Hidden dependencies cause delays | Explicit blocker tracking |
| Vague next action | "Continue work" → confusion | Specific: "Implement register.ts line 42" |
| No learnings captured | Institutional memory lost | Auto-capture via `learn` skill |