---
name: design-system-validate
description: Use when you need to validate UI code against design system tokens and component library specifications, or audit UI for design consistency, responsiveness, performance, and WCAG accessibility standards.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 1
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "design system validation"
  - "token compliance"
  - "design audit"
  - "component validation"
  - "design system check"
  - "audit UI"
  - "design consistency"
  - "WCAG audit"
disable-model-invocation: true
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
---

<!-- TOKEN CEILING: ~2K -->

# Design System Validate Plugin

## Iron Law

**NO UI WITHOUT DESIGN TOKEN COMPLIANCE**

## Overview

Enforces design system compliance across all UI code. Checks that colors, typography, spacing, and components match the defined design tokens. Also audits for design consistency, responsiveness, performance, and WCAG accessibility standards (merged from design-system-auditor).

## When to Use

- After generating new UI components
- Before design review
- When onboarding new team members
- Design token updates

## Validation Rules

- No hardcoded color values (all from tokens)
- Typography uses design system scale
- Spacing follows 4/8dp rhythm
- Components use library components where available
- No CSS custom properties not defined in tokens
- Responsive: layout holds at mobile/desktop breakpoints, no horizontal scroll on mobile
- Performance: no layout shifts, images sized, fonts preloaded
- Accessibility: WCAG contrast, focus states, semantic HTML, ARIA labels

## Integration

Registered in `state.json`:
```json
{
  "plugins": ["design-system-validate"],
  "pluginConfig": {
    "design-system-validate": {
      "strictMode": true
    }
  }
}
```