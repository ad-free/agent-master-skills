# Integration Guide

## Overview

This document shows how `image-to-design-spec` integrates with other skills in the agent-master-skills ecosystem.

## Integration Points

```
image-to-design-spec
    │
    ├──→ dev-craft (Phase 2: ALIGN)
    ├──→ ui-craft (Phase 2: ALIGN)
    └──→ planning-and-task-breakdown (Step 1)
```

## dev-craft Integration

### When to Invoke

In Phase 2 (ALIGN), after stack detection, if user provides a screenshot.

### How to Invoke

```bash
python scripts/analyze.py --image <path> --format json --output .dev-craft/runs/<slug>/image-analysis.json
```

### What to Do with Output

1. Review extracted colors and confirm with user
2. Add detected components to requirements
3. Feed color palette into DESIGN phase for token generation
4. Use layout hints for architecture decisions

### Integration Example

```markdown
## Phase 2: ALIGN

### Stack Detection
[... existing stack detection ...]

### Image Analysis (NEW)
If user provides screenshot:
1. Run image analysis script
2. Present findings:
   ```
   IMAGE ANALYSIS:
   - Colors extracted: [primary, secondary, accent, background]
   - Layout type: sidebar-main
   - Sidebar: left, 20% width
   - Components detected: [navigation, sidebar, card_grid]
   - Mode: dark
   → Are these observations correct?
   ```
 3. Save to `.dev-craft/runs/<slug>/image-analysis.json`
 4. Reference in Phase 3 (DESIGN) for token generation
```

### State Integration

Add to `.dev-craft/runs/<slug>/state.json`:

```json
{
  "imageAnalysis": {
    "available": true,
    "path": ".dev-craft/runs/<slug>/image-analysis.json",
    "colors": ["#1a1a2e", "#16213e", "#e94560"],
    "layout": "sidebar-main",
    "mode": "dark"
  }
}
```

## ui-craft Integration

### When to Invoke

In Phase 2 (ALIGN), when user provides visual reference.

### How to Invoke

```bash
python scripts/analyze.py --image <path> --format json --output .ui-craft/image-analysis.json
```

### What to Do with Output

1. Generate design tokens directly from extracted colors
2. Create `.ui-craft/design-system/MASTER.md` from analysis
3. Skip manual token definition
4. Use component hints for component selection

### Integration Example

```markdown
## Phase 2: ALIGN

### Stack Detection
[... existing stack detection ...]

### Design System from Image (NEW)
If user provides screenshot:
1. Run image analysis
2. Auto-generate design tokens:
   ```
   Generated from image analysis:
   - Primary: #1a1a2e → --color-primary-500
   - Secondary: #16213e → --color-secondary-500
   - Accent: #e94560 → --color-accent-500
   ```
3. Create `.ui-craft/design-system/MASTER.md`
4. Generate Tailwind config from colors
5. Present to user for confirmation
```

### State Integration

Add to `.ui-craft/state.json`:

```json
{
  "designSystem": {
    "source": "image-analysis",
    "path": ".ui-craft/design-system/MASTER.md",
    "tokensPath": ".ui-craft/tokens/tokens.css"
  }
}
```

## planning-and-task-breakdown Integration

### When to Invoke

In Step 1 (Enter Plan Mode), if user provides screenshot as requirement reference.

### How to Invoke

```bash
python scripts/analyze.py --image <path> --format md
```

### What to Do with Output

1. Add detected components to task list
2. Add color tokens to design tasks
3. Add layout structure to architecture tasks
4. Use complexity score for task sizing

### Integration Example

```markdown
## Step 1: Enter Plan Mode

### Image Analysis (NEW)
If user provides screenshot:
1. Run image analysis
2. Enrich requirements:
   ```
   VISUAL REFERENCE ANALYSIS:
   - Layout: sidebar-main with header
   - Components: [nav, sidebar, cards, table]
   - Colors: dark mode, accent #e94560
   - Complexity: 0.45 (Medium)

   TASK ADDITIONS:
   - Create design tokens (colors from image)
   - Build layout structure (sidebar-main)
   - Implement navigation component
   - Build sidebar component
   - Create card grid component
   ```
3. Continue to Step 1 with enriched context
```

## Cross-Skill Workflow

### Full Pipeline with Image Reference

```
1. User provides screenshot
2. planning-and-task-breakdown
   └─→ Runs image analysis
   └─→ Creates enriched plan
3. dev-craft or ui-craft
   └─→ Reuses image analysis
   └─→ Builds from enriched plan
4. Result: Code matches visual reference
```

### Shared Analysis

To avoid re-analyzing the same image:

1. First skill to run saves to `.dev-craft/runs/<slug>/image-analysis.json`
2. Subsequent skills read from same file
3. All skills work from same analysis data

## Plugin Integration

### dev-craft Plugins

| Plugin | Integration |
|--------|-------------|
| `security-audit` | Uses color analysis to check contrast |
| `performance-profiling` | Uses complexity score for optimization hints |

### ui-craft Plugins

| Plugin | Integration |
|--------|-------------|
| `figma-sync` | Compares extracted tokens with Figma tokens |
| `visual-regression` | Uses extracted colors as baseline |
| `design-system-validate` | Validates against extracted tokens |
| `accessibility-deep` | Uses WCAG contrast data from analysis |
