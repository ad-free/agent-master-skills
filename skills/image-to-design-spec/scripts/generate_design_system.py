#!/usr/bin/env python3
"""
Design System Generator Module
Creates a complete design system from extracted image analysis.

Inspired by: design-dna (Design DNA), anydesign (design.md + tokens),
design-token-extractor (W3C DTCG + CSS layers)

Output: Complete design system with tokens, components, typography, spacing
"""

import json
from pathlib import Path
from datetime import datetime


def generate_shade_scale(hex_color: str) -> dict:
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    steps = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
    result = {}
    for step in steps:
        factor = step / 1000
        if step < 500:
            blend = 1 - (step / 500) * 0.5
            nr = int(r + (255 - r) * blend)
            ng = int(g + (255 - g) * blend)
            nb = int(b + (255 - b) * blend)
        elif step == 500:
            nr, ng, nb = r, g, b
        else:
            blend = (step - 500) / 500
            nr = int(r * (1 - blend))
            ng = int(g * (1 - blend))
            nb = int(b * (1 - blend))
        result[step] = (
            f"#{max(0, min(255, nr)):02x}{max(0, min(255, ng)):02x}{max(0, min(255, nb)):02x}"
        )
    return result


def generate_spacing_scale(base: int = 8) -> dict:
    scale = {
        "0": "0px",
        "0.5": f"{base / 2}px",
        "1": f"{base}px",
        "1.5": f"{base * 1.5}px",
        "2": f"{base * 2}px",
        "2.5": f"{base * 2.5}px",
        "3": f"{base * 3}px",
        "4": f"{base * 4}px",
        "5": f"{base * 5}px",
        "6": f"{base * 6}px",
        "8": f"{base * 8}px",
        "10": f"{base * 10}px",
        "12": f"{base * 12}px",
        "16": f"{base * 16}px",
        "20": f"{base * 20}px",
        "24": f"{base * 24}px",
    }
    return scale


def generate_typography_scale(
    heading_style: str = "sans-serif", body_style: str = "sans-serif"
) -> dict:
    from standards import (
        FONT_FAMILIES,
        FONT_SIZES,
        FONT_WEIGHTS,
        LINE_HEIGHTS,
        LETTER_SPACINGS,
    )

    return {
        "fontFamilies": {
            "heading": FONT_FAMILIES["sans"],
            "body": FONT_FAMILIES["sans"],
            "mono": FONT_FAMILIES["mono"],
            "display": FONT_FAMILIES["display"],
        },
        "fontSizes": FONT_SIZES,
        "fontWeights": FONT_WEIGHTS,
        "lineHeights": LINE_HEIGHTS,
        "letterSpacings": LETTER_SPACINGS,
    }


def generate_border_radius_tokens(border_radius: int) -> dict:
    if border_radius <= 0:
        return {
            "none": "0px",
            "sm": "2px",
            "md": "4px",
            "lg": "6px",
            "xl": "8px",
            "2xl": "12px",
            "full": "9999px",
        }
    elif border_radius < 8:
        return {
            "none": "0px",
            "sm": f"{border_radius}px",
            "md": f"{border_radius + 2}px",
            "lg": f"{border_radius + 4}px",
            "xl": f"{border_radius + 6}px",
            "2xl": f"{border_radius + 8}px",
            "full": "9999px",
        }
    else:
        return {
            "none": "0px",
            "sm": f"{border_radius // 2}px",
            "md": f"{border_radius}px",
            "lg": f"{border_radius + 4}px",
            "xl": f"{border_radius + 8}px",
            "2xl": f"{border_radius + 16}px",
            "full": "9999px",
        }


def generate_shadow_tokens(has_shadow: bool, intensity: str) -> dict:
    if not has_shadow:
        return {
            "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
            "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
            "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
            "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
            "2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
            "inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)",
            "none": "none",
        }
    elif intensity == "light":
        return {
            "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
            "md": "0 2px 4px -1px rgba(0, 0, 0, 0.08), 0 1px 2px -1px rgba(0, 0, 0, 0.04)",
            "lg": "0 4px 8px -2px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.04)",
            "xl": "0 8px 16px -4px rgba(0, 0, 0, 0.1), 0 4px 8px -4px rgba(0, 0, 0, 0.04)",
            "2xl": "0 12px 24px -6px rgba(0, 0, 0, 0.12)",
            "inner": "inset 0 1px 2px 0 rgba(0, 0, 0, 0.04)",
            "none": "none",
        }
    elif intensity == "medium":
        return {
            "sm": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)",
            "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)",
            "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)",
            "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)",
            "2xl": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
            "inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)",
            "none": "none",
        }
    else:
        return {
            "sm": "0 2px 4px 0 rgba(0, 0, 0, 0.15)",
            "md": "0 6px 10px -2px rgba(0, 0, 0, 0.15), 0 3px 6px -3px rgba(0, 0, 0, 0.15)",
            "lg": "0 15px 25px -5px rgba(0, 0, 0, 0.15), 0 6px 10px -6px rgba(0, 0, 0, 0.15)",
            "xl": "0 25px 35px -8px rgba(0, 0, 0, 0.2), 0 10px 15px -8px rgba(0, 0, 0, 0.15)",
            "2xl": "0 35px 60px -15px rgba(0, 0, 0, 0.3)",
            "inner": "inset 0 4px 8px 0 rgba(0, 0, 0, 0.1)",
            "none": "none",
        }


def generate_component_specs(
    layout_type: str, border_radius: int, has_glass: bool
) -> list:
    components = []

    base_button = {
        "name": "Button",
        "description": "Primary interactive element",
        "variants": ["primary", "secondary", "outline", "ghost"],
        "sizes": ["sm", "md", "lg"],
        "tokens": {
            "borderRadius": f"{border_radius}px" if border_radius > 0 else "6px",
            "fontWeight": "600",
            "paddingX": "1.5rem",
            "paddingY": "0.5rem",
            "transition": "all 0.2s ease",
        },
    }
    components.append(base_button)

    base_input = {
        "name": "Input",
        "description": "Text input field",
        "variants": ["default", "error", "disabled"],
        "sizes": ["sm", "md", "lg"],
        "tokens": {
            "borderRadius": f"{border_radius}px" if border_radius > 0 else "6px",
            "borderWidth": "1px",
            "borderColor": "#e5e7eb",
            "paddingX": "1rem",
            "paddingY": "0.75rem",
            "fontSize": "1rem",
        },
    }
    components.append(base_input)

    base_card = {
        "name": "Card",
        "description": "Container for grouping content",
        "variants": ["default", "elevated", "outlined"],
        "tokens": {
            "borderRadius": f"{border_radius}px" if border_radius > 0 else "8px",
            "padding": "1.5rem",
            "shadow": "0 1px 3px rgba(0,0,0,0.1)",
        },
    }
    if has_glass:
        base_card["variants"].append("glass")
        base_card["tokens"]["backdropFilter"] = "blur(12px)"
        base_card["tokens"]["backgroundColor"] = "rgba(255, 255, 255, 0.8)"
    components.append(base_card)

    if layout_type == "sidebar-main":
        components.append(
            {
                "name": "Sidebar",
                "description": "Navigation sidebar",
                "tokens": {
                    "width": "250px",
                    "backgroundColor": "#f5f5f5",
                    "borderRight": "1px solid #e5e7eb",
                    "padding": "1.5rem",
                },
            }
        )

    if layout_type == "centered-card":
        components.append(
            {
                "name": "AuthForm",
                "description": "Authentication form (login/signup)",
                "tokens": {
                    "maxWidth": "24rem",
                    "padding": "2rem",
                    "borderRadius": f"{border_radius}px"
                    if border_radius > 0
                    else "8px",
                    "backgroundColor": "#ffffff",
                },
            }
        )

    if layout_type == "hero-fullscreen":
        components.append(
            {
                "name": "Hero",
                "description": "Full-screen hero section",
                "tokens": {
                    "minHeight": "100vh",
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "textAlign": "center",
                    "padding": "2rem",
                },
            }
        )

    components.append(
        {
            "name": "Navigation",
            "description": "Top navigation bar",
            "tokens": {
                "height": "64px",
                "paddingX": "1.5rem",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
            },
        }
    )

    return components


def generate_design_system(data: dict) -> dict:
    palette = data.get("colors", {}).get("palette", {})
    layout = data.get("layout", {})
    mode = data.get("colors", {}).get("mode", "light")

    primary = palette.get("primary", "#1a1a2e")
    accent = palette.get("accent", "#e94560")
    bg = palette.get("background", "#ffffff")
    surface = palette.get("surface", "#f5f5f5")
    text_primary = palette.get("text-primary", "#1a1a2e")

    border_radius = layout.get("estimated_border_radius", 8)
    has_shadow = layout.get("has_shadow", False)
    shadow_intensity = layout.get("shadow_intensity", "light")
    has_glass = layout.get("has_glass_effect", False)
    layout_type = layout.get("layout_type", "single-column")

    color_tokens = {}
    for role, color in palette.items():
        color_tokens[role] = {
            "value": color,
            "shades": generate_shade_scale(color),
        }

    typography = generate_typography_scale()
    spacing = generate_spacing_scale()
    border_radius_tokens = generate_border_radius_tokens(border_radius)
    shadows = generate_shadow_tokens(has_shadow, shadow_intensity)
    components = generate_component_specs(layout_type, border_radius, has_glass)

    breakpoints = layout.get(
        "responsive_breakpoints",
        {
            "sm": "640px",
            "md": "768px",
            "lg": "1024px",
            "xl": "1280px",
            "2xl": "1536px",
        },
    )

    design_system = {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "meta": {
            "name": "Extracted Design System",
            "generated": datetime.now().isoformat(),
            "source": data.get("meta", {}).get("source", ""),
            "mode": mode,
        },
        "tokens": {
            "color": color_tokens,
            "typography": typography,
            "spacing": spacing,
            "borderRadius": border_radius_tokens,
            "shadows": shadows,
            "breakpoints": breakpoints,
        },
        "components": components,
        "cssVariables": generate_css_variables(
            color_tokens, typography, spacing, border_radius_tokens, shadows
        ),
        "tailwindConfig": generate_tailwind_config(
            color_tokens,
            typography,
            spacing,
            border_radius_tokens,
            shadows,
            breakpoints,
        ),
    }

    return design_system


def generate_css_variables(color_tokens, typography, spacing, radius, shadows) -> str:
    lines = [":root {"]
    lines.append("  /* Colors */")
    for role, data in color_tokens.items():
        lines.append(f"  --color-{role}: {data['value']};")
    lines.append("")

    lines.append("  /* Typography */")
    for key, value in typography["fontFamilies"].items():
        lines.append(f"  --font-{key}: {value};")
    lines.append("")

    lines.append("  /* Spacing */")
    for key, value in spacing.items():
        lines.append(f"  --space-{key}: {value};")
    lines.append("")

    lines.append("  /* Border Radius */")
    for key, value in radius.items():
        lines.append(f"  --radius-{key}: {value};")
    lines.append("")

    lines.append("  /* Shadows */")
    for key, value in shadows.items():
        lines.append(f"  --shadow-{key}: {value};")
    lines.append("}")
    return "\n".join(lines)


def generate_tailwind_config(
    color_tokens, typography, spacing, radius, shadows, breakpoints
) -> str:
    colors = {}
    for role, data in color_tokens.items():
        shades = data.get("shades", {})
        colors[role] = {str(k): v for k, v in shades.items()}

    config = {
        "theme": {
            "extend": {
                "colors": colors,
                "fontFamily": typography["fontFamilies"],
                "fontSize": typography["fontSizes"],
                "fontWeight": typography["fontWeights"],
                "lineHeight": typography["lineHeights"],
                "spacing": spacing,
                "borderRadius": radius,
                "boxShadow": shadows,
                "screens": breakpoints,
            }
        }
    }
    return f"module.exports = {json.dumps(config, indent=2)};"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate design system from extracted tokens"
    )
    parser.add_argument("--input", required=True, help="JSON file from analyze.py")
    parser.add_argument("--output", help="Output directory")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    ds = generate_design_system(data)

    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)

        (output_dir / "design-system.json").write_text(
            json.dumps(ds, indent=2), encoding="utf-8"
        )
        (output_dir / "tokens.css").write_text(ds["cssVariables"], encoding="utf-8")
        (output_dir / "tailwind.config.js").write_text(
            ds["tailwindConfig"], encoding="utf-8"
        )

        spec_lines = ["# Design System", ""]
        spec_lines.append("## Tokens")
        spec_lines.append(f"- Mode: {ds['meta']['mode']}")
        spec_lines.append(f"- Generated: {ds['meta']['generated']}")
        spec_lines.append("")
        spec_lines.append("## Colors")
        for role, data in ds["tokens"]["color"].items():
            spec_lines.append(f"- **{role}:** `{data['value']}`")
        spec_lines.append("")
        spec_lines.append("## Components")
        for comp in ds["components"]:
            spec_lines.append(f"- **{comp['name']}:** {comp['description']}")
        (output_dir / "DESIGN-SPEC.md").write_text(
            "\n".join(spec_lines), encoding="utf-8"
        )

        print(f"Design system written to {args.output}")
    else:
        print(json.dumps(ds, indent=2))
