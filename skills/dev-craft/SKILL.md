---
name: dev-craft
description: Full-stack engineering pipeline with persistent memory. Detects stack, scans code smells, enforces modern patterns, runs lint/type/test per slice. Resumes via .dev-craft/ state.
---

# dev-craft

## Overview

Turns a prompt into production-quality code.
Every phase has a clear goal, exit criteria, and a human checkpoint.
Persists state to `.dev-craft/` so work survives across sessions.

**Philosophy:** Transparent, human-orchestrated, composable.
Skip any phase. Edit any phase. The pipeline serves you.

## When to Use

- Given a prompt, PLAN.md, or feature request
- Starting a new project or feature
- Task spans multiple files or modules
- Resuming work from a previous session
- Need more than a single-file change

**When NOT to use:** Single-line fixes, typo corrections, trivial config changes.

## The Iron Law

```
NO CODE WITHOUT DESIGN APPROVAL
```

Implementation without approved spec = wasted hours of rework.

## Memory System

`.dev-craft/` directory created on first run:

```
.dev-craft/
├── state.json       # currentPhase, completed, stack, slices
├── plan.md          # Evolving plan from Align → Design
├── context.md       # Domain glossary (shared language)
├── decisions/       # ADRs — key decisions captured
│   └── 001-*.md
├── sessions/        # Handoff docs for context rotation
│   └── session-YYYYMMDD-N.md
└── config.json      # Project config (linter, formatter, test cmds)
```

### Resume Logic

| Scenario | Behavior |
|---|---|
| No `.dev-craft/` | Phase 1 if codebase exists, Phase 2 if greenfield |
| `state.json` exists | Load state, skip completed phases |
| All phases complete | Ask "New task on same project?" |
| Context near limit | Generate handoff doc, resume next session |

## Stack Detection

Run during Phase 2 (ALIGN).
Scan dependency files for exact versions.

If linter/formatter detected, every slice MUST pass it.
If none found, surface to human:
*"No linter/formatter — recommend installing one. Proceed without?"*

## Pipeline Phases

```
[0] LOAD → [1] ARCH-SCAN → [2] ALIGN → [3] DESIGN → [4] SOURCE
    → [5] BUILD → [6] TEST → [7] REVIEW → [8] HARDEN → [9] SHIP
```

Each phase:
```
Phase → Output
LOAD → state.json initialized
ARCH-SCAN → Smell report (remediate first?)
ALIGN → CONTEXT.md (shared language)
DESIGN → PLAN.md + ADRs
SOURCE → Fetched docs
BUILD → Vertical slices (TDD)
TEST → Test output
REVIEW → Code review
HARDEN → Clean + security
SHIP → Commit + ADRs
```

---

### [0] LOAD — Initialize or Resume

Read `.dev-craft/state.json`:

**Not found →** Detect existing source code:
- Existing code (src/, lib/, app/) → Phase 1 (ARCH-SCAN)
- Greenfield → Phase 2 (ALIGN), skip ARCH-SCAN

**Found + complete →** Ask: "New feature? Start fresh?"

**Found + incomplete →** Load context.md, restore slice progress.

Write state after LOAD.

---

### [1] ARCH-SCAN — Codebase Smell Detection

**Goal:** Assess codebase health before adding new code.

**Process:**

1. Scan for Fowler's code smells:
   - Mysterious Name, Duplicated Code, Feature Envy
   - Data Clumps, Primitive Obsession, Repeated Switches
   - Shotgun Surgery, Divergent Change, Speculative Generality
   - Message Chains, Middle Man, Refused Bequest, Dead Code

2. Scan for design system health:
   - Check for tailwind.config.*, tokens.css, theme.ts
   - Check for shadcn/ui components (components/ui/)
   - Check for CSS custom properties (:root { --color-* })
   - Flag inconsistencies

3. Surface report:
   ```
   SMELL REPORT:
   1. [Duplicated Code] src/utils/format.ts:45-52
      → Extract shared function
   2. [Primitive Obsession] src/models/user.ts
      → Create discriminated union
   ```

4. Ask human to prioritize fixes

**Exit criterion:** Human approves remediation or defers.

**State write:** Save smells to state.json for REVIEW.

---

### [2] ALIGN — Grill + Detect + Glossary

**Goal:** Surface assumptions, sharpen requirements.

**Process:**

1. Ask one question at a time with best guess attached

2. Surface assumptions:
   ```
   ASSUMPTIONS:
   1. Web app (not native mobile)
   2. Auth uses JWT in httpOnly cookies
   3. Database is PostgreSQL
   → Correct me now or I'll proceed.
   ```

3. Define "Out of scope" explicitly

4. Detect stack:
   ```
   STACK DETECTED:
   - Python 3.12, FastAPI, SQLAlchemy 2.0
   - Node 22, React 19, Vite 6
   - Linter: ruff, Formatter: ruff
   - Type checker: mypy
   ```

5. Build glossary in context.md

**Exit criterion:** Human confirms scope with explicit yes.

**State write:** Save stack to state.json. Save context.md.

---

### [3] DESIGN — Spec + Plan + ADRs

**Goal:** Produce spec, task breakdown, architecture decisions.

**Process:**

1. Write spec covering:
   - Objective (what and why)
   - Commands (build, test, lint, type, dev)
   - Project structure
   - Code style (see references/modern-patterns.md)
   - Testing strategy
   - Boundaries (Always do / Ask first / Never do)

2. Map dependency graph

3. Slice vertically:
   ```
   Slice 1: User can create item (DB + API + UI)
   Slice 2: User can list items (query + API + UI)
   Slice 3: User can edit item (update + API + UI)
   ```

4. Write tasks with acceptance criteria

5. Write ADRs for architecture decisions:
   ```markdown
   # ADR-001: [Title]
   Status: Accepted
   Context: [Problem]
   Decision: [What we chose]
   Alternatives: [What else was considered]
   Consequences: [Impact]
   ```

**Exit criterion:** Human reviews and approves.

**State write:** Save plan.md. Save ADRs to decisions/.

---

### [4] SOURCE — Document Verification

**Goal:** Verify framework decisions against official docs.

**Process:**

1. Read exact versions from dependency files
2. Fetch specific official docs for each feature
3. Extract patterns, API signatures, deprecation warnings
4. Cite sources inline during BUILD:
   ```python
   # Source: https://docs.sqlalchemy.org/en/20/core/
   async with engine.connect() as conn:
       ...
   ```
5. Flag uncovered patterns:
   ```
   UNVERIFIED: No official docs for this pattern.
   Based on training data — verify before shipping.
   ```

**Source hierarchy:**
| Priority | Source |
|---|---|
| 1 | Official docs |
| 2 | Official blog/changelog |
| 3 | MDN Web Standards |
| ❌ | Stack Overflow, blog posts |

**Exit criterion:** All dependencies verified.

**State write:** Save source references to state.

---

### [5] BUILD — TDD + Incremental

**Goal:** Implement one vertical slice at a time.

**Process per slice:**

```
1. RED    — Write failing test
2. GREEN  — Write minimal code to pass
3. LINT   — Run linter + formatter
4. TYPE   — Run type checker
5. TEST   — Run test suite
6. COMMIT — Atomic commit
```

**Rules:**
- **Simplicity first** — Three similar lines > premature abstraction
- **Scope discipline** — Don't touch code outside slice
- **One slice at a time** — Pipeline loops over slices
- **TDD seams** — Test at public interfaces only
- **Mock at boundaries only** — Real > fakes > stubs > mocks
- **Feature flags** — For risky production changes
- **Form generation** — React Hook Form + Zod (React projects)
- **Design system** — Use tokens, no ad-hoc values

**Exit criterion:** All slices implemented and committed.

**State write:** Save slices to state.json.

---

### [6] TEST — Full Suite + Diagnose

**Goal:** Run full test suite. Fix every failure.

**Process:**

1. Run full suite: `npm test` / `pytest` / `cargo test`

2. If all pass → Proceed to Phase 7

3. If any fail → **Invoke:** `debugging-and-error-recovery`
   - This skill handles structured root-cause investigation
   - Do NOT embed debugging procedures here — defer to the skill

4. Re-run full suite after every fix

**Exit criterion:** Full test suite passes.

**State write:** Update state.

---

### [7] REVIEW — Seven-Axis Audit

**Goal:** Quality gate before shipping.

**Invoke:** `code-review-and-quality` for seven-axis review.

**Process:**

1. Load `code-review-and-quality` skill
2. Review entire diff across seven axes:
   - Correctness, Readability, Architecture
   - Performance, Security, Testing, Modern Patterns
3. Categorize findings (Critical/Required/Nit/Optional)
4. Fix all Critical/Required findings

**Exit criterion:** All Critical/Required resolved.

**State write:** Save review findings.

**Exit criterion:** All Critical/Required resolved.

**State write:** Save review findings.

---

### [8] HARDEN — Clean + Security + Simplify

**Goal:** Remove scaffolding, close security gaps.

**Clean:**
- Remove debug instrumentation
- Delete throwaway prototypes
- Check for zombie code

**Security:**
- Run dependency audit
- Run threat model (STRIDE)
- Verify secrets in env vars
- Check SSRF, injection, XSS

**Simplify:**
- Understand before simplifying (Chesterton's Fence)
- Simplify one thing at a time
- Run tests after each change
- Rule of 500: >500 lines → automate

**Exit criterion:** Zero security findings.

**State write:** Update state.

---

### [9] SHIP — Docs + Commit + Finalize

**Goal:** Deliver with full traceability.

**Process:**

1. Update ADRs for any BUILD/HARDEN decisions
2. Update CONTEXT.md with new terms
3. Final verification:
   - Lint + type + test + build all pass
   - Run secrets scanner
   - Dead code removed
4. Update CHANGELOG
5. Atomic commit:
   ```
   type(scope): short description

   - What changed and why
   - Key decisions (reference ADRs)
   - What was intentionally NOT done
   ```
6. Define rollback strategy:
   - Feature flag toggling: < 1 minute
   - Code revert: specify commit
   - Database: migration revert command

**Exit criterion:** Clean commit with rollback plan.

---

### [H] HANDOFF — Cross-Session Context

**When:** Context > 80% full, or human says "continue later".

**Process:**

1. Save state to state.json:
   - Current phase and slice position
   - Incomplete tasks
   - Pending decisions

2. Write handoff to sessions/session-YYYYMMDD-N.md:
   - What was accomplished
   - What's in progress
   - What's next
   - Known issues

3. Summarize: "Session saved. Run dev-craft to resume."

---

## Workflow Orchestration

For complex features spanning multiple domains.

### Workflow Types

| Workflow | Pipeline |
|----------|----------|
| SaaS MVP | dev-craft + ui-craft |
| Admin Dashboard | dev-craft + ui-craft |
| E-commerce | dev-craft + ui-craft |
| API Service | dev-craft only |
| Landing Page | ui-craft only |

### Orchestration Pattern

```
1. PLAN — Decompose into backend/frontend slices
2. BACKEND — Run dev-craft for API/database/auth
3. HANDOFF — Generate API contract
4. FRONTEND — Run ui-craft using API contract
5. INTEGRATION — Run dev-craft for testing
6. SHIP — Coordinate commits
```

### Cross-Skill Communication

dev-craft needs UI:
- Note in state.json: `"uiSliceNeeded": ["login-form"]`
- Generate API contract in api-contract.md
- Resume with ui-craft

ui-craft needs backend:
- Note in state.json: `"backendSliceNeeded": ["auth-api"]`
- Generate API spec in api-spec.md
- Resume with dev-craft

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I know what they want" | #1 cause of AI failure is misalignment |
| "Just start coding" | No spec = scope creep, wrong architecture |
| "Tests later" | You won't. Tests after test implementation |
| "Too simple to verify" | Training data is stale |
| "Lint after slices" | Lint debt compounds |
| "Tests pass, it's good" | Tests don't catch architecture/security |
| "Commit at the end" | Large commits destroy history |
| "Prototype, skip security" | Prototypes become production |
| "Fix architecture later" | Rot compounds fast |
| "Skip arch scan" | 2-min scan prevents 2-hour rework |

## Red Flags

- Skipping ARCH-SCAN on codebase with > 10 files
- Starting without completed Align phase
- Human checkpoints skipped
- Code before fetching current-version docs
- Multiple slices in one commit
- Lint/type/tests failing but proceeding
- No ADRs for decisions
- "Fix it later" for Critical findings
- No .dev-craft/ directory
- Security review skipped
- Commit messages: "WIP", "fix", "update"

## Verification

- [ ] ARCH-SCAN was run (or deferred with approval)
- [ ] .dev-craft/state.json exists with status: complete
- [ ] All slices implemented and committed
- [ ] Full test suite passes
- [ ] Linter + formatter pass
- [ ] Type checker passes
- [ ] No debug tags or temp files
- [ ] ADRs written for decisions
- [ ] CONTEXT.md up to date
- [ ] Security audit passed
- [ ] No secrets in diff
- [ ] Commit references ADRs
- [ ] Human approved every checkpoint

## See Also

- `references/modern-patterns.md` — Per-language guidance
- `references/phase-templates.md` — Templates for documents
