# Output Format Reference

## Complete Output Schema

The `analyze.py` script produces a JSON object with the following structure:

```json
{
  "meta": { },
  "image": { },
  "colors": { },
  "layout": { },
  "components": [ ],
  "typography": { },
  "design_tokens": { },
  "gemini_analysis": null | { },
  "guided_questions": null | [ ]
}
```

## Field Descriptions

### meta

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Original image filename |
| `analyzed_at` | string | ISO 8601 timestamp |
| `analysis_layers` | array | Which analysis layers ran |
| `dependencies` | object | Which deps are available |

### image

| Field | Type | Description |
|-------|------|-------------|
| `path` | string | Full path to image |
| `width` | integer | Image width in pixels |
| `height` | integer | Image height in pixels |
| `aspect_ratio` | string | Common ratio (16:9, 4:3, etc.) |
| `format` | string | Image format (PNG, JPEG, etc.) |

### colors

| Field | Type | Description |
|-------|------|-------------|
| `dominant` | array | Top N hex colors by area |
| `palette` | object | Semantic color roles |
| `mode` | string | "light" or "dark" |
| `colors` | array | Full color details |

#### colors.palette roles

| Role | Description |
|------|-------------|
| `primary` | Main brand color |
| `secondary` | Supporting color |
| `accent` | Highlight/action color |
| `background` | Page background |
| `text` | Primary text color |

#### colors.colors[] (detailed)

| Field | Type | Description |
|-------|------|-------------|
| `hex` | string | Hex color code |
| `rgb` | object | {r, g, b} values |
| `hsl` | object | {h, s, l} values |
| `area_percent` | float | Percentage of image area |
| `text_color` | string | Best contrast text (#000 or #fff) |
| `wcag_contrast_light` | float | Contrast ratio vs white |
| `wcag_contrast_dark` | float | Contrast ratio vs black |
| `semantic_role` | string | Assigned role |

### layout

| Field | Type | Description |
|-------|------|-------------|
| `width` | integer | Image width |
| `height` | integer | Image height |
| `aspect_ratio` | string | Common ratio |
| `layout_type` | string | Detected layout pattern |
| `has_header` | boolean | Header detected |
| `has_footer` | boolean | Footer detected |
| `has_sidebar` | boolean | Sidebar detected |
| `sidebar_position` | string | "left", "right", or "none" |
| `sidebar_width_percent` | float | Sidebar width as % |
| `max_content_width` | integer | Max content width px |
| `regions` | array | Detected regions |
| `density` | float | Content density (0-1) |
| `estimated_grid_columns` | integer | Grid columns (1-4) |
| `spacing_hint` | string | "tight", "normal", "spacious" |
| `responsive_breakpoints` | object | Suggested breakpoints |
| `complexity_score` | float | Overall complexity (0-1) |

#### layout.layout_type values

| Value | Description |
|-------|-------------|
| `single-column` | No sidebar, simple layout |
| `sidebar-main` | Sidebar + main content |
| `grid` | Multi-column grid |
| `dashboard` | Complex grid + sidebar + header |

### components[] (Gemini only)

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Component name |
| `confidence` | float | Detection confidence (0-1) |
| `region` | string | Location in layout |
| `description` | string | Brief description |

### typography (Gemini only)

| Field | Type | Description |
|-------|------|-------------|
| `heading_style` | string | "sans-serif" or "serif" |
| `body_style` | string | "sans-serif" or "serif" |
| `heading_weight` | string | "bold" or "normal" |
| `estimated_sizes` | object | Estimated font sizes |

### design_tokens

| Field | Type | Description |
|-------|------|-------------|
| `colors` | object | Color tokens |
| `spacing` | object | Spacing tokens (Gemini) |
| `border_radius` | object | Border radius tokens (Gemini) |

## Format-Specific Output

### JSON (`--format json`)

Complete schema as shown above.

### Markdown (`--format md`)

Human-readable design spec with sections:
- Image info
- Color palette
- Layout description
- Components (if detected)
- Design tokens
- Responsive breakpoints

### CSS (`--format css`)

```css
:root {
  --color-primary: #1a1a2e;
  --color-secondary: #16213e;
  --color-accent: #e94560;
  --color-1: #1a1a2e;
  --color-2: #16213e;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
}
```

### SCSS (`--format scss`)

```scss
$color-primary: #1a1a2e;
$color-secondary: #16213e;
$color-accent: #e94560;

$colors: (
  'primary': #1a1a2e,
  'secondary': #16213e,
  'accent': #e94560,
);
```

### Tailwind (`--format tailwind`)

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f0f5',
          100: '#d4d4e0',
          // ... shade ramps
          900: '#0d0d17',
          950: '#06060b',
        },
      },
    },
  },
};
```

### W3C DTCG (`--format w3c`)

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "color": {
    "primary": {
      "$type": "color",
      "$value": "#1a1a2e",
      "$description": "RGB(26, 26, 46)"
    }
  }
}
```
