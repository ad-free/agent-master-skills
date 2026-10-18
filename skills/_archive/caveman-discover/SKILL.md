---
name: caveman-discover
description: Use when you need compact, lazy exploration of a codebase or problem. Quick scan with minimal token usage — finds what matters without over-investigating.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
triggers:
  - "caveman discover"
  - "compact discovery"
  - "quick scan"
  - "lazy exploration"
  - "what's in here"
metadata:
  origin: agent-master-skills
  domain: exploration
  integrates-with: [caveman, graphify, codegraph]
---

# Caveman Discover

Compact, lazy exploration. Find what matters with minimal tokens.

## When to Use

- Quick codebase orientation: "what's in here?"
- Finding a specific pattern without deep investigation
- Pre-scan before committing to a full graphify or codegraph query

## Workflow

1. **Glob for structure** — `ls` or `find` to see directory layout
2. **Grep for key terms** — one focused search for the topic
3. **Read 1-3 files** — only what the grep surfaces
4. **Report** — 3-5 lines: what exists, where, key findings

## Output

Compact summary. No essays. Path references: `path:line`.

## When NOT to Use

- Deep architecture questions → use `graphify`
- Exact symbol lookup → use `codegraph`
- Full codebase audit → use `agent-architecture-audit`