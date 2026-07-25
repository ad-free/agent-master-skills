---
name: dispatching-parallel-agents
description: Use when you have multiple independent tasks that can run concurrently.
  Parallel execution for non-dependent work.
metadata:
  origin: agent-master-skills
owner: noname.spyware@gmail.com
allowedTools:
- file
- http

---

# Dispatching Parallel Agents

## Overview

Run independent tasks simultaneously. Don't wait for one task when you can start another.

**Core principle:** Parallel work is faster than sequential work — when tasks are truly independent.

## When to Use

- Multiple independent test files to run
- Multiple files to create${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/modify (no dependencies)
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
1. VERIFY independence
2. PREPARE context for each agent
3. DISPATCH all agents simultaneously
4. WAIT for all to complete
5. INTEGRATE results
```

### Step 1: Verify Independence

Check each task pair:
- Task A output → Task B input? → NOT independent
- Task A modifies file X → Task B modifies file X? → NOT independent
- Task A needs decision D → Task B needs decision D? → NOT independent

### Step 2: Prepare Context

For each agent, prepare:
- **Task description** — what to do
- **Required context** — what it needs to know
- **Output format** — how to report results
- **Boundaries** — what NOT to touch

**Keep context minimal.** Each agent gets only what it needs.

### Step 3: Dispatch

Dispatch ALL agents in ONE message:

```
Dispatching 3 parallel agents:

Agent 1: [task description]
Agent 2: [task description]
Agent 3: [task description]

All agents: report results when complete.
```

### Step 4: Wait

**Do NOT proceed until ALL agents complete.**

If an agent fails:
1. Note the failure
2. Continue waiting for others
3. Handle failures after all complete

### Step 5: Integrate

After all agents complete:
1. Collect all results
2. Check for conflicts
3. Merge results
4. Verify combined result

## Model Selection

Use the right model for each task:

| Task Type | Model | Reason |
|-----------|-------|--------|
| Mechanical (1-2 files, clear spec) | Fast${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/cheap model | Simple execution — use platform's fastest available |
| Integration (multiple files) | Standard | Needs judgment |
| Architecture (design decisions) | Most capable | Needs deep reasoning |
| Review (quality assessment) | Standard or capable | Needs judgment |

**Always specify model explicitly.** Don't inherit session default.

## Progress Tracking

Track parallel work:

```
PARALLEL STATUS:
- Agent 1: [task] → [status]
- Agent 2: [task] → [status]
- Agent 3: [task] → [status]

Completed: [count]${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/[total]
Failed: [count]
```

## Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "These tasks are probably independent" | Probably ≠ verified. Check. |
| "It'll be faster in parallel" | Not if they conflict. Verify independence first. |
| "I'll just dispatch and hope" | Hope is not a strategy. Verify. |
| "The agents will figure it out" | Agents need clear, independent tasks. Prepare context. |
| "I don't need to track progress" | You'll lose track. Track explicitly. |
| "One agent can do multiple tasks" | Maybe. But parallel is faster for independent tasks. |

## Red Flags — STOP and Go Sequential

- Tasks modify the same file
- Tasks depend on each other's output
- Tasks need shared state
- Tasks require human decisions between them
- You can't verify independence
- More than 5 parallel agents (coordination overhead)

**All of these mean: Execute sequentially.**

## Conflict Resolution

If parallel agents create conflicts:

1. **Stop** — don't try to fix conflicts in parallel
2. **Identify** — what files${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/methods conflicted
3. **Resolve** — manually merge or re-sequence
4. **Prevent** — next time, verify independence better

## Parallel vs Sequential Decision Tree

```
Multiple tasks?
├── Yes
│   ├── Independent? (no shared files, no dependencies)
│   │   ├── Yes → PARALLEL
│   │   └── No → SEQUENTIAL
│   └── Same file?
│       ├── Yes → SEQUENTIAL
│       └── No → Check dependencies
│           ├── None → PARALLEL
│           └── Some → SEQUENTIAL
└── No → Single task
```

## Integration

**Use with:**
- `agent-orchestration` — Orchestrate parallel task execution
- `dev-craft` Phase 5 BUILD (TDD loop) — Run independent tests in parallel
- `verification-before-completion` — Verify all parallel results before claiming done