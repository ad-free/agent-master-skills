---
name: debug
description: Debug mode — systematic root cause investigation
model: nemotron-3-ultra-free
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
default-skills:
  - debugging-and-error-recovery
  - verification-before-completion
  - qa-and-edge-case-tester
---

# Debug Context

## Purpose
Optimized for reproducing, isolating, and fixing bugs systematically.

## Default Behaviors
- **Model**: nemotron-3-ultra-free (deep analysis, hypothesis testing)
- **Preamble**: Minimal (tier 2) — focus on error context
- **Skills**: debugging-and-error-recovery
- **Verification**: verification-before-completion mandatory

## Debugging Methodology (4-Phase)
1. **REPRODUCE** — Deterministic reproduction, capture full context
2. **ISOLATE** — Narrow to root cause, binary search, git bisect
3. **HYPOTHESIZE** — Evidence-based hypotheses, test each
4. **VERIFY** — Fix root cause, regression test, all gates green

## Required Evidence for Each Phase
- Error trace, input, state (REPRODUCE)
- Minimal failing case, call stack (ISOLATE)
- Hypothesis + test + result (HYPOTHESIZE)
- Fix + regression test + lint/type/test (VERIFY)

## Token Budget
- Minimal preamble, maximum for error analysis
- No auto-compact during active debugging
- Budget: ~100K tokens

## Cost Optimization
- Route simple lookups to deepseek-v4-flash-free
- Cache error patterns in learnings
- Reuse reproduction scripts

## Completion Protocol
- **DONE** — Root cause fixed, regression test added, all gates green
- **DONE_WITH_CONCERNS** — Fixed but [known limitation/needs monitoring]
- **BLOCKED** — Cannot reproduce after 2 rounds, or root cause unclear → ESCALATE
- **NEEDS_CONTEXT** — Need [error logs/env access/reproduction steps/data]