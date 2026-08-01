---
name: planning-and-task-breakdown
description: |
  Decompose specs into ordered, verifiable tasks with DAG-based dependency
  mapping and Gherkin/Given-When-Then acceptance criteria. Use when you have a
  spec (PRODUCT.md/DOMAIN.md) and need implementable units. Invoked by: planner
  → implementer.
model: nemotron-3-ultra-free
version: 2.0.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "plan this feature"
  - "break down this task"
  - "create implementation plan"
  - "split this into tasks"
  - "dependency map"
  - "acceptance criteria"
metadata:
  origin: agent-master-skills
  output: PLAN.md
  preferred-model: nemotron-3-ultra-free
  version: 2.0.0
  domain: planning
  integrates-with: [product-thinking, project-discovery, dev-craft, ui-craft]
---

TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# Planning & Task Breakdown

## Relationship to existing skills

- `product-thinking` — produces PRODUCT.md that feeds into this skill's Step 0
- `project-discovery` — produces DOMAIN.md that feeds into this skill's Step 0
- `dev-craft` — consumes PLAN.md as input for implementation
- `ui-craft` — consumes PLAN.md for frontend implementation
- `grilling` — adversarial review of the plan before implementation

## When to Use

- You have a spec and need implementable units
- Task feels too large or vague to start
- Work needs parallelization across agents/sessions
- Need to communicate scope to human
- Implementation order isn't obvious

**When NOT to use:** Single-file changes with obvious scope, or spec already has well-defined tasks.

## When NOT to Use

- The task is a single file with obvious scope
- The spec is vague and hasn't been refined yet (run `product-thinking` first)
- You're implementing without a plan (violates the Iron Law)

## Workflow

### Phase 1: EXTRACT — Gather requirements from the spec

1. Read the spec (PRODUCT.md, DOMAIN.md, or user description)
2. Extract every capability, constraint, and non-functional rule as a requirement row
3. Preserve priority markers verbatim (`[REQUIRED P1]`, `🔴`, `G1/G3`, `⚪ [FUTURE PHASE]`)
4. Assign each requirement a stable ID: `REQ-001`, `REQ-002`, ...
5. Capture concrete constraints as requirements, not prose

**Exit criterion:** All requirements extracted with stable IDs and priorities.

### Phase 2: MAP — Build the DAG dependency graph

Map what depends on what using a strict DAG (Directed Acyclic Graph):

```
DAG STRUCTURE:

nodes = [each task]
edges = [dependency relationships: task A → task B means A must complete before B]

Rules:
- No circular dependencies (DAG must be acyclic)
- Every task has at most one "primary" dependency chain
- Cross-cutting tasks (shared utilities) are roots with no upstream deps
- Leaf nodes are the final deliverables
```

**DAG construction process:**

1. List all tasks from Phase 1
2. For each task, identify its direct dependencies (what must be done first)
3. Detect cycles — if A depends on B and B depends on A, split or reorder
4. Topological sort — order tasks so all dependencies come before dependents
5. Assign phases based on dependency depth:
   - Phase 1: Root tasks (no dependencies)
   - Phase 2: Tasks that depend only on Phase 1
   - Phase 3: Tasks that depend on Phase 1 + Phase 2
   - etc.

**Exit criterion:** All tasks ordered in a valid DAG with no cycles, phases assigned.

### Phase 3: DECOMPOSE — Break tasks into vertical slices

Each task must be a vertical slice (schema + API + UI for fullstack, or the minimal complete unit for single-domain):

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
```

**Exit criterion:** All tasks are vertical slices, no horizontal layering.

### Phase 4: CRITERIA — Generate Gherkin acceptance criteria for every sub-task

Every sub-task must have explicit Given-When-Then acceptance criteria:

```gherkin
Given [precondition/context]
When [action/event]
Then [expected outcome/observable behavior]
And [additional observable behavior]
```

**Rules for Gherkin criteria:**
- Every task must have at least one Given-When-Then scenario
- Given must state the initial state/context (not the action)
- When must be a single, testable action
- Then must be an observable, verifiable outcome (not an implementation detail)
- And clauses add additional observable outcomes
- No "and the system should work" — every Then must be testable

**Example:**
```gherkin
Task: User can create account

Given I am on the registration page
When I submit valid email, password, and name
Then a new account is created in the database
And I am redirected to the login page
And a welcome email is sent to the registered address

Given I am on the registration page
When I submit with an already-registered email
Then I see an error message "Email already in use"
And no account is created
```

**Exit criterion:** Every task has at least one Given-When-Then scenario that is testable and observable.

### Phase 5: VALIDATE — Verify the plan

1. **Traceability check:** Every P1/G1 requirement from the spec is traced to at least one task
2. **DAG check:** No circular dependencies, all dependencies are ordered correctly
3. **Slice check:** Every task is a vertical slice (not horizontal layering)
4. **Criteria check:** Every task has Given-When-Then acceptance criteria
5. **Sizing check:** No task exceeds L size (5-8 files); break down XL tasks
6. **Checkpoint check:** Verification checkpoints exist every 2-3 tasks
7. **Dependency check:** No task starts before its dependencies are complete

**Exit criterion (HARD GATE):** All validation checks pass. P1/G1 requirements 100% traced. DAG is valid. Every task has Gherkin criteria.

## The Iron Law

```
NO IMPLEMENTATION WITHOUT A WRITTEN PLAN
```

"I'll figure it out as I go" = tangled mess and rework.

## Task Template

Each task follows this structure:

```markdown
## Task [N]: [Short title]

**Requirement refs:** REQ-001, REQ-002   <!-- trace back to source spec rows -->

**Description:** One paragraph explaining what this task accomplishes.

**DAG dependency:** [Task numbers this depends on, or "None"]
**DAG dependents:** [Task numbers that depend on this, or "None"]
**Phase:** [1-5 based on DAG depth]

**Acceptance criteria (Given-When-Then):**
```gherkin
Given [precondition]
When [action]
Then [observable outcome]
```

**Verification:**
- [ ] Tests pass: `npm test -- --grep "feature"`
- [ ] Build succeeds: `npm run build`
- [ ] Manual check: [what to verify]

**Files likely touched:**
- `src/file.ts`
- `tests/test.ts`

**Estimated scope:** [XS/L]
```

> **REQ-IDs are mandatory for spec-driven work.** Every task must cite the source-spec requirement row(s) it satisfies. A task with no `Requirement refs:` is a symptom that the plan is being written from memory, not from the spec — the exact failure mode that drops P1 requirements. If you cannot cite a REQ-ID, either the requirement was never extracted (go back to Phase 1) or the task is out of scope.

> **DAG dependency is mandatory.** Every task must list its direct dependencies. A task with no `DAG dependency:` entry that depends on another task is a planning error — it will be built out of order.

> **Gherkin criteria are mandatory.** Every task must have at least one Given-When-Then scenario. A task with no acceptance criteria cannot be verified and should not be implemented.

## Task Sizing

| Size | Files | Scope | Example |
|------|-------|-------|---------|
| XS | 1 | Single function/config | Add validation rule |
| S | 1-2 | One component/endpoint | New API endpoint |
| M | 3-5 | One feature slice | User registration flow |
| L | 5-8 | Multi-component | Search with filtering |
| XL | 8+ | **Too large — break down** | — |

**Break down if:**
- Takes more than one focused session (2+ hours)
- Acceptance criteria need 3+ bullet points
- Touches 2+ independent subsystems
- Task title has "and" in it

## Module-Level Planning

For large projects (3+ modules), plan at module level first:

1. List all modules with priorities
2. Map dependencies between modules (DAG)
3. Define build order (foundation → core → extended)
4. Per module: define features and slices
5. Per feature: define Given-When-Then acceptance criteria

## Dependency-Aware Phasing

When planning large projects, order tasks by DAG dependency chain so each phase produces usable output:

| Phase | Modules | Strategy |
|-------|---------|----------|
| Phase 1: Foundation | Auth, Employee | No downstream dependencies — build first |
| Phase 2: Transaction | Attendance, Leave | Depends on Employee |
| Phase 3: Processing | Payroll, Tax | Depends on Attendance + Employee |
| Phase 4: Evaluation | KPI, Review | Depends on Employee + Payroll |
| Phase 5: Extended | Recruitment, Onboarding | Stand-alone modules |
| Phase 6: Mobile/Integration | API consumers | Need stable API from all phases |

**Bad:** Build Payroll directly (missing Employee + Attendance data)
**Good:** Employee → Attendance → Payroll (each phase produces usable output)

## Verification

Before starting implementation:

- [ ] Every task has Given-When-Then acceptance criteria
- [ ] Every task has DAG dependencies identified and ordered
- [ ] DAG has no circular dependencies (valid topological sort)
- [ ] Every task cites `Requirement refs:` (REQ-IDs) from the source spec
- [ ] `requirements.md` traceability matrix exists and P1/G1 coverage is 100%
- [ ] No task touches more than ~5 files
- [ ] Checkpoints exist every 2-3 tasks
- [ ] Every task is a vertical slice (not horizontal layering)
- [ ] Human has reviewed and approved plan

Can't check all boxes? Plan is incomplete. Don't start.

## Integration

Upstream: `product-thinking` (PRODUCT.md) → `project-discovery` (DOMAIN.md).
Downstream: `dev-craft` / `ui-craft` consume PLAN.md.

## Outputs / Handoffs

On completion, invokes: `skill("grilling")` with context:
- `planPath`: "PLAN.md"
- `requirementsPath`: "requirements.md" (if exists)
- `domainPath`: "DOMAIN.md" (if exists)

**Grilling** performs adversarial review of the plan, outputs `risk-register.md`, then invokes `skill("dev-craft")` or `skill("ui-craft")` for implementation.

## Quality Gates

- [ ] All P1/G1 requirements traced to a task with Given-When-Then criteria
- [ ] DAG is valid (no cycles, topological sort exists)
- [ ] Every task has DAG dependencies and dependents listed
- [ ] Every task is a vertical slice
- [ ] No XL-sized tasks remain (all broken down)
- [ ] Verification checkpoints exist every 2-3 tasks
- [ ] Human has reviewed and approved plan

## Error Handling

| Failure Mode | Response |
|--------------|----------|
| Circular dependency in DAG | Break the cycle by reordering or splitting a task |
| Missing REQ-ID trace | Go back to Phase 1, extract the requirement |
| No Given-When-Then criteria | Add at least one scenario per task before proceeding |
| Task is too large (XL) | Break it down into smaller vertical slices |
| P1/G1 requirement has no task | Add a task to cover the requirement before proceeding |

## References

- `references/PLAN.md` — Plan document template consumed by dev-craft
- `references/dag-template.md` — DAG construction template and cycle detection
- `references/gherkin-template.md` — Given-When-Then scenario template with examples