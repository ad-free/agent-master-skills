---
name: planning-and-task-breakdown
description: Use when you have a spec and need work broken into ordered, verifiable
  tasks with acceptance criteria.
metadata:
  origin: agent-master-skills
owner: noname.spyware@gmail.com
allowedTools:
- file
- http

---

Skill Chain: product-thinking (PRODUCT.md) → project-discovery (DOMAIN.md)
  → planning-and-task-breakdown (PLAN.md) → dev-craft (implementation)

# Planning & Task Breakdown

## Overview

Decompose work into small, verifiable tasks with explicit acceptance criteria.
Good task breakdown = reliable agent work.
Every task should be small enough to implement, test, and verify in a single focused session.

### Input Sources

This skill can consume:
- PRODUCT.md from `product-thinking` — structured product spec with modules, features, priorities
- DOMAIN.md from `project-discovery` — extracted domain model with entities and dependencies
- Spec text or user description — free-form requirements
- Existing task list — refine and reorder

If PRODUCT.md or DOMAIN.md is available, load it first to get the module${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/feature structure.
If the input is still vague, suggest running `product-thinking` first.

## When to Use

- You have a spec and need implementable units
- Task feels too large or vague to start
- Work needs parallelization across agents${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/sessions
- Need to communicate scope to human
- Implementation order isn't obvious

**When NOT to use:** Single-file changes with obvious scope, or spec already has well-defined tasks.

## Invocation Protocol

**Load when:** Starting new feature, unclear scope, or task feels too large
**Invoke via:** `skill(name="planning-and-task-breakdown")`
**Resume to:** Feed plan into dev-craft or ui-craft ALIGN phase

## The Iron Law

```
NO IMPLEMENTATION WITHOUT A WRITTEN PLAN
```

"I'll figure it out as I go" = tangled mess and rework.

## The Planning Process

### Step 0: Image Analysis (if screenshot provided)

Before planning, analyze any visual reference material:

```bash
python ~${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/analyze.py --image <path> --format md
```

Use output to enrich requirements:
- Add detected components to task list
- Add colors to design token tasks
- Add layout to structure tasks
- Use complexity score for task sizing

```
VISUAL REFERENCE ANALYSIS:
- Layout: [detected layout type]
- Components: [detected components]
- Colors: [extracted palette]
- Mode: [light${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/dark]
→ Added to requirements context.
```

### Step 1: Enter Plan Mode

Before writing any code, operate in read-only mode:

- Read the spec and relevant codebase sections
- Identify existing patterns and conventions
- Map dependencies between components
- Note risks and unknowns

**Do NOT write code during planning.**
Output is a plan document, not implementation.

### Step 2: Collect Everything

Gather from prompt${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/file:

```
COLLECTED:
- Core requirement: [what user wants]
- Constraints: [time, tech, scope]
- Assumptions: [what you think they mean]
- Gaps: [what's missing]
```

**Sources:**
- User's prompt or message
- Attached files (specs, designs, docs)
- Existing codebase (if any)
- External references (URLs, docs)

### Validate Before Trusting

Before entering upstream consumption mode, verify the document is complete:

- [ ] PRODUCT.md: All 6 sections populated (Domain, Scope, Features, Priority, Questions, Glossary)
- [ ] DOMAIN.md: All modules have priorities and dependencies
- [ ] No placeholder text ("...", "TBD", empty tables)
- [ ] Features have explicit priorities (not all UNKNOWN)

If validation fails → Fall back to normal planning mode with user questions.
Only the sections that are incomplete need clarification — don't re-ask about documented sections.

**Upstream Consumption Mode:**

When PRODUCT.md or DOMAIN.md is available:

1. **Extract modules directly** from the upstream document
2. **Skip the "Ask Questions" loop** (already answered in product-thinking)
3. **Go straight to dependency mapping and slicing**
4. **Only ask questions about gaps**, not about already-documented features

Example extract from PRODUCT.md:
```
Module: Employee (G1) — CRUD, documents, org chart → depends on Auth
Module: Attendance (G1) — clock in${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/out, shifts, overtime → depends on Employee
```

This avoids redundant questioning and keeps context focused on planning structure.

### Step 3: Verify Assumptions

Check against reality:

```
VERIFIED:
- Feasible: [yes${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/no with reasoning]
- Existing patterns: [what's already there]
- Dependencies: [available${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/needed]
- Risk areas: [what could go wrong]
```

### Step 4: Ask Questions

Ask ONE question at a time with best guess:

```
QUESTION: [single question]
YOUR GUESS: [what you think]
WHY: [reasoning]
OPTIONS: [if applicable]
```

**Stop asking when:**
- Core requirement is clear
- Scope is defined
- Major decisions made
- You can write the plan

### Step 5: Identify Dependency Graph

Map what depends on what:

```
Database schema
    │
    ├── API models${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/types
    │       │
    │       ├── API endpoints
    │       │       │
    │       │       └── Frontend API client
    │       │               │
    │       │               └── UI components
    │       │
    │       └── Validation logic
    │
    └── Seed data / migrations
```

Implementation order: bottom-up, build foundations first.

### Step 6: Slice Vertically

Build one complete feature path at a time.

**Bad (horizontal):**
```
Task 1: Build entire database schema
Task 2: Build all API endpoints
Task 3: Build all UI components
Task 4: Connect everything
```

**Good (vertical):**
```
Task 1: User can create account (schema + API + UI)
Task 2: User can log in (auth schema + API + UI)
Task 3: User can create task (task schema + API + UI)
Task 4: User can view task list (query + API + UI)
```

Each slice delivers working, testable functionality.

### Step 7: Write Tasks

Each task follows this structure:

```markdown
## Task [N]: [Short title]

**Requirement refs:** REQ-001, REQ-002   <!-- trace back to source spec rows -->

**Description:** One paragraph explaining what this task accomplishes.

**Acceptance criteria:**
- [ ] [Specific, testable condition]
- [ ] [Specific, testable condition]

**Verification:**
- [ ] Tests pass: `npm test -- --grep "feature"`
- [ ] Build succeeds: `npm run build`
- [ ] Manual check: [what to verify]

**Dependencies:** [Task numbers or "None"]

**Files likely touched:**
- `src${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/file.ts`
- `tests${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/test.ts`

**Estimated scope:** [XS${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/L]
```

> **REQ-IDs are mandatory for spec-driven work.** Every task must cite the source-spec
> requirement row(s) it satisfies. A task with no `Requirement refs:` is a symptom that
> the plan is being written from memory, not from the spec — the exact failure mode that
> drops P1 requirements. If you cannot cite a REQ-ID, either the requirement was never
> extracted (go back to Step 0${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Step 2) or the task is out of scope.

### Step 8: Order and Checkpoint

Arrange tasks so:

1. Dependencies satisfied (foundation first)
2. Each task leaves system in working state
3. Verification checkpoints every 2-3 tasks
4. High-risk tasks early (fail fast)

Add explicit checkpoints:

```markdown
## Checkpoint: After Tasks 1-3
- [ ] All tests pass
- [ ] Application builds
- [ ] Core user flow works end-to-end
- [ ] Human review before proceeding
```

### Step 9: Design Review

Present design in sections:

1. **Architecture** — high-level structure
2. **Components** — what we're building
3. **Data Flow** — how data moves
4. **Error Handling** — what happens when things fail
5. **Testing** — how we verify it works

After each section: "Does this look right so far?"
Wait for approval before continuing.

### Step 9.5: Spec Coverage Self-Review (COVERAGE GATE)

This is the most important step for spec-driven work. A plan can look complete and
still omit 6 P1 requirements. Do this review yourself — do not delegate it.

**1. Extract requirements from the source spec (exhaustive, literal):**
   - Read the spec line by line. For every capability, constraint, or non-functional
     rule, write one requirement row. Preserve the spec's own priority markers
     (`[REQUIRED P1]`, `🔴`, `G1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G3`, `⚪ [FUTURE PHASE]`) verbatim.
   - Capture *concrete* constraints as requirements, not prose
     (e.g. "JWT payload = only user_id + company_id + permission_version" → a row).
   - If a source spec was not provided, skip this step and note it.

2. **Assign each requirement a stable ID:** `REQ-001`, `REQ-002`, ...

3. **Trace every requirement to a task.** Each REQ-ID must map to ≥1 task whose
   `Requirement refs:` and acceptance criteria verify it.

4. **Build the traceability matrix** and save to `requirements.md` (consumed by
   dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ui-craft as the COVERAGE GATE artifact):

   ```markdown
   # Requirements Traceability Matrix — <feature>

   Source spec: <path> (<N> lines)
   Extracted: <M> requirements (P1: x, G1: y, G2: z, Future: w)

   | REQ-ID | Priority | Requirement (verbatim clause) | Traced Task(s) | Status |
   |--------|----------|-------------------------------|----------------|--------|
   | REQ-001 | P1 | employee_code via PG SEQUENCE | Task 1 | ✅ |
   | REQ-011 | P1 | cross-day shifts, UTC+7 display | Task 4 | ⚠️ GAP |
   | REQ-027 | G1 | leave: full${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/hourly + carry-forward | — | ❌ GAP |

   ## Gaps
   - REQ-011: no task covers UTC+7 presentation conversion
   - REQ-027: Leave module absent from plan
   ```

5. **Re-read the spec against the matrix.** For each section, confirm a row exists and
   each row maps to a task. Search for skipped priority markers:
   `grep -nE "REQUIRED P1|🔴|G1|must implement|Must have" <spec>`.

6. **Resolve gaps before writing the plan:**
   - Every P1 / G1 requirement **must** have a traced task. Add missing tasks.
   - G2${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G3 gaps may be deferred **only with explicit human acknowledgement**.
   - Do NOT write the final plan (Step 10) until P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1 coverage is 100%.

**Exit criterion (HARD GATE):** 100% of P1 + G1 requirements traced to a task with
acceptance criteria. This gate is what prevents "pipeline ran, requirements missing."

### Step 10: Write the Plan

Save to `docs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/YYYY-MM-DD-feature-name.md`.

## Task Sizing

| Size | Files | Scope | Example |
|------|-------|-------|---------|
| XS | 1 | Single function${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/config | Add validation rule |
| S | 1-2 | One component${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/endpoint | New API endpoint |
| M | 3-5 | One feature slice | User registration flow |
| L | 5-8 | Multi-component | Search with filtering |
| XL | 8+ | **Too large — break down** | — |

**Break down if:**
- Takes more than one focused session (2+ hours)
- Acceptance criteria need 3+ bullet points
- Touches 2+ independent subsystems
- Task title has "and" in it

## Module-Level Planning

For large projects (3+ modules), plan at module level first instead of a flat task list:

1. List all modules with priorities
2. Map dependencies between modules
3. Define build order (foundation → core → extended)
4. Per module: define features and slices
5. Per feature: define acceptance criteria

### Module Planning Pattern

```markdown
Module: [Module Name] ([Priority])
  Features:
    - [Feature 1]
    - [Feature 2]
  Dependencies: [Other modules]
  Slices:
    - [Slice 1: schema + API + form]
    - [Slice 2: query + API + table]
```

### Example (HRM)

```
Module: Employee (G1)
  Features:
    - CRUD employee records
    - Document upload
    - Org chart
  Dependencies: Auth
  Slices:
    - Create employee (schema + API + form)
    - List employees (query + API + table)
    - Edit employee (update + API + form)

Module: Attendance (G1)
  Features:
    - Clock in${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/out
    - Shift management
    - Overtime calculation
  Dependencies: Employee, Shift
  Slices:
    - Clock in${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/out API
    - Attendance dashboard
```

## Dependency-Aware Phasing

When planning large projects, order tasks by dependency chain so each phase produces usable output:

| Phase | Modules | Strategy |
|-------|---------|----------|
| Phase 1: Foundation | Auth, Employee | No downstream dependencies — build first |
| Phase 2: Transaction | Attendance, Leave | Depend on Employee |
| Phase 3: Processing | Payroll, Tax | Depend on Attendance + Employee |
| Phase 4: Evaluation | KPI, Review | Depend on Employee + Payroll |
| Phase 5: Extended | Recruitment, Onboarding | Stand-alone modules |
| Phase 6: Mobile${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Integration | API consumers | Need stable API from all phases |

**Bad**: Build Payroll directly (missing Employee + Attendance data)
**Good**: Employee → Attendance → Payroll (each phase produces usable output)

## Plan Document Template

The PLAN.md is the handoff document to dev-craft. It must contain enough structure for the ALIGN phase to consume directly.

```markdown
# PLAN.md — [Feature${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Project Name]

Generated from: [PRODUCT.md / DOMAIN.md / spec text]

## Overview
[One paragraph summary]

## Module / Feature Map
| Module | Features | Priority | Dependencies |
|--------|----------|----------|-------------|
| Module 1 | F1, F2, F3 | G1 | — |
| Module 2 | F4, F5 | G1 | Module 1 |

## Build Order
Phase 1 (Foundation): [modules]
Phase 2 (Core): [modules]
Phase 3 (Extended): [modules]

## Task List

### Phase 1: Foundation
- [ ] Task 1: [description]
- [ ] Task 2: [description]

### Checkpoint: Foundation
- [ ] All tests pass
- [ ] Build succeeds

### Phase 2: Core Features
- [ ] Task 3: [description]
- [ ] Task 4: [description]

### Checkpoint: Core
- [ ] End-to-end flow works

### Phase 3: Polish
- [ ] Task 5: [description]
- [ ] Task 6: [description]

### Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] Ready for review

## Dependencies
- Module dependency graph
- Data flow between modules

## Priorities
G1 (Must have): [features]
G2 (Should have): [features]
G3 (Nice to have): [features]

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [High${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Low] | [Strategy] |

## Open Questions
- [Question needing human input]
```

## Output Files

- **Plan document:** `PLAN.md` at project root (for dev-craft consumption). For **multi-repo** topology (separate BE + FE repos), place `PLAN.md` and the traceability matrix in the BE repo (`contractRepo`) so both sides reference one plan; or split per repo when the work is fully independent. dev-craft's SCOPE gate carries the `topology` decision.
- **Task list:** included in PLAN.md under each phase
- **Traceability matrix:** `requirements.md` at project root (the COVERAGE GATE artifact — consumed by dev-craft `[3.7] REQUIREMENTS-EXTRACTION` and ui-craft `[3.7]`)
- **Legacy archive (optional):** `docs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/YYYY-MM-DD-feature.md` for historical record

> **Multi-repo verification:** a fullstack ticket across two repos needs tests${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/build run in *both* repos. When generating acceptance criteria, list the per-repo verify command (e.g. `cd be-repo && pytest` **and** `cd fe-repo && npm test`), not a single root command.

## Parallelization

**Safe to parallelize:**
- Independent feature slices
- Tests for implemented features
- Documentation

**Must be sequential:**
- Database migrations
- Shared state changes
- Dependency chains

**Needs coordination:**
- Features sharing API contract
- Define contract first, then parallelize

## Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "I'll figure it out as I go" | Tangled mess and rework. 10 min planning saves hours. |
| "Tasks are obvious" | Write them down. Explicit tasks surface hidden dependencies. |
| "Planning is overhead" | Planning IS the task. Implementation without plan is typing. |
| "I can hold it in my head" | Context windows are finite. Plans survive session boundaries. |
| "This is too simple to plan" | Simple projects need plans too. Plans prevent rework. |

## Red Flags — STOP and Plan

- Starting implementation without written task list
- Tasks say "implement feature" without acceptance criteria
- No verification steps in plan
- All tasks are XL-sized
- No checkpoints between tasks
- Dependency order not considered
- Starting to code before planning

**All of these mean: Stop. Plan properly.**

## Verification

Before starting implementation:

- [ ] Every task has acceptance criteria
- [ ] Every task has verification step
- [ ] Every task cites `Requirement refs:` (REQ-IDs) from the source spec
- [ ] `requirements.md` traceability matrix exists and P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1 coverage is 100%
- [ ] Task dependencies identified and ordered
- [ ] No task touches more than ~5 files
- [ ] Checkpoints exist between phases
- [ ] Human has reviewed and approved plan

Can't check all boxes? Plan is incomplete. Don't start.

## Integration

**Use with:**
- `product-thinking` — Upstream: provides PRODUCT.md input with structured modules and priorities
- `project-discovery` — Upstream: provides DOMAIN.md input with domain entities and dependencies
- `dev-craft` — Downstream: consumes PLAN.md in ALIGN phase for implementation
- `ui-craft` — Downstream: consumes UI-related tasks from PLAN.md
- `code-review-and-quality` — Review plan for completeness
- `dispatching-parallel-agents` — Parallelize independent tasks based on plan

**Skill Chain:**
```
product-thinking (PRODUCT.md)
       │
       ▼
project-discovery (DOMAIN.md)
       │
       ▼
planning-and-task-breakdown (PLAN.md) ◄── You are here
       │
       ├──► dev-craft (implementation)
       └──► ui-craft (UI implementation)
```