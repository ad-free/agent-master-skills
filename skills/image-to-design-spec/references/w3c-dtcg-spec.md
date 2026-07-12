# W3C Design Tokens Community Group (DTCG) Specification

## Overview

The W3C Design Tokens Community Group defines a standard format for design tokens that can be shared across tools and platforms.

**Specification:** https://www.designtokens.org/format/

## Token Format

Each token follows this structure:

```json
{
  "token-name": {
    "$type": "token-type",
    "$value": "token-value",
    "$description": "optional description",
    "$extensions": {
      "com.example.vendor": "optional vendor data"
    }
  }
}
```

## Token Types

| Type | Description | Example Value |
|------|-------------|---------------|
| `color` | Color value | `"#ff0000"` or `"rgb(255, 0, 0)"` |
| `dimension` | Size value | `"16px"` or `"1rem"` |
| `fontFamily` | Font family | `"Inter, sans-serif"` |
| `fontWeight` | Font weight | `"bold"` or `700` |
| `fontSize` | Font size | `"16px"` |
| `lineHeight` | Line height | `1.5` or `"24px"` |
| `letterSpacing` | Letter spacing | `"0.5px"` |
| `borderRadius` | Border radius | `"8px"` |
| `shadow` | Box shadow | See composite below |
| `composite` | Complex value | See shadow example |

## Color Tokens

```json
{
  "color": {
    "primary": {
      "$type": "color",
      "$value": "#3b82f6",
      "$description": "Primary brand color"
    },
    "background": {
      "$type": "color",
      "$value": "{color.white}",
      "$description": "Page background"
    }
  }
}
```

### Color Formats

| Format | Example | Notes |
|--------|---------|-------|
| Hex | `"#ff0000"` | Most common |
| RGB | `"rgb(255, 0, 0)"` | Functional |
| HSL | `"hsl(0, 100%, 50%)"` | Human-readable |
| Reference | `"{color.primary}"` | Alias to another token |

## Dimension Tokens

```json
{
  "spacing": {
    "sm": {
      "$type": "dimension",
      "$value": "0.25rem"
    },
    "md": {
      "$type": "dimension",
      "$value": "0.5rem"
    },
    "lg": {
      "$type": "dimension",
      "$value": "1rem"
    }
  }
}
```

## Typography Composite Tokens

```json
{
  "font": {
    "heading": {
      "$type": "typography",
      "$value": {
        "fontFamily": "{fontFamily.heading}",
        "fontSize": "2rem",
        "fontWeight": "700",
        "lineHeight": "1.2"
      }
    }
  }
}
```

## Shadow Composite Tokens

```json
{
  "shadow": {
    "sm": {
      "$type": "shadow",
      "$value": {
        "offsetX": "0px",
        "offsetY": "1px",
        "blur": "2px",
        "spread": "0px",
        "color": "rgba(0, 0, 0, 0.1)"
      }
    }
  }
}
```

## Token References (Aliases)

Tokens can reference other tokens using curly braces:

```json
{
  "color": {
    "primary": {
      "$type": "color",
      "$value": "#3b82f6"
    },
    "primary-light": {
      "$type": "color",
      "$value": "{color.primary}",
      "$description": "Inherits from primary"
    }
  }
}
```

## Extensions

Vendor-specific data goes in `$extensions`:

```json
{
  "color": {
    "primary": {
      "$type": "color",
      "$value": "#3b82f6",
      "$extensions": {
        "com.agent-master-skills": {
          "confidence": 0.92,
          "source": "kmeans-extraction",
          "area_percent": 15.3
        }
      }
    }
  }
}
```

## Consuming Tokens

### Style Dictionary

```javascript
// config.js
module.exports = {
  source: ["tokens/**/*.json"],
  platforms: {
    css: {
      transformGroup: "css",
      buildPath: "build/css/",
      files: [
        {
          destination: "variables.css",
          format: "css/variables",
        },
      ],
    },
  },
};
```

### Figma Variables

Use Figma Tokens plugin to import W3C DTCG JSON.

### Tailwind CSS

Convert tokens to Tailwind config:

```javascript
// tailwind.config.js
const tokens = require("./tokens.json");

module.exports = {
  theme: {
    extend: {
      colors: {
        primary: tokens.color.primary.$value,
        secondary: tokens.color.secondary.$value,
      },
    },
  },
};
```

## Our Output Format

The `export_tokens.py` script generates W3C DTCG-compliant JSON:

```json
{
  "$schema": "https://design-tokens.github.io/community-group/format/",
  "meta": {
    "source": "screenshot.png",
    "generated": "2026-07-12T10:30:00Z"
  },
  "color": {
    "primary": {
      "$type": "color",
      "$value": "#1a1a2e",
      "$description": "RGB(26, 26, 46)",
      "$extensions": {
        "com.agent-master-skills.confidence": 0.85,
        "com.agent-master-skills.source": "kmeans-extraction"
      }
    }
  }
}
```

## References

- [W3C DTCG Specification](https://www.designtokens.org/format/)
- [Style Dictionary](https://styledictionary.com/)
- [Figma Tokens](https://docs.tokens.studio/)
