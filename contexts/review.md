---
name: review
description: Review mode — code review, security audit, quality gates
model: nemotron-3-ultra-free
preamble-tier: 4
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Task
default-skills:
  - code-review-and-quality
  - verification-before-completion
  - secops-and-vulnerability-scanner
  - verification-before-completion
---

# Review Context

## Purpose
Optimized for analyzing code, finding issues, and validating quality.

## Default Behaviors
- **Model**: nemotron-3-ultra-free (deep analysis, 1M context)
- **Preamble**: Extended (tier 4) — full SHARED.md, all references
- **Skills**: code-review-and-quality, verification-before-completion, secops-and-vulnerability-scanner
- **No Write** — Read-only analysis by default

## Review Pipeline
1. **Structure** — Architecture, patterns, conventions
2. **Deterministic** — Lint, typecheck, tests, build
3. **Security** — SAST, dependencies, secrets, OWASP
4. **Convention** — Style, naming, imports, docs
5. **LLM Judge** — Holistic quality, maintainability

## Output Format
```
## REVIEW REPORT: <target>

### Blocking Issues (must fix)
- [ ] Issue — file:line — severity — fix suggestion

### Non-Blocking (should fix)
- [ ] Issue — file:line — suggestion

### Praise
- Good pattern at file:line
```

## Completion Protocol
- **DONE** — All gates green, no blocking issues
- **DONE_WITH_CONCERNS** — Minor issues documented
- **BLOCKED** — Blocking issues found, listed with fixes
- **NEEDS_CONTEXT** — Need clarification on [intent/requirement]