---
name: planning-and-task-breakdown
description: Breaks work into ordered, verifiable tasks. Use when you have a spec and need implementable units with acceptance criteria.
---

# Planning & Task Breakdown

## Overview

Decompose work into small, verifiable tasks with explicit acceptance criteria.
Good task breakdown = reliable agent work.
Every task should be small enough to implement, test, and verify in a single focused session.

## When to Use

- You have a spec and need implementable units
- Task feels too large or vague to start
- Work needs parallelization across agents/sessions
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

### Step 1: Enter Plan Mode

Before writing any code, operate in read-only mode:

- Read the spec and relevant codebase sections
- Identify existing patterns and conventions
- Map dependencies between components
- Note risks and unknowns

**Do NOT write code during planning.**
Output is a plan document, not implementation.

### Step 2: Collect Everything

Gather from prompt/file:

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

### Step 3: Verify Assumptions

Check against reality:

```
VERIFIED:
- Feasible: [yes/no with reasoning]
- Existing patterns: [what's already there]
- Dependencies: [available/needed]
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
    ├── API models/types
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
- `src/path/to/file.ts`
- `tests/path/to/test.ts`

**Estimated scope:** [XS/S/M/L]
```

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

### Step 10: Write the Plan

Save to `docs/plans/YYYY-MM-DD-feature-name.md`.

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

## Plan Document Template

```markdown
# Implementation Plan: [Feature Name]

## Overview
[One paragraph summary]

## Architecture Decisions
- [Decision 1 and rationale]
- [Decision 2 and rationale]

## Task List

### Phase 1: Foundation
- [ ] Task 1: ...
- [ ] Task 2: ...

### Checkpoint: Foundation
- [ ] Tests pass, builds clean

### Phase 2: Core Features
- [ ] Task 3: ...
- [ ] Task 4: ...

### Checkpoint: Core Features
- [ ] End-to-end flow works

### Phase 3: Polish
- [ ] Task 5: ...
- [ ] Task 6: ...

### Checkpoint: Complete
- [ ] All acceptance criteria met
- [ ] Ready for review

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [High/Med/Low] | [Strategy] |

## Open Questions
- [Question needing human input]
```

## Output Files

- **Plan document:** `docs/plans/YYYY-MM-DD-feature.md`
- **Task list:** `docs/plans/YYYY-MM-DD-feature-tasks.md`

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
- [ ] Task dependencies identified and ordered
- [ ] No task touches more than ~5 files
- [ ] Checkpoints exist between phases
- [ ] Human has reviewed and approved plan

Can't check all boxes? Plan is incomplete. Don't start.

## Integration

**Use with:**
- `dev-craft` — Plan feeds into dev-craft ALIGN phase
- `ui-craft` — Plan feeds into ui-craft ALIGN phase
- `verification-before-completion` — Verify plan is complete
- `code-review-and-quality` — Review plan for completeness
- `dispatching-parallel-agents` — Parallelize independent tasks
