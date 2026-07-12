#!/usr/bin/env python3
"""
Code Generation Module
Generates working code in multiple frameworks from extracted design tokens.

Inspired by: screenshot-to-code (GPT-4o → React/Vue/HTML), img2ui (multi-framework),
design-dna (Design DNA extraction), ScreenCoder (multi-agent architecture)

Supported frameworks:
- React + Tailwind CSS (Next.js compatible)
- Vue + Tailwind CSS (Nuxt compatible)
- HTML + CSS (vanilla, no build step)
- HTML + CSS + Tailwind CDN (quick prototype)

Uses industry-standard numbers from global companies (Tailwind, Material, Apple)
"""

import json
from pathlib import Path
from dataclasses import dataclass

from standards import (
    SIDEBAR_WIDTHS,
    BORDER_RADIUS,
    BORDER_RADIUS_MAP,
    snap_to_border_radius,
)


@dataclass
class CodeGenOptions:
    framework: str = "react"
    include_layout: bool = True
    include_components: bool = True
    include_responsive: bool = True
    dark_mode: bool = False
    component_name: str = "Page"


def hex_to_rgb(hex_color: str) -> dict:
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return {"r": r, "g": g, "b": b}


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


def detect_layout_structure(data: dict) -> dict:
    layout = data.get("layout", {})
    layout_type = layout.get("layout_type", "single-column")
    has_header = layout.get("has_header", False)
    has_footer = layout.get("has_footer", False)
    has_sidebar = layout.get("has_sidebar", False)
    sidebar_position = layout.get("sidebar_position", "left")
    sidebar_width = layout.get("sidebar_width_percent", 20)
    is_centered = layout_type == "centered-card"
    is_hero = layout_type == "hero-fullscreen"

    return {
        "type": layout_type,
        "has_header": has_header,
        "has_footer": has_footer,
        "has_sidebar": has_sidebar,
        "sidebar_position": sidebar_position,
        "sidebar_width": sidebar_width,
        "is_centered": is_centered,
        "is_hero": is_hero,
        "has_gradient": layout.get("has_gradient", False),
        "gradient_direction": layout.get("gradient_direction", ""),
        "has_shadow": layout.get("has_shadow", False),
        "shadow_intensity": layout.get("shadow_intensity", ""),
        "border_radius": layout.get("estimated_border_radius", 0),
        "has_glass": layout.get("has_glass_effect", False),
        "background_type": layout.get("background_type", "solid"),
    }


def get_palette(data: dict) -> dict:
    return data.get("colors", {}).get(
        "palette",
        {
            "primary": "#1a1a2e",
            "secondary": "#16213e",
            "accent": "#e94560",
            "background": "#ffffff",
            "surface": "#f5f5f5",
            "text-primary": "#1a1a2e",
        },
    )


def generate_react_tailwind(data: dict, opts: CodeGenOptions) -> str:
    palette = get_palette(data)
    layout = detect_layout_structure(data)
    name = opts.component_name

    primary = palette.get("primary", "#1a1a2e")
    accent = palette.get("accent", "#e94560")
    bg = palette.get("background", "#ffffff")
    surface = palette.get("surface", "#f5f5f5")
    text_primary = palette.get("text-primary", "#1a1a2e")

    imports = [
        "import React from 'react';",
    ]

    bg_style = ""
    if layout["has_gradient"]:
        direction = layout.get("gradient_direction", "vertical")
        if "vertical" in direction:
            bg_style = f"bg-gradient-to-b from-[{primary}] to-[{accent}]"
        elif "horizontal" in direction:
            bg_style = f"bg-gradient-to-r from-[{primary}] to-[{accent}]"
        elif "diagonal" in direction:
            bg_style = f"bg-gradient-to-br from-[{primary}] to-[{accent}]"
        else:
            bg_style = f"bg-gradient-to-b from-[{primary}] to-[{accent}]"
    elif layout["is_hero"]:
        bg_style = f"bg-gradient-to-b from-[{primary}]/80 to-[{primary}]"

    glass_class = ""
    if layout["has_glass"]:
        glass_class = "backdrop-blur-md bg-white/10 border border-white/20"

    shadow_class = ""
    if layout["has_shadow"]:
        intensity = layout.get("shadow_intensity", "light")
        shadow_map = {"light": "shadow-sm", "medium": "shadow-md", "heavy": "shadow-lg"}
        shadow_class = shadow_map.get(intensity, "shadow-sm")

    radius = layout.get("border_radius", 0)
    if radius >= 24:
        radius_class = "rounded-full"
    elif radius >= 16:
        radius_class = "rounded-2xl"
    elif radius >= 8:
        radius_class = "rounded-xl"
    elif radius > 0:
        radius_class = "rounded-lg"
    else:
        radius_class = "rounded-none"

    sidebar_width_pct = layout.get("sidebar_width", 20)
    sidebar_pixel_width = (
        int(1280 * sidebar_width_pct / 100) if sidebar_width_pct else 256
    )
    standard_sidebar_width = min(
        SIDEBAR_WIDTHS.values(), key=lambda x: abs(x - sidebar_pixel_width)
    )

    lines = []
    lines.extend(imports)
    lines.append("")
    lines.append(f"export default function {name}() {{")

    if layout["type"] == "hero-fullscreen":
        lines.append(f"  return (")
        lines.append(
            f'    <div className="min-h-screen {bg_style} flex flex-col items-center justify-center text-white px-4">'
        )
        lines.append(f'      <h1 className="text-5xl font-bold mb-4">Welcome</h1>')
        lines.append(
            f'      <p className="text-xl mb-8 opacity-90">Your tagline here</p>'
        )
        lines.append(
            f'      <button className="px-8 py-3 bg-[{accent}] {radius_class} font-semibold hover:opacity-90 transition">'
        )
        lines.append(f"        Get Started")
        lines.append(f"      </button>")
        lines.append(f"    </div>")
        lines.append(f"  );")

    elif layout["type"] == "centered-card":
        lines.append(f"  return (")
        lines.append(
            f'    <div className="min-h-screen bg-[{bg}] flex items-center justify-center px-4">'
        )
        lines.append(
            f'      <div className="w-full max-w-md p-8 bg-[{surface}] {radius_class} {shadow_class} {glass_class}">'
        )
        lines.append(
            f'        <h2 className="text-2xl font-bold text-[{text_primary}] mb-6">Sign Up</h2>'
        )
        lines.append(f'        <form className="space-y-4">')
        lines.append(f"          <input")
        lines.append(f'            type="email"')
        lines.append(f'            placeholder="Email"')
        lines.append(
            f'            className="w-full px-4 py-3 {radius_class} border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[{accent}]"'
        )
        lines.append(f"          />")
        lines.append(f"          <input")
        lines.append(f'            type="password"')
        lines.append(f'            placeholder="Password"')
        lines.append(
            f'            className="w-full px-4 py-3 {radius_class} border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[{accent}]"'
        )
        lines.append(f"          />")
        lines.append(f"          <button")
        lines.append(f'            type="submit"')
        lines.append(
            f'            className="w-full py-3 bg-[{accent}] text-white {radius_class} font-semibold hover:opacity-90 transition"'
        )
        lines.append(f"          >")
        lines.append(f"            Submit")
        lines.append(f"          </button>")
        lines.append(f"        </form>")
        lines.append(f"      </div>")
        lines.append(f"    </div>")
        lines.append(f"  );")

    elif layout["type"] == "sidebar-main":
        sidebar_w = (
            f"w-{standard_sidebar_width // 4}"
            if standard_sidebar_width <= 128
            else f"w-[{standard_sidebar_width}px]"
        )
        lines.append(f"  return (")
        lines.append(f'    <div className="min-h-screen flex bg-[{bg}]">')
        lines.append(
            f'      <aside className="{sidebar_w} bg-[{surface}] p-6 border-r border-gray-200">'
        )
        lines.append(
            f'        <div className="text-lg font-bold text-[{text_primary}] mb-6">Logo</div>'
        )
        lines.append(f'        <nav className="space-y-2">')
        lines.append(
            f"          {{['Dashboard', 'Settings', 'Profile'].map((item) => ("
        )
        lines.append(
            f'            <a key={{item}} href="#" className="block px-4 py-2 {radius_class} hover:bg-[{primary}]/10 text-[{text_primary}]">'
        )
        lines.append(f"              {{item}}")
        lines.append(f"            </a>")
        lines.append(f"          ))}}")
        lines.append(f"        </nav>")
        lines.append(f"      </aside>")
        lines.append(f'      <main className="flex-1 p-8">')
        lines.append(
            f'        <h1 className="text-2xl font-bold text-[{text_primary}] mb-4">Dashboard</h1>'
        )
        lines.append(f'        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">')
        lines.append(f"          {{[1, 2, 3].map((i) => (")
        lines.append(
            f'            <div key={{i}} className="p-6 bg-[{surface}] {radius_class} {shadow_class}">'
        )
        lines.append(
            f'              <div className="text-sm text-gray-500 mb-2">Card {{i}}</div>'
        )
        lines.append(
            f'              <div className="text-2xl font-bold text-[{text_primary}]">Content</div>'
        )
        lines.append(f"            </div>")
        lines.append(f"          ))}}")
        lines.append(f"        </div>")
        lines.append(f"      </main>")
        lines.append(f"    </div>")
        lines.append(f"  );")

    elif layout["type"] == "grid":
        cols = (
            layout.get("grid_columns", 3)
            if "grid_columns" in layout
            else data.get("layout", {}).get("estimated_grid_columns", 3)
        )
        lines.append(f"  return (")
        lines.append(f'    <div className="min-h-screen bg-[{bg}] p-8">')
        lines.append(
            f'      <h1 className="text-2xl font-bold text-[{text_primary}] mb-6">Gallery</h1>'
        )
        lines.append(
            f'      <div className="grid grid-cols-1 md:grid-cols-{cols} gap-6">'
        )
        lines.append(f"        {{Array.from({{ length: 12 }}).map((_, i) => (")
        lines.append(
            f'          <div key={{i}} className="aspect-square bg-[{surface}] {radius_class} {shadow_class} hover:scale-105 transition-transform cursor-pointer" />'
        )
        lines.append(f"        ))}}")
        lines.append(f"      </div>")
        lines.append(f"    </div>")
        lines.append(f"  );")

    else:
        lines.append(f"  return (")
        lines.append(f'    <div className="min-h-screen bg-[{bg}] px-4 py-12">')
        lines.append(f'      <div className="max-w-3xl mx-auto">')
        lines.append(
            f'        <h1 className="text-3xl font-bold text-[{text_primary}] mb-8">Title</h1>'
        )
        lines.append(f'        <div className="space-y-6">')
        lines.append(
            f'          <div className="p-6 bg-[{surface}] {radius_class} {shadow_class}">'
        )
        lines.append(
            f'            <p className="text-[{text_primary}]">Content goes here.</p>'
        )
        lines.append(f"          </div>")
        lines.append(f"        </div>")
        lines.append(f"      </div>")
        lines.append(f"    </div>")
        lines.append(f"  );")

    lines.append("}")
    return "\n".join(lines)


def generate_vue_tailwind(data: dict, opts: CodeGenOptions) -> str:
    palette = get_palette(data)
    layout = detect_layout_structure(data)
    name = opts.component_name

    primary = palette.get("primary", "#1a1a2e")
    accent = palette.get("accent", "#e94560")
    bg = palette.get("background", "#ffffff")
    surface = palette.get("surface", "#f5f5f5")
    text_primary = palette.get("text-primary", "#1a1a2e")

    bg_class = ""
    if layout["has_gradient"]:
        direction = layout.get("gradient_direction", "vertical")
        if "vertical" in direction:
            bg_class = f"bg-gradient-to-b from-[{primary}] to-[{accent}]"
        elif "horizontal" in direction:
            bg_class = f"bg-gradient-to-r from-[{primary}] to-[{accent}]"
        else:
            bg_class = f"bg-gradient-to-br from-[{primary}] to-[{accent}]"

    shadow_class = ""
    if layout["has_shadow"]:
        intensity = layout.get("shadow_intensity", "light")
        shadow_map = {"light": "shadow-sm", "medium": "shadow-md", "heavy": "shadow-lg"}
        shadow_class = shadow_map.get(intensity, "shadow-sm")

    radius = layout.get("border_radius", 0)
    if radius >= 24:
        radius_class = "rounded-full"
    elif radius >= 16:
        radius_class = "rounded-2xl"
    elif radius >= 8:
        radius_class = "rounded-xl"
    elif radius > 0:
        radius_class = "rounded-lg"
    else:
        radius_class = "rounded-none"

    glass_class = ""
    if layout["has_glass"]:
        glass_class = "backdrop-blur-md bg-white/10 border border-white/20"

    lines = []
    lines.append("<template>")
    lines.append(f"  <div :class=\"['min-h-screen', bgClass]\">")

    if layout["type"] == "hero-fullscreen":
        lines.append(
            f'    <div class="flex flex-col items-center justify-center text-white px-4">'
        )
        lines.append(f'      <h1 class="text-5xl font-bold mb-4">Welcome</h1>')
        lines.append(f'      <p class="text-xl mb-8 opacity-90">Your tagline here</p>')
        lines.append(
            f"      <button :class=\"['px-8 py-3 font-semibold transition hover:opacity-90', accentBg, '{radius_class}']\">"
        )
        lines.append(f"        Get Started")
        lines.append(f"      </button>")
        lines.append(f"    </div>")

    elif layout["type"] == "centered-card":
        lines.append(f'    <div class="flex items-center justify-center px-4">')
        lines.append(
            f"      <div :class=\"['w-full max-w-md p-8', '{radius_class}', '{shadow_class}', '{glass_class}']\" :style=\"{{ backgroundColor: surface }}\">"
        )
        lines.append(
            f'        <h2 class="text-2xl font-bold mb-6" :style="{{ color: textPrimary }}>Sign Up</h2>'
        )
        lines.append(f'        <form class="space-y-4">')
        lines.append(
            f'          <input type="email" placeholder="Email" :class="[\'w-full px-4 py-3\', \'{radius_class}\']" :style="inputStyle" />'
        )
        lines.append(
            f'          <input type="password" placeholder="Password" :class="[\'w-full px-4 py-3\', \'{radius_class}\']" :style="inputStyle" />'
        )
        lines.append(
            f'          <button type="submit" :class="[\'w-full py-3 text-white font-semibold transition hover:opacity-90\', \'{radius_class}\']" :style="{{ backgroundColor: accent }}">Submit</button>'
        )
        lines.append(f"        </form>")
        lines.append(f"      </div>")
        lines.append(f"    </div>")

    else:
        sidebar_w = (
            layout.get("sidebar_width", 20) if layout["type"] == "sidebar-main" else 20
        )
        lines.append(f'    <div class="flex">')
        lines.append(
            f"      <aside :class=\"['p-6 border-r border-gray-200']\" :style=\"{{ width: '{sidebar_w}%', backgroundColor: surface }}\">"
        )
        lines.append(
            f'        <div class="text-lg font-bold mb-6" :style="{{ color: textPrimary }}">Logo</div>'
        )
        lines.append(f'        <nav class="space-y-2">')
        lines.append(
            f"          <a v-for=\"item in ['Dashboard', 'Settings', 'Profile']\" :key=\"item\" href=\"#\""
        )
        lines.append(f"            :class=\"['block px-4 py-2', '{radius_class}']\"")
        lines.append(
            f'            :style="{{ color: textPrimary }}">{{{{ item }}}}</a>'
        )
        lines.append(f"        </nav>")
        lines.append(f"      </aside>")
        lines.append(f'      <main class="flex-1 p-8">')
        lines.append(
            f'        <h1 class="text-2xl font-bold mb-4" :style="{{ color: textPrimary }}">Dashboard</h1>'
        )
        lines.append(f'        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">')
        lines.append(f'          <div v-for="i in 3" :key="i"')
        lines.append(
            f"            :class=\"['p-6', '{radius_class}', '{shadow_class}']\""
        )
        lines.append(f'            :style="{{ backgroundColor: surface }}">')
        lines.append(
            f'            <div class="text-sm text-gray-500 mb-2">Card {{{{ i }}}}</div>'
        )
        lines.append(
            f'            <div class="text-2xl font-bold" :style="{{ color: textPrimary }}">Content</div>'
        )
        lines.append(f"          </div>")
        lines.append(f"        </div>")
        lines.append(f"      </main>")
        lines.append(f"    </div>")

    lines.append(f"  </div>")
    lines.append("</template>")
    lines.append("")
    lines.append("<script setup>")
    lines.append(f"import {{ ref, computed }} from 'vue'")
    lines.append(f"")
    lines.append(f"const primary = '{primary}'")
    lines.append(f"const accent = '{accent}'")
    lines.append(f"const bg = '{bg}'")
    lines.append(f"const surface = '{surface}'")
    lines.append(f"const textPrimary = '{text_primary}'")
    lines.append(f"")
    lines.append(f"const bgClass = computed(() => '{bg_class}')")
    lines.append(f"")
    lines.append(f"const accentBg = computed(() => 'bg-[{accent}]')")
    lines.append(f"")
    lines.append("const inputStyle = computed(() => ({")
    lines.append("    border: '1px solid #e5e7eb',")
    lines.append("    backgroundColor: 'white',")
    lines.append("    outline: 'none',")
    lines.append("  }))")
    lines.append("</script>")
    return "\n".join(lines)


def generate_html_css(data: dict, opts: CodeGenOptions) -> str:
    palette = get_palette(data)
    layout = detect_layout_structure(data)
    name = opts.component_name

    primary = palette.get("primary", "#1a1a2e")
    accent = palette.get("accent", "#e94560")
    bg = palette.get("background", "#ffffff")
    surface = palette.get("surface", "#f5f5f5")
    text_primary = palette.get("text-primary", "#1a1a2e")

    radius = layout.get("border_radius", 0)
    shadow = ""
    if layout["has_shadow"]:
        intensity = layout.get("shadow_intensity", "light")
        shadow_map = {
            "light": "0 1px 3px rgba(0,0,0,0.1)",
            "medium": "0 4px 6px rgba(0,0,0,0.1)",
            "heavy": "0 10px 25px rgba(0,0,0,0.15)",
        }
        shadow = shadow_map.get(intensity, "0 1px 3px rgba(0,0,0,0.1)")

    gradient = ""
    if layout["has_gradient"]:
        direction = layout.get("gradient_direction", "vertical")
        if "vertical" in direction:
            gradient = f"linear-gradient(180deg, {primary}, {accent})"
        elif "horizontal" in direction:
            gradient = f"linear-gradient(90deg, {primary}, {accent})"
        elif "diagonal" in direction:
            gradient = f"linear-gradient(135deg, {primary}, {accent})"
        else:
            gradient = f"linear-gradient(180deg, {primary}, {accent})"

    html_content = ""
    css_styles = []

    if layout["type"] == "hero-fullscreen":
        html_content = f"""    <div class="hero">
      <h1>Welcome</h1>
      <p>Your tagline here</p>
      <button class="btn-primary">Get Started</button>
    </div>"""
        css_styles = [
            f"* {{ margin: 0; padding: 0; box-sizing: border-box; }}",
            f"body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}",
            f".hero {{ min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; color: white; padding: 1rem; background: {gradient if gradient else primary}; }}",
            f".hero h1 {{ font-size: 3rem; font-weight: 700; margin-bottom: 1rem; }}",
            f".hero p {{ font-size: 1.25rem; margin-bottom: 2rem; opacity: 0.9; }}",
            f".btn-primary {{ padding: 0.75rem 2rem; background: {accent}; color: white; border: none; border-radius: {radius}px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }}",
            f".btn-primary:hover {{ opacity: 0.9; }}",
        ]

    elif layout["type"] == "centered-card":
        html_content = f"""    <div class="card-container">
      <div class="card">
        <h2>Sign Up</h2>
        <form>
          <input type="email" placeholder="Email" />
          <input type="password" placeholder="Password" />
          <button type="submit" class="btn-primary">Submit</button>
        </form>
      </div>
    </div>"""
        css_styles = [
            f"* {{ margin: 0; padding: 0; box-sizing: border-box; }}",
            f"body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: {bg}; }}",
            f".card-container {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 1rem; }}",
            f".card {{ width: 100%; max-width: 24rem; padding: 2rem; background: {surface}; border-radius: {radius}px; {f'box-shadow: {shadow};' if shadow else ''} }}",
            f".card h2 {{ font-size: 1.5rem; font-weight: 700; color: {text_primary}; margin-bottom: 1.5rem; }}",
            f"form {{ display: flex; flex-direction: column; gap: 1rem; }}",
            f"input {{ width: 100%; padding: 0.75rem 1rem; border: 1px solid #e5e7eb; border-radius: {radius}px; font-size: 1rem; outline: none; }}",
            f"input:focus {{ box-shadow: 0 0 0 3px {accent}33; border-color: {accent}; }}",
            f".btn-primary {{ width: 100%; padding: 0.75rem; background: {accent}; color: white; border: none; border-radius: {radius}px; font-size: 1rem; font-weight: 600; cursor: pointer; }}",
        ]

    elif layout["type"] == "sidebar-main":
        sidebar_pct = layout.get("sidebar_width", 20)
        sidebar_pixel = int(1280 * sidebar_pct / 100) if sidebar_pct else 256
        standard_sidebar = min(
            SIDEBAR_WIDTHS.values(), key=lambda x: abs(x - sidebar_pixel)
        )
        html_content = f"""    <div class="layout">
      <aside class="sidebar">
        <div class="logo">Logo</div>
        <nav>
          <a href="#">Dashboard</a>
          <a href="#">Settings</a>
          <a href="#">Profile</a>
        </nav>
      </aside>
      <main class="main">
        <h1>Dashboard</h1>
        <div class="grid">
          <div class="card">Card 1</div>
          <div class="card">Card 2</div>
          <div class="card">Card 3</div>
        </div>
      </main>
    </div>"""
        css_styles = [
            f"* {{ margin: 0; padding: 0; box-sizing: border-box; }}",
            f"body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: {bg}; }}",
            f".layout {{ display: flex; min-height: 100vh; }}",
            f".sidebar {{ width: {standard_sidebar}px; background: {surface}; padding: 1.5rem; border-right: 1px solid #e5e7eb; }}",
            f".logo {{ font-size: 1.25rem; font-weight: 700; color: {text_primary}; margin-bottom: 1.5rem; }}",
            f"nav {{ display: flex; flex-direction: column; gap: 0.5rem; }}",
            f"nav a {{ display: block; padding: 0.5rem 1rem; color: {text_primary}; text-decoration: none; border-radius: {radius}px; transition: background 0.2s; }}",
            f"nav a:hover {{ background: {primary}1a; }}",
            f".main {{ flex: 1; padding: 2rem; }}",
            f".main h1 {{ font-size: 1.5rem; font-weight: 700; color: {text_primary}; margin-bottom: 1rem; }}",
            f".grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }}",
            f".card {{ padding: 1.5rem; background: {surface}; border-radius: {radius}px; {f'box-shadow: {shadow};' if shadow else ''} }}",
        ]

    else:
        html_content = f"""    <div class="container">
      <h1>Title</h1>
      <div class="content">
        <p>Content goes here.</p>
      </div>
    </div>"""
        css_styles = [
            f"* {{ margin: 0; padding: 0; box-sizing: border-box; }}",
            f"body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: {bg}; }}",
            f".container {{ max-width: 48rem; margin: 0 auto; padding: 3rem 1rem; }}",
            f"h1 {{ font-size: 1.875rem; font-weight: 700; color: {text_primary}; margin-bottom: 2rem; }}",
            f".content {{ padding: 1.5rem; background: {surface}; border-radius: {radius}px; {f'box-shadow: {shadow};' if shadow else ''} }}",
            f".content p {{ color: {text_primary}; }}",
        ]

    css_block = "\n".join(css_styles)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name}</title>
  <style>
{css_block}
  </style>
</head>
<body>
{html_content}
</body>
</html>"""


def generate_code(
    data: dict, framework: str = "react", component_name: str = "Page"
) -> str:
    opts = CodeGenOptions(framework=framework, component_name=component_name)

    if framework == "react":
        return generate_react_tailwind(data, opts)
    elif framework == "vue":
        return generate_vue_tailwind(data, opts)
    elif framework == "html":
        return generate_html_css(data, opts)
    else:
        return generate_react_tailwind(data, opts)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate code from design tokens")
    parser.add_argument("--input", required=True, help="JSON file from analyze.py")
    parser.add_argument(
        "--framework", choices=["react", "vue", "html"], default="react"
    )
    parser.add_argument("--component-name", default="Page")
    parser.add_argument("--output", help="Output file path")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    result = generate_code(data, args.framework, args.component_name)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Written to {args.output}")
    else:
        print(result)
