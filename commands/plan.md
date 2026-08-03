---
name: plan
description: Full planning workflow — scope → plan → review → approve
triggers:
  - "plan this"
  - "create a plan"
  - "plan feature"
  - "plan project"
---

# /plan — Planning Workflow

## When to Use
- Starting a new feature or project
- Need structured task breakdown before implementation
- Want to review architecture/approach before coding

## Workflow

### 1. Scope (product-thinking → planning-and-task-breakdown)
```
skill("product-thinking")  # If idea is vague
skill("planning-and-task-breakdown")  # Creates PLAN.md with tasks, DAG, acceptance criteria
```

### 2. Review (grilling → architecture-decision-records)
```
skill("grilling")  # Stress-test the plan
skill("architecture-decision-records")  # Document key decisions as ADRs
```

### 3. Approve
- Present PLAN.md to user
- Get explicit approval before implementation
- Record decision in PLAN.md

## Output
- `PLAN.md` with phased tasks, dependencies, acceptance criteria
- `ADR-*.md` for architectural decisions
- Clear go/no-go for implementation

## Completion
**DONE** — PLAN.md created, reviewed, and approved
**DONE_WITH_CONCERNS** — Plan created but needs clarification on [X]
**BLOCKED** — Cannot proceed; missing [requirements/specs/stakeholder input]
**NEEDS_CONTEXT** — Need [specific info] to create meaningful plan