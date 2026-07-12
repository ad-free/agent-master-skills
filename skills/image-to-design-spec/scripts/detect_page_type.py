#!/usr/bin/env python3
"""
Page Type Classification Module
Classifies page intent from detected layout and components.

Page types: landing, login, dashboard, pricing, settings, blog, portfolio, ecommerce
"""


def classify_page(
    components: list, layout: dict, typography: dict | None = None
) -> dict:
    if typography is None:
        typography = {}
    scores = {}

    has_sidebar = layout.get("has_sidebar", False)
    layout_type = layout.get("layout_type", "single-column")
    bg_type = layout.get("background_type", "solid")
    is_centered = layout_type == "centered-card"
    is_hero = layout_type == "hero-fullscreen"
    has_gradient = layout.get("has_gradient", False)
    complexity = layout.get("complexity_score", 0)

    comp_types = [c["type"] for c in components]
    has_charts = "chart" in comp_types
    has_cards = "card" in comp_types
    has_inputs = "input" in comp_types
    has_buttons = "button" in comp_types
    has_nav = "navigation" in comp_types
    has_toggles = "toggle" in comp_types
    has_progress = "progress-bar" in comp_types
    has_avatar = "avatar" in comp_types
    card_count = comp_types.count("card")
    chart_count = comp_types.count("chart")
    button_count = comp_types.count("button")

    text_has_text = typography.get("has_text", False) if typography else False
    text_density = typography.get("text_density", 0) if typography else 0

    # landing page: hero fullscreen, gradient overlay, centered CTA
    if is_hero and has_gradient and has_buttons and not has_sidebar:
        scores["landing"] = 0.85

    # landing page (non-hero): gradient/photo background + inputs/buttons = sign-up or landing
    if not is_hero and has_gradient and has_inputs and not has_sidebar:
        scores["landing"] = 0.7
        scores["login"] = 0.65
        scores["register"] = 0.6

    # login/register: centered card, inputs, one primary button
    if is_centered and has_inputs and has_buttons:
        scores["login"] = 0.4 + (0.2 if button_count == 1 else 0)
        scores["register"] = 0.3 + (0.2 if has_inputs else 0)

    # dashboard: sidebar, cards, charts, avatar, high complexity
    if has_sidebar and has_cards and complexity > 0.6:
        base = 0.5
        if has_charts:
            base += 0.3
        if has_nav or has_avatar:
            base += 0.1
        if card_count >= 3:
            base += 0.1
        scores["dashboard"] = min(base, 0.95)

    # analytics: charts, progress bars, sidebar
    if has_charts and has_progress and complexity > 0.5:
        scores["analytics"] = 0.6 + (0.15 if has_sidebar else 0)

    # pricing: multiple cards, one button each, no inputs
    if card_count >= 3 and has_buttons and not has_inputs:
        scores["pricing"] = 0.55

    # settings: form elements, toggles, inputs, no charts
    if has_toggles and has_inputs and not has_charts:
        scores["settings"] = 0.6 + (0.15 if has_nav else 0)

    # blog/content: high text density, single column, no charts
    if text_has_text and text_density > 0.05 and not has_sidebar and not has_charts:
        scores["blog"] = 0.5 + (0.2 if text_density > 0.1 else 0)

    # portfolio: cards, no sidebar, no inputs, moderate complexity
    if has_cards and not has_sidebar and not has_inputs and not has_charts:
        scores["portfolio"] = 0.45

    # ecommerce: cards, buttons, navigation, no charts
    if has_cards and has_buttons and has_nav and not has_charts and card_count >= 4:
        scores["ecommerce"] = 0.5

    if not scores:
        if has_sidebar:
            scores["dashboard"] = 0.4
        elif is_centered:
            scores["login"] = 0.4
        elif is_hero:
            scores["landing"] = 0.5
        else:
            scores["generic"] = 0.6

    sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_types[0]
    alternatives = [{"type": t, "confidence": c} for t, c in sorted_types[1:]]

    reasons = {
        "dashboard": "sidebar + cards + charts = admin dashboard",
        "landing": "hero fullscreen + gradient + CTA = landing page",
        "login": "centered card + inputs + single CTA = login form",
        "register": "centered card + inputs = registration form",
        "analytics": "charts + progress bars = analytics view",
        "pricing": "multiple cards + buttons = pricing page",
        "settings": "toggles + inputs + no charts = settings page",
        "blog": "high text density + single column = blog page",
        "portfolio": "cards + no sidebar = portfolio",
        "ecommerce": "cards + nav + buttons = ecommerce listing",
        "generic": "unable to classify definitively",
    }

    return {
        "page_type": primary[0],
        "confidence": round(primary[1], 2),
        "reasoning": reasons.get(primary[0], ""),
        "alternative_types": alternatives,
    }


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Classify page type from analysis data"
    )
    parser.add_argument("--input", required=True, help="JSON file from analyze.py")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    result = classify_page(
        data.get("components", []),
        data.get("layout", {}),
        data.get("typography", {}),
    )

    print(json.dumps(result, indent=2))
