# Handoff Protocol Reference

Standardized agent-to-agent and session-to-session context transfer.

## Handoff Document Format

```markdown
# Handoff: <source> → <target>

## Context
- Feature: <feature name>
- Current state: <what's done, what's next>
- Session: <slug>
- Agent: <current agent>

## Key Files Modified
- `path/to/file1.ts` — <description>
- `path/to/file2.ts` — <description>

## Decisions Made
- Decision: <what> — Rationale: <why> — ADR: <link>

## Blockers / Open Questions
- Blocker: <description> — Owner: <agent/user>
- Question: <what> — Need input from: <who>

## Test Status (Fresh Evidence)
- `npm test` → 47 passed, 0 failed (as of <timestamp>)
- `npm run lint` → 0 errors
- `npm run typecheck` → 0 errors

## State Reference
- `state.json`: `.dev-craft/runs/<slug>/state.json`
- Current slice: <N>
- Next slice: <N+1>

## Resume Instructions
1. Load `skill("context-engineering")`
2. Read `state.json` for `<slug>`
3. Continue from slice <N>
```

## Agent-to-Agent Handoff (Skill Chain)

When agent A invokes agent B:

```markdown
## Handoff: agent-A → agent-B

### Task
<specific task for agent B>

### Inputs
- File: `path/to/input.ts` — <what it contains>
- Spec: `PLAN.md#slice-3` — <acceptance criteria>

### Constraints
- Must follow: <pattern/convention>
- Must not: <anti-pattern>
- Token budget: <standard|extended>

### Expected Output
- Files: `path/to/output.ts`
- Tests: `path/to/output.test.ts`
- Verification: `npm test -- output.test.ts`
```

## Session-to-Session Handoff

When context > 60% or explicit rotation:

1. **Context Guard** generates handoff document
2. **Saves** to `.dev-craft/runs/<slug>/handoff-<timestamp>.md`
3. **Updates** `state.json` with `lastHandoff` pointer
4. **Next session** loads via `skill("context-engineering")` → reads handoff + state

## Required Fields for All Handoffs

| Field | Description |
|-------|-------------|
| `from` | Source agent/session |
| `to` | Target agent/session |
| `timestamp` | ISO8601 |
| `task` | What was being done |
| `progress` | What's complete |
| `next` | Immediate next action |
| `files` | Modified files with descriptions |
| `decisions` | Key decisions with rationale |
| `blockers` | Any blocking issues |
| `evidence` | Fresh verification results |

## Validation

- Handoff must be readable by target agent without additional context
- All file paths must be relative to repo root
- Evidence must be from current session (fresh)
- Decisions must link to ADRs or discussion