---
name: token-budget
description: |
  DEPRECATED — merged into `cost-optimizer`. Do not load this skill; load skill("cost-optimizer") instead.
model: nemotron-3-ultra-free
version: 2.1.0
preamble-tier: 3
allowed-tools:
  - Read
triggers:
  - "token budget"
  - "token count"
  - "response length"
  - "short version"
  - "brief answer"
  - "detailed answer"
  - "exhaustive answer"
metadata:
  origin: agent-master-skills
  deprecated: true
  superseded-by: cost-optimizer
---

# Token Budget (Deprecated)

This skill has been merged into `cost-optimizer` — load skill("cost-optimizer") instead and use its Response Depth Budget flow for all response-depth choice, token estimation, and budget enforcement.

This shim will be removed in a future release.
