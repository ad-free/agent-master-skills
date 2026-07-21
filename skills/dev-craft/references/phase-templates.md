# Phase Templates

Templates for documents produced during the dev-craft pipeline. These are consumed by agents in subsequent phases and phases.

## Spec Template (Phase 3 — DESIGN)

```markdown
# Spec: [Project/Feature Name]

## Objective
[What we're building and why. User stories or acceptance criteria.]

## Tech Stack
[Framework, language, key dependencies with versions detected in Phase 1]

## Commands
- Build: `npm run build` | `uv build` | `cargo build`
- Test: `npm test` | `pytest` | `cargo test`
- Lint: `npx eslint . --fix` | `ruff check --fix .`
- Format: `npx prettier --write .` | `ruff format .`
- Type: `npx tsc --noEmit` | `mypy .`
- Dev: `npm run dev` | `uvicorn app.main:app --reload`

## Project Structure
```
src/           → Source code
tests/         → Test files
docs/          → Documentation
```

## Code Style
[One real code snippet showing the style for each language in use.
 Follow references/modern-patterns.md for guidance.]

## Testing Strategy
- Framework: [pytest / vitest / jest / etc.]
- Location: [tests/ or colocated]
- Coverage target: [e.g. > 80% on new code]
- Levels: unit > integration > e2e

## Boundaries
- Always do: [list]
- Ask first: [list]
- Never do: [list]

## Success Criteria
- [Specific, testable condition]
- [Specific, testable condition]

## Open Questions
- [Anything unresolved needing human input]
```

## Task Template (Phase [3] — DESIGN)

```markdown
## Task [N]: [Short descriptive title]

**Description:** One paragraph explaining what this task accomplishes.

**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Verification:**
- [ ] Tests pass: `npm test -- --grep "pattern"`
- [ ] Lint passes: `ruff check .`
- [ ] Type check: `mypy .`
- [ ] Build: `npm run build`

**Dependencies:** [Task numbers or "None"]

**Files likely touched:**
- `src/path/to/file.ts`
- `tests/path/to/test.ts`

**Estimated scope:** [XS / S / M / L]
```

## ADR Template (Phase 3 — DESIGN)

```markdown
# ADR-[NNN]: [Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded]

**Date:** [YYYY-MM-DD]

## Context
[What is the problem or decision that needs to be made? What constraints exist?]

## Decision
[What did we decide? Be specific — include code examples, interface sketches, or config if relevant.]

## Alternatives Considered
| Alternative | Pros | Cons |
|---|---|---|
| Option A | ... | ... |
| Option B | ... | ... |

## Consequences
[What tradeoffs did we accept? What does this enable or prevent in the future?]
```

## Task Breakdown Example (Phase 3 — DESIGN)

### Phase 1: Foundation
- [ ] Task 1: Set up database schema and migrations
- [ ] Task 2: Define shared types and API contracts

### Checkpoint: Foundation
- [ ] Database migrations run clean
- [ ] Types compile

### Phase 2: Core Feature — User Can Create Items
- [ ] Task 3: Create item API endpoint
- [ ] Task 4: Create item UI

### Checkpoint: Core Flow
- [ ] User can create an item end-to-end
- [ ] Tests pass

### Phase 3: Core Feature — User Can View Items
- [ ] Task 5: List items query + API
- [ ] Task 6: List items UI

### Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] Human review approved

## Handoff Template (Phase H)

```markdown
# Session Handoff: [YYYY-MM-DD-N]

## Status
- **Completed phases:** [list]
- **Current phase:** [phase name]
- **Current slice:** [slice N of M]
- **Context used:** [X tokens / max]

## What Was Accomplished
- [What was done in this session]

## What's In Progress
- [What's partially done]

## Next Steps
1. [Next action]
2. [Following action]

## Pending Decisions
- [Decision needed from human]

## Known Issues
- [Bugs, blockers, unresolved questions]

## Artifacts
- Spec: `.dev-craft/runs/<slug>/plan.md`
- ADRs: `.dev-craft/runs/<slug>/decisions/`
- State: `.dev-craft/runs/<slug>/state.json`
- Runs index: `.dev-craft/index.json`
```

## State File Format (`.dev-craft/runs/<slug>/state.json`)

```json
{
  "version": 1,
  "status": "in_progress" | "complete",
  "currentPhase": 5,
  "completed": [0, 0.5, 1, 2, 3, 3.5, 4],
  "currentSlice": 3,
  "totalSlices": 8,
  "stack": {
    "python": { "version": "3.12", "framework": "fastapi" },
    "node": { "version": "22" },
    "react": { "version": "19" },
    "linter": "ruff",
    "formatter": "ruff",
    "typeChecker": "mypy"
  },
  "source": "PLAN.md" | "PROJ-123" | "prompt",
  "lastRun": "2026-07-10T14:30:00Z",
  "sessions": ["session-20260710-1", "session-20260710-2"]
}
```

## Estimation Template (Phase 3 — DESIGN)

```markdown
MODULE ESTIMATION:
[Module Name]: ~[X] days ([N] slices × [Y] day)
```

**Process:**

1. Review each module's estimated effort
2. Compare against any stated budget/schedule from domain.md
3. Flag significant discrepancies:
   ```
   Module        Expected (from spec)   My estimate     Delta
   Attendance    4.5                    5.0             ~10%
   Payroll       5.2                    8.0             ⚠ ~35%
   ```
4. Ask user: "Total estimated effort is ~X days. Does this match your expectations?"

## Run Index Format (`.dev-craft/index.json`)

Registry of every run — the audit trail used to improve the skill over time.

```json
{
  "activeSlug": "PROJ-123",
  "runs": [
    {
      "slug": "PROJ-123",
      "source": "PROJ-123",
      "createdAt": "2026-07-10T14:30:00Z",
      "lastRun": "2026-07-12T09:15:00Z",
      "status": "complete",
      "outcome": "shipped"
    },
    {
      "slug": "billing-service",
      "source": "prompt",
      "createdAt": "2026-07-14T10:00:00Z",
      "lastRun": "2026-07-14T10:00:00Z",
      "status": "in_progress",
      "outcome": null
    }
  ]
}
```
