---
name: design-system-auditor
description: DEPRECATED — merged into `design-system-validate`. Use that skill for design consistency, responsiveness, performance, and WCAG audits.
model: gpt-5-nano
version: 2.1.0
preamble-tier: 1
allowed-tools:
  - Read
triggers:
  - "audit UI"
  - "design consistency"
  - "design tokens"
  - "WCAG audit"
  - "accessibility check"
disable-model-invocation: true
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  deprecated: true
  superseded-by: design-system-validate
---

# design-system-auditor (DEPRECATED)

This skill has been merged into `skill("design-system-validate")`. Load that skill instead.

Removal notice: this shim will be removed in a future release; update all references to `design-system-validate`.
