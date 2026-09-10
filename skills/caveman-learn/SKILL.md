---
name: caveman-learn
description: Use when you need compact, lazy learning capture. Quick session notes with minimal overhead — records what matters without verbose documentation.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Write
  - Bash
triggers:
  - "caveman learn"
  - "compact learning"
  - "quick notes"
  - "lazy capture"
  - "record learnings"
metadata:
  origin: agent-master-skills
  domain: context
  integrates-with: [caveman, learn, context-engineering, handoff]
---

# Caveman Learn

Compact learning capture. Record what matters with minimal tokens.

## When to Use

- End of session: capture key decisions and outcomes
- Quick retrospective: what worked, what didn't
- Before context rotation: preserve durable insights

## Workflow

1. **Scan session** — identify key decisions, fixes, insights
2. **Write 3-5 bullet points** — no essays
3. **Store** — update learnings DB or handoff doc

## Output

Bullet points. Decisions, outcomes, file references.

## When NOT to Use

- Full retrospective → use `retro`
- Structured knowledge base → use `learn`
- Session handoff → use `handoff`