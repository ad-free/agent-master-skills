---
name: spec
description: Create specification — discovery → product thinking → structured spec
triggers:
  - "spec this"
  - "write spec"
  - "create spec"
  - "document requirements"
  - "turn into ticket"
---

# /spec — Specification Workflow

## When to Use
- Have a vague idea or requirements document
- Need to create a backlog-ready spec
- Converting requirements to structured specification
- Filing a detailed GitHub issue

## Workflow

### 1. Discovery (if specs provided)
```
skill("project-discovery")  # Parse Excel/CSV/MD/PDF → DOMAIN.md
```

### 2. Product Thinking
```
skill("product-thinking")  # 4-round refinement: problem → solution → scope → spec
```

### 3. Planning
```
skill("planning-and-task-breakdown")  # Decompose spec into verifiable tasks
```

### 4. Architecture (if needed)
```
skill("architecture-decision-records")  # Document key decisions
```

## Output
- `PRODUCT.md` — Product specification
- `DOMAIN.md` — Domain model (if discovered)
- `PLAN.md` — Implementation plan with tasks
- `ADR-*.md` — Architecture decisions

## Completion
**DONE** — Spec complete, tasks defined, ready for implementation
**DONE_WITH_CONCERNS** — Spec done but [open questions/needs stakeholder review]
**BLOCKED** — Cannot proceed without [requirements/stakeholder/decision]
**NEEDS_CONTEXT** — Need [requirements doc/stakeholder access/business context]