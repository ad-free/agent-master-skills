---
name: design-system-validate
description: Use when you need the design-system-validate skill (plugin).

---

---
name: design-system-validate
description: Use when validates UI code against design system tokens and component library specifications.
metadata:
  origin: agent-master-skills---

# Design System Validate Plugin

## Overview

Enforces design system compliance across all UI code. Checks that colors, typography, spacing, and components match the defined design tokens.

## When to Use

- After generating new UI components
- Before design review
- When onboarding new team members
- Design token updates

## Validation Rules

- No hardcoded color values (all from tokens)
- Typography uses design system scale
- Spacing follows 4${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/8dp rhythm
- Components use library components where available
- No CSS custom properties not defined in tokens

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