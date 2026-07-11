#!/usr/bin/env python3
"""
Project UI/UX scanner for ui-craft.
Scans existing projects for UI/UX health, accessibility, and design consistency.
"""

import json
import os
import re
from pathlib import Path


class UIAudit:
    """Scans a project for UI/UX health metrics."""

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.findings = []
        self.stack = {}
        self.components = []
        self.style_analysis = {}
        self.accessibility_issues = []
        self.responsive_issues = []

    def scan_stack(self) -> dict:
        """Detect framework stack and versions."""
        stack = {}
        pkg_json = self.project_dir / "package.json"
        if pkg_json.exists():
            import json

            try:
                with open(pkg_json, "r", encoding="utf-8") as f:
                    data = json.load(f)
                deps = {
                    **data.get("dependencies", {}),
                    **data.get("devDependencies", {}),
                }
                for key in [
                    "react",
                    "next",
                    "vue",
                    "tailwindcss",
                    "typescript",
                    "shadcn",
                ]:
                    if key in deps:
                        stack[key] = deps[key].lstrip("^~>=<")
            except (json.JSONDecodeError, IOError):
                pass
        return stack

    def scan_components(self) -> list:
        """Scan for UI component files."""
        components = []
        component_dirs = ["src/components", "src/ui", "components", "app/components"]
        for comp_dir in component_dirs:
            dir_path = self.project_dir / comp_dir
            if dir_path.exists():
                for ext in ["*.tsx", "*.jsx", "*.vue", "*.svelte"]:
                    components.extend(
                        [
                            str(f.relative_to(self.project_dir))
                            for f in dir_path.rglob(ext)
                        ]
                    )
        return components

    def scan_colors(self) -> dict:
        """Scan for color usage patterns."""
        findings = {
            "ad_hoc_hex_values": [],
            "css_variables": [],
            "tailwind_colors": [],
            "unique_hex_values": set(),
        }
        hex_pattern = re.compile(r"#[0-9a-fA-F]{3,8}")
        var_pattern = re.compile(r"var\(--[\w-]+\)")
        tailwind_color = re.compile(r"(?:bg|text|border|ring|outline)-\[?#?[a-zA-Z]")

        for ext in ["*.tsx", "*.jsx", "*.ts", "*.js", "*.css", "*.vue", "*.svelte"]:
            for filepath in self.project_dir.rglob(ext):
                try:
                    content = filepath.read_text(encoding="utf-8")
                    hexes = hex_pattern.findall(content)
                    for h in hexes:
                        if h.lower() not in self._get_token_colors():
                            findings["ad_hoc_hex_values"].append(
                                {
                                    "file": str(filepath.relative_to(self.project_dir)),
                                    "hex": h,
                                }
                            )
                except Exception:
                    pass

        return findings

    def _get_token_colors(self) -> set:
        """Get known token colors from design system files."""
        tokens = set()
        token_patterns = ["*.css", "tailwind.config.*", "theme.ts", "tokens.json"]
        for pattern in token_patterns:
            for f in self.project_dir.rglob(pattern):
                try:
                    content = f.read_text(encoding="utf-8")
                    hexes = re.findall(r"#[0-9a-fA-F]{3,8}", content)
                    tokens.update(h.lower() for h in hexes)
                except Exception:
                    pass
        return tokens

    def scan_accessibility(self) -> list:
        """Scan for accessibility issues."""
        issues = []
        for ext in ["*.tsx", "*.jsx", "*.vue", "*.svelte", "*.html"]:
            for filepath in self.project_dir.rglob(ext):
                try:
                    content = filepath.read_text(encoding="utf-8")
                    rel_path = str(filepath.relative_to(self.project_dir))

                    # Check for missing aria labels on interactive elements
                    if re.search(
                        r"<(button|input|a|nav|select|textarea)\b",
                        content,
                        re.IGNORECASE,
                    ):
                        if not re.search(r"aria-label\s*=", content):
                            pass  # Too many false positives, flag only obvious cases

                    # Check for missing focus styles
                    if ":focus" not in content and "focus:" not in content:
                        issues.append(
                            {
                                "type": "ACCESSIBILITY",
                                "severity": "MEDIUM",
                                "file": rel_path,
                                "message": "No focus styles detected",
                            }
                        )

                    # Check for low contrast colors
                    hex_colors = re.findall(r"#[0-9a-fA-F]{6}", content)
                    for hex_color in hex_colors:
                        contrast = self._estimate_contrast(hex_color)
                        if contrast and contrast < 4.5:
                            issues.append(
                                {
                                    "type": "ACCESSIBILITY",
                                    "severity": "HIGH",
                                    "file": rel_path,
                                    "message": f"Low contrast color: {hex_color} (estimated ratio: {contrast:.1f}:1)",
                                }
                            )

                    # Check for missing aria labels
                    if re.search(
                        r"<(button|input|a|select|textarea)\b[^>]*>",
                        content,
                        re.IGNORECASE,
                    ):
                        if not re.search(r"aria-label\s*=", content) and not re.search(
                            r"aria-labelledby\s*=", content
                        ):
                            pass  # Too many false positives, flag only obvious cases

                except Exception:
                    pass

        return issues

    def _estimate_contrast(self, hex_color: str) -> float | None:
        """Estimate contrast ratio for a hex color against white background."""
        try:
            hex_color = hex_color.lstrip("#")
            r, g, b = (
                int(hex_color[0:2], 16),
                int(hex_color[2:4], 16),
                int(hex_color[4:6], 16),
            )
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return (luminance + 0.05) / 0.05  # Simplified ratio against white
        except (ValueError, IndexError):
            return None

    def scan_responsive(self) -> list:
        """Scan for responsive design issues."""
        issues = []
        for ext in ["*.css", "*.tsx", "*.jsx", "*.vue", "*.svelte"]:
            for filepath in self.project_dir.rglob(ext):
                try:
                    content = filepath.read_text(encoding="utf-8")
                    rel_path = str(filepath.relative_to(self.project_dir))

                    # Check for viewport meta tag in HTML
                    if filepath.suffix in [".html", ".htm"]:
                        if '<meta name="viewport"' not in content:
                            issues.append(
                                {
                                    "type": "RESPONSIVE",
                                    "severity": "HIGH",
                                    "file": rel_path,
                                    "message": "Missing viewport meta tag",
                                }
                            )

                    # Check for breakpoints
                    if "tailwind.config" in str(filepath):
                        if "screens" not in content and "breakpoints" not in content:
                            issues.append(
                                {
                                    "type": "RESPONSIVE",
                                    "severity": "MEDIUM",
                                    "file": rel_path,
                                    "message": "No custom breakpoints defined in Tailwind config",
                                }
                            )

                except Exception:
                    pass
        return issues

    def scan_dark_mode(self) -> dict:
        """Check for dark mode support."""
        result = {"supported": False, "files": []}
        for ext in ["*.css", "*.tsx", "*.jsx", "*.vue", "*.svelte"]:
            for filepath in self.project_dir.rglob(ext):
                try:
                    content = filepath.read_text(encoding="utf-8")
                    if (
                        ".dark" in content
                        or "dark:" in content
                        or "prefers-color-scheme: dark" in content
                    ):
                        result["supported"] = True
                        result["files"].append(
                            str(filepath.relative_to(self.project_dir))
                        )
                except Exception:
                    pass
        return result

    def scan_design_tokens(self) -> dict:
        """Check for design token usage."""
        result = {
            "css_variables": False,
            "tailwind_config": False,
            "theme_file": False,
            "ad_hoc_colors": [],
        }
        hex_pattern = re.compile(r"#[0-9a-fA-F]{6}\b")

        # Check for CSS variables
        for ext in ["*.css", "*.scss", "*.pcss"]:
            for filepath in self.project_dir.rglob(ext):
                try:
                    content = filepath.read_text(encoding="utf-8")
                    if (
                        "--color-" in content
                        or "--space-" in content
                        or "--font-" in content
                    ):
                        result["css_variables"] = True
                except Exception:
                    pass

        # Check for Tailwind config
        for pattern in ["tailwind.config.*", "tailwind.config.*"]:
            if list(self.project_dir.rglob(pattern)):
                result["tailwind_config"] = True
                break

        # Check for theme file
        for pattern in ["theme.ts", "theme.js", "tokens.css", "tokens.json"]:
            if list(self.project_dir.rglob(pattern)):
                result["theme_file"] = True
                break

        return result

    def generate_report(self) -> dict:
        """Generate complete UI/UX health report."""
        return {
            "stack": self.scan_stack(),
            "components": self.scan_components(),
            "style": self.scan_colors(),
            "accessibility": self.scan_accessibility(),
            "responsive": self.scan_responsive(),
            "dark_mode": self.scan_dark_mode(),
            "design_tokens": self.scan_design_tokens(),
        }

    def format_report(self, report: dict) -> str:
        """Format the audit report for display."""
        lines = []
        lines.append("=" * 60)
        lines.append("UI/UX HEALTH REPORT")
        lines.append("=" * 60)
        lines.append("")

        # Stack
        lines.append("STACK:")
        for key, value in report.get("stack", {}).items():
            lines.append(f"  - {key}: {value}")
        lines.append("")

        # Components
        components = report.get("components", [])
        lines.append(f"COMPONENTS: {len(components)} found")
        if components:
            for comp in components[:10]:
                lines.append(f"  - {comp}")
            if len(components) > 10:
                lines.append(f"  ... and {len(components) - 10} more")
        lines.append("")

        # Style findings
        style = report.get("style", {})
        if style.get("ad_hoc_hex_values"):
            lines.append(
                f"STYLE: {len(style['ad_hoc_hex_values'])} ad-hoc hex values found"
            )
            for item in style["ad_hoc_hex_values"][:5]:
                lines.append(f"  - {item['hex']} in {item['file']}")
            lines.append("")

        # Accessibility findings
        a11y = report.get("accessibility", [])
        if a11y:
            lines.append(f"ACCESSIBILITY: {len(a11y)} issues found")
            for issue in a11y[:5]:
                lines.append(
                    f"  [{issue['severity']}] {issue['message']} ({issue['file']})"
                )
            lines.append("")

        # Responsive findings
        responsive = report.get("responsive", [])
        if responsive:
            lines.append(f"RESPONSIVE: {len(responsive)} issues found")
            for issue in responsive[:5]:
                lines.append(
                    f"  [{issue['severity']}] {issue['message']} ({issue['file']})"
                )
            lines.append("")

        # Dark mode
        dark_mode = report.get("dark_mode", {})
        if dark_mode.get("supported"):
            lines.append("DARK MODE: Supported")
        else:
            lines.append("DARK MODE: Not detected")
        lines.append("")

        # Design tokens
        tokens = report.get("design_tokens", {})
        if tokens.get("css_variables"):
            lines.append("DESIGN TOKENS: CSS variables detected")
        if tokens.get("tailwind_config"):
            lines.append("DESIGN TOKENS: Tailwind config detected")
        if tokens.get("theme_file"):
            lines.append("DESIGN TOKENS: Theme file detected")

        return "\n".join(lines)
