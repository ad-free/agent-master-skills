---
name: design-intelligence
description: Use when you need structured design system generation with color palettes, typography pairings, UI styles, and component patterns for a UI project.
model: big-pickle
version: 1.0.0
preamble-tier: 1
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "design system"
  - "design tokens"
  - "color palette"
  - "typography"
  - "ui style"
metadata:
  origin: agent-master-skills
  plugin-for: ui-craft
  phase: DESIGN
  preferred-model: big-pickle
---

<!-- TOKEN CEILING: ~2K -->

# Design Intelligence Plugin

## When to Use

Starting a new UI project, redesigning, or generating design tokens.

## Design System Generation

### Step 1: Collect Requirements

Ask the user or infer from context:
- **Industry**: fintech, health, e-commerce, SaaS, media, gaming, education, enterprise, social, creative
- **Audience**: consumers, enterprise admins, developers, designers, executives, children
- **Platform**: web, mobile (iOS/Android), desktop, cross-platform
- **Design vibe**: professional, playful, luxury, minimal, technical, friendly, bold

### Step 2: Select UI Style

Match style to industry and vibe:

| Vibe | Recommended Styles |
|------|-------------------|
| Professional / Enterprise | Clean corporate, Minimal, Flat 2.0, Microsoft Fluent |
| Modern / Consumer | Glassmorphism, Neumorphism, Bento Grid, Liquid Glass |
| Creative / Artistic | Brutalism, Neo-brutalism, Swiss Design, Memphis |
| Luxury / Premium | Dark luxury, Minimal with serif, Glassmorphism gold |
| Friendly / Casual | Soft UI, Rounded corners, Playful gradients, Claymorphism |
| Technical / Developer | Terminal aesthetic, Monochrome, Skeleton UI, ASCII/retro |

### Step 3: Generate Color Palette

Generate a 7-color system:

```
Primary:     dominant brand color (buttons, links, active states)
Secondary:   supporting accent (badges, secondary actions, highlights)
Surface:     main background (cards, modals, sidebars)
Background:  page-level background (slightly different from surface for depth)
Text:        primary content color (near-black on light, near-white on dark)
Muted:       secondary text, disabled states, placeholders
Border:      dividers, input borders, card outlines (subtle)
```

Include light and dark variants. Ensure WCAG AA contrast (4.5:1 for text).

### Step 4: Choose Typography

Pair a heading font with a body font:

| Industry | Heading | Body | Use Case |
|----------|---------|------|----------|
| Fintech | Inter (sans) | Inter | Clean, professional, dense data |
| Creative | Playfair Display (serif) | Source Sans | Editorial, storytelling |
| SaaS | Manrope (sans) | Manrope | Modern, compact dashboards |
| Luxury | Cormorant Garamond (serif) | Lato | Premium feel, spacious |
| Technical | JetBrains Mono (mono) | Inter | Dev tools, code-heavy |
| E-commerce | Plus Jakarta Sans | Plus Jakarta Sans | Friendly, rounded, approachable |
| Enterprise | IBM Plex Sans | IBM Plex Sans | Corporate, multi-language |

Specify: font name, weight scale (300/400/500/600/700), line height (1.5 body, 1.2 heading), letter-spacing for headings (-0.02em to 0).

### Step 5: Component Patterns

For each component type, specify the style direction:

```
Buttons:   filled (primary), outlined (secondary), ghost (tertiary), danger (red)
Cards:     surface bg, rounded corners (8-16px), subtle shadow, optional border
Inputs:    outlined/underlined/filled, focus ring in primary color, error in red
Modals:    center-aligned, backdrop overlay, surface bg, 500-720px max-width
Navigation: top bar (web) / bottom tab (mobile) / sidebar (desktop app)
Avatars:   circular, initials fallback with primary bg, online indicator dot
Tags:      small rounded pills, secondary bg with muted text
```

## Design Token Output

Generate `design-system/MASTER.md` with: color tokens (primary/secondary/surface/background/text/muted/border), font tokens (heading + body), radius tokens (sm/md/lg), shadow tokens (sm/md/lg), style metadata, and component library patterns per the selections above.

## Anti-Patterns

- Don't mix glassmorphism and brutalism in the same project
- Don't use marketing buzzwords as design direction ("make it pop")
- Don't generate color palettes without checking contrast ratios
- Don't use more than 2 font families — 1 heading + 1 body is enough
- Don't pick styles based on personal preference; match industry expectations
