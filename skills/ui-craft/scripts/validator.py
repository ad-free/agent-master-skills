#!/usr/bin/env python3
"""
Design token validation for ui-craft.
Validates color contrast, token consistency, circular references,
and design system compliance.
"""

import re
from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    """A single validation issue."""

    severity: Severity
    message: str
    path: str = ""
    suggestion: str = ""


@dataclass
class ValidationResult:
    """Aggregated validation result."""

    issues: list[ValidationIssue] = field(default_factory=list)
    passed: bool = True

    def add(self, issue: ValidationIssue) -> None:
        self.issues.append(issue)
        if issue.severity == Severity.ERROR:
            self.passed = False

    def summary(self) -> str:
        errors = sum(1 for i in self.issues if i.severity == Severity.ERROR)
        warnings = sum(1 for i in self.issues if i.severity == Severity.WARNING)
        infos = sum(1 for i in self.issues if i.severity == Severity.INFO)
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {errors} errors, {warnings} warnings, {infos} info"


# ── Color Utilities ──────────────────────────────────────────────────────────

HEX_PATTERN = re.compile(r"^#?([0-9a-fA-F]{3,8})$")
HSL_PATTERN = re.compile(r"hsl\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*\)")
RGB_PATTERN = re.compile(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")


def parse_hex(hex_str: str) -> tuple[int, int, int] | None:
    """Parse hex color to (r, g, b). Returns None if invalid."""
    match = HEX_PATTERN.match(hex_str.strip())
    if not match:
        return None
    h = match.group(1)
    if len(h) == 3:
        h = h[0] * 2 + h[1] * 2 + h[2] * 2
    elif len(h) == 8:
        h = h[:6]
    if len(h) != 6:
        return None
    try:
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        return (r, g, b)
    except ValueError:
        return None


def parse_hsl(hsl_str: str) -> tuple[int, int, int] | None:
    """Parse HSL color to (r, g, b). Returns None if invalid."""
    match = HSL_PATTERN.match(hsl_str.strip())
    if not match:
        return None
    h, s, l = int(match.group(1)), int(match.group(2)), int(match.group(3))
    return hsl_to_rgb(h, s, l)


def parse_rgb(rgb_str: str) -> tuple[int, int, int] | None:
    """Parse RGB color to (r, g, b). Returns None if invalid."""
    match = RGB_PATTERN.match(rgb_str.strip())
    if not match:
        return None
    return (int(match.group(1)), int(match.group(2)), int(match.group(3)))


def parse_color(color: str) -> tuple[int, int, int] | None:
    """Parse any supported color format to (r, g, b)."""
    color = color.strip()
    if color.startswith("#"):
        return parse_hex(color)
    if color.startswith("hsl"):
        return parse_hsl(color)
    if color.startswith("rgb"):
        return parse_rgb(color)
    return parse_hex(color)


def hsl_to_rgb(h: int, s: int, l: int) -> tuple[int, int, int]:
    """Convert HSL to RGB."""

    def hue_to_rgb(p: float, q: float, t: float) -> float:
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    q = l * (1 + s) if l < 0.5 else l - s + (s * l)
    p = 2 * l - q

    r = int(round(hue_to_rgb(p, q, (h + 240) / 360)) * 255)
    g = int(round(hue_to_rgb(p, q, (h + 120) / 360)) * 255)
    b = int(round(hue_to_rgb(p, q, h / 360)) * 255)
    return (r, g, b)


def relative_luminance(r: int, g: int, b: int) -> float:
    """Calculate relative luminance per WCAG 2.1."""

    def linearize(c: int) -> float:
        c_srgb = c / 255.0
        return (
            c_srgb / 12.92 if c_srgb <= 0.04045 else ((c_srgb + 0.055) / 1.055) ** 2.4
        )

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(color1: tuple[int, int, int], color2: tuple[int, int, int]) -> float:
    """Calculate WCAG contrast ratio between two colors."""
    l1 = relative_luminance(*color1)
    l2 = relative_luminance(*color2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def wcag_level(ratio: float) -> str:
    """Return WCAG level for a contrast ratio."""
    if ratio >= 7.0:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3.0:
        return "AA-large"
    return "fail"


# ── Token Validators ─────────────────────────────────────────────────────────


def validate_color_contrast(
    foreground: str,
    background: str,
    min_ratio: float = 4.5,
    label: str = "",
) -> list[ValidationIssue]:
    """Validate contrast ratio between two colors."""
    issues = []
    fg = parse_color(foreground)
    bg = parse_color(background)

    if fg is None:
        issues.append(
            ValidationIssue(
                severity=Severity.ERROR,
                message=f"Invalid foreground color: {foreground}",
                path=label,
                suggestion="Use hex (#RRGGBB), rgb(), or hsl() format",
            )
        )
        return issues
    if bg is None:
        issues.append(
            ValidationIssue(
                severity=Severity.ERROR,
                message=f"Invalid background color: {background}",
                path=label,
                suggestion="Use hex (#RRGGBB), rgb(), or hsl() format",
            )
        )
        return issues

    ratio = contrast_ratio(fg, bg)
    level = wcag_level(ratio)
    label_str = f" ({label})" if label else ""

    if ratio < min_ratio:
        issues.append(
            ValidationIssue(
                severity=Severity.ERROR,
                message=f"Insufficient contrast{label_str}: {ratio:.2f}:1 (need {min_ratio}:1, got {level})",
                suggestion=f"Darken foreground or lighten background to reach {min_ratio}:1 ratio",
            )
        )
    elif ratio < 7.0 and min_ratio < 7.0:
        issues.append(
            ValidationIssue(
                severity=Severity.INFO,
                message=f"Contrast{label_str}: {ratio:.2f}:1 ({level}). Consider AAA (7:1) for better accessibility",
            )
        )

    return issues


def validate_color_format(color: str, label: str = "") -> list[ValidationIssue]:
    """Validate that a color string is in a supported format."""
    issues = []
    parsed = parse_color(color)
    if parsed is None:
        issues.append(
            ValidationIssue(
                severity=Severity.WARNING,
                message=f"Unrecognized color format{f' ({label})' if label else ''}: {color}",
                suggestion="Use hex (#RRGGBB), rgb(r, g, b), or hsl(h, s%, l%)",
            )
        )
    return issues


def validate_hex_length(color: str, label: str = "") -> list[ValidationIssue]:
    """Validate hex color length (#RGB, #RRGGBB, or #RRGGBBAA)."""
    issues = []
    if not color.startswith("#"):
        return issues
    h = color[1:]
    if len(h) not in (3, 6, 8):
        issues.append(
            ValidationIssue(
                severity=Severity.WARNING,
                message=f"Invalid hex length{f' ({label})' if label else ''}: {color}",
                suggestion="Use #RGB, #RRGGBB, or #RRGGBBAA format",
            )
        )
    return issues


def validate_design_tokens(design_system: dict) -> ValidationResult:
    """Validate an entire design system dictionary."""
    result = ValidationResult()
    colors = design_system.get("colors", {})
    typography = design_system.get("typography", {})
    spacing = design_system.get("spacing_scale", {})

    # ── Color validation ─────────────────────────────────────────────
    color_pairs = [
        ("primary", "on_primary", "Primary text on background"),
        ("secondary", "on_secondary", "Secondary text on background"),
        ("background", "foreground", "Body text on background"),
        ("surface", "on_surface", "Surface text"),
        ("error", "on_error", "Error text"),
    ]

    for fg_key, bg_key, label in color_pairs:
        fg_val = colors.get(fg_key, "")
        bg_val = colors.get(bg_key, "")
        if fg_val and bg_val:
            issues = validate_color_contrast(fg_val, bg_val, min_ratio=4.5, label=label)
            for issue in issues:
                result.add(issue)

    # Validate all color formats
    for name, value in colors.items():
        if value:
            issues = validate_color_format(value, label=name)
            for issue in issues:
                result.add(issue)
            issues = validate_hex_length(value, label=name)
            for issue in issues:
                result.add(issue)

    # ── Typography validation ────────────────────────────────────────
    heading = typography.get("heading", "")
    body = typography.get("body", "")
    if heading and not re.match(r"^[A-Za-z\s'\"]+$", heading):
        result.add(
            ValidationIssue(
                severity=Severity.WARNING,
                message=f"Heading font name may be invalid: {heading}",
                path="typography.heading",
                suggestion="Font names should contain only letters, spaces, and quotes",
            )
        )
    if body and not re.match(r"^[A-Za-z\s'\"]+$", body):
        result.add(
            ValidationIssue(
                severity=Severity.WARNING,
                message=f"Body font name may be invalid: {body}",
                path="typography.body",
                suggestion="Font names should contain only letters, spaces, and quotes",
            )
        )

    # ── Spacing scale validation ─────────────────────────────────────
    if spacing:
        values = []
        for k, v in spacing.items():
            try:
                num = float(str(v).replace("px", "").replace("rem", ""))
                values.append((k, num))
            except (ValueError, TypeError):
                result.add(
                    ValidationIssue(
                        severity=Severity.WARNING,
                        message=f"Invalid spacing value: {k} = {v}",
                        path=f"spacing.{k}",
                        suggestion="Use numeric values (px or rem)",
                    )
                )

        if len(values) >= 2:
            sorted_vals = sorted(values, key=lambda x: x[1])
            for i in range(1, len(sorted_vals)):
                prev_name, prev_val = sorted_vals[i - 1]
                curr_name, curr_val = sorted_vals[i]
                if prev_val == curr_val:
                    result.add(
                        ValidationIssue(
                            severity=Severity.WARNING,
                            message=f"Duplicate spacing values: {prev_name} = {curr_name} = {prev_val}",
                            suggestion="Consider unique values for each spacing token",
                        )
                    )

    return result


def validate_token_references(tokens: dict) -> ValidationResult:
    """Check for circular references in token definitions."""
    result = ValidationResult()

    def _resolve(key: str, chain: set[str]) -> str | None:
        if key in chain:
            result.add(
                ValidationIssue(
                    severity=Severity.ERROR,
                    message=f"Circular reference detected: {' -> '.join(chain)} -> {key}",
                    path=key,
                    suggestion="Remove circular dependency in token references",
                )
            )
            return None
        val = tokens.get(key)
        if val is None:
            return None
        if isinstance(val, str) and val.startswith("{") and val.endswith("}"):
            ref = val[1:-1]
            chain.add(key)
            return _resolve(ref, chain)
        return str(val)

    for key in tokens:
        _resolve(key, set())

    return result


def validate_accessibility(design_system: dict) -> ValidationResult:
    """Run full accessibility checks on design system."""
    result = ValidationResult()
    colors = design_system.get("colors", {})

    required_pairs = [
        ("primary", "on_primary"),
        ("background", "foreground"),
        ("surface", "on_surface"),
        ("error", "on_error"),
    ]

    for fg_key, bg_key in required_pairs:
        if fg_key not in colors or bg_key not in colors:
            result.add(
                ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"Missing color pair: {fg_key} / {bg_key}",
                    suggestion=f"Define both {fg_key} and {bg_key} for accessible contrast",
                )
            )

    return result


def validate_spacing_scale(spacing: dict) -> ValidationResult:
    """Validate spacing scale for consistency and uniqueness."""
    result = ValidationResult()
    if not spacing:
        return result

    values = []
    for k, v in spacing.items():
        try:
            num = float(str(v).replace("px", "").replace("rem", ""))
            values.append((k, num))
        except (ValueError, TypeError):
            result.add(
                ValidationIssue(
                    severity=Severity.WARNING,
                    message=f"Non-numeric spacing value: {k} = {v}",
                    path=f"spacing.{k}",
                )
            )

    if len(values) < 4:
        result.add(
            ValidationIssue(
                severity=Severity.INFO,
                message=f"Spacing scale has only {len(values)} steps. Consider 6-10 steps for consistent rhythm",
            )
        )

    return result


def validate_full_design_system(design_system: dict) -> ValidationResult:
    """Run all validators against a complete design system."""
    result = ValidationResult()

    # Color validation
    color_result = validate_design_tokens(design_system)
    result.issues.extend(color_result.issues)
    if not color_result.passed:
        result.passed = False

    # Token references
    flat_tokens = {}
    for section in ["colors", "typography", "spacing_scale"]:
        section_data = design_system.get(section, {})
        if isinstance(section_data, dict):
            for k, v in section_data.items():
                if isinstance(v, str):
                    flat_tokens[f"{section}.{k}"] = v
    if flat_tokens:
        ref_result = validate_token_references(flat_tokens)
        result.issues.extend(ref_result.issues)
        if not ref_result.passed:
            result.passed = False

    # Accessibility
    a11y_result = validate_accessibility(design_system)
    result.issues.extend(a11y_result.issues)

    # Spacing
    spacing_result = validate_spacing_scale(design_system.get("spacing_scale", {}))
    result.issues.extend(spacing_result.issues)

    return result
