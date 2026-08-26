---
name: design-system-auditor
description: |
  Use when you need to audit UI code for design consistency, responsiveness, performance,
  and WCAG accessibility standards against design tokens and component library specs.
model: big-pickle
version: 2.1.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - "audit UI"
  - "design consistency"
  - "design tokens"
  - "WCAG audit"
  - "accessibility check"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.1.0
  domain: frontend
  integrates-with: [ui-component-builder, ui-craft, accessibility-deep]
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Design System Auditor

Audit UI code for design consistency, responsiveness, performance, and
WCAG accessibility standards. Use when validating UI against design
tokens and accessibility standards.

## Iron Law

**NO UI WITHOUT DESIGN TOKEN COMPLIANCE**
