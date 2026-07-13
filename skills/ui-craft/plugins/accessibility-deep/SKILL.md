---
name: accessibility-deep
description: WCAG 2.2 AAA compliance auditing with automated and manual testing patterns.
metadata:
  origin: agent-master-skills
---

# Accessibility Deep Plugin

## Overview

Deep accessibility audit beyond basic checks. Covers WCAG 2.2 Level AAA requirements, screen reader flows, and cognitive accessibility.

## When to Use

- Accessibility compliance required (legal/regulatory)
- After initial a11y checks pass (basic Level A/AA)
- User base includes people with disabilities
- Public sector or regulated industry applications

## Audit Layers

1. **Automated** — axe-core, Lighthouse, WAVE
2. **Keyboard** — Full keyboard navigation audit
3. **Screen reader** — NVDA/VoiceOver flow testing
4. **Cognitive** — Reading level, focus management, reduced motion
5. **Color** — Contrast ≥ 7:1 (AAA), non-color indicators

## Integration

Registered in `state.json`:
```json
{
  "plugins": ["accessibility-deep"],
  "pluginConfig": {
    "accessibility-deep": {
      "level": "AAA",
      "runAutomated": true
    }
  }
}
```
