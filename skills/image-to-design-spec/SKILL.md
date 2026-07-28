---
name: image-to-design-spec
description: Use when analyzing UI screenshots or images to generate structured design
  specs with colors, layout, components, and design tokens.
model: big-pickle
version: 1.0.0
preamble-tier: 2
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "analyze image"
  - "extract design"
  - "image to design"
  - "screenshot to spec"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle

---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

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

All commands run from `skills/`. Common flags:

| Flag | Description |
|------|-------------|
| `--image <path>` | Input image (required) |
| `--format <fmt>` | Output format: `md`, `json`, `css`, `scss`, `tailwind`, `w3c` |
| `--gemini` | Enable Gemini Vision analysis |
| `--guided` | Use guided questions fallback |
| `--code <fw>` | Generate component: `react`, `vue`, `html` |
| `--design-system` | Generate full design system |
| `--output <path>` | Output file path |

```bash
python scripts/analyze.py --image screenshot.png --format json --gemini
```

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

See `references/output-schema.json` for the full output structure.

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

The scripts must be run from the `skills/` directory:

```bash
cd skills/image-to-design-spec
python scripts/analyze.py --image /screenshot.png --format md
```

Or use absolute paths:

```bash
python /analyze.py --image /screenshot.png --format md
```

## Prerequisites

### Required

```bash
pip install Pillow numpy
```

### Optional (for Gemini analysis)

```bash
pip install google-genai
# REDACTED_SECRET
```

### Check Dependencies

```bash
python -c "from PIL import Image; print('Pillow OK')"
python -c "import numpy; print('NumPy OK')"
python -c "from google import genai; print('Gemini OK')"
```

## Integration with Other Skills

- **dev-craft ALIGN phase:** `python scripts/analyze.py --image <path> --format json --output .dev-craft/image-analysis.json` → add results to ALIGN assumptions
- **ui-craft ALIGN phase:** Generate design tokens directly, create `.ui-craft/MASTER.md` from analysis, skip manual token definition
- **planning Step 0:** Run `--format md`, add detected components/colors/layout to task list before Step 1

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
| `references/integration-guide.md` | How dev-craft/planning use this skill |
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