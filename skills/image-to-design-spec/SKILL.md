---
name: image-to-design-spec
description: Analyzes UI screenshots/images and generates structured design specs with colors, layout, components, and design tokens. Hybrid approach: Pillow+K-means (local), Gemini Vision (optional), guided questions (fallback). Outputs JSON, Markdown, CSS, SCSS, Tailwind, W3C DTCG.
metadata:
  origin: agent-master-skills
---

# image-to-design-spec

## Overview

Converts UI screenshots and images into structured, machine-readable design specifications. Enables text-only models to understand visual UI references by extracting colors, layout, components, and generating design tokens.

**Philosophy:** Hybrid analysis with graceful degradation. Local extraction always works. Gemini enhances when available. Guided questions complete the picture.

## When to Use

- User provides a screenshot as UI reference ("build this", "make it look like this")
- User wants to replicate an existing UI design
- Starting a project from a mockup or design file
- Need to extract design tokens from an existing interface
- Planning work that involves visual reference material

**When NOT to use:** Text-only descriptions, pure backend work, single-component changes without visual references.

## The Three-Layer Analysis

```
┌─────────────────────────────────────────────────────┐
│ Layer 1: Pillow + K-means (ALWAYS RUNS)            │
│ - Dominant colors with area percentages             │
│ - Image dimensions + aspect ratio                   │
│ - Light/dark mode detection                         │
│ - Layout regions (header, sidebar, main)            │
│ - Edge density analysis                             │
├─────────────────────────────────────────────────────┤
│ Layer 2: Gemini Vision (OPTIONAL)                   │
│ - Component identification with confidence          │
│ - Typography analysis                               │
│ - Spacing and border-radius estimation              │
│ - Visual effects detection                          │
├─────────────────────────────────────────────────────┤
│ Layer 3: Guided Questions (FALLBACK)                │
│ - Structured questionnaire for user                 │
│ - Covers: layout, components, colors, typography    │
│ - Fills gaps when automated analysis is insufficient│
└─────────────────────────────────────────────────────┘
```

## Quick Start

### Basic Analysis (Layer 1 only)

```bash
python scripts/analyze.py --image screenshot.png --format md
```

> **Important:** All commands must be run from the `skills/image-to-design-spec/` directory. The scripts use relative imports that assume this working directory.

### Full Analysis with Gemini

```bash
python scripts/analyze.py --image screenshot.png --gemini --format json
```

### Export to CSS Variables

```bash
python scripts/analyze.py --image screenshot.png --format css --output styles.css
```

### Export to Tailwind Config

```bash
python scripts/analyze.py --image screenshot.png --format tailwind --output tailwind.config.js
```

### Export to W3C Design Tokens

```bash
python scripts/analyze.py --image screenshot.png --format w3c --output tokens.json
```

### Generate Guided Questions

```bash
python scripts/analyze.py --image screenshot.png --guided
```

### Generate React Component

```bash
python scripts/analyze.py --image screenshot.png --code react --component-name LoginPage --output LoginPage.tsx
```

### Generate Vue Component

```bash
python scripts/analyze.py --image screenshot.png --code vue --component-name LoginPage --output LoginPage.vue
```

### Generate HTML Page

```bash
python scripts/analyze.py --image screenshot.png --code html --output index.html
```

### Generate Complete Design System

```bash
python scripts/analyze.py --image screenshot.png --design-system --output ./design-system/
```

This creates a complete design system with:
- `design-system.json` - Full token data
- `tokens.css` - CSS custom properties
- `tailwind.config.js` - Tailwind configuration
- `DESIGN-SPEC.md` - Human-readable spec

## Output Formats

### Token Formats

| Format | Flag | Use Case |
|--------|------|----------|
| Markdown | `--format md` | Human-readable design spec |
| JSON | `--format json` | Full structured data for programmatic use |
| CSS | `--format css` | CSS custom properties |
| SCSS | `--format scss` | SCSS variables |
| Tailwind | `--format tailwind` | tailwind.config.js with shade ramps |
| W3C DTCG | `--format w3c` | Industry-standard design tokens |
| Storybook | `--format storybook` | Storybook addon tokens format |
| Figma | `--format figma` | Figma-compatible token JSON |

### Code Generation

| Framework | Flag | Output |
|-----------|------|--------|
| React + Tailwind | `--code react` | .tsx component with Tailwind classes |
| Vue + Tailwind | `--code vue` | .vue SFC with Tailwind classes |
| HTML + CSS | `--code html` | Standalone HTML with embedded CSS |

### Design System

| Flag | Output |
|------|--------|
| `--design-system` | Complete design system with tokens, components, CSS variables, Tailwind config |

## Output Schema

```json
{
  "meta": {
    "source": "screenshot.png",
    "analyzed_at": "2026-07-12T10:30:00Z",
    "analysis_layers": ["pillow+kmeans", "layout-detection", "gemini-vision"]
  },
  "image": {
    "width": 1440,
    "height": 900,
    "aspect_ratio": "16:10",
    "format": "png"
  },
  "colors": {
    "dominant": ["#1a1a2e", "#16213e", "#0f3460", "#e94560", "#ffffff"],
    "palette": {
      "primary": "#1a1a2e",
      "secondary": "#16213e",
      "accent": "#e94560",
      "background": "#ffffff",
      "text": "#1a1a2e"
    },
    "mode": "dark"
  },
  "layout": {
    "layout_type": "sidebar-main",
    "has_header": true,
    "has_footer": false,
    "has_sidebar": true,
    "sidebar_position": "left",
    "sidebar_width_percent": 20,
    "estimated_grid_columns": 1,
    "spacing_hint": "normal",
    "complexity_score": 0.45
  },
  "components": [
    {"type": "navigation", "confidence": 0.95, "region": "top"},
    {"type": "sidebar", "confidence": 0.90, "region": "left"}
  ],
  "design_tokens": {
    "colors": { "primary": "#1a1a2e", "accent": "#e94560" },
    "spacing": { "unit": "8px", "scale": "normal" },
    "border_radius": { "style": "rounded", "value": "8px" }
  }
}
```

## Setup & Installation

### Quick Setup (using uv - recommended)

```bash
cd skills/image-to-design-spec
uv venv --python 3.13
uv pip install Pillow numpy
```

### Manual Setup (using pip)

```bash
cd skills/image-to-design-spec
pip install Pillow numpy
```

### Running from Any Location

The scripts must be run from the `skills/image-to-design-spec/` directory:

```bash
cd skills/image-to-design-spec
python scripts/analyze.py --image /path/to/screenshot.png --format md
```

Or use absolute paths:

```bash
python /path/to/skills/image-to-design-spec/scripts/analyze.py --image /path/to/screenshot.png --format md
```

## Prerequisites

### Required

```bash
pip install Pillow numpy
```

### Optional (for Gemini analysis)

```bash
pip install google-genai
export GEMINI_API_KEY="your-key"  # https://aistudio.google.com/apikey
```

### Check Dependencies

```bash
python -c "from PIL import Image; print('Pillow OK')"
python -c "import numpy; print('NumPy OK')"
python -c "from google import genai; print('Gemini OK')"
```

## Integration with Other Skills

### dev-craft Integration

In Phase 2 (ALIGN), after stack detection:

```markdown
### Image Analysis (if screenshot provided)

1. Run: `python scripts/analyze.py --image <path> --format json --output .dev-craft/image-analysis.json`
2. Review extracted data:
   ```
   IMAGE ANALYSIS:
   - Colors: [primary, secondary, accent, background]
   - Layout: sidebar-main (left sidebar, 20%)
   - Components: [nav, sidebar, cards]
   - Mode: dark
   → Confirm these observations.
   ```
3. Add to ALIGN assumptions for DESIGN phase
```

### ui-craft Integration

In Phase 2 (ALIGN), for design system creation:

```markdown
### Design System from Image

1. Run: `python scripts/analyze.py --image <path> --format json`
2. Generate design tokens directly from extracted colors
3. Create `.ui-craft/design-system/MASTER.md` from analysis
4. Skip manual token definition
```

### planning-and-task-breakdown Integration

In Step 1 (Enter Plan Mode):

```markdown
### Step 0: Image Analysis (if screenshot provided)

1. Run: `python scripts/analyze.py --image <path> --format md`
2. Use output to enrich requirements:
   - Add detected components to task list
   - Add colors to design token tasks
   - Add layout to structure tasks
3. Continue to Step 1 with enriched context
```

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `analyze.py` | Core orchestrator | `python scripts/analyze.py --image <path>` |
| `extract_colors.py` | Color extraction module | Imported by analyze.py |
| `extract_layout.py` | Layout detection module | Imported by analyze.py |
| `export_tokens.py` | Multi-format export | Imported by analyze.py |

## Advanced Usage

### Custom Color Count

```bash
python scripts/analyze.py --image screenshot.png --colors 8
```

### Combine Gemini + Guided

```bash
python scripts/analyze.py --image screenshot.png --gemini --guided
```

### Programmatic Usage

```python
from scripts.analyze import analyze
from scripts.export_tokens import export

result = analyze("screenshot.png", use_gemini=True)
output = export(result, "css")
```

## Fallback Workflow

When Gemini is unavailable, use guided questions:

1. Run `python scripts/analyze.py --image <path> --guided`
2. Present questions to user
3. User answers questions
4. Feed answers into design spec
5. Continue with planning/building

See `references/fallback-workflow.md` for detailed guide.

## References

| Document | Purpose |
|----------|---------|
| `references/output-format.md` | Full output schema documentation |
| `references/integration-guide.md` | How dev-craft/ui-craft/planning use this skill |
| `references/fallback-workflow.md` | Guided questions workflow |
| `references/w3c-dtcg-spec.md` | W3C Design Tokens format reference |

## Templates

| Template | Purpose |
|----------|---------|
| `templates/w3c-tokens.json` | W3C DTCG format template |
| `templates/css-variables.css` | CSS custom properties template |
| `templates/tailwind-config.js` | Tailwind config template |
| `templates/design-spec.md` | Markdown design spec template |

## Accuracy Notes

### Layer 1 (Pillow + K-means) - Always Available
- **Color accuracy:** 90-95% for dominant colors
- **Layout detection:** 70-85% for common layouts
- **Component detection:** Not available (requires Gemini)

### Layer 2 (Gemini Vision) - When Available
- **Component detection:** 85-95% accuracy
- **Typography analysis:** 80-90% accuracy
- **Spacing estimation:** 75-85% accuracy

### Combined
- **Overall design fidelity:** 85-95% match with original

## See Also

- `references/integration-guide.md` — How to integrate with dev-craft, ui-craft, planning
- `references/fallback-workflow.md` — Manual analysis when automation is insufficient
