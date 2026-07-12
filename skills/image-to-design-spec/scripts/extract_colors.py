#!/usr/bin/env python3
"""
Color Extraction Module
K-means clustering + Pillow for dominant color extraction from images.

Inspired by: huebrew (median-cut), colorthief, img2ui (K-means), chromaspec
Output: hex colors with area percentages, semantic slot assignments
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
import json
import math

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("Error: numpy not installed. Run: pip install numpy", file=sys.stderr)
    sys.exit(1)


@dataclass
class Color:
    r: int
    g: int
    b: int
    area_percent: float = 0.0
    hex: str = ""
    hsl: dict = field(default_factory=dict)
    semantic_role: str = ""
    text_color: str = ""
    wcag_contrast_light: float = 0.0
    wcag_contrast_dark: float = 0.0

    def __post_init__(self):
        self.hex = f"#{self.r:02x}{self.g:02x}{self.b:02x}"
        self.hsl = rgb_to_hsl(self.r, self.g, self.b)
        self.text_color = best_text_color(self.r, self.g, self.b)
        self.wcag_contrast_light = contrast_ratio(self.r, self.g, self.b, 255, 255, 255)
        self.wcag_contrast_dark = contrast_ratio(self.r, self.g, self.b, 0, 0, 0)

    def to_dict(self):
        return {
            "hex": self.hex,
            "rgb": {"r": self.r, "g": self.g, "b": self.b},
            "hsl": self.hsl,
            "area_percent": round(self.area_percent, 1),
            "text_color": self.text_color,
            "wcag_contrast_light": round(self.wcag_contrast_light, 2),
            "wcag_contrast_dark": round(self.wcag_contrast_dark, 2),
            "semantic_role": self.semantic_role,
        }


def rgb_to_hsl(r: int, g: int, b: int) -> dict:
    rn, gn, bn = r / 255.0, g / 255.0, b / 255.0
    mx, mn = max(rn, gn, bn), min(rn, gn, bn)
    l = (mx + mn) / 2.0

    if mx == mn:
        h = s = 0.0
    else:
        d = mx - mn
        s = d / (2.0 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == rn:
            h = (gn - bn) / d + (6 if gn < bn else 0)
        elif mx == gn:
            h = (bn - rn) / d + 2
        else:
            h = (rn - gn) / d + 4
        h /= 6.0

    return {"h": round(h * 360), "s": round(s * 100), "l": round(l * 100)}


def relative_luminance(r: int, g: int, b: int) -> float:
    rs, gs, bs = r / 255.0, g / 255.0, b / 255.0
    rl = rs / 12.92 if rs <= 0.04045 else ((rs + 0.055) / 1.055) ** 2.4
    gl = gs / 12.92 if gs <= 0.04045 else ((gs + 0.055) / 1.055) ** 2.4
    bl = bs / 12.92 if bs <= 0.04045 else ((bs + 0.055) / 1.055) ** 2.4
    return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl


def contrast_ratio(r1: int, g1: int, b1: int, r2: int, g2: int, b2: int) -> float:
    l1 = relative_luminance(r1, g1, b1)
    l2 = relative_luminance(r2, g2, b2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def best_text_color(r: int, g: int, b: int) -> str:
    return "#ffffff" if relative_luminance(r, g, b) < 0.179 else "#000000"


def color_distance(c1: tuple, c2: tuple) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def kmeans_colors(pixels: np.ndarray, k: int = 6, max_iter: int = 50) -> list:
    np.random.seed(42)
    n = pixels.shape[0]
    indices = np.random.choice(n, k, replace=False)
    centroids = pixels[indices].astype(float)

    for _ in range(max_iter):
        dists = np.sqrt(
            ((pixels[:, np.newaxis].astype(float) - centroids[np.newaxis, :]) ** 2).sum(
                axis=2
            )
        )
        labels = dists.argmin(axis=1)

        new_centroids = np.array(
            [
                pixels[labels == i].mean(axis=0)
                if (labels == i).any()
                else centroids[i]
                for i in range(k)
            ]
        )

        if np.allclose(centroids, new_centroids, atol=1.0):
            break
        centroids = new_centroids

    counts = np.bincount(labels, minlength=k)
    total = counts.sum()
    results = []
    for i in range(k):
        r, g, b = int(centroids[i][0]), int(centroids[i][1]), int(centroids[i][2])
        area = (counts[i] / total) * 100
        results.append((r, g, b, area))

    results.sort(key=lambda x: x[3], reverse=True)
    return results


def assign_semantic_roles(colors: list) -> list:
    if not colors:
        return colors

    sorted_by_luminance = sorted(
        colors, key=lambda c: relative_luminance(c.r, c.g, c.b)
    )

    sorted_by_area = sorted(colors, key=lambda c: c.area_percent, reverse=True)

    for c in colors:
        lum = relative_luminance(c.r, c.g, c.b)
        sat = c.hsl["s"]

        if lum < 0.08:
            c.semantic_role = "text-primary"
        elif lum < 0.15 and sat < 20:
            c.semantic_role = "text-secondary"
        elif lum > 0.92 and sat < 10:
            c.semantic_role = "surface"
        elif lum > 0.85 and sat < 15:
            c.semantic_role = "background"
        elif sat < 20 and 0.5 < lum < 0.8:
            c.semantic_role = "neutral"
        elif 0.15 < lum < 0.25:
            c.semantic_role = "secondary"

    assigned = [c.semantic_role for c in colors if c.semantic_role]

    for c in sorted_by_area:
        if c.semantic_role == "" and c.hsl["s"] > 25:
            if "primary" not in assigned:
                c.semantic_role = "primary"
                assigned.append("primary")
            elif "accent" not in assigned:
                c.semantic_role = "accent"
                assigned.append("accent")
            break

    for c in sorted_by_area:
        if c.semantic_role == "" and c.hsl["s"] > 20:
            if "accent" not in assigned:
                c.semantic_role = "accent"
                assigned.append("accent")
                break

    if "background" not in assigned:
        for c in sorted_by_area:
            if c.area_percent > 15 and relative_luminance(c.r, c.g, c.b) > 0.8:
                c.semantic_role = "background"
                assigned.append("background")
                break

    if "surface" not in assigned:
        for c in sorted_by_area:
            if (
                c.area_percent > 5
                and c.area_percent < 25
                and relative_luminance(c.r, c.g, c.b) > 0.9
            ):
                c.semantic_role = "surface"
                assigned.append("surface")
                break

    return colors


def extract_colors(
    image_path: str,
    num_colors: int = 6,
    max_pixels: int = 100000,
) -> list:
    img = Image.open(image_path).convert("RGB")
    orig_w, orig_h = img.size

    pixels = np.array(img).reshape(-1, 3)

    if len(pixels) > max_pixels:
        indices = np.random.choice(len(pixels), max_pixels, replace=False)
        pixels = pixels[indices]

    raw = kmeans_colors(pixels, k=num_colors)
    colors = []
    for r, g, b, area in raw:
        c = Color(r=r, g=g, b=b, area_percent=area)
        colors.append(c)

    colors = assign_semantic_roles(colors)
    return colors


def detect_mode(colors: list) -> str:
    dark_pixels = 0
    light_pixels = 0
    for c in colors:
        lum = relative_luminance(c.r, c.g, c.b)
        weight = c.area_percent / 100.0
        if lum < 0.179:
            dark_pixels += weight
        else:
            light_pixels += weight
    return "dark" if dark_pixels > light_pixels else "light"


def build_palette(colors: list) -> dict:
    palette = {}
    for c in colors:
        role = c.semantic_role or "neutral"
        if role not in palette:
            palette[role] = c.hex
    return palette


def extract_from_image(image_path: str, num_colors: int = 6) -> dict:
    colors = extract_colors(image_path, num_colors=num_colors)
    mode = detect_mode(colors)
    palette = build_palette(colors)

    return {
        "dominant": [c.hex for c in colors],
        "palette": palette,
        "mode": mode,
        "colors": [c.to_dict() for c in colors],
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract dominant colors from an image"
    )
    parser.add_argument("--image", required=True, help="Path to image")
    parser.add_argument("--colors", type=int, default=6, help="Number of colors")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    result = extract_from_image(args.image, args.colors)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Mode: {result['mode']}")
        print(f"Dominant colors:")
        for i, c in enumerate(result["colors"]):
            print(
                f"  {i + 1}. {c['hex']} ({c['area_percent']}%) [{c['semantic_role']}]"
            )
