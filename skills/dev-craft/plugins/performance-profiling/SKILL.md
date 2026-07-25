---
name: performance-profiling
description: Use when you need performance bottleneck detection and optimization for backend services.
metadata:
  origin: agent-master-skills
---

# Performance Profiling Plugin

## Overview

Systematic performance analysis for backend services. Identifies bottlenecks through profiling, load testing, and query analysis.

## When to Use

- Slow API response times
- High database query latency
- Memory leaks or excessive CPU usage
- Before scaling infrastructure
- After significant code changes

## Profiling Tools by Stack

| Stack | Profiler | Command |
|-------|----------|---------|
| Node.js | `clinic` | `clinic doctor -- node server.js` |
| Python | `cProfile` / `py-spy` | `python -m cProfile -o output.prof script.py` |
| Go | `pprof` | `go tool pprof htt/heap` |
| Rust | `perf` / `flamegraph` | `cargo flamegraph` |

## Query Analysis

- Enable slow query logging
- Run `EXPLAIN ANALYZE` on all queries in hot paths
- Check for missing indexes (sequential scans)
- Check for N+1 query patterns

## Integration

Registered in `state.json`:
```json
{
  "plugins": ["performance-profiling"]
}
```