---
name: performance-profiler-and-tuner
description: |
  Analyze bottlenecks, memory leaks, query optimizations, bundle sizes,
  and runtime execution profiling. Use when performance is degraded,
  a bottleneck is identified, or optimization is needed. Do NOT use
  for general code refactoring (see refactor-and-cleanup) or for
  security auditing (see secops-and-vulnerability-scanner).
  
model: big-pickle
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "performance profiling"
  - "bottleneck analysis"
  - "memory leak"
  - "query optimization"
  - "bundle size"
  - "runtime profiling"
  - "performance tuning"
  - "slow query"
  - "optimize performance"
  - "profile execution"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: specialized-engineering
  integrates-with: [observability-engineering, dev-craft]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# performance-profiler-and-tuner

## Relationship to existing skills

- dev-craft/plugins/performance-profiling: Provides the performance profiling plugin within dev-craft; performance-profiler-and-tuner provides a standalone profiling workflow.
- debugging-and-error-recovery: Uses profiling results to identify performance-related bugs; performance-profiler-and-tuner produces the profiling data that debugging-and-error-recovery then uses.
- refactor-and-cleanup: Cleans up code that may be causing performance issues; performance-profiler-and-tuner identifies the specific performance bottlenecks.
- secops-and-vulnerability-scanner: Security can impact performance (e.g., excessive input validation); performance-profiler-and-tuner ensures security does not degrade performance.

## When to Use

- Application is running slower than expected
- A specific bottleneck has been identified (slow query, slow API, slow render)
- Memory usage is growing over time (potential leak)
- Bundle size is larger than expected
- Query performance needs optimization
- Runtime execution profiling is needed
- Pre-release performance validation
- Comparing performance between two implementations

## When NOT to Use

- General code refactoring — see refactor-and-cleanup
- Security auditing — see secops-and-vulnerability-scanner
- Architecture decision documentation — see architecture-decision-records
- Adding new features — see dev-craft
- General debugging — see debugging-and-error-recovery

## Workflow

### Phase 1: Performance Baseline

1. **Define the performance target**: what is the acceptable performance threshold? (response time, memory usage, bundle size, throughput)
2. **Measure the current performance**: run benchmarks, profiling tools, or monitoring to establish a baseline
3. **Identify the symptom**: is it slow response time, high memory usage, large bundle size, or low throughput?
4. **Determine the scope**: which part of the system is affected? (frontend, backend, database, network, infrastructure)
5. **Document the baseline**: record the current performance metrics for comparison

### Phase 2: Bottleneck Identification

1. **Run profiling tools**:
   - Backend: CPU profiler, memory profiler, APM tools (New Relic, Datadog, Prometheus)
   - Frontend: Lighthouse, Chrome DevTools Performance panel, bundle analyzer
   - Database: query analyzer, EXPLAIN plans, slow query log
   - Network: bandwidth analysis, latency measurement
2. **Identify the top bottlenecks**: rank by impact (time spent, memory used, bundle size)
3. **Classify each bottleneck**:
   - CPU-bound: excessive computation, inefficient algorithms
   - Memory-bound: memory leaks, excessive allocations, large object graphs
   - I/O-bound: slow database queries, network calls, file reads
   - Bundle-bound: large dependencies, unused code, unoptimized assets
4. **Document each bottleneck** with location, impact, and root cause hypothesis

### Phase 3: Root Cause Analysis

1. **Investigate each bottleneck**: trace the execution path from symptom to root cause
2. **For CPU bottlenecks**: identify the hot functions, loops, or algorithms causing the slowdown
3. **For memory bottlenecks**: identify the objects that are not being garbage collected, the retention paths, and the allocation patterns
4. **For I/O bottlenecks**: identify the slow queries, network calls, or file operations
5. **For bundle bottlenecks**: identify the large dependencies, unused imports, or unoptimized assets
6. **Validate root causes**: use profiling data to confirm each hypothesis
7. **Prioritize bottlenecks** by impact and ease of fix

### Phase 4: Optimization

1. **Apply optimizations in priority order**:
   - CPU: algorithm improvement, caching, parallelization, lazy loading
   - Memory: object pooling, lazy initialization, weak references, garbage collection tuning
   - I/O: query optimization, indexing, connection pooling, CDN, caching
   - Bundle: tree-shaking, code splitting, lazy imports, asset optimization
2. **Measure after each optimization**: compare against the baseline to verify improvement
3. **Avoid premature optimization**: only optimize bottlenecks that are proven to be impactful
4. **Document each optimization**: what was changed, why, and the measured impact

### Phase 5: Validation

1. **Re-run benchmarks**: verify that performance has improved
2. **Compare against the baseline**: document the improvement percentage
3. **Check for regressions**: ensure optimizations did not introduce new bottlenecks
4. **Run load testing**: verify that performance holds under load
5. **Verify memory stability**: ensure no new memory leaks were introduced
6. **Run the full test suite**: ensure optimizations did not break functionality

### Phase 6: Reporting

1. **Compile the performance report**: baseline, bottlenecks found, optimizations applied, results
2. **Generate a performance regression alert**: if any metric worsened, flag it
3. **Update performance documentation**: document the performance characteristics and targets
4. **Set performance budgets**: define acceptable thresholds for future development

## Context Management

- Track profiling state in `.dev-craft/performance/<project>/state.json` with fields: `session_id`, `baseline_metrics`, `bottlenecks`, `optimizations_applied`, `current_metrics`, `status`
- On session resume, check state.json for any in-progress profiling session and continue from the last completed phase

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read profiling output, benchmark results, and source code | Only read project source and profiling data |
| Write | Create performance reports and optimization plans | Follow the performance report format |
| Edit | Apply optimizations to source code | One optimization at a time; measure impact after each |
| Bash | Run profiling tools, benchmarks, and load tests | Use established tools (Lighthouse, profiler, APM, query analyzer) |
| Grep | Find performance anti-patterns (N+1 queries, unnecessary re-renders) | Search within the target scope |
| Glob | Find profiling output and benchmark files | Pattern: `**/*.{json,html,csv}` |
| Task | Spawn subagent for deep profiling or load testing | Subagent must report findings, not make edits |

## Output Contract

On completion, the skill must produce:

1. A performance baseline report with current metrics
2. A bottleneck analysis document with root causes and impact
3. An optimization plan with prioritized changes
4. A performance improvement report with before/after metrics
5. Updated state.json with the profiling session results
6. Performance documentation and budgets

## Quality Gates

- [ ] Performance baseline is established before optimization begins
- [ ] All bottlenecks are identified with root causes
- [ ] Optimizations are applied in priority order
- [ ] Each optimization is measured against the baseline
- [ ] No regressions are introduced by optimizations
- [ ] Full test suite passes after all optimizations
- [ ] Performance improvement is documented with before/after metrics
- [ ] Performance budgets are defined for future development

## Error Handling

- **Profiling tool fails**: retry once; if it fails again, use manual profiling or alternative tools
- **Optimization causes a regression**: revert the optimization, investigate the cause, and try a different approach
- **Bottleneck cannot be reproduced**: document the conditions that failed to reproduce, escalate to the user with the observed discrepancy
- **Memory leak suspected but not confirmed**: run extended profiling with memory snapshots at intervals
- **Load test fails after optimization**: identify which optimization caused the failure, revert that optimization, and investigate