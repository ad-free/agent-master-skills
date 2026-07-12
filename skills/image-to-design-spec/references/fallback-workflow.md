# Fallback Workflow

## When to Use

- Gemini API is not available (no API key)
- Image is complex and needs human interpretation
- Automated analysis produces low-confidence results
- User wants to provide additional context beyond what's extracted

## Workflow

### Step 1: Run Automated Analysis

```bash
python scripts/analyze.py --image <path> --guided --format md
```

This produces:
- Color extraction (always works)
- Layout detection (always works)
- Guided questions for human input

### Step 2: Present Results to User

```markdown
## Image Analysis Results

### Extracted Automatically
- **Colors:** [list of hex colors with roles]
- **Layout:** [detected layout type]
- **Mode:** [light/dark]

### Needs Your Input
Please answer these questions to complete the analysis:
[... guided questions ...]
```

### Step 3: Collect User Answers

Present questions one category at a time:

1. **Layout questions** — Structure and navigation
2. **Component questions** — UI elements present
3. **Color questions** — Theme and accent details
4. **Typography questions** — Font styles and sizes
5. **Style questions** — Overall design aesthetic

### Step 4: Merge into Design Spec

Combine automated analysis with user answers:

```json
{
  "colors": { "/* automated */": "..." },
  "layout": { "/* automated + user confirmed */": "..." },
  "components": { "/* user-provided */": "..." },
  "typography": { "/* user-provided */": "..." }
}
```

### Step 5: Generate Output

```bash
python scripts/analyze.py --image <path> --format md --output design-spec.md
```

## Guided Questions Reference

### Layout Questions

| Question | Why It Matters |
|----------|----------------|
| What is the overall layout type? | Determines component structure |
| Is there a header/navbar? | Navigation architecture |
| Is there a footer? | Page structure |
| Is there a sidebar? Left or right? | Layout grid decisions |

### Component Questions

| Question | Why It Matters |
|----------|----------------|
| What UI components do you see? | Component library selection |
| Are there data visualizations? | Chart/graph dependencies |
| What navigation pattern? | Navigation component choice |
| Are there interactive elements? | Form/interaction components |

### Color Questions

| Question | Why It Matters |
|----------|----------------|
| Light or dark mode? | Theme configuration |
| What are the main colors? | Color token generation |
| Gradient or shadow effects? | CSS complexity |
| Is there a brand color? | Primary token assignment |

### Typography Questions

| Question | Why It Matters |
|----------|----------------|
| Serif or sans-serif headings? | Font family selection |
| Body text size? | Type scale |
| Monospace text present? | Code font needs |
| Different font weights? | Weight tokens |

### Style Questions

| Question | Why It Matters |
|----------|----------------|
| Overall style? | Design direction |
| Border style? | Border-radius tokens |
| Spacing? | Spacing scale |
| Special effects? | CSS complexity |

## Manual Analysis Template

When automation fails completely, use this template:

```markdown
# Manual UI Analysis

## Image: [filename]

## Layout
- Type: [sidebar-main / single-column / grid / dashboard]
- Header: [yes/no]
- Footer: [yes/no]
- Sidebar: [yes/no, position, width%]

## Colors
- Background: [hex]
- Primary text: [hex]
- Secondary text: [hex]
- Accent: [hex]
- Border: [hex]

## Components
1. [Component name] - [location] - [description]
2. [Component name] - [location] - [description]

## Typography
- Headings: [font style, weight, size]
- Body: [font style, weight, size]
- Code: [yes/no]

## Style
- Overall: [minimal / modern / corporate / playful]
- Corners: [sharp / rounded / pill]
- Spacing: [tight / normal / spacious]
- Effects: [none / shadows / gradients / glass]
```

## Confidence Levels

| Level | Meaning | Action |
|-------|---------|--------|
| High (>0.85) | Reliable extraction | Use directly |
| Medium (0.6-0.85) | Needs confirmation | Present to user |
| Low (<0.6) | Unreliable | Use guided questions |
