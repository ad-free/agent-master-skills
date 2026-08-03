---
name: context-save
description: Save session progress — checkpoint state, learnings, decisions
triggers:
  - "save progress"
  - "checkpoint"
  - "save my work"
  - "context save"
---

# /context-save — Context Checkpoint

## When to Use
- Ending a work session
- Before switching tasks
- After significant progress
- Before risky operations

## Workflow

### 1. Capture State
```
skill("context-compressor-and-pruner")  # Summarize context, prune stale
```

### 2. Persist Learnings
```
skill("learn")  # Log project learnings
```

### 3. Save Handoff
```
skill("handoff")  # Create structured handoff document
```

### 4. Git Checkpoint (optional)
```
git add -A && git commit -m "checkpoint: [description]"
```

## Output
- `.dev-craft/state.json` or `.ui-craft/state.json` updated
- `handoff-<timestamp>.md` created
- Learnings appended to `.learnings/`
- Git checkpoint (if requested)

## Completion
**DONE** — State saved, handoff created, learnings captured
**DONE_WITH_CONCERNS** — Saved but [incomplete phase/temp files]
**BLOCKED** — Cannot write state, disk full, or permission denied
**NEEDS_CONTEXT** — Need [confirmation on what to save/branch name]