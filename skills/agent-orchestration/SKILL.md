---
name: agent-orchestration
description: |
  DEPRECATED — merged into `conductor`. Load `conductor` instead; this shim
  exists only so existing installs and references keep resolving.
model: nemotron-3-ultra-free
version: 1.0.0
preamble-tier: 3
allowed-tools:
  - Read
triggers:
  - "orchestrate parallel agents"
  - "run backend and frontend in parallel"
  - "coordinate multiple agents"
  - "split work across agents"
metadata:
  origin: agent-master-skills
  deprecated: true
  superseded-by: conductor
---
# `agent-orchestration` — Deprecated
Merged into `conductor`. Load `skill("conductor")` instead. This file will be removed in a future release.
