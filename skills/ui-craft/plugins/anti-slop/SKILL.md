---
name: anti-slop
description: Use when building UI components to enforce anti-generic design rules — no emoji icons, no generic gradients, proper spacing, and motion that follows design principles.
metadata:
  origin: agent-master-skills
  plugin-for: ui-craft
  phase: BUILD
---

# Anti-Slop Plugin

## When to Use

Building or reviewing UI components to avoid generic "AI-generated" patterns.

## Hard Rules

### Icons

- **No emoji as icons.** Emoji render differently across platforms and look unprofessional.
- Use SVG icons (Lucide, Phosphor, Heroicons, or custom).
- Icons must have consistent stroke-width (1.5-2px) and viewBox.
- Decorative icons get `aria-hidden="true"`.

### Gradients

- **No generic diagonal gradients.** Blue-to-purple or pink-to-orange gradients are banned unless part of an intentional brand identity.
- Gradients must have a clear purpose: depth, atmosphere, or brand accent.
- Use hard stops or subtle transitions (>50% one color) — not muddy middle blends.
- Gradient text only for large headings, never body text.

### Spacing

- Use a consistent 4px or 8px spacing scale. Never arbitrary values.
- Minimum touch target: 44x44px (mobile), 32x32px (desktop).
- Section padding: minimum 48px vertical, 16px horizontal (mobile).
- Card padding: minimum 16px, prefer 20-24px.
- No content flush against edges — always use padding.

### Typography

- Max line length: 66-75 characters for body text.
- Body text min size: 16px (never 12px or 14px for primary content).
- Heading hierarchy must be visually distinct: h1 > h2 > h3 by at least 4px.
- No letter-spacing on body text; headings may use -0.02em to 0.
- Line height: 1.5-1.7 for body, 1.1-1.3 for headings.

### Layout

- No content centered by default — use left-aligned text for readability.
- Whitespace is a design element, not empty space. Intentional breathing room.
- 12-column grid is the default for responsive layouts.
- No full-width text paragraphs — constrain to 600-720px max-width.

### Motion

- Every animation must respect `prefers-reduced-motion`.
- Duration: 150-300ms for micro-interactions; 300-500ms for transitions.
- Easing: `cubic-bezier(0.4, 0, 0.2, 1)` for modern feel; no linear easing.
- No auto-playing animations, no parallax without scroll control.
- Stagger delays: 30-50ms between items, never more than 100ms.


