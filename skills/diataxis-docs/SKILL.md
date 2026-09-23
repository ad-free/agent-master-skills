---
name: diataxis-docs
description: |
  DEPRECATED — merged into `documentation-engineering`. Use that skill for all documentation work, including Diataxis-quadrant organization and sync-on-ship.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 2
allowed-tools:
  - Read
triggers:
  - "docs sync"
  - "diataxis"
  - "documentation"
  - "update docs"
  - "doc sync"
metadata:
  origin: agent-master-skills
  deprecated: true
  superseded-by: documentation-engineering
---

# diataxis-docs (Deprecated)

Merged into `documentation-engineering`, which now covers Diataxis-quadrant organization and sync-on-ship. Load `skill("documentation-engineering")` instead.
