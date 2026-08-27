# Instinct Extraction Rules

Patterns to extract from sessions and convert into instincts.

## Code Patterns

### Error Handling
- **Pattern**: Consistent error handling approach (Result types, typed errors, no swallowed errors)
- **Context**: backend, TypeScript/Python/Go, error-handling
- **Trigger**: code-review, session-end
- **Example**: "Use `Result<T, E>` for all fallible operations in TypeScript services"

### Defensive Programming
- **Pattern**: Input validation at boundaries, guard clauses, fail-fast
- **Context**: all, defensive-programming
- **Trigger**: code-review, session-end
- **Example**: "Validate all external inputs at API handlers with Zod schemas"

### Type Safety
- **Pattern**: No `any` types, strict mode, explicit return types
- **Context**: TypeScript, Python (mypy), strict-typing
- **Trigger**: code-review, session-end
- **Example**: "Enable `strict: true` in tsconfig, use `unknown` with narrowing instead of `any`"

### Testing Patterns
- **Pattern**: TDD at pre-agreed seams, vertical slices, independent test data
- **Context**: all, testing, TDD
- **Trigger**: dev-craft BUILD phase, session-end
- **Example**: "Write failing test at public interface seam before implementation"

## Workflow Patterns

### Planning
- **Pattern**: Always create PLAN.md before implementation, vertical slices
- **Context**: all, planning
- **Trigger**: session-start, planning-and-task-breakdown
- **Example**: "Run planning-and-task-breakdown before any multi-file change"

### Verification
- **Pattern**: Run lint + typecheck + test before claiming done, read actual output
- **Context**: all, verification, quality-gates
- **Trigger**: verification-before-completion, session-end
- **Example**: "Execute `ruff check && mypy --strict && pytest` and read output before 'done'"

### Git Hygiene
- **Pattern**: Feature branches, conventional commits, no direct pushes to main
- **Context**: all, git, workflow
- **Trigger**: session-end, ship
- **Example**: "Branch naming: `<type>/<scope>-<description>`, conventional commit messages"

### Context Management
- **Pattern**: Create session files, update state.json at each phase, handoff at 70% context
- **Context**: all, context-engineering, dev-craft, ui-craft
- **Trigger**: session-start, session-end, dev-craft phases
- **Example**: "Update .dev-craft/state.json after every phase transition"

## Architectural Patterns

### API Design
- **Pattern**: Design API contract before implementation, OpenAPI spec, versioning
- **Context**: backend, API, api-design
- **Trigger**: api-design, dev-craft CONTRACT phase
- **Example**: "Write api-contract.md in dev-craft Phase 4.5 before building endpoints"

### Database Migrations
- **Pattern**: Reversible migrations, data backfill scripts, zero-downtime patterns
- **Context**: backend, database, migrations
- **Trigger**: database-migrations, dev-craft
- **Example**: "Every migration has up/down, test rollback before applying"

### Security
- **Pattern**: No hardcoded secrets, input validation, auth at boundaries, dependency scanning
- **Context**: all, security
- **Trigger**: bug-hunting, security-audit, code-review
- **Example**: "Run dependency audit on every deploy, block on Critical/High CVEs"

## UI/Frontend Patterns

### Design System
- **Pattern**: Use design tokens, no hardcoded colors/spacing, component contracts
- **Context**: frontend, React/Vue/Svelte, design-system
- **Trigger**: ui-craft, design-system-validate
- **Example**: "All colors from tokens: `color-primary`, never `#3b82f6`"

### Accessibility
- **Pattern**: WCAG 2.1 AA checklist on every component, semantic HTML, focus states
- **Context**: frontend, accessibility, a11y
- **Trigger**: ui-craft BUILD, accessibility-deep
- **Example**: "Every interactive element has visible focus state and aria-label"

### Performance
- **Pattern**: No layout shifts, preload fonts, optimize images, code splitting
- **Context**: frontend, performance
- **Trigger**: ui-craft HARDEN, performance-profiling
- **Example**: "Add width/height to all images, preload critical fonts"

## Extraction Heuristics

### From Session Transcripts
1. Look for repeated phrases: "always", "never", "make sure to", "don't forget"
2. Identify decisions: "we decided to", "the pattern is", "convention is"
3. Find corrections: "actually", "instead", "better to", "fixed by"
4. Note tool usage patterns: "run X before Y", "check Z first"

### From Code Reviews
1. Convention violations → positive pattern ("use X instead of Y")
2. Repeated suggestions across files → team convention
3. Security findings → preventive patterns
4. Performance issues → optimization patterns

### From Bug Fixes
1. Root cause → prevention pattern
2. Fix approach → reusable fix pattern
3. Test added → regression test pattern

### From Retrospectives
1. "What worked well" → positive patterns to reinforce
2. "What didn't work" → anti-patterns to avoid
3. "Action items" → process improvements

## Confidence Calculation Rules

### Base Confidence by Source
| Source | Base Confidence |
|--------|----------------|
| Explicit user save | 0.7 |
| Retrospective | 0.6 |
| Code review finding | 0.5 |
| Session end auto-extract | 0.3 |
| Bug fix pattern | 0.4 |
| Handoff document | 0.4 |

### Confidence Modifiers
| Modifier | Value | Condition |
|----------|-------|-----------|
| Successful application | +0.1 | Per confirmed use (max +0.4) |
| User confirmation | +0.1 | Explicit "this worked" (max +0.2) |
| Cross-session validation | +0.1 | Same pattern in 3+ sessions (max +0.1) |
| Failed application | -0.05 | Per failure (min 0.0) |
| Time decay | -0.01/day | Since last_use (min 0.1) |
| Superseded by new pattern | -0.2 | When better pattern found |

### Status Transitions
```
quarantined (conf < 0.5) 
  → active (conf ≥ 0.5, apps ≥ 1)
    → reliable (conf ≥ 0.8, apps ≥ 3)
      → promoted (conf ≥ 0.9, apps ≥ 5, cross-project)
        → archived (if not used 90 days or superseded)
```

## Extraction Pipeline

```
Session/Handoff/Retro Input
         ↓
   Parse for patterns (LLM + heuristics)
         ↓
   Deduplicate against existing instincts
         ↓
   Score initial confidence
         ↓
   Store as quarantined instinct
         ↓
   [SessionStart] Match context → inject active+
         ↓
   [Application] Track success/failure
         ↓
   Update confidence → status transition
```

## Anti-Patterns (What NOT to Extract)

- One-off fixes with no recurrence
- Project-specific hacks (hardcoded paths, workarounds)
- Personal preferences not validated by team
- Patterns contradicting established conventions
- Overly specific patterns (exact code vs. principle)
- Patterns from failed attempts without root cause analysis