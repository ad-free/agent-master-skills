---
name: dev
description: Development mode — implementation, coding, building
model: big-pickle
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
default-skills:
  - dev-craft
  - ui-craft
  - planning-and-task-breakdown
  - debugging-and-error-recovery
  - verification-before-completion
---

# Development Context

## Purpose
Optimized for writing code, implementing features, and building systems.

## Default Behaviors
- **Model**: big-pickle (coding-optimized)
- **Preamble**: Standard (tier 3) — includes SHARED.md, relevant skill refs
- **Skills**: Auto-load dev-craft, ui-craft, planning-and-task-breakdown
- **Verification**: verification-before-completion after each phase

## Phase Flow
1. **SCOPE** → planning-and-task-breakdown (if no PLAN.md)
2. **BUILD** → dev-craft / ui-craft (TDD enforced via tdd-enforcer)
3. **TEST** → qa-and-edge-case-tester
4. **HARDEN** → verification-before-completion, secops-and-vulnerability-scanner
5. **REVIEW** → code-review-and-quality

## Token Budget
- Standard: ~50K tokens per phase
- Extended: ~100K for complex features
- Auto-compact at phase boundaries

## Cost Optimization
- Route simple tasks to deepseek-v4-flash-free
- Cache system prompts per skill
- Track tokens per phase

## Completion Protocol
Every phase ends with:
- **DONE** / **DONE_WITH_CONCERNS** / **BLOCKED** / **NEEDS_CONTEXT**
- Evidence: lint output, test results, typecheck
- Handoff document if switching context