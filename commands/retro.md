---
name: retro
description: Weekly retrospective — analyze commits, patterns, metrics, extract learnings
triggers:
  - "weekly retro"
  - "retrospective"
  - "what did we ship"
  - "engineering retrospective"
  - "sprint retro"
---

# /retro — Weekly Retrospective

## When to Use
- End of week/sprint
- Project health check
- Continuous improvement
- Team reflection

## Workflow

### 1. Analyze History
```
skill("retro")  # Analyze commit history, work patterns, code quality metrics
```

### 2. Extract Learnings
```
skill("learn")  # Search, prune, export learnings across sessions
```

### 3. Generate Report
- What shipped (features, fixes, improvements)
- What didn't (blockers, deferrals, tech debt)
- Patterns (velocity, quality, collaboration)
- Metrics (cycle time, review time, defect rate)
- Praise & growth areas per person

### 4. Action Items
- Capture improvements as tasks
- Update processes/skills if needed
- Schedule follow-ups

## Output
- Retrospective report (markdown)
- Action items with owners
- Updated learnings
- Process improvements identified

## Completion
**DONE** — Retro complete, report generated, actions captured
**DONE_WITH_CONCERNS** — Retro done but [low participation/incomplete data]
**BLOCKED** — No git history, or tool failure
**NEEDS_CONTEXT** — Need [date range/team members/focus areas]