#!/usr/bin/env python3
"""
HTML style guide preview generator for ui-craft.
Generates self-contained HTML files that render the design system visually.
"""

import json
from pathlib import Path


def generate_design_system_preview(design_system: dict) -> str:
    """Generate a self-contained HTML preview of the design system."""
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    style = design_system.get("style", {})
    pattern = design_system.get("pattern", {})

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Design System Preview</title>
<style>
  :root {{
    {_generate_css_vars(design_system)}
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: '{design_system.get("typography", {}).get("body", "Inter")}', sans-serif;
    background: var(--color-background);
    color: var(--color-foreground);
    padding: 2rem;
    line-height: 1.6;
  }}
  .container {{ max-width: 1200px; margin: 0 auto; }}
  h1, h2, h3, h4 {{ font-family: '{design_system.get("typography", {}).get("heading", "Inter")}', sans-serif; }}
  h1 {{ font-size: 2.5rem; font-weight: 700; }}
  h2 {{ font-size: 2rem; font-weight: 600; margin-top: 2rem; }}
  h3 {{ font-size: 1.5rem; font-weight: 600; }}
  .section {{ margin: 2rem 0; padding: 1.5rem; border: 1px solid var(--color-border); border-radius: 12px; }}
  .color-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; }}
  .color-swatch {{ padding: 1rem; border-radius: 8px; border: 1px solid var(--color-border); }}
  .color-swatch .preview {{ height: 60px; border-radius: 6px; margin-bottom: 0.5rem; }}
  .color-swatch .label {{ font-size: 0.875rem; }}
  .color-swatch .hex {{ font-size: 0.75rem; color: var(--color-muted-foreground); font-family: monospace; }}
  .component-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; }}
  .component-preview {{ padding: 1.5rem; border: 1px solid var(--color-border); border-radius: 8px; }}
  .btn {{ display: inline-flex; align-items: center; justify-content: center; border-radius: 8px; font-size: 0.875rem; font-weight: 500; padding: 0.5rem 1rem; cursor: pointer; transition: all 200ms; }}
  .btn-primary {{ background: var(--color-primary); color: white; }}
  .btn-secondary {{ background: var(--color-secondary); color: white; }}
  .btn-outline {{ border: 1px solid var(--color-border); background: transparent; }}
  .dark-mode {{ display: none; }}
  body.dark .dark-mode {{ display: block; }}
  body.dark .light-mode {{ display: none; }}

  /* Device Frame Styles */
  .device-frame {{
    position: relative;
    margin: 2rem 0;
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    overflow: hidden;
    background: white;
  }}
  .device-frame::before {{
    content: "";
    position: absolute;
    top: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 8px;
    background: #ddd;
    border-radius: 4px;
    z-index: 10;
  }}
  .device-header {{
    background: #f5f5f5;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--color-border);
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }}
  .device-dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #ddd;
  }}
  .device-dot.active {{
    background: #4CAF50;
  }}
  .device-content {{
    padding: 1.5rem;
  }}
  .device {{ margin-bottom: 3rem; }}
  .device-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--color-muted-foreground);
  }}
  .device-toggle {{
    display: inline-flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }}
  .device-btn {{
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
    font-size: 0.75rem;
    cursor: pointer;
    border: 1px solid var(--color-border);
    background: transparent;
  }}
  .device-btn.active {{
    background: var(--color-primary);
    color: white;
    border-color: var(--color-primary);
  }}
  .device-iframe {{
    width: 100%;
    height: 300px;
    border: none;
    background: white;
  }}
  .device-tabs {{
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }}
  .device-tab {{
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-size: 0.875rem;
    cursor: pointer;
    border: 1px solid var(--color-border);
    background: transparent;
  }}
  .device-tab.active {{
    background: var(--color-muted);
  }}
</style>
</head>
<body>
<div class="container">
  <h1>Design System Preview</h1>
  <p>Project: {design_system.get("project_name", "Untitled")}</p>
  <p>Style: {design_system.get("style", {}).get("name", "Minimalism")}</p>

  <div class="section">
    <h2>Color Palette</h2>
    <div class="color-grid">
      {_generate_color_swatches(design_system)}
    </div>
  </div>

  <div class="section">
    <h2>Typography</h2>
    <h1>Heading 1</h1>
    <h2>Heading 2</h2>
    <h3>Heading 3</h3>
    <p style="font-size: 1rem;">Body text — The quick brown fox jumps over the lazy dog.</p>
    <p style="font-size: 0.875rem; color: var(--color-muted-foreground);">Small text — The quick brown fox jumps over the lazy dog.</p>
  </div>

  <div class="section">
    <h2>Components</h2>
    <div class="component-grid">
      <div class="component-preview">
        <h3>Buttons</h3>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 1rem;">
          <button class="btn btn-primary">Primary</button>
          <button class="btn btn-secondary">Secondary</button>
          <button class="btn btn-outline">Outline</button>
        </div>
      </div>
      <div class="component-preview">
        <h3>Card</h3>
        <div style="border: 1px solid var(--color-border); border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
          <h3 style="margin: 0 0 0.5rem;">Card Title</h3>
          <p style="color: var(--color-muted-foreground); font-size: 0.875rem;">This is a card with some content.</p>
        </div>
      </div>
      <div class="component-preview">
        <h3>Input</h3>
        <input
          placeholder="Type something..."
          style="width: 100%; padding: 0.75rem 1rem; border: 1px solid var(--color-border); border-radius: 8px; font-size: 1rem; background: var(--color-background); color: var(--color-foreground);"
        />
      </div>
    </div>
  </div>
</div>
</body>
</html>"""

    return html


def _generate_css_vars(design_system: dict) -> str:
    """Generate CSS variable declarations from design system."""
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    spacing = design_system.get("spacing_scale", {})

    vars = []
    color_map = {
        "--color-primary": colors.get("primary", "#2563EB"),
        "--color-primary-foreground": colors.get("on_primary", "#FFFFFF"),
        "--color-secondary": colors.get("secondary", "#3B82F6"),
        "--color-accent": colors.get("accent", "#F97316"),
        "--color-background": colors.get("background", "#F8FAFC"),
        "--color-foreground": colors.get("foreground", "#1E293B"),
        "--color-muted": colors.get("muted", "#F1F5F9"),
        "--color-muted-foreground": colors.get("muted_foreground", "#64748B"),
        "--color-border": colors.get("border", "#E2E8F0"),
        "--color-destructive": colors.get("destructive", "#EF4444"),
        "--color-ring": colors.get("ring", "#2563EB"),
    }
    for name, hex_val in color_map.items():
        vars.append(f"  {name}: {hex_val};")
    vars.append(
        f"  --font-heading: '{typography.get('heading', 'Inter')}', sans-serif;"
    )
    vars.append(f"  --font-body: '{typography.get('body', 'Inter')}', sans-serif;")
    return "\n".join(vars)


def _generate_color_swatches(design_system: dict) -> str:
    """Generate HTML for color swatches."""
    colors = design_system.get("colors", {})
    swatches = []
    color_entries = [
        ("Primary", "primary"),
        ("Secondary", "secondary"),
        ("Accent", "accent"),
        ("Background", "background"),
        ("Foreground", "foreground"),
        ("Muted", "muted"),
        ("Border", "border"),
        ("Destructive", "destructive"),
    ]
    for label, key in color_entries:
        hex_val = colors.get(key, "")
        if hex_val:
            swatches.append(
                f'<div class="color-swatch">'
                f'<div class="preview" style="background: {hex_val};"></div>'
                f'<div class="label">{label}</div>'
                f'<div class="hex">{hex_val}</div>'
                f"</div>"
            )
    return "\n".join(swatches)


def generate_preview(design_system: dict, output_path: str) -> str:
    """Generate and save the HTML preview file."""
    html = generate_design_system_preview(design_system)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return str(path)
