---
name: agent-eval
description: |
  Use when comparing coding agents head-to-head on custom tasks with pass rate, cost, time,
  and consistency metrics. Compare agents, measure performance before adopting a new tool/model,
  or run regression checks when an agent updates its model or tooling. Do NOT use for per-skill
  golden regression testing (see eval-harness).
model: nemotron-3-ultra-free
version: 1.0.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "compare agents"
  - "agent benchmark"
  - "which agent is best"
  - "agent selection"
  - "head-to-head"
  - "agent eval"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 1.0.0
  domain: quality-safety
  integrates-with: [eval-harness, verification-before-completion, verification-before-completion]
  source-enhancements: v1.0.0 from ECC agent-eval
---
TOKEN CEILING: ~3K tokens. If skill exceeds, extract sections to references/.

# Agent Eval

A lightweight framework for comparing coding agents head-to-head on reproducible tasks. Every "which agent is best?" comparison runs on vibes — this tool systematizes it.

## When to Activate

- Comparing agents (agent-master-skills subagents, Claude Code, Aider, Codex, etc.) on your own codebase
- Measuring agent performance before adopting a new tool or model
- Running regression checks when an agent updates its model or tooling
- Producing data-backed agent selection decisions for a team

## Core Concepts

### YAML Task Definitions

Define tasks declaratively. Each task specifies what to do, which files to touch, and how to judge success:

```yaml
name: add-retry-logic
description: Add exponential backoff retry to the HTTP client
repo: ./my-project
files:
  - src/http_client.py
prompt: |
  Add retry logic with exponential backoff to all HTTP requests.
  Max 3 retries. Initial delay 1s, max delay 30s.
judge:
  - type: pytest
    command: pytest tests/test_http_client.py -v
  - type: grep
    pattern: "exponential_backoff|retry"
    files: src/http_client.py
commit: "abc1234"  # pin to specific commit for reproducibility
```

### Git Worktree Isolation

Each agent run gets its own git worktree — no Docker required. Provides reproducibility isolation so agents cannot interfere with each other or corrupt the base repo.

### Metrics Collected

| Metric | What It Measures |
|--------|-----------------|
| Pass rate | Did the agent produce code that passes the judge? |
| Cost | API spend per task (when available) |
| Time | Wall-clock seconds to completion |
| Consistency | Pass rate across repeated runs (e.g., 3/3 = 100%) |

## Workflow

### 1. Define Tasks

Create a `tasks/` directory with YAML files, one per task:

```bash
mkdir -p .eval-agents/tasks
# Write task definitions (see template above)
```

### 2. Run Agents

Execute agents against your tasks:

```bash
agent-eval run --task tasks/add-retry-logic.yaml --agent code-reviewer --agent implementer --runs 3
```

Each run:
1. Creates a fresh git worktree from the specified commit
2. Hands the prompt to the agent
3. Runs the judge criteria
4. Records pass/fail, cost, and time

For agent-master-skills subagents, spawn via the Task tool with the agent's `model` override. For external agents (Claude Code, Aider, Codex), invoke their CLI in the worktree.

### 3. Compare Results

Generate a comparison report:

```bash
agent-eval report --format table
```

```
Task: add-retry-logic (3 runs each)
┌──────────────┬───────────┬────────┬────────┬─────────────┐
│ Agent        │ Pass Rate │ Cost   │ Time   │ Consistency │
├──────────────┼───────────┼────────┼────────┼─────────────┤
│ implementer  │ 3/3       │ $0.12  │ 45s    │ 100%        │
│ code-reviewer│ 2/3       │ $0.08  │ 38s    │  67%        │
└──────────────┴───────────┴────────┴────────┴─────────────┘
```

## Judge Types

### Code-Based (deterministic)

```yaml
judge:
  - type: pytest
    command: pytest tests/ -v
  - type: command
    command: npm run build
```

### Pattern-Based

```yaml
judge:
  - type: grep
    pattern: "class.*Retry"
    files: src/**/*.py
```

### Model-Based (LLM-as-judge)

```yaml
judge:
  - type: llm
    prompt: |
      Does this implementation correctly handle exponential backoff?
      Check for: max retries, increasing delays, jitter.
```

## Metrics & Reliability

### pass@k

- `pass@1`: First attempt success rate
- `pass@3`: Success within 3 attempts (at least one success)
- Recommended: **run at least 3 trials** per agent to capture variance — agents are non-deterministic

### pass^k

- `pass^3`: All 3 consecutive trials succeed — stability test for critical paths

### Cost Tracking

Track cost alongside pass rate — a 95% agent at 10x the cost may not be the right choice. See `cost-optimizer` for model pricing and budget tracking.

## Best Practices

- **Start with 3-5 tasks** that represent your real workload, not toy examples
- **Run at least 3 trials** per agent to capture variance
- **Pin the commit** in your task YAML so results are reproducible across days/weeks
- **Include at least one deterministic judge** (tests, build) per task — LLM judges add noise
- **Track cost alongside pass rate** — a 95% agent at 10x the cost may not be the right choice
- **Version your task definitions** — they are test fixtures, treat them as code
- **Isolate with git worktrees** — never run agents against the live working tree

## Anti-Patterns

- Comparing agents on toy tasks that don't reflect real workload
- Single trial per agent — non-deterministic results
- LLM-only judges — adds noise, no ground truth
- Ignoring cost and latency while chasing pass rates
- Running agents against the base repo without worktree isolation

## Output Contract

On completion, produce:

1. Task definitions (YAML, in `.eval-agents/tasks/`)
2. Run results (pass/fail, cost, time per run)
3. Comparison report (table format)
4. Recommendations with trade-offs (pass rate vs cost vs time)
5. Updated `.eval-agents/results.json`

## Completion Status Protocol

- **DONE** — Comparison complete, report generated, recommendation documented
- **DONE_WITH_CONCERNS** — Report done but [missing cost data/limited trials]
- **BLOCKED** — Cannot run [agents unavailable/worktree failure]
- **NEEDS_CONTEXT** — Need [task definitions/target agents/commit to pin]

## References

- `references/agent-eval-task-schema.json` — Task definition schema
- `skills/eval-harness/` — Per-skill golden regression (sister skill)
- `skills/cost-optimizer/` — Cost tracking and model routing
