---
name: context-restore
description: Resume session — load state, learnings, handoff, continue from last phase
triggers:
  - "resume"
  - "restore context"
  - "where was I"
  - "continue work"
---

# /context-restore — Session Resume

## When to Use
- Starting a new session
- Switching back to a project
- After context-save checkpoint
- Multi-session work

## Workflow

### 1. Load State
```
skill("context-engineering")  # Load memory hierarchy, restore context
```

### 2. Read Handoff
```
skill("handoff")  # Read latest handoff document
```

### 3. Review Learnings
```
skill("learn")  # Show relevant project learnings
```

### 4. Check Git Status
```
git status
git log --oneline -5
```

### 5. Resume from Last Phase
- Read `PLAN.md` for current task
- Check `.dev-craft/state.json` or `.ui-craft/state.json`
- Continue from last incomplete phase

## Output
- Restored context summary
- Current task and phase
- Blockers/decisions from last session
- Next steps

## Completion
**DONE** — Context restored, ready to continue
**DONE_WITH_CONCERNS** — Restored but [stale state/missing handoff]
**BLOCKED** — No saved state found, or state corrupted
**NEEDS_CONTEXT** — Need [which session/project/branch to restore]