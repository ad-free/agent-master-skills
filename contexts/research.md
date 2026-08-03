---
name: research
description: Research mode — exploration, discovery, analysis, learning
model: nemotron-3-ultra-free
preamble-tier: 2
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - WebSearch
  - Task
default-skills:
  - project-discovery
  - product-thinking
  - architecture-patterns
  - backend-patterns
---

# Research Context

## Purpose
Optimized for exploring codebases, researching solutions, and learning.

## Default Behaviors
- **Model**: nemotron-3-ultra-free (best reasoning, 1M context)
- **Preamble**: Minimal (tier 2) — only essential AGENTS.md
- **Skills**: Discovery and thinking skills
- **Tools**: WebFetch, WebSearch enabled for external research

## Workflow
1. **Discover** — project-discovery (parse specs), codegraph_explore (codebase)
2. **Analyze** — architecture-patterns, backend-patterns, frontend patterns
3. **Synthesize** — product-thinking for structured output
4. **Document** — documentation-engineering for findings

## Token Budget
- Minimal preamble, maximum context for exploration
- No auto-compact — preserve research context
- Budget: ~200K tokens for deep research

## Cost Optimization
- Use deepseek-v4-flash-free for simple lookups
- Route complex analysis to nemotron-3-ultra-free
- Cache research findings in learnings

## Output
- Structured findings (markdown)
- Architecture decision records (ADRs)
- Recommendations with trade-offs
- References and sources

## Completion Protocol
- **DONE** — Research complete, findings documented
- **DONE_WITH_CONCERNS** — Partial findings, [gaps identified]
- **BLOCKED** — Cannot access [source/system/docs]
- **NEEDS_CONTEXT** — Need [specific question/scope/constraints]