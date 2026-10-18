---
name: caveman-optimize
description: Use when you need compact performance optimization with minimal changes. Quick bottleneck scan with targeted fixes — no over-engineering.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
triggers:
  - "caveman optimize"
  - "compact optimization"
  - "quick perf fix"
  - "lazy optimize"
  - "speed up"
metadata:
  origin: agent-master-skills
  domain: performance
  integrates-with: [caveman, performance-profiler-and-tuner, debugging-and-error-recovery]
---

# Caveman Optimize

Compact performance optimization. Fix bottlenecks with minimal changes.

## When to Use

- Quick perf scan: "what's slow?"
- Targeted bottleneck fix
- Pre-commit optimization check

## Workflow

1. **Grep for hot paths** — loops, queries, I/O
2. **Read 1-3 files** — focus on bottleneck
3. **Apply minimal fix** — stdlib first, no new deps
4. **Report** — what changed, expected impact

## Output

Minimal diff. Expected performance impact.

## When NOT to Use

- Full profiling → use `performance-profiler-and-tuner`
- Memory leaks → use `debugging-and-error-recovery`
- Architecture redesign → use `architecture-patterns`