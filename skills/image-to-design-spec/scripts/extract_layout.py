#!/usr/bin/env python3
"""
Layout Detection Module
Analyzes image structure to detect UI layout patterns.

Uses edge detection and region analysis to identify:
- Layout type (sidebar-main, single-column, grid, dashboard)
- Header/footer/sidebar presence
- Content regions and density
- Typography hints (serif vs sans-serif based on edge patterns)

Uses industry-standard numbers from globals companies (Tailwind, Material, Apple)
"""

import sys
import math
from pathlib import Path
from dataclasses import dataclass, field
import json

try:
    from PIL import Image, ImageFilter, ImageStat
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("Error: numpy not installed. Run: pip install numpy", file=sys.stderr)
    sys.exit(1)

from standards import (
    SIDEBAR_WIDTHS,
    HEADER_HEIGHTS,
    MAX_CONTENT_WIDTHS,
    BREAKPOINTS,
    snap_to_border_radius,
    snap_to_sidebar_width,
)


@dataclass
class LayoutRegion:
    name: str
    x_start: float
    y_start: float
    x_end: float
    y_end: float
    width_percent: float
    height_percent: float
    density: float = 0.0
    confidence: float = 0.8


@dataclass
class LayoutAnalysis:
    width: int
    height: int
    aspect_ratio: str
    layout_type: str
    has_header: bool
    has_footer: bool
    has_sidebar: bool
    sidebar_position: str
    sidebar_width_percent: float
    max_content_width: int
    regions: list
    density: float
    estimated_grid_columns: int
    spacing_hint: str
    responsive_breakpoints: dict
    complexity_score: float
    has_gradient: bool = False
    gradient_direction: str = ""
    has_shadow: bool = False
    shadow_intensity: str = ""
    estimated_border_radius: int = 0
    detected_shapes: list = None
    background_type: str = ""
    has_glass_effect: bool = False

    def __post_init__(self):
        if self.detected_shapes is None:
            self.detected_shapes = []

    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "aspect_ratio": self.aspect_ratio,
            "layout_type": self.layout_type,
            "has_header": self.has_header,
            "has_footer": self.has_footer,
            "has_sidebar": self.has_sidebar,
            "sidebar_position": self.sidebar_position,
            "sidebar_width_percent": self.sidebar_width_percent,
            "max_content_width": self.max_content_width,
            "regions": [
                {
                    "name": r.name,
                    "x_start": r.x_start,
                    "y_start": r.y_start,
                    "x_end": r.x_end,
                    "y_end": r.y_end,
                    "width_percent": r.width_percent,
                    "height_percent": r.height_percent,
                    "density": round(r.density, 2),
                    "confidence": round(r.confidence, 2),
                }
                for r in self.regions
            ],
            "density": round(self.density, 2),
            "estimated_grid_columns": self.estimated_grid_columns,
            "spacing_hint": self.spacing_hint,
            "responsive_breakpoints": self.responsive_breakpoints,
            "complexity_score": round(self.complexity_score, 2),
            "has_gradient": self.has_gradient,
            "gradient_direction": self.gradient_direction,
            "has_shadow": self.has_shadow,
            "shadow_intensity": self.shadow_intensity,
            "estimated_border_radius": self.estimated_border_radius,
            "detected_shapes": self.detected_shapes,
            "background_type": self.background_type,
            "has_glass_effect": self.has_glass_effect,
        }


def compute_edge_density(img: Image.Image) -> np.ndarray:
    gray = img.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    arr = np.array(edges, dtype=float)
    return arr


def region_density(arr: np.ndarray, y1: int, y2: int, x1: int, x2: int) -> float:
    if y2 <= y1 or x2 <= x1:
        return 0.0
    region = arr[y1:y2, x1:x2]
    return float(region.mean()) / 255.0


def detect_header_footer(edges: np.ndarray, h: int, w: int) -> tuple:
    header_height = max(1, int(h * 0.08))
    footer_start = max(0, h - int(h * 0.06))

    header_region = edges[:header_height, :]
    footer_region = edges[footer_start:, :]

    header_density = float(header_region.mean()) / 255.0
    footer_density = float(footer_region.mean()) / 255.0

    threshold = 0.03
    return header_density > threshold, footer_density > threshold


def detect_sidebar(edges: np.ndarray, h: int, w: int) -> tuple:
    left_width = max(1, int(w * 0.35))
    right_start = max(0, w - int(w * 0.35))

    left_region = edges[:, :left_width]
    right_region = edges[:, right_start:]

    left_density = float(left_region.mean()) / 255.0
    right_density = float(right_region.mean()) / 255.0

    threshold = 0.04
    min_sidebar_width = int(w * 0.08)

    if left_density > threshold and left_density > right_density * 1.2:
        smooth_width = 10
        col_densities = []
        for col in range(left_width):
            col_density = float(edges[:, col].mean()) / 255.0
            col_densities.append(col_density)

        sidebar_w = 0
        for i in range(len(col_densities) - smooth_width):
            window_avg = sum(col_densities[i : i + smooth_width]) / smooth_width
            if window_avg < threshold * 0.6:
                sidebar_w = i + smooth_width // 2
                break

        if sidebar_w < min_sidebar_width:
            sidebar_w = int(w * 0.18)

        sidebar_w = min(sidebar_w, int(w * 0.3))

        standard_width = snap_to_sidebar_width((sidebar_w / w) * 100, w)
        standard_percent = (standard_width / w) * 100

        return True, "left", round(standard_percent, 1)

    if right_density > threshold and right_density > left_density * 1.2:
        smooth_width = 10
        col_densities = []
        for col in range(w - 1, right_start, -1):
            col_density = float(edges[:, col].mean()) / 255.0
            col_densities.append(col_density)

        sidebar_w = 0
        for i in range(len(col_densities) - smooth_width):
            window_avg = sum(col_densities[i : i + smooth_width]) / smooth_width
            if window_avg < threshold * 0.6:
                sidebar_w = i + smooth_width // 2
                break

        if sidebar_w < min_sidebar_width:
            sidebar_w = int(w * 0.18)

        sidebar_w = min(sidebar_w, int(w * 0.3))

        standard_width = snap_to_sidebar_width((sidebar_w / w) * 100, w)
        standard_percent = (standard_width / w) * 100

        return True, "right", round(standard_percent, 1)

    return False, "none", 0.0


def estimate_grid_columns(edges: np.ndarray, h: int, w: int, has_sidebar: bool) -> int:
    if has_sidebar:
        main_start = int(w * 0.25)
        main_edges = edges[:, main_start:]
    else:
        main_edges = edges

    col_profile = main_edges.mean(axis=0)
    threshold = col_profile.mean() * 1.3

    peaks = []
    in_peak = False
    peak_start = 0
    for i, val in enumerate(col_profile):
        if val > threshold and not in_peak:
            in_peak = True
            peak_start = i
        elif val <= threshold and in_peak:
            in_peak = False
            peaks.append((peak_start, i))

    if len(peaks) >= 5:
        return 4
    elif len(peaks) >= 3:
        return 3
    elif len(peaks) >= 1:
        return 2
    else:
        return 1


def estimate_density(img: Image.Image) -> tuple:
    small = img.resize((100, 100), Image.LANCZOS)
    arr = np.array(small, dtype=float)
    unique_colors = len(np.unique(arr.reshape(-1, 3), axis=0))
    normalized = min(1.0, unique_colors / 2000.0)

    if normalized < 0.1:
        return normalized, "minimal"
    elif normalized < 0.3:
        return normalized, "normal"
    elif normalized < 0.6:
        return normalized, "dense"
    else:
        return normalized, "very-dense"


def estimate_spacing(edges: np.ndarray, h: int, w: int) -> str:
    gray_center = edges[h // 4 : 3 * h // 4, w // 4 : 3 * w // 4]
    profile = gray_center.mean(axis=0)

    smooth_count = 0
    total = len(profile)
    for i in range(1, total - 1):
        if profile[i] < profile[i - 1] * 0.7 and profile[i] < profile[i + 1] * 0.7:
            smooth_count += 1

    ratio = smooth_count / max(total, 1)
    if ratio < 0.05:
        return "tight"
    elif ratio < 0.15:
        return "normal"
    else:
        return "spacious"


def detect_aspect_ratio(w: int, h: int) -> str:
    ratio = w / h
    common = [
        (16 / 9, "16:9"),
        (16 / 10, "16:10"),
        (4 / 3, "4:3"),
        (3 / 2, "3:2"),
        (21 / 9, "21:9"),
        (1 / 1, "1:1"),
    ]
    closest = min(common, key=lambda x: abs(x[0] - ratio))
    return closest[1]


def compute_responsive_breakpoints(w: int) -> dict:
    return {
        "sm": BREAKPOINTS["sm"],
        "md": BREAKPOINTS["md"],
        "lg": BREAKPOINTS["lg"],
        "xl": BREAKPOINTS["xl"],
        "2xl": BREAKPOINTS["2xl"],
    }


def detect_gradient(img: Image.Image) -> tuple:
    small = img.resize((100, 100), Image.LANCZOS)
    arr = np.array(small, dtype=float)

    top_half = arr[:50, :, :].mean()
    bottom_half = arr[50:, :, :].mean()
    left_half = arr[:, :50, :].mean()
    right_half = arr[:, 50:, :].mean()

    vertical_diff = abs(top_half - bottom_half) / 255.0
    horizontal_diff = abs(left_half - right_half) / 255.0

    threshold = 0.03

    if vertical_diff > threshold and vertical_diff > horizontal_diff:
        direction = "vertical" if top_half < bottom_half else "vertical-reversed"
        return True, direction
    elif horizontal_diff > threshold:
        direction = "horizontal" if left_half < right_half else "horizontal-reversed"
        return True, direction

    diag_tl = arr[:50, :50, :].mean()
    diag_br = arr[50:, 50:, :].mean()
    diag_tr = arr[:50, 50:, :].mean()
    diag_bl = arr[50:, :50, :].mean()

    diag1_diff = abs(diag_tl - diag_br) / 255.0
    diag2_diff = abs(diag_tr - diag_bl) / 255.0

    if diag1_diff > threshold and diag1_diff > diag2_diff:
        direction = "diagonal" if diag_tl < diag_br else "diagonal-reversed"
        return True, direction
    elif diag2_diff > threshold:
        direction = "diagonal" if diag_tr < diag_bl else "diagonal-reversed"
        return True, direction

    center = arr[30:70, 30:70, :].mean()
    edges_avg = (
        arr[:20, :, :].mean()
        + arr[80:, :, :].mean()
        + arr[:, :20, :].mean()
        + arr[:, 80:, :].mean()
    ) / 4
    radial_diff = abs(center - edges_avg) / 255.0

    if radial_diff > threshold:
        return True, "radial"

    return False, ""


def detect_shadow(img: Image.Image) -> tuple:
    small = img.resize((200, 200), Image.LANCZOS)
    gray = small.convert("L")
    arr = np.array(gray, dtype=float)

    center_region = arr[60:140, 60:140]
    bottom_edge = arr[140:160, 60:140]
    right_edge = arr[60:140, 140:160]

    center_mean = center_region.mean()
    bottom_mean = bottom_edge.mean()
    right_mean = right_edge.mean()

    bottom_diff = (center_mean - bottom_mean) / 255.0
    right_diff = (center_mean - right_mean) / 255.0

    if bottom_diff > 0.02 or right_diff > 0.02:
        intensity = "light"
        if bottom_diff > 0.05 or right_diff > 0.05:
            intensity = "medium"
        if bottom_diff > 0.1 or right_diff > 0.1:
            intensity = "heavy"
        return True, intensity

    return False, ""


def estimate_border_radius(img: Image.Image) -> int:
    small = img.resize((400, 400), Image.LANCZOS)
    gray = small.convert("L")
    arr = np.array(gray, dtype=float)

    corners = [
        (0, 0, 100, 100),
        (0, 300, 100, 400),
        (300, 0, 400, 100),
        (300, 300, 400, 400),
    ]

    radius_scores = []
    for y1, x1, y2, x2 in corners:
        corner_region = arr[y1:y2, x1:x2]
        corner_value = corner_region[0, 0]
        bg_value = corner_region[-1, -1]

        radius = 0
        max_r = min(50, (y2 - y1) // 2, (x2 - x1) // 2)
        for r in range(max_r):
            edge_val = corner_region[r, r]
            if abs(edge_val - bg_value) > abs(corner_value - bg_value) * 0.3:
                radius = r
                break
        radius_scores.append(radius)

    center_region = arr[150:250, 100:300]
    h, w = center_region.shape
    button_candidates = []

    for row in range(h):
        for col in range(w - 50):
            segment = center_region[row, col : col + 50]
            if segment.std() > 30 and len(np.unique(segment > 128)) > 1:
                button_candidates.append((row, col))

    if button_candidates:
        btn_rows = [r for r, c in button_candidates]
        btn_cols = [c for r, c in button_candidates]
        btn_h = max(btn_rows) - min(btn_rows) if btn_rows else 0
        btn_w = max(btn_cols) - min(btn_cols) if btn_cols else 0

        if btn_w > btn_h * 1.5:
            radius_scores.append(30)

    avg_radius = sum(radius_scores) / len(radius_scores) if radius_scores else 0

    return snap_to_border_radius(int(avg_radius))


def detect_photo_background(img: Image.Image) -> tuple:
    small = img.resize((100, 100), Image.LANCZOS)
    arr = np.array(small, dtype=float)

    unique_colors = len(np.unique(arr.reshape(-1, 3).astype(int), axis=0))
    color_variance = np.std(arr.reshape(-1, 3), axis=0).mean()

    h, w = arr.shape[:2]
    top_quarter = arr[: h // 4, :, :].mean()
    bottom_quarter = arr[3 * h // 4 :, :, :].mean()
    variation = abs(top_quarter - bottom_quarter) / 255.0

    edge = small.convert("L").filter(ImageFilter.FIND_EDGES)
    edge_arr = np.array(edge, dtype=float)
    edge_density = edge_arr.mean() / 255.0

    if unique_colors > 300 and color_variance > 30:
        if edge_density > 0.05:
            return True, "photo"
        else:
            return True, "gradient"
    elif unique_colors > 150 and variation > 0.08:
        return True, "gradient-photo"

    return False, "solid"


def detect_glass_effect(img: Image.Image) -> bool:
    small = img.resize((200, 200), Image.LANCZOS)
    arr = np.array(small, dtype=float)

    center_region = arr[80:120, 60:140]
    surrounding = np.concatenate(
        [
            arr[60:80, 60:140].reshape(-1, 3),
            arr[120:140, 60:140].reshape(-1, 3),
        ],
        axis=0,
    )

    center_alpha = np.mean(
        center_region[:, :, :3] if arr.shape[2] >= 3 else center_region
    )
    surround_alpha = np.mean(
        surrounding[:, :3] if surrounding.shape[1] >= 3 else surrounding
    )

    center_color_variance = np.std(
        center_region[:, :, :3] if arr.shape[2] >= 3 else center_region
    )
    surround_color_variance = np.std(
        surrounding[:, :3] if surrounding.shape[1] >= 3 else surrounding
    )

    if center_color_variance < surround_color_variance * 0.5:
        return True

    edge = small.convert("L").filter(ImageFilter.FIND_EDGES)
    edge_arr = np.array(edge, dtype=float)
    center_edges = edge_arr[80:120, 60:140].mean()
    surround_edges = np.mean(
        [edge_arr[60:80, 60:140].mean(), edge_arr[120:140, 60:140].mean()]
    )

    if center_edges < surround_edges * 0.7:
        return True

    return False


def detect_centered_card(img: Image.Image) -> tuple:
    small = img.resize((200, 200), Image.LANCZOS)
    gray = small.convert("L")
    arr = np.array(gray, dtype=float)

    center = arr[60:140, 40:160]
    border_top = arr[50:60, 40:160]
    border_bottom = arr[140:150, 40:160]
    border_left = arr[60:140, 30:40]
    border_right = arr[60:140, 160:170]

    center_mean = center.mean()
    border_means = [
        border_top.mean(),
        border_bottom.mean(),
        border_left.mean(),
        border_right.mean(),
    ]
    avg_border = sum(border_means) / len(border_means)

    contrast = abs(center_mean - avg_border) / 255.0

    if contrast > 0.05:
        center_color = arr[100, 100]
        is_lighter = center_mean > avg_border

        if center_color > 200 and is_lighter:
            return True, "light-card-on-dark"
        elif center_color < 100 and not is_lighter:
            return True, "dark-card-on-light"

        return True, "card"

    return False, ""


def detect_shapes(img: Image.Image) -> list:
    small = img.resize((200, 200), Image.LANCZOS)
    gray = small.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    arr = np.array(edges, dtype=float)

    shapes = []

    h, w = arr.shape
    quadrants = [
        (0, h // 2, 0, w // 2),
        (0, h // 2, w // 2, w),
        (h // 2, h, 0, w // 2),
        (h // 2, h, w // 2, w),
    ]

    for i, (y1, y2, x1, x2) in enumerate(quadrants):
        region = arr[y1:y2, x1:x2]
        edge_density = region.mean() / 255.0

        if edge_density > 0.05:
            positions = ["top-left", "top-right", "bottom-left", "bottom-right"]
            shapes.append(
                {
                    "type": "region",
                    "position": positions[i],
                    "edge_density": round(edge_density, 3),
                }
            )

    return shapes


def analyze_layout(image_path: str) -> LayoutAnalysis:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    small = img.resize((min(w, 400), min(h, 400)), Image.LANCZOS)
    edges = compute_edge_density(small)
    sh, sw = edges.shape

    has_header, has_footer = detect_header_footer(edges, sh, sw)
    has_sidebar, sidebar_pos, sidebar_pct = detect_sidebar(edges, sh, sw)
    grid_cols = estimate_grid_columns(edges, sh, sw, has_sidebar)
    density_val, density_label = estimate_density(img)
    spacing = estimate_spacing(edges, sh, sw)
    aspect = detect_aspect_ratio(w, h)
    breakpoints = compute_responsive_breakpoints(w)

    has_gradient, gradient_dir = detect_gradient(img)
    has_shadow, shadow_intensity = detect_shadow(img)
    border_radius = estimate_border_radius(img)
    is_centered_card, card_type = detect_centered_card(img)
    shapes = detect_shapes(img)
    bg_type, bg_detail = detect_photo_background(img)
    has_glass = detect_glass_effect(img)

    regions = []
    if has_header:
        header_h = int(sh * 0.08) / sh
        regions.append(
            LayoutRegion(
                name="header",
                x_start=0,
                y_start=0,
                x_end=1.0,
                y_end=header_h,
                width_percent=100.0,
                height_percent=round(header_h * 100, 1),
                density=region_density(edges, 0, int(sh * 0.08), 0, sw),
            )
        )
    if has_sidebar:
        if sidebar_pos == "left":
            sidebar_x = sidebar_pct / 100
            regions.append(
                LayoutRegion(
                    name="sidebar",
                    x_start=0,
                    y_start=0,
                    x_end=sidebar_x,
                    y_end=1.0,
                    width_percent=round(sidebar_pct, 1),
                    height_percent=100.0,
                    density=region_density(edges, 0, sh, 0, int(sw * sidebar_x)),
                )
            )
        else:
            sidebar_x = 1 - sidebar_pct / 100
            regions.append(
                LayoutRegion(
                    name="sidebar",
                    x_start=sidebar_x,
                    y_start=0,
                    x_end=1.0,
                    y_end=1.0,
                    width_percent=round(sidebar_pct, 1),
                    height_percent=100.0,
                    density=region_density(edges, 0, sh, int(sw * sidebar_x), sw),
                )
            )

    if is_centered_card:
        card_w_percent = 50.0
        regions.append(
            LayoutRegion(
                name="card",
                x_start=0.25,
                y_start=0.1,
                x_end=0.75,
                y_end=0.9,
                width_percent=card_w_percent,
                height_percent=80.0,
                density=region_density(
                    edges, int(sh * 0.1), int(sh * 0.9), int(sw * 0.25), int(sw * 0.75)
                ),
                confidence=0.85,
            )
        )
    else:
        main_x_start = (
            (sidebar_pct / 100) if has_sidebar and sidebar_pos == "left" else 0
        )
        main_x_end = (
            (1 - sidebar_pct / 100) if has_sidebar and sidebar_pos == "right" else 1.0
        )
        regions.append(
            LayoutRegion(
                name="main-content",
                x_start=main_x_start,
                y_start=0,
                x_end=main_x_end,
                y_end=1.0,
                width_percent=round((main_x_end - main_x_start) * 100, 1),
                height_percent=100.0,
                density=region_density(
                    edges, 0, sh, int(sw * main_x_start), int(sw * main_x_end)
                ),
            )
        )

    if is_centered_card:
        layout_type = "centered-card"
    elif has_sidebar:
        layout_type = "sidebar-main"
    elif grid_cols >= 3:
        layout_type = "grid"
    elif has_sidebar and has_header and grid_cols >= 2:
        layout_type = "dashboard"
    elif bg_type == "photo":
        layout_type = "hero-fullscreen"
    else:
        layout_type = "single-column"

    complexity = density_val * 0.4 + (grid_cols / 4) * 0.3 + (len(regions) / 5) * 0.3
    if has_gradient:
        complexity += 0.1
    if has_shadow:
        complexity += 0.05
    if bg_type == "photo":
        complexity += 0.1

    return LayoutAnalysis(
        width=w,
        height=h,
        aspect_ratio=aspect,
        layout_type=layout_type,
        has_header=has_header,
        has_footer=has_footer,
        has_sidebar=has_sidebar,
        sidebar_position=sidebar_pos,
        sidebar_width_percent=round(sidebar_pct, 1),
        max_content_width=MAX_CONTENT_WIDTHS["2xl"],
        regions=regions,
        density=round(density_val, 3),
        estimated_grid_columns=grid_cols,
        spacing_hint=spacing,
        responsive_breakpoints=breakpoints,
        complexity_score=round(complexity, 3),
        has_gradient=has_gradient,
        gradient_direction=gradient_dir,
        has_shadow=has_shadow,
        shadow_intensity=shadow_intensity,
        estimated_border_radius=border_radius,
        detected_shapes=shapes,
        background_type=bg_detail,
        has_glass_effect=has_glass,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze UI layout from screenshot")
    parser.add_argument("--image", required=True, help="Path to image")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    result = analyze_layout(args.image)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"Image: {result.width}x{result.height} ({result.aspect_ratio})")
        print(f"Layout: {result.layout_type}")
        print(f"Header: {'yes' if result.has_header else 'no'}")
        print(f"Footer: {'yes' if result.has_footer else 'no'}")
        print(
            f"Sidebar: {'yes' if result.has_sidebar else 'no'} ({result.sidebar_position}, {result.sidebar_width_percent}%)"
        )
        print(f"Grid columns: {result.estimated_grid_columns}")
        print(f"Density: {result.density} ({result.spacing_hint})")
        print(f"Complexity: {result.complexity_score}")
        print(f"Regions:")
        for r in result.regions:
            print(
                f"  - {r.name}: {r.width_percent}%x{r.height_percent}% (density: {r.density:.2f})"
            )
