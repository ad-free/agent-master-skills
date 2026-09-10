---
name: caveman-explore
description: Use when you need compact codebase exploration with minimal context. Quick scan for patterns, structure, or specific code without deep investigation.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
triggers:
  - "caveman explore"
  - "compact exploration"
  - "quick look"
  - "lazy scan"
  - "what's here"
metadata:
  origin: agent-master-skills
  domain: exploration
  integrates-with: [caveman, graphify, codegraph]
---

# Caveman Explore

Compact codebase exploration. Find patterns with minimal tokens.

## When to Use

- Quick pattern scan: "what's here?"
- Finding similar code without deep investigation
- Pre-scan before committing to graphify

## Workflow

1. **Glob for files** — directory structure
2. **Grep for patterns** — one focused search
3. **Read 1-3 files** — only what's needed
4. **Report** — 3-5 lines: patterns found, locations

## Output

Compact findings. Path references: `path:line`.

## When NOT to Use

- Deep architecture → use `graphify`
- Exact symbol → use `codegraph`
- Full audit → use `agent-architecture-audit`