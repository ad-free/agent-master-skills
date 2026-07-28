---
name: dispatching-parallel-agents
description: |
  Run independent tasks simultaneously using subagents. Use when multiple tasks
  have no dependencies and can execute concurrently.
  Invoked by: implementer, orchestrator, test-engineer.
version: 1.1.0
preamble-tier: 3
allowed-tools:
  - Agent
  - Read
  - Bash
  - Grep
  - Glob
triggers:
  - "run these in parallel"
  - "dispatch parallel agents"
  - "execute concurrently"
  - "run tests in parallel"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  independence-verification: required
  integrates-with: [agent-orchestration, dev-craft]
---

TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# Dispatching Parallel Agents

## Overview

Run independent tasks simultaneously. Don't wait for one task when you can start another.

**Core principle:** Parallel work is faster than sequential work — when tasks are truly independent.

## When to Use

- Multiple independent test files to run
- Multiple files to create/modify (no dependencies)
- Multiple searches to perform
- Multiple reviews to conduct
- Multiple reports to generate

**When NOT to use:**
- Tasks depend on each other's output
- Tasks modify the same file
- Tasks need shared context
- Tasks require human decisions between them

## Invocation Protocol

**Load when:** Multiple independent tasks exist that can run concurrently
**Invoke via:** `skill(name="dispatching-parallel-agents")`
**Resume to:** Continue current phase after all parallel tasks complete

## The Iron Law

```
NO PARALLEL DISPATCH WITHOUT INDEPENDENCE VERIFICATION
```

If tasks share state, parallel execution creates conflicts. Verify independence first.

## Independence Check

Before dispatching in parallel, verify:

```
INDEPENDENCE CHECK:
- [ ] Tasks don't modify the same files
- [ ] Tasks don't depend on each other's output
- [ ] Tasks don't need shared context
- [ ] Tasks don't require sequential human decisions
- [ ] Tasks are truly isolated
```

**Any "no" = sequential execution.**

## Dispatch Process

```
1. VERIFY independence — check each task pair for shared files, output dependencies, or shared decisions
2. PREPARE context — for each agent: task description, required context, output format, boundaries (keep minimal)
3. DISPATCH all agents in ONE message with task descriptions
4. WAIT — do NOT proceed until all complete; note failures, handle after
5. INTEGRATE — collect results, check conflicts, merge, verify

## Model Selection

| Task Type | Model |
|-----------|-------|
| Mechanical (1-2 files, clear spec) | Fast/cheap |
| Integration (multiple files) | Standard |
| Architecture (design decisions) | Most capable |
| Review (quality assessment) | Standard or capable |

**Always specify model explicitly.** Don't inherit session default.

## Progress Tracking

Track parallel work:

```
PARALLEL STATUS:
- Agent 1: [task] → [status]
- Agent 2: [task] → [status]
- Agent 3: [task] → [status]

Completed: [count]/[total]
Failed: [count]
```

## Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "These tasks are probably independent" | Probably ≠ verified. Check. |
| "It'll be faster in parallel" | Not if they conflict. Verify first. |
| "I'll just dispatch and hope" | Hope is not a strategy. Verify. |
| "The agents will figure it out" | Agents need clear, independent tasks. |

## Red Flags — STOP and Go Sequential

Same file modifications, output dependencies, shared state, interdependent human decisions, can't verify independence, or more than 5 parallel agents. **All of these mean: execute sequentially.**

## Conflict Resolution

If parallel agents create conflicts:

1. **Stop** — don't try to fix conflicts in parallel
2. **Identify** — what files/methods conflicted
3. **Resolve** — manually merge or re-sequence
4. **Prevent** — next time, verify independence better

## Parallel vs Sequential Decision Tree

Tasks independent (no shared files, no dependencies)? → **PARALLEL**. Same file, shared state, or output dependencies? → **SEQUENTIAL**. Use the Independence Check above.

## Integration

**Use with:** `agent-orchestration`, `dev-craft` BUILD (parallel tests), `verification-before-completion`.