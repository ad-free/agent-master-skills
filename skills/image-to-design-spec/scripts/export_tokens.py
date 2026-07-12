#!/usr/bin/env python3
"""
Design Token Export Module
Converts extracted colors/layout into multiple output formats:
- JSON (full data)
- Markdown (human-readable)
- CSS custom properties
- SCSS variables
- Tailwind config
- W3C DTCG format

Inspired by: huebrew (CSS/Tailwind export), design-token-extractor (W3C DTCG),
img2ui (multi-format), anydesign (design.md output)
"""

import sys
import json
import math
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass


def relative_luminance(r: int, g: int, b: int) -> float:
    rs, gs, bs = r / 255.0, g / 255.0, b / 255.0
    rl = rs / 12.92 if rs <= 0.04045 else ((rs + 0.055) / 1.055) ** 2.4
    gl = gs / 12.92 if gs <= 0.04045 else ((gs + 0.055) / 1.055) ** 2.4
    bl = bs / 12.92 if bs <= 0.04045 else ((bs + 0.055) / 1.055) ** 2.4
    return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl


def contrast_ratio(r1: int, g1: int, b1: int, r2: int, g2: int, b2: int) -> float:
    l1 = relative_luminance(r1, g1, b1)
    l2 = relative_luminance(r2, g2, b2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def generate_shades(hex_color: str, steps: list | None = None) -> dict:
    if steps is None:
        steps = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]

    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)

    result = {}
    for step in steps:
        factor = 1 - (step / 1000)
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

        nr = max(0, min(255, nr))
        ng = max(0, min(255, ng))
        nb = max(0, min(255, nb))
        result[step] = f"#{nr:02x}{ng:02x}{nb:02x}"

    return result


def export_json(data: dict) -> str:
    return json.dumps(data, indent=2)


def export_markdown(data: dict, source: str = "") -> str:
    lines = []
    lines.append(f"# Design Spec: {source}")
    lines.append(f"\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")

    lines.append("## Image\n")
    img = data.get("image", {})
    lines.append(f"- **Dimensions:** {img.get('width', '?')}x{img.get('height', '?')}")
    lines.append(f"- **Aspect Ratio:** {img.get('aspect_ratio', '?')}")
    lines.append(f"- **Mode:** {data.get('colors', {}).get('mode', '?')}")

    lines.append("\n## Color Palette\n")
    palette = data.get("colors", {}).get("palette", {})
    for role, color in palette.items():
        lines.append(f"- **{role}:** `{color}`")

    lines.append("\n## Dominant Colors\n")
    dominant = data.get("colors", {}).get("dominant", [])
    for i, color in enumerate(dominant):
        lines.append(f"{i + 1}. `{color}`")

    lines.append("\n## Layout\n")
    layout = data.get("layout", {})
    lines.append(f"- **Type:** {layout.get('layout_type', '?')}")
    lines.append(f"- **Background:** {layout.get('background_type', 'solid')}")
    lines.append(f"- **Header:** {'Yes' if layout.get('has_header') else 'No'}")
    lines.append(f"- **Footer:** {'Yes' if layout.get('has_footer') else 'No'}")
    lines.append(
        f"- **Sidebar:** {'Yes (' + layout.get('sidebar_position', '') + ', ' + str(layout.get('sidebar_width_percent', 0)) + '%)' if layout.get('has_sidebar') else 'No'}"
    )
    lines.append(f"- **Grid Columns:** {layout.get('estimated_grid_columns', '?')}")
    lines.append(f"- **Density:** {layout.get('spacing_hint', '?')}")
    lines.append(f"- **Complexity:** {layout.get('complexity_score', 0):.2f}")

    if layout.get("has_gradient"):
        lines.append(
            f"- **Gradient:** Yes ({layout.get('gradient_direction', 'unknown')})"
        )
    if layout.get("has_shadow"):
        lines.append(f"- **Shadow:** Yes ({layout.get('shadow_intensity', 'unknown')})")
    if layout.get("estimated_border_radius", 0) > 0:
        lines.append(f"- **Border Radius:** ~{layout.get('estimated_border_radius')}px")
    if layout.get("has_glass_effect"):
        lines.append(f"- **Glass Effect:** Yes (backdrop-filter detected)")

    lines.append("\n## Page Type\n")
    page_type = data.get("page_type", {})
    if page_type.get("page_type"):
        lines.append(
            f"- **Type:** {page_type.get('page_type', '?')} (confidence: {page_type.get('confidence', 0):.0%})"
        )
        lines.append(f"- **Reasoning:** {page_type.get('reasoning', '')}")
        if page_type.get("alternative_types"):
            alt = page_type["alternative_types"]
            alt_strs = [f"{a['type']} ({a['confidence']:.0%})" for a in alt[:2]]
            lines.append(f"- **Alternatives:** {', '.join(alt_strs)}")

    lines.append("\n## Components (Detected)\n")
    components = data.get("components", [])
    if components:
        grouped = {}
        for comp in components:
            ct = comp.get("type", "?")
            grouped.setdefault(ct, []).append(comp)
        for ctype, clist in grouped.items():
            avg_conf = sum(c.get("confidence", 0) for c in clist) / len(clist)
            lines.append(
                f"- **{ctype}** x{len(clist)} (avg confidence: {avg_conf:.0%})"
            )
    else:
        lines.append("*No components detected.*")

    lines.append("\n## Typography\n")
    typo = data.get("typography", {})
    if typo.get("has_text"):
        lines.append(f"- **Font Style:** {typo.get('font_style', '?')}")
        lines.append(
            f"- **Heading:** ~{typo.get('estimated_heading_size', '?')} ({typo.get('heading_px', '?')}px)"
        )
        lines.append(
            f"- **Body:** ~{typo.get('estimated_body_size', '?')} ({typo.get('body_px', '?')}px)"
        )
        clusters = typo.get("size_clusters", [])
        if clusters:
            cluster_str = ", ".join(
                f"{c['class']} ({c['px']}px ×{c['count']})" for c in clusters
            )
            lines.append(f"- **Size Scale:** {cluster_str}")
        lines.append(f"- **Text Regions:** {typo.get('detected_regions', 0)}")
    else:
        lines.append("*Text regions not detected.*")

    lines.append("\n## Tech Stack Recommendation\n")
    tech = data.get("tech_stack", {})
    recs = tech.get("recommendations", {})
    if recs:
        lines.append(
            f"- **Frontend:** {recs.get('frontend', {}).get('framework', '?')} — {recs.get('frontend', {}).get('reason', '')}"
        )
        lines.append(
            f"- **Styling:** {recs.get('styling', {}).get('solution', '?')} — {recs.get('styling', {}).get('reason', '')}"
        )
        if recs.get("state"):
            lines.append(
                f"- **State:** {recs['state'].get('library', '?')} — {recs['state'].get('reason', '')}"
            )
        if recs.get("charts"):
            lines.append(
                f"- **Charts:** {recs['charts'].get('library', '?')} — {recs['charts'].get('reason', '')}"
            )
        if recs.get("auth"):
            lines.append(
                f"- **Auth:** {recs['auth'].get('library', '?')} — {recs['auth'].get('reason', '')}"
            )
        lines.append(
            f"- **Backend:** {recs.get('backend', {}).get('framework', '?')} — {recs.get('backend', {}).get('reason', '')}"
        )
        lines.append(
            f"- **Deployment:** {recs.get('deployment', {}).get('platform', '?')} — {recs.get('deployment', {}).get('reason', '')}"
        )

    tokens = data.get("design_tokens", {})
    if tokens.get("colors"):
        lines.append("\n## Design Tokens\n")
        lines.append("### Colors (CSS Variables)\n```css")
        lines.append(":root {")
        for name, value in tokens.get("colors", {}).items():
            if isinstance(value, str):
                lines.append(f"  --color-{name}: {value};")
        lines.append("}")
        lines.append("```\n")

    lines.append("\n## Responsive Breakpoints\n")
    bp = layout.get("responsive_breakpoints", {})
    for name, value in bp.items():
        lines.append(f"- **{name}:** {value}px")

    return "\n".join(lines)


def export_css(data: dict) -> str:
    lines = [":root {"]
    palette = data.get("colors", {}).get("palette", {})
    for role, color in palette.items():
        lines.append(f"  --color-{role}: {color};")

    dominant = data.get("colors", {}).get("dominant", [])
    for i, color in enumerate(dominant):
        lines.append(f"  --color-{i + 1}: {color};")

    layout = data.get("layout", {})
    bp = layout.get("responsive_breakpoints", {})
    for name, value in bp.items():
        lines.append(f"  --breakpoint-{name}: {value}px;")

    lines.append("}")
    return "\n".join(lines)


def export_scss(data: dict) -> str:
    lines = []
    palette = data.get("colors", {}).get("palette", {})
    for role, color in palette.items():
        lines.append(f"$color-{role}: {color};")

    dominant = data.get("colors", {}).get("dominant", [])
    for i, color in enumerate(dominant):
        lines.append(f"$color-{i + 1}: {color};")

    lines.append("")
    lines.append("// Color map")
    lines.append("$colors: (")
    for role, color in palette.items():
        lines.append(f"  '{role}': {color},")
    lines.append(");")

    return "\n".join(lines)


def export_tailwind(data: dict) -> str:
    lines = ["module.exports = {", "  theme: {", "    extend: {", "      colors: {"]
    palette = data.get("colors", {}).get("palette", {})

    for role, color in palette.items():
        shades = generate_shades(color)
        lines.append(f"        '{role}': {{")
        for step, hex_val in shades.items():
            lines.append(f"          {step}: '{hex_val}',")
        lines.append("        },")

    lines.append("      },")
    lines.append("    },")
    lines.append("  },")
    lines.append("};")
    return "\n".join(lines)


def export_w3c(data: dict, source: str = "") -> str:
    tokens = {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "meta": {
            "source": source,
            "generated": datetime.now().isoformat(),
        },
        "color": {},
    }

    palette = data.get("colors", {}).get("palette", {})
    for role, color in palette.items():
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        tokens["color"][role] = {
            "$type": "color",
            "$value": color,
            "$description": f"RGB({r}, {g}, {b})",
            "$extensions": {
                "com.agent-master-skills.confidence": 0.85,
                "com.agent-master-skills.source": "kmeans-extraction",
            },
        }

    dominant = data.get("colors", {}).get("dominant", [])
    for i, color in enumerate(dominant):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        tokens["color"][f"dominant-{i + 1}"] = {
            "$type": "color",
            "$value": color,
            "$description": f"Dominant color {i + 1}: RGB({r}, {g}, {b})",
            "$extensions": {
                "com.agent-master-skills.area_percent": data.get("colors", {})
                .get("colors", [{}])[i]
                .get("area_percent", 0)
                if i < len(data.get("colors", {}).get("colors", []))
                else 0,
            },
        }

    return json.dumps(tokens, indent=2)


def export_storybook(data: dict, source: str = "") -> str:
    palette = data.get("colors", {}).get("palette", {})
    layout = data.get("layout", {})

    colors_obj = {}
    for role, color in palette.items():
        colors_obj[role] = {"value": color}

    tokens = {
        "color": colors_obj,
        "spacing": {
            "unit": {"value": "8px"},
            "xs": {"value": "4px"},
            "sm": {"value": "8px"},
            "md": {"value": "16px"},
            "lg": {"value": "24px"},
            "xl": {"value": "32px"},
            "2xl": {"value": "48px"},
        },
        "borderRadius": {
            "none": {"value": "0"},
            "sm": {"value": "4px"},
            "md": {"value": "8px"},
            "lg": {"value": "12px"},
            "xl": {"value": "16px"},
            "full": {"value": "9999px"},
        },
        "typography": {
            "fontFamily": {
                "value": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
            },
            "fontSize": {
                "xs": {"value": "0.75rem"},
                "sm": {"value": "0.875rem"},
                "base": {"value": "1rem"},
                "lg": {"value": "1.125rem"},
                "xl": {"value": "1.25rem"},
                "2xl": {"value": "1.5rem"},
                "3xl": {"value": "1.875rem"},
            },
        },
    }

    return f"""// Storybook storybook-addon-design-tokens format
// Source: {source}
// Generated: {datetime.now().isoformat()}

module.exports = {json.dumps(tokens, indent=2)};
"""


def export_figma(data: dict, source: str = "") -> str:
    palette = data.get("colors", {}).get("palette", {})
    layout = data.get("layout", {})

    figma_doc = {
        "schemaVersion": "1.0",
        "name": f"Design Tokens - {source}",
        "generated": datetime.now().isoformat(),
        "categories": [
            {
                "name": "Colors",
                "tokens": [
                    {
                        "name": role,
                        "type": "color",
                        "value": color,
                        "description": f"{role} color",
                    }
                    for role, color in palette.items()
                ],
            },
            {
                "name": "Spacing",
                "tokens": [
                    {"name": "xs", "type": "spacing", "value": "4px"},
                    {"name": "sm", "type": "spacing", "value": "8px"},
                    {"name": "md", "type": "spacing", "value": "16px"},
                    {"name": "lg", "type": "spacing", "value": "24px"},
                    {"name": "xl", "type": "spacing", "value": "32px"},
                ],
            },
            {
                "name": "Border Radius",
                "tokens": [
                    {"name": "none", "type": "borderRadius", "value": "0px"},
                    {"name": "sm", "type": "borderRadius", "value": "4px"},
                    {"name": "md", "type": "borderRadius", "value": "8px"},
                    {"name": "lg", "type": "borderRadius", "value": "12px"},
                    {"name": "full", "type": "borderRadius", "value": "9999px"},
                ],
            },
        ],
    }

    return json.dumps(figma_doc, indent=2)


EXPORTERS = {
    "json": export_json,
    "md": export_markdown,
    "markdown": export_markdown,
    "css": export_css,
    "scss": export_scss,
    "tailwind": export_tailwind,
    "w3c": export_w3c,
    "storybook": export_storybook,
    "figma": export_figma,
}


def export(data: dict, format: str, source: str = "") -> str:
    exporter = EXPORTERS.get(format)
    if not exporter:
        print(
            f"Warning: Unknown format '{format}', falling back to JSON", file=sys.stderr
        )
        return export_json(data)

    if format in ("md", "markdown", "w3c", "storybook", "figma"):
        return exporter(data, source)
    else:
        return exporter(data)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Export design tokens")
    parser.add_argument("--input", required=True, help="JSON file from analyze.py")
    parser.add_argument(
        "--format", choices=list(EXPORTERS.keys()), default="md", help="Output format"
    )
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--source", default="", help="Source image name")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    result = export(data, args.format, args.source)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Written to {args.output}")
    else:
        print(result)
