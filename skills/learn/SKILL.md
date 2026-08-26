---
name: learn
description: |
  Use when you need to capture, search, prune, or export persistent project learnings
  across sessions. Runs proactively after major milestones and retrospectives.
model: gpt-5-nano
version: 2.1.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - "what have we learned"
  - "show learnings"
  - "prune stale learnings"
  - "export learnings"
  - "didn't we fix this before"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 2.1.0
  domain: context-memory
  integrates-with: [retro, handoff, context-engineering]
---
TOKEN CEILING: ~3K tokens. If skill exceeds, extract sections to references/.

# Learn

Persistent project learnings manager. Search, prune, export learnings across sessions.
Use when asked "what have we learned", "show learnings", "prune stale learnings", "export learnings".
Proactively suggest when user asks "didn't we fix this before?".
