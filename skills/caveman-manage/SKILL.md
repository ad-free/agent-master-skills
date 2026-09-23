---
name: caveman-manage
description: Use when you need compact state management with minimal overhead. Quick checkpoints, context saves, and session management without verbose documentation.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Write
  - Bash
triggers:
  - "caveman manage"
  - "compact state"
  - "quick checkpoint"
  - "lazy save"
  - "save progress"
metadata:
  origin: agent-master-skills
  domain: context
  integrates-with: [caveman, context-engineering, handoff, continuous-learning-v2]
---

# Caveman Manage

Compact state management. Save progress with minimal tokens.

## When to Use

- Quick checkpoint: "save where I am"
- Context rotation: preserve state before switching
- Session end: compact handoff

## Workflow

1. **Identify current state** — what's done, what's next
2. **Write compact checkpoint** — 5-10 lines max
3. **Store** — update state.json or handoff doc

## Output

Compact state snapshot. No essays.

## When NOT to Use

- Full context engineering → use `context-engineering`
- Session handoff → use `handoff`
- Learning capture → use `caveman-learn`