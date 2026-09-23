---
name: learn
description: |
  DEPRECATED — merged into `continuous-learning-v2`. Do not load this skill; load skill("continuous-learning-v2") instead.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 2
allowed-tools:
  - Read
triggers:
  - "what have we learned"
  - "show learnings"
  - "prune stale learnings"
  - "export learnings"
  - "didn't we fix this before"
metadata:
  origin: agent-master-skills
  deprecated: true
  superseded-by: continuous-learning-v2
---

# Learn (Deprecated)

This skill has been merged into `continuous-learning-v2` — load skill("continuous-learning-v2") instead and use its Project Learnings Query Aliases (`instinct-status`, `instinct-prune`, `instinct-export`) for all learnings query, capture, prune, and export flows.

This shim will be removed in a future release.
