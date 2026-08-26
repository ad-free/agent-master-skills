---
name: retro
description: |
  Use when you need a weekly engineering retrospective with git analysis, team contributions,
  code quality trends, and actionable learnings. Also runs proactively at sprint end.
model: deepseek-v4-flash-free
version: 2.1.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
triggers:
  - "weekly retro"
  - "what did we ship"
  - "engineering retrospective"
  - "retro"
metadata:
  origin: agent-master-skills
  preferred-model: deepseek-v4-flash-free
  version: 2.1.0
  domain: orchestration
  integrates-with: [learn, prompt-optimizer]
---
TOKEN CEILING: ~3K tokens. If skill exceeds, extract sections to references/.

# Retro

Weekly engineering retrospective. Analyzes commit history, work patterns, and code quality metrics
with persistent history and trend tracking. Team-aware: per-person contributions with praise and growth areas.

Use when asked "weekly retro", "what did we ship", "engineering retrospective".
Proactively suggest at end of work week or sprint.
