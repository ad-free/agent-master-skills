---
name: visual-regression
description: Use when you need the visual-regression skill (plugin).

---

---
name: visual-regression
description: Use when playwright${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Cypress screenshot comparison for visual testing and regression detection.
metadata:
  origin: agent-master-skills---

# Visual Regression Plugin

## Overview

Automated visual comparison testing. Captures screenshots at defined breakpoints and compares against baselines to detect unintended visual changes.

## When to Use

- After UI component changes
- Before deploying UI updates
- Design system token changes
- Third-party dependency updates that affect UI

## Integration

Registered in `state.json`:
```json
{
  "plugins": ["visual-regression"],
  "pluginConfig": {
    "visual-regression": {
      "breakpoints": [375, 768, 1024, 1440],
      "threshold": 0.001,
      "tool": "playwright"
    }
  }
}
```