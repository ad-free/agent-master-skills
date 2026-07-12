#!/usr/bin/env python3
"""
Image-to-Design-Spec Orchestrator
Main entry point for analyzing UI screenshots and generating design specs.

Hybrid approach:
- Layer 1: Pillow + K-means (always) - colors, dimensions, layout
- Layer 2: Gemini Vision (optional) - component analysis
- Layer 3: Guided questions (fallback) - user description

Output formats: JSON, Markdown, CSS, SCSS, Tailwind, W3C DTCG
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from extract_colors import extract_from_image, detect_mode, build_palette
from extract_layout import analyze_layout
from export_tokens import export
from generate_code import generate_code
from generate_design_system import generate_design_system
from detect_components import detect_components
from detect_typography import detect_typography
from detect_page_type import classify_page
from recommend_tech_stack import recommend_tech_stack


def check_dependencies() -> dict:
    deps = {"pillow": False, "numpy": False, "gemini": False}

    try:
        from PIL import Image

        deps["pillow"] = True
    except ImportError:
        pass

    try:
        import numpy

        deps["numpy"] = True
    except ImportError:
        pass

    try:
        from google import genai

        deps["gemini"] = bool(os.environ.get("GEMINI_API_KEY"))
    except ImportError:
        pass

    return deps


def load_env():
    env_paths = [
        Path(__file__).parent.parent.parent / ".env",
        Path.home() / ".opencode" / ".env",
        Path.home() / ".claude" / ".env",
    ]
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = str(line).strip()
                    if line and not str(line).startswith("#") and "=" in str(line):
                        key, value = str(line).split("=", 1)
                        if key not in os.environ:
                            os.environ[key] = value.strip("\"'")
    return


def analyze_with_gemini(image_path: str) -> dict | None:
    load_env()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        with open(image_path, "rb") as f:
            image_bytes = f.read()

        ext = Path(image_path).suffix.lower()
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }
        mime = mime_map.get(ext, "image/png")

        prompt = """Analyze this UI screenshot. Return a JSON object with:
{
  "components": [
    {"type": "component_name", "confidence": 0.95, "region": "location", "description": "brief description"}
  ],
  "typography": {
    "heading_style": "sans-serif or serif",
    "body_style": "sans-serif or serif",
    "heading_weight": "bold or normal",
    "estimated_sizes": {"h1": "2rem", "h2": "1.5rem", "body": "1rem"}
  },
  "spacing": {
    "unit": "estimated base unit in px",
    "padding_scale": "tight, normal, or spacious"
  },
  "border_radius": {
    "style": "sharp, rounded, pill",
    "estimated_radius": "4px, 8px, 12px, etc."
  },
  "effects": {
    "shadows": true/false,
    "gradients": true/false,
    "blur": true/false
  },
  "description": "Brief overall description of the UI"
}

Return ONLY valid JSON, no markdown."""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime),
                        types.Part.from_text(text=prompt),
                    ],
                )
            ],
        )

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(text)

    except Exception as e:
        print(f"Gemini analysis failed: {e}", file=sys.stderr)
        return None


def generate_guided_questions() -> list:
    return [
        {
            "category": "Layout",
            "questions": [
                "What is the overall layout type? (sidebar + main, single column, grid, dashboard)",
                "Is there a header/navbar at the top?",
                "Is there a footer at the bottom?",
                "Is there a sidebar? If yes, left or right side?",
            ],
        },
        {
            "category": "Components",
            "questions": [
                "What UI components do you see? (cards, tables, forms, buttons, modals, navigation)",
                "Are there any data visualizations? (charts, graphs, progress bars, gauges)",
                "What navigation pattern is used? (top nav, sidebar nav, tabs, breadcrumbs, bottom nav)",
                "Are there any interactive elements? (dropdowns, toggles, sliders, search bars)",
            ],
        },
        {
            "category": "Colors",
            "questions": [
                "Is this primarily light mode or dark mode?",
                "What are the main colors you see? (background, text, accent, borders)",
                "Are there any gradient or shadow effects?",
                "Is there a brand color that stands out?",
            ],
        },
        {
            "category": "Typography",
            "questions": [
                "Are headings serif or sans-serif?",
                "Is body text small, medium, or large?",
                "Is there any monospace text? (code blocks, data displays)",
                "Are there different font weights? (bold, semibold, regular, light)",
            ],
        },
        {
            "category": "Style",
            "questions": [
                "What is the overall style? (minimal, modern, corporate, playful, luxurious)",
                "What border style do you see? (sharp corners, rounded, pill-shaped)",
                "Is the spacing compact, normal, or spacious?",
                "Are there any special visual effects? (glassmorphism, neon, gradients, animations)",
            ],
        },
    ]


def analyze(
    image_path: str,
    num_colors: int = 6,
    use_gemini: bool = False,
    guided: bool = False,
    verbose: bool = False,
) -> dict:
    result = {
        "meta": {
            "source": str(Path(image_path).name),
            "analyzed_at": datetime.now().isoformat(),
            "analysis_layers": [],
            "dependencies": check_dependencies(),
        },
        "image": {},
        "colors": {},
        "layout": {},
        "components": [],
        "typography": {},
        "page_type": {},
        "tech_stack": {},
        "design_tokens": {},
        "gemini_analysis": None,
        "guided_questions": None,
    }

    try:
        from PIL import Image

        img = Image.open(image_path)
        result["image"] = {
            "path": str(image_path),
            "width": img.size[0],
            "height": img.size[1],
            "format": img.format,
            "mode": img.mode,
        }
        img.close()
    except Exception as e:
        print(f"Error opening image: {e}", file=sys.stderr)
        return result

    aspect = result["image"]["width"] / result["image"]["height"]
    common = [
        (16 / 9, "16:9"),
        (16 / 10, "16:10"),
        (4 / 3, "4:3"),
        (3 / 2, "3:2"),
        (21 / 9, "21:9"),
        (1 / 1, "1:1"),
    ]
    closest = min(common, key=lambda x: abs(x[0] - aspect))
    result["image"]["aspect_ratio"] = closest[1]

    print("Layer 1: Analyzing colors...", file=sys.stderr)
    color_data = extract_from_image(image_path, num_colors)
    result["colors"] = color_data
    result["meta"]["analysis_layers"].append("pillow+kmeans")

    print("Layer 1: Analyzing layout...", file=sys.stderr)
    layout = analyze_layout(image_path)
    result["layout"] = layout.to_dict()
    result["meta"]["analysis_layers"].append("layout-detection")

    print("Layer 1: Detecting components...", file=sys.stderr)
    result["components"] = detect_components(image_path, result["layout"])
    result["meta"]["analysis_layers"].append("component-detection")

    print("Layer 1: Analyzing typography...", file=sys.stderr)
    result["typography"] = detect_typography(image_path)
    result["meta"]["analysis_layers"].append("typography-detection")

    print("Layer 1: Classifying page type...", file=sys.stderr)
    result["page_type"] = classify_page(
        result["components"], result["layout"], result["typography"]
    )
    result["meta"]["analysis_layers"].append("page-classification")

    print("Layer 1: Recommending tech stack...", file=sys.stderr)
    result["tech_stack"] = recommend_tech_stack(
        result["page_type"]["page_type"], result["components"]
    )

    if use_gemini:
        print("Layer 2: Analyzing with Gemini Vision...", file=sys.stderr)
        gemini = analyze_with_gemini(image_path)
        if gemini:
            result["gemini_analysis"] = gemini
            result["meta"]["analysis_layers"].append("gemini-vision")
            if gemini.get("components"):
                result["components"].extend(gemini["components"])
            if gemini.get("typography"):
                result["typography"].update(gemini["typography"])
            if gemini.get("spacing"):
                result["design_tokens"]["spacing"] = gemini["spacing"]
            if gemini.get("border_radius"):
                result["design_tokens"]["border_radius"] = gemini["border_radius"]
        else:
            print("Gemini analysis unavailable", file=sys.stderr)

    if guided:
        print("Layer 3: Generating guided questions...", file=sys.stderr)
        result["guided_questions"] = generate_guided_questions()

    result["design_tokens"]["colors"] = color_data.get("palette", {})

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Analyze UI screenshot and generate design spec",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze.py --image screenshot.png --format md
  python analyze.py --image screenshot.png --format css --output styles.css
  python analyze.py --image screenshot.png --format tailwind --output tailwind.config.js
  python analyze.py --image screenshot.png --format w3c --output tokens.json
  python analyze.py --image screenshot.png --format storybook --output tokens.js
  python analyze.py --image screenshot.png --format figma --output figma-tokens.json
  python analyze.py --image screenshot.png --code react --output Page.tsx
  python analyze.py --image screenshot.png --code vue --output Page.vue
  python analyze.py --image screenshot.png --code html --output page.html
  python analyze.py --image screenshot.png --design-system --output ./design-system/
  python analyze.py --image screenshot.png --gemini --format json
  python analyze.py --image screenshot.png --guided
        """,
    )
    parser.add_argument("--image", required=True, help="Path to image file")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    parser.add_argument(
        "--format",
        "-f",
        choices=[
            "json",
            "md",
            "markdown",
            "css",
            "scss",
            "tailwind",
            "w3c",
            "storybook",
            "figma",
        ],
        default="md",
        help="Output format (default: md)",
    )
    parser.add_argument(
        "--code",
        choices=["react", "vue", "html"],
        help="Generate working code in specified framework",
    )
    parser.add_argument(
        "--component-name",
        default="Page",
        help="Component name for code generation (default: Page)",
    )
    parser.add_argument(
        "--design-system",
        action="store_true",
        help="Generate complete design system (tokens, components, CSS variables, Tailwind config)",
    )
    parser.add_argument(
        "--colors", type=int, default=6, help="Number of dominant colors (default: 6)"
    )
    parser.add_argument(
        "--gemini", action="store_true", help="Enable Gemini Vision analysis"
    )
    parser.add_argument(
        "--guided", action="store_true", help="Generate guided questions for user"
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    if not Path(args.image).exists():
        print(f"Error: Image file not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    deps = check_dependencies()
    if not deps["pillow"]:
        print("Error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
        sys.exit(1)
    if not deps["numpy"]:
        print("Error: numpy not installed. Run: pip install numpy", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing: {args.image}", file=sys.stderr)
    result = analyze(
        image_path=args.image,
        num_colors=args.colors,
        use_gemini=args.gemini,
        guided=args.guided,
        verbose=args.verbose,
    )

    if args.code:
        output = generate_code(result, args.code, args.component_name)
    elif args.design_system:
        ds = generate_design_system(result)
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
            print(f"Design system written to {args.output}", file=sys.stderr)
            return
        else:
            output = json.dumps(ds, indent=2)
    else:
        output = export(
            result,
            args.format,
            args.image,
        )

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Written to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
