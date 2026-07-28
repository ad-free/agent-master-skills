---
name: animation-craft
description: Use when you need advanced animation patterns for micro-interactions, page transitions, and motion design.
model: big-pickle
version: 1.0.0
preamble-tier: 1
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "animation"
  - "motion design"
  - "micro interaction"
  - "page transition"
  - "css animation"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
---

<!-- TOKEN CEILING: ~2K -->

# Animation Craft Plugin

## Overview

Produces production-quality animations following motion design principles. Works with Framer Motion (React), Vue Transition, and CSS animations.

## When to Use

- Micro-interactions (hover, focus, tap)
- Page transitions and route changes
- Loading states and skeleton animations
- Staggered list/container animations
- Gesture-driven interactions

## Core Principles

- Duration: 150-300ms for micro-interactions
- Easing: ease-in-out for UI, spring for natural feel
- `prefers-reduced-motion` respected at all times
- No layout-shifting animations
- Accessible: no flashing (epilepsy risk)

## Integration

Registered in `state.json`:
```json
{
  "plugins": ["animation-craft"],
  "pluginConfig": {
    "animation-craft": {
      "defaultDuration": 200,
      "respectReducedMotion": true
    }
  }
}
```