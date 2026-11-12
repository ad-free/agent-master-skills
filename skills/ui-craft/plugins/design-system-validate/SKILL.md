---
name: design-system-validate
description: Use when you need to validate UI code against design system tokens and component library specifications, or audit UI for design consistency, responsiveness, performance, and WCAG accessibility standards.
disable-model-invocation: true
metadata:
  version: 1.0.0
  origin: agent-master-skills
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