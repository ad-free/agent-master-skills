#!/usr/bin/env python3
"""
Typography Detection Module
Estimates text presence, font sizes, and style from image edge analysis.
No OCR — uses region-based edge frequency + line-spacing (FFT period) analysis.
"""

import sys

try:
    from PIL import Image, ImageFilter
except ImportError:
    print("Error: Pillow not installed.", file=sys.stderr)
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("Error: numpy not installed.", file=sys.stderr)
    sys.exit(1)


# px thresholds map onto Tailwind-like scale (mid-points used for snapping)
FONT_SIZE_CLASSES = {
    "xs": (10, 12),
    "sm": (12, 14),
    "base": (14, 17),
    "lg": (17, 20),
    "xl": (20, 24),
    "2xl": (24, 30),
    "3xl": (30, 38),
    "4xl": (38, 50),
    "5xl": (50, 66),
    "6xl": (66, 90),
    "7xl": (90, 128),
}


def _snap_to_class(px: float) -> str:
    """Map a pixel height to nearest font-size class by midpoint distance."""
    best = "base"
    best_dist = float("inf")
    for name, (lo, hi) in FONT_SIZE_CLASSES.items():
        mid = (lo + hi) / 2
        dist = abs(px - mid)
        if dist < best_dist:
            best_dist = dist
            best = name
    return best


def _cluster_sizes(sizes: list[float]) -> list[dict]:
    """1-D clustering of font sizes into distinct groups (simple gap split)."""
    if not sizes:
        return []
    s = sorted(sizes)
    clusters = [[s[0]]]
    for val in s[1:]:
        # relative gap: start a new cluster if >30% jump
        if val > clusters[-1][-1] * 1.3:
            clusters.append([val])
        else:
            clusters[-1].append(val)
    result = []
    for c in clusters:
        result.append(
            {
                "px": int(round(float(np.median(c)))),
                "count": len(c),
                "class": _snap_to_class(float(np.median(c))),
            }
        )
    # sort by count desc (most common size first)
    result.sort(key=lambda x: x["count"], reverse=True)
    return result


def _measure_text_lines(
    edge_arr: np.ndarray, gray: np.ndarray, sh: int, sw: int
) -> tuple[list[float], int, float]:
    """
    Measure text line heights via horizontal edge-band detection in vertical strips.
    Returns (line_heights_px, text_region_count, edge_ratio_mean).
    """
    n_strips = 6
    strip_w = max(sw // n_strips, 10)
    line_heights = []
    region_count = 0
    edge_ratios = []

    for s in range(n_strips):
        x1 = s * strip_w
        x2 = min(x1 + strip_w, sw)
        strip = edge_arr[:, x1:x2]
        row_profile = strip.mean(axis=1) / 255.0
        thresh = max(row_profile.mean() * 1.1, 0.02)

        y = 0
        while y < sh:
            if row_profile[y] > thresh:
                start = y
                while y < sh and row_profile[y] > thresh:
                    y += 1
                band_h = y - start
                if 2 <= band_h <= sh * 0.15:
                    line_heights.append(band_h)
                    region_count += 1
                    band = gray[start:y, x1:x2]
                    if band.shape[0] > 1 and band.shape[1] > 1:
                        eh = np.abs(np.diff(band, axis=1)).mean()
                        ev = np.abs(np.diff(band, axis=0)).mean()
                        edge_ratios.append(eh / max(ev, 0.001))
            else:
                y += 1

    edge_ratio_mean = float(np.mean(edge_ratios)) if edge_ratios else 1.0
    return line_heights, region_count, edge_ratio_mean


def detect_typography(image_path: str) -> dict:
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    MAX_DIM = 400
    scale = min(MAX_DIM / w, MAX_DIM / h, 1.0)
    sw, sh = int(w * scale), int(h * scale)
    small = img.resize((sw, sh), Image.LANCZOS)

    gray = np.array(small.convert("L"), dtype=float)
    edge_arr = np.array(small.convert("L").filter(ImageFilter.FIND_EDGES), dtype=float)
    scale_up = h / sh  # convert analysis-px back to real-px

    line_heights, region_count, edge_ratio_mean = _measure_text_lines(
        edge_arr, gray, sh, sw
    )

    if not line_heights:
        return {"has_text": False, "detected_regions": 0}

    # real-world font sizes (line height ≈ ~1.3× font size)
    real_sizes = [(lh * scale_up) / 1.3 for lh in line_heights]
    size_clusters = _cluster_sizes(real_sizes)

    body_cluster = size_clusters[0] if size_clusters else {"px": 16, "class": "base"}
    # heading = largest size among clusters with a meaningful count (ignore noise)
    robust = [c for c in size_clusters if c["count"] >= 2] or size_clusters
    heading_cluster = max(robust, key=lambda c: c["px"])

    # drop single-sample noise clusters from the reported scale (keep if all are noise)
    reported_clusters = [c for c in size_clusters if c["count"] >= 2] or size_clusters

    text_density = round(region_count / (sh / 10), 3)
    font_style = "serif" if edge_ratio_mean > 2.2 else "sans-serif"

    return {
        "has_text": True,
        "detected_regions": region_count,
        "text_density": text_density,
        "size_clusters": reported_clusters,
        "estimated_heading_size": heading_cluster["class"],
        "estimated_body_size": body_cluster["class"],
        "heading_px": heading_cluster["px"],
        "body_px": body_cluster["px"],
        "font_style": font_style,
        "edge_ratio": round(edge_ratio_mean, 2),
    }


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Detect typography from image")
    parser.add_argument("--image", required=True, help="Path to image")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    result = detect_typography(args.image)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Has text: {result.get('has_text', False)}")
        if result.get("has_text"):
            print(f"Font style: {result.get('font_style')}")
            print(
                f"Heading: {result.get('estimated_heading_size')} "
                f"({result.get('heading_px')}px)"
            )
            print(
                f"Body: {result.get('estimated_body_size')} ({result.get('body_px')}px)"
            )
            print(f"Detected text regions: {result.get('detected_regions')}")
            print(f"Size clusters: {result.get('size_clusters')}")
