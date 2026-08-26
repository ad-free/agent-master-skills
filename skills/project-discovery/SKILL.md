---
name: project-discovery
description: |
  Use when you have requirement documents (xlsx/csv/md/pdf) and need to parse them into a structured DOMAIN.md.
model: nemotron-3-ultra-free
version: 2.1.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "parse requirements"
  - "ingest spec"
  - "xlsx to domain"
  - "csv to domain"
  - "project discovery"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.1.0
  domain: planning
  integrates-with: [product-thinking, planning-and-task-breakdown]
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Project Discovery

Parse existing spec files (Excel, CSV, MD, PDF, text) into structured DOMAIN.md.
Use when user provides requirement documents — before planning or dev-craft.
Invoked by: triage, planner.

## Supported Formats

| Format | Parsing |
|--------|---------|
| Excel (.xlsx) | Sheet → entity, rows → features, columns → attributes |
| CSV | Same as Excel |
| Markdown | Headings → hierarchy, lists → features, tables → entities |
| PDF | Text extraction → heuristic structure |
| Plain text | Heuristic structure |

## Output: DOMAIN.md

```markdown
# Domain Model: <project>

## Entities
- <entity>: <description> [attributes]

## Features
- <feature>: <description> [priority, dependencies]

## Constraints
- <constraint>

## Priorities
- P0: <features>
- P1: <features>
- P2: <features>
```
