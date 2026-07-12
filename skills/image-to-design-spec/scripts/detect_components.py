#!/usr/bin/env python3
"""
Component Detection Module
Detects UI components using region-based analysis:
  1. Color quantization → connected components → uniform-color regions
  2. Edge cluster detection → bounded rects
  3. Layout-aware classification (uses sidebar/header/grid from layout if available)
"""

import sys
from dataclasses import dataclass, field
from collections import deque

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


@dataclass
class Component:
    type: str
    confidence: float
    region: tuple
    details: dict = field(default_factory=dict)

    def to_dict(self):
        x1, y1, x2, y2 = self.region
        return {
            "type": self.type,
            "confidence": round(self.confidence, 2),
            "region": {
                "x_start": round(x1, 3),
                "y_start": round(y1, 3),
                "x_end": round(x2, 3),
                "y_end": round(y2, 3),
            },
            "details": self.details,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _norm_rect(x1, y1, x2, y2, w, h):
    """Return normalized (0-1) region tuple."""
    return (x1 / w, y1 / h, x2 / w, y2 / h)


def _iou(b1, b2, w, h):
    """Intersection-over-union (normalized coords ok if same scale)."""
    x1 = max(b1[0], b2[0])
    y1 = max(b1[1], b2[1])
    x2 = min(b1[2], b2[2])
    y2 = min(b1[3], b2[3])
    if x1 >= x2 or y1 >= y2:
        return 0.0
    ai = (x2 - x1) * (y2 - y1)
    a1 = (b1[2] - b1[0]) * (b1[3] - b1[1])
    a2 = (b2[2] - b2[0]) * (b2[3] - b2[1])
    return ai / (a1 + a2 - ai)


def _rectangularity(mask):
    """How rectangular a binary shape is (1.0 = perfect rect)."""
    coords = np.argwhere(mask)
    if len(coords) < 10:
        return 0.0
    y1, x1 = coords.min(axis=0)
    y2, x2 = coords.max(axis=0)
    h, w = y2 - y1 + 1, x2 - x1 + 1
    area = h * w
    if area == 0:
        return 0.0
    return len(coords) / area


# ---------------------------------------------------------------------------
# Stage 1: Colour-quantized connected-component analysis
# ---------------------------------------------------------------------------


def _kmeans_colors(arr: np.ndarray, k: int = 8, max_iter: int = 15) -> tuple:
    """Simple k-means colour quantization. Returns (palette, labels)."""
    h, w, _ = arr.shape
    pixels = arr.reshape(-1, 3)
    rng = np.random.default_rng(42)
    idx = rng.choice(len(pixels), k, replace=False)
    centroids = pixels[idx].astype(float)

    labels = np.zeros(len(pixels), dtype=int)
    for _ in range(max_iter):
        dists = np.sum((pixels[:, None, :] - centroids[None, :, :]) ** 2, axis=2)
        labels = np.argmin(dists, axis=1)
        new_centroids = centroids.copy()
        for i in range(k):
            members = pixels[labels == i]
            if len(members) > 0:
                new_centroids[i] = members.mean(axis=0)
        if np.allclose(centroids, new_centroids, atol=1.0):
            break
        centroids = new_centroids

    return centroids.astype(int), labels.reshape(h, w)


def _flood_fill(labels: np.ndarray, h: int, w: int) -> list[dict]:
    """Connected components of same label via BFS flood-fill."""
    visited = np.zeros((h, w), dtype=bool)
    regions = []

    for sy in range(h):
        for sx in range(w):
            if visited[sy, sx]:
                continue
            color_idx = labels[sy, sx]
            q = deque()
            q.append((sx, sy))
            visited[sy, sx] = True
            min_x = max_x = sx
            min_y = max_y = sy
            count = 0

            while q:
                cx, cy = q.popleft()
                count += 1
                min_x = min(min_x, cx)
                max_x = max(max_x, cx)
                min_y = min(min_y, cy)
                max_y = max(max_y, cy)

                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if (
                        0 <= nx < w
                        and 0 <= ny < h
                        and not visited[ny, nx]
                        and labels[ny, nx] == color_idx
                    ):
                        visited[ny, nx] = True
                        q.append((nx, ny))

            bw = max_x - min_x + 1
            bh = max_y - min_y + 1
            if bw < 3 or bh < 3 or count < 8:
                continue

            regions.append(
                {
                    "x1": min_x,
                    "y1": min_y,
                    "x2": max_x,
                    "y2": max_y,
                    "color_idx": int(color_idx),
                    "pixel_count": count,
                    "fill_ratio": count / (bw * bh) if bw * bh > 0 else 0.0,
                }
            )

    return regions


def _merge_same_row(regions: list, h: int, gap_px: int = 2) -> list:
    """Merge same-colour regions that are side-by-side in the same row."""
    if not regions:
        return []
    merged = []
    sorted_r = sorted(regions, key=lambda r: (r["y1"], r["x1"]))
    used = [False] * len(sorted_r)
    for i, a in enumerate(sorted_r):
        if used[i]:
            continue
        used[i] = True
        cx1, cy1, cx2, cy2 = a["x1"], a["y1"], a["x2"], a["y2"]
        c_idx = a["color_idx"]
        for j in range(i + 1, len(sorted_r)):
            if used[j]:
                continue
            b = sorted_r[j]
            if b["color_idx"] != c_idx:
                continue
            row_overlap = max(0, min(cx2, b["x2"]) - max(cx1, b["x1"])) > 0
            vert_gap = b["y1"] - cy2
            if row_overlap and 0 <= vert_gap <= gap_px:
                cx1 = min(cx1, b["x1"])
                cy1 = min(cy1, b["y1"])
                cx2 = max(cx2, b["x2"])
                cy2 = max(cy2, b["y2"])
                used[j] = True
        merged.append(
            {
                "x1": cx1,
                "y1": cy1,
                "x2": cx2,
                "y2": cy2,
                "color_idx": c_idx,
                "pixel_count": a["pixel_count"],
                "fill_ratio": a["fill_ratio"],
            }
        )
    return merged


def _find_color_regions(arr: np.ndarray, h: int, w: int) -> list[dict]:
    """Quantize colours, flood-fill, merge same-row → list of candidate regions."""
    palette, labels = _kmeans_colors(arr, k=8)
    regions = _flood_fill(labels, h, w)
    regions = _merge_same_row(regions, h)
    for r in regions:
        bw = r["x2"] - r["x1"] + 1
        bh = r["y2"] - r["y1"] + 1
        r["area_ratio"] = (bw * bh) / (w * h)
        r["aspect"] = bw / max(bh, 1)
    return regions


# ---------------------------------------------------------------------------
# Stage 2: Layout-constrained scanning for components colour regions miss
# ---------------------------------------------------------------------------


def _find_grid_cells(edges: np.ndarray, h: int, w: int) -> list[dict]:
    """Find grid-like subdivisions via projection profiles."""
    h_proj = edges.mean(axis=1) / 255.0
    v_proj = edges.mean(axis=0) / 255.0

    h_thresh = np.percentile(h_proj, 20)
    v_thresh = np.percentile(v_proj, 20)

    h_gaps = []
    i = 0
    while i < h:
        if h_proj[i] < h_thresh:
            start = i
            while i < h and h_proj[i] < h_thresh:
                i += 1
            if i - start >= 2:
                h_gaps.append((start, i))
        else:
            i += 1

    v_gaps = []
    i = 0
    while i < w:
        if v_proj[i] < v_thresh:
            start = i
            while i < w and v_proj[i] < v_thresh:
                i += 1
            if i - start >= 2:
                v_gaps.append((start, i))
        else:
            i += 1

    if len(h_gaps) < 2 and len(v_gaps) < 2:
        return []

    mid_h = [(s + e) // 2 for s, e in h_gaps]
    mid_v = [(s + e) // 2 for s, e in v_gaps]

    y_edges = sorted([0] + mid_h + [h])
    x_edges = sorted([0] + mid_v + [w])

    cells = []
    for yi in range(len(y_edges) - 1):
        for xi in range(len(x_edges) - 1):
            y1, y2 = y_edges[yi], y_edges[yi + 1]
            x1, x2 = x_edges[xi], x_edges[xi + 1]
            cw, ch = x2 - x1, y2 - y1
            if cw > w * 0.03 and ch > h * 0.03 and cw < w * 0.9 and ch < h * 0.9:
                cell_edges = edges[y1:y2, x1:x2].mean() / 255.0
                cells.append(
                    {
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2,
                        "edge_density": cell_edges,
                    }
                )
    return cells


def _detect_nav_strip(
    gray: np.ndarray, edges: np.ndarray, h: int, w: int
) -> dict | None:
    """Horizontal navigation strip at the top."""
    nav_strip_h = min(int(h * 0.10), 60)
    strip = edges[:nav_strip_h, :]
    edge_avg = strip.mean() / 255.0
    if edge_avg < 0.01:
        return None
    v_proj = edges[:nav_strip_h, :].mean(axis=0) / 255.0
    peaks = sum(
        1
        for i in range(1, len(v_proj) - 1)
        if v_proj[i] > v_proj[i - 1] and v_proj[i] > v_proj[i + 1] and v_proj[i] > 0.02
    )
    if 2 < peaks < 40 and nav_strip_h > h * 0.02:
        return {
            "x1": 0,
            "y1": 0,
            "x2": w,
            "y2": nav_strip_h,
            "confidence": min(0.5 + peaks * 0.02, 0.85),
        }
    return None


def _detect_sidebar_nav(
    gray: np.ndarray, edges: np.ndarray, h: int, w: int, sidebar_x: int | None
) -> list[dict]:
    """Menu items inside a sidebar region."""
    if sidebar_x is None or sidebar_x > w * 0.3:
        return []
    items = []
    item_h = int(h * 0.035)
    if item_h < 8:
        return []
    step = item_h
    for y in range(0, h - item_h, step):
        block = edges[y : y + item_h, :sidebar_x]
        edge_avg = block.mean() / 255.0
        color_block = gray[y : y + item_h, :sidebar_x]
        if 0.005 < edge_avg < 0.1 and color_block.std() > 5:
            items.append(
                {
                    "x1": 0,
                    "y1": y,
                    "x2": sidebar_x,
                    "y2": y + item_h,
                    "edge_density": edge_avg,
                }
            )
    return items


# ---------------------------------------------------------------------------
# Stage 3: Region classification
# ---------------------------------------------------------------------------


def _classify_region(
    r: dict,
    gray: np.ndarray,
    edges: np.ndarray,
    arr: np.ndarray,
    h: int,
    w: int,
    sidebar_w: int | None = None,
) -> Component | None:
    """Classify a candidate region into a component type or return None."""
    x1, y1, x2, y2 = r["x1"], r["y1"], r["x2"], r["y2"]
    rw, rh = x2 - x1, y2 - y1
    if rw < 6 or rh < 6:
        return None

    aspect = rw / max(rh, 1)
    area_ratio = (rw * rh) / (w * h)

    sub_gray = gray[y1:y2, x1:x2]
    sub_edges = edges[y1:y2, x1:x2]
    sub_color = arr[y1:y2, x1:x2]

    edge_density = float(sub_edges.mean() / 255.0)
    interior_std = float(sub_gray.std())
    mean_intensity = float(sub_gray.mean())

    is_in_sidebar = sidebar_w is not None and x1 < sidebar_w

    r_dict = {
        **r,
        "rw": rw,
        "rh": rh,
        "aspect": aspect,
        "area_ratio": area_ratio,
        "edge_density": edge_density,
        "interior_std": interior_std,
        "mean_intensity": mean_intensity,
        "is_in_sidebar": is_in_sidebar,
    }

    # --- Button: small, compact, coloured, ~2–5:1 aspect ---
    if 0.002 < area_ratio < 0.10 and 1.2 < aspect < 6:
        if interior_std > 15 and edge_density < 0.12:
            is_orange = np.any(sub_color.mean(axis=(0, 1)) > 150)
            conf = 0.5 + min(interior_std * 0.005, 0.25)
            if edge_density > 0.02:
                conf += 0.1
            conf = min(conf, 0.85)
            return Component(
                "button",
                round(conf, 2),
                _norm_rect(x1, y1, x2, y2, w, h),
                {
                    "width_px": rw,
                    "height_px": rh,
                    "aspect_ratio": round(aspect, 1),
                    "is_colored": bool(interior_std > 25),
                },
            )

    # --- Input: wide, thin, aspect > 3, light interior, bordered ---
    if aspect > 2.5 and rh < h * 0.06 and rh >= 5:
        top_border = edges[y1, x1:x2].mean() / 255.0 if y1 + 1 < h else 0
        bot_border = edges[y2 - 1, x1:x2].mean() / 255.0 if y2 - 1 >= 0 else 0
        border_score = (top_border + bot_border) / 2
        if border_score > 0.01 and interior_std < 25:
            conf = 0.6 + min(border_score * 5, 0.25)
            conf = min(conf, 0.85)
            return Component(
                "input",
                round(conf, 2),
                _norm_rect(x1, y1, x2, y2, w, h),
                {"width_px": rw, "height_px": rh},
            )

    # --- Chart: large region with high edge density + data-ink pattern ---
    if area_ratio > 0.03 and rw > w * 0.12 and rh > h * 0.08:
        h_edge = np.abs(np.diff(sub_gray, axis=1)).mean()
        v_edge = np.abs(np.diff(sub_gray, axis=0)).mean()
        has_gridlines = 0.2 < (h_edge / max(v_edge, 0.001)) < 3.0
        color_variety = sub_color.reshape(-1, 3).std(axis=0).mean()
        if edge_density > 0.04 and has_gridlines and color_variety > 25:
            conf = min(0.4 + edge_density * 3 + color_variety * 0.003, 0.8)
            return Component(
                "chart",
                round(conf, 2),
                _norm_rect(x1, y1, x2, y2, w, h),
                {
                    "edge_density": round(edge_density, 3),
                    "color_variance": round(color_variety, 1),
                },
            )

    # --- Card: medium-large, clean interior, border/shadow ---
    if area_ratio > 0.02 and area_ratio < 0.8 and 0.5 < aspect < 3.0:
        border_top = gray[y1 : y1 + 2, x1:x2].mean()
        border_bot = gray[y2 - 2 : y2, x1:x2].mean()
        border_l = gray[y1:y2, x1 : x1 + 2].mean()
        border_r = gray[y1:y2, x2 - 2 : x2].mean()
        interior = gray[y1 + 2 : y2 - 2, x1 + 2 : x2 - 2]
        border_avg = (border_top + border_bot + border_l + border_r) / 4
        interior_avg = interior.mean()
        delta = abs(border_avg - interior_avg)
        if delta > 8 and interior.std() < 35 and interior.std() > 2:
            conf = min(0.35 + delta * 0.02, 0.85)
            return Component(
                "card",
                round(conf, 2),
                _norm_rect(x1, y1, x2, y2, w, h),
                {"width_px": rw, "height_px": rh, "aspect_ratio": round(aspect, 1)},
            )

    # --- Avatar: small square near top corners ---
    if 0.001 < area_ratio < 0.03 and 0.8 < aspect < 1.3:
        is_top_left = y1 < h * 0.15 and x1 < w * 0.2
        is_top_right = y1 < h * 0.15 and x2 > w * 0.8
        if (is_top_left or is_top_right) and interior_std > 10:
            conf = min(0.4 + edge_density * 5, 0.7)
            return Component(
                "avatar",
                round(conf, 2),
                _norm_rect(x1, y1, x2, y2, w, h),
                {"size_px": (rw + rh) // 2},
            )

    return None


# ---------------------------------------------------------------------------
# Post-processing
# ---------------------------------------------------------------------------


def _merge_overlapping_components(comps: list, iou_thresh: float = 0.5) -> list:
    """Keep highest-confidence component per overlapping group."""
    if not comps:
        return []
    sorted_c = sorted(comps, key=lambda c: c.confidence, reverse=True)
    kept = []
    w, h = 1.0, 1.0
    for c in sorted_c:
        overlap = False
        for k in kept:
            if _iou(c.region, k.region, w, h) > iou_thresh:
                # If same type, keep the better one
                if c.type == k.type:
                    overlap = True
                    break
                # Different type: keep both but discount lower confidence one
                if c.confidence < k.confidence - 0.15:
                    overlap = True
                    break
        if not overlap:
            kept.append(c)
    return kept


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def detect_components(image_path: str, layout: dict | None = None) -> list:
    """
    Detect UI components using multi-strategy region analysis.

    Args:
        image_path: Path to the UI screenshot.
        layout: Optional dict from extract_layout (sidebar, header, etc.).

    Returns:
        List of component dicts.
    """
    img = Image.open(image_path).convert("RGB")
    w, h = img.size

    # Analysis scale
    MAX_DIM = 400
    scale = min(MAX_DIM / w, MAX_DIM / h, 1.0)
    sw, sh = int(w * scale), int(h * scale)
    small = img.resize((sw, sh), Image.LANCZOS)

    arr = np.array(small, dtype=float)
    gray = np.mean(arr, axis=2)
    edges = np.array(small.convert("L").filter(ImageFilter.FIND_EDGES), dtype=float)

    sidebar_w = None
    if layout and layout.get("has_sidebar"):
        sidebar_w_px = layout.get("sidebar_width_percent", 0)
        if sidebar_w_px:
            sidebar_w = int(sw * sidebar_w_px / 100)

    candidates: list[Component] = []

    # ------ Strategy A: colour-quantized regions ------
    color_regions = _find_color_regions(arr, sh, sw)
    for r in color_regions:
        comp = _classify_region(r, gray, edges, arr, sh, sw, sidebar_w)
        if comp and comp.confidence >= 0.4:
            candidates.append(comp)

    # ------ Strategy B: grid cells (for charts, cards) ------
    grid_cells = _find_grid_cells(edges, sh, sw)
    for gc in grid_cells:
        comp = _classify_region(gc, gray, edges, arr, sh, sw, sidebar_w)
        if comp and comp.confidence >= 0.5:
            if not any(
                c.type == comp.type and _iou(c.region, comp.region, 1, 1) > 0.4
                for c in candidates
            ):
                candidates.append(comp)

    # ------ Strategy C: navigation strip ------
    nav = _detect_nav_strip(gray, edges, sh, sw)
    if nav:
        candidates.append(
            Component(
                "navigation",
                round(nav["confidence"], 2),
                _norm_rect(nav["x1"], nav["y1"], nav["x2"], nav["y2"], sw, sh),
                {"nav_height_px": nav["y2"] - nav["y1"]},
            )
        )

    # ------ Strategy D: sidebar nav items ------
    if sidebar_w:
        side_items = _detect_sidebar_nav(gray, edges, sh, sw, sidebar_w)
        if side_items:
            total = len(side_items)
            candidate = Component(
                "navigation",
                round(0.5 + total * 0.015, 2),
                _norm_rect(0, 0, sidebar_w, sh, sw, sh),
                {"nav_items": total, "is_sidebar": True},
            )
            candidates.append(candidate)

    # ------ Merge overlapping ------
    candidates = _merge_overlapping_components(candidates)

    return [c.to_dict() for c in candidates]


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Detect UI components from image")
    parser.add_argument("--image", required=True, help="Path to image")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    result = detect_components(args.image)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Components detected: {len(result)}")
        for c in result:
            print(f"  - {c['type']} (confidence: {c['confidence']})")
            if c.get("details"):
                for k, v in c["details"].items():
                    print(f"      {k}: {v}")
