#!/usr/bin/env python3
"""
Design Standards Module
Industry-standard numbers used by global companies (Google, Apple, Meta, Tailwind, etc.)

Based on:
- Tailwind CSS defaults
- Material Design 3
- Apple Human Interface Guidelines
- Golden Ratio (1.618)
- Major design systems (Ant Design, Chakra UI, Mantine)
"""

GOLDEN_RATIO = 1.618


FONT_FAMILIES = {
    "sans": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    "serif": "Georgia, 'Times New Roman', Times, serif",
    "mono": "'JetBrains Mono', 'Fira Code', 'SF Mono', 'Cascadia Code', Consolas, monospace",
    "display": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "body": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
}


FONT_STACKS = {
    "system": "-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
    "google": "'Google Sans', 'Product Sans', Roboto, Arial, sans-serif",
    "apple": "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', sans-serif",
    "microsoft": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    "inter": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    "sf": "'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif",
    "roboto": "'Roboto', -apple-system, BlinkMacSystemFont, sans-serif",
    "open-sans": "'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif",
    "noto": "'Noto Sans', -apple-system, BlinkMacSystemFont, sans-serif",
}


SPACING_SCALE = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    8,
    10,
    12,
    16,
    20,
    24,
    32,
    40,
    48,
    56,
    64,
    80,
    96,
    128,
]

SPACING_PX = {
    0: "0px",
    0.5: "2px",
    1: "4px",
    1.5: "6px",
    2: "8px",
    2.5: "10px",
    3: "12px",
    3.5: "14px",
    4: "16px",
    5: "20px",
    6: "24px",
    7: "28px",
    8: "32px",
    9: "36px",
    10: "40px",
    11: "44px",
    12: "48px",
    14: "56px",
    16: "64px",
    20: "80px",
    24: "96px",
    28: "112px",
    32: "128px",
    36: "144px",
    40: "160px",
    44: "176px",
    48: "192px",
    52: "208px",
    56: "224px",
    60: "240px",
    64: "256px",
    72: "288px",
    80: "320px",
    96: "384px",
}


FONT_SIZES = {
    "xs": "0.75rem",
    "sm": "0.875rem",
    "base": "1rem",
    "lg": "1.125rem",
    "xl": "1.25rem",
    "2xl": "1.5rem",
    "3xl": "1.875rem",
    "4xl": "2.25rem",
    "5xl": "3rem",
    "6xl": "3.75rem",
    "7xl": "4.5rem",
    "8xl": "6rem",
    "9xl": "8rem",
}

FONT_SIZE_PX = {
    "xs": 12,
    "sm": 14,
    "base": 16,
    "lg": 18,
    "xl": 20,
    "2xl": 24,
    "3xl": 30,
    "4xl": 36,
    "5xl": 48,
    "6xl": 60,
    "7xl": 72,
    "8xl": 96,
    "9xl": 128,
}


FONT_WEIGHTS = {
    "thin": "100",
    "extralight": "200",
    "light": "300",
    "regular": "400",
    "medium": "500",
    "semibold": "600",
    "bold": "700",
    "extrabold": "800",
    "black": "900",
}


LINE_HEIGHTS = {
    "none": "1",
    "tight": "1.25",
    "snug": "1.375",
    "normal": "1.5",
    "relaxed": "1.625",
    "loose": "2",
}

LETTER_SPACINGS = {
    "tighter": "-0.05em",
    "tight": "-0.025em",
    "normal": "0em",
    "wide": "0.025em",
    "wider": "0.05em",
    "widest": "0.1em",
}


BORDER_RADIUS = [0, 2, 4, 6, 8, 12, 16, 24, 32, 40, 48, 56, 64, 9999]

BORDER_RADIUS_MAP = {
    0: "none",
    2: "sm",
    4: "md",
    6: "lg",
    8: "xl",
    12: "2xl",
    16: "3xl",
    24: "full",
}


BREAKPOINTS = {
    "sm": 640,
    "md": 768,
    "lg": 1024,
    "xl": 1280,
    "2xl": 1536,
}


SIDEBAR_WIDTHS = {
    "compact": 64,
    "narrow": 240,
    "default": 256,
    "medium": 280,
    "wide": 320,
    "extra-wide": 360,
}


MAX_CONTENT_WIDTHS = {
    "sm": 640,
    "md": 768,
    "lg": 1024,
    "xl": 1152,
    "2xl": 1280,
    "3xl": 1536,
    "full": 1920,
}


HEADER_HEIGHTS = {
    "sm": 48,
    "md": 56,
    "default": 64,
    "lg": 72,
    "xl": 80,
}


GOLDEN_RATIO_SPACING = [4, 6, 8, 10, 16, 26, 42, 68, 110, 178]

GOLDEN_RATIO_FONT = [12, 14, 16, 18, 20, 24, 28, 32, 38, 44, 52, 62, 74, 88, 104]


def snap_to_spacing(value: int) -> int:
    """Snap a value to the nearest standard spacing."""
    closest = min(SPACING_SCALE, key=lambda x: abs(x - value))
    return closest


def snap_to_font_size(px: int) -> int:
    """Snap a pixel value to the nearest standard font size."""
    closest = min(FONT_SIZE_PX.values(), key=lambda x: abs(x - px))
    return closest


def snap_to_border_radius(value: int) -> int:
    """Snap a value to the nearest standard border radius."""
    closest = min(BORDER_RADIUS, key=lambda x: abs(x - value))
    return closest


def snap_to_sidebar_width(percent: float, image_width: int) -> int:
    """Snap sidebar percentage to standard width in pixels."""
    px_width = int(image_width * percent / 100)
    closest = min(SIDEBAR_WIDTHS.values(), key=lambda x: abs(x - px_width))
    return closest


def snap_to_max_width(value: int) -> int:
    """Snap to nearest standard max content width."""
    closest = min(MAX_CONTENT_WIDTHS.values(), key=lambda x: abs(x - value))
    return closest


def golden_ratio_scale(base: int = 16, steps: int = 8) -> list:
    """Generate a font size scale using golden ratio."""
    sizes = []
    for i in range(steps):
        size = base * (GOLDEN_RATIO**i)
        snapped = snap_to_font_size(int(size))
        sizes.append(snapped)
    return sizes


def modular_scale(base: int = 16, ratio: float = 1.25, steps: int = 8) -> list:
    """Generate a modular scale for typography."""
    sizes = []
    for i in range(-2, steps - 2):
        size = base * (ratio**i)
        snapped = snap_to_font_size(int(size))
        sizes.append(snapped)
    return sizes
