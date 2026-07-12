# agent-master-skills

Skills for AI coding agents — composable, disciplined, evidence-based.

## Skills

### Core Pipelines

| Skill | Purpose | Phases |
|-------|---------|--------|
| `dev-craft` | Backend development pipeline | 10 (LOAD → SHIP) |
| `ui-craft` | Frontend development pipeline | 9 (LOAD → SHIP) |

### Essential Skills

| Skill | Purpose | Iron Law |
|-------|---------|----------|
| `planning-and-task-breakdown` | Breaks work into ordered tasks | NO IMPLEMENTATION WITHOUT A WRITTEN PLAN |
| `debugging-and-error-recovery` | Root-cause investigation | NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST |
| `verification-before-completion` | Evidence gates | NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE |
| `code-review-and-quality` | Code review protocols | NO CODE WITHOUT REVIEW EVIDENCE |
| `dispatching-parallel-agents` | Parallel execution | NO PARALLEL DISPATCH WITHOUT INDEPENDENCE VERIFICATION |

## Philosophy

1. **Plan before code** — write the plan, then implement
2. **Evidence over assumption** — prove it works, don't assume
3. **Root cause over symptoms** — investigate before fixing
4. **Review over trust** — systematic quality checks
5. **Independence over speed** — parallel only when safe

## Integration

Skills compose with the core pipelines:

```
planning → feeds into dev-craft/ui-craft ALIGN phase
dev-craft BUILD → uses debugging-and-error-recovery
dev-craft REVIEW → uses code-review-and-quality
dev-craft SHIP → uses verification-before-completion
ui-craft BUILD → uses debugging-and-error-recovery
ui-craft REVIEW → uses code-review-and-quality
ui-craft SHIP → uses verification-before-completion
Any phase → uses dispatching-parallel-agents for independent tasks
```

## Usage

Each skill is standalone and can be used independently or composed with pipelines.

See `skills/SHARED.md` for the complete skill inventory and integration map.
