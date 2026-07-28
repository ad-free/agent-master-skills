---
name: visual-regression
description: Use when you need Playwright or Cypress screenshot comparison for visual testing and regression detection.
model: big-pickle
version: 1.0.0
preamble-tier: 1
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "visual regression"
  - "screenshot test"
  - "visual test"
  - "ui snapshot"
  - "pixel diff"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
---

<!-- TOKEN CEILING: ~2K -->

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