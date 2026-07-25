# Redesign Audit Checklist — ui-craft Reference

**Source:** taste-skill/redesign-skill  
**Order:** Priority-ranked for maximum visual impact with minimum risk. Apply sequentially.

---

## Phase 1: Typography Upgrades (Biggest Impact, Lowest Risk)

| # | Check | Fix |
|---|-------|-----|
| 1.1 | Browser default fonts or Inter everywhere | Replace with character font: Geist, Outfit, Cabinet Grotesk, Satoshi. For editorial: pair serif header + sans body |
| 1.2 | Headlines lack presence | Increase display size, tighten letter-spacing, reduce line-height. Headlines must feel heavy/intentional |
| 1.3 | Body text too wide (>65ch) | Limit paragraph width to ~65ch. Increase line-height for readability |
| 1.4 | Only Regular (400) + Bold (700) weights used | Introduce Medium (500) + SemiBold (600) for subtle hierarchy |
| 1.5 | Numbers in proportional font | Use monospace or font-variant-numeric: tabular-nums for data-heavy UI |
| 1.6 | Missing letter-spacing adjustments | Negative tracking for large headers, positive for small caps/labels |
| 1.7 | All-caps subheaders everywhere (eyebrow abuse) | Use lowercase italics, sentence case, or small-caps instead. Max 1 eyebrow per 3 sections |
| 1.8 | Orphaned words (single word on last line) | Fix with text-wrap: balance or text-wrap: pretty |

---

## Phase 2: Color Palette Cleanup

| # | Check | Fix |
|---|-------|-----|
| 2.1 | Pure #000000 background | Replace with off-black: #0a0a0a, #121212, or tinted dark navy |
| 2.2 | Oversaturated accents (>80% saturation) | Desaturate to blend with neutrals |
| 2.3 | More than one accent color | Pick ONE. Remove the rest. Consistency > variety |
| 2.4 | Mixing warm and cool grays | Stick to ONE gray family. Tint all grays consistently (warm OR cool) |
| 2.5 | Purple/blue AI gradient aesthetic | Replace with neutral bases + single considered accent |
| 2.6 | Generic box-shadow (pure black low opacity) | Tint shadows to background hue. Use colored shadows (e.g., dark blue on blue bg) |
| 2.7 | Flat design with zero texture | Add subtle noise/grain/micro-patterns to backgrounds |
| 2.8 | Perfectly even linear 45 gradients | Break with radial gradients, noise overlays, or mesh gradients |
| 2.9 | Inconsistent lighting direction | Audit all shadows -> single consistent light source |
| 2.10 | Random dark section in light page (or vice versa) | Either commit to full dark mode OR consistent background tone. For contrast: slightly darker shade of same palette, not jump to #111 |
| 2.11 | Empty flat sections (text on plain bg only) | Add high-quality background imagery (blurred/overlaid/masked), subtle patterns, or ambient gradients. Use https://picsum.photos/seed/{name}/1920/1080 for placeholders |

---

## Phase 3: Hover & Active States (Makes Interface Feel Alive)

| # | Check | Fix |
|---|-------|-----|
| 3.1 | No hover states on buttons | Add background shift, slight scale, or translate on hover |
| 3.2 | No active/pressed feedback | Add subtle scale(0.98) or translateY(1px) on press |
| 3.3 | Instant transitions (0 duration) | Add smooth 200-300ms transitions to ALL interactive elements |
| 3.4 | Missing focus ring | Ensure visible focus indicators for keyboard navigation (a11y requirement) |
| 3.5 | No loading states | Replace generic spinners with skeleton loaders matching final layout shape |
| 3.6 | No empty states | Design composed getting started view for empty dashboards |
| 3.7 | No error states | Add clear inline error messages for forms. No window.alert() |
| 3.8 | Dead links (href="#") | Real destinations OR visually disable |
| 3.9 | No active nav indicator | Style current page differently so users know where they are |
| 3.10 | Anchor jumps instantly | Add scroll-behavior: smooth |
| 3.11 | Animating top/left/width/height | Switch to transform + opacity for GPU-accelerated animation |

---

## Phase 4: Layout & Spacing (Grid, Max-Width, Consistency)

| # | Check | Fix |
|---|-------|-----|
| 4.1 | Everything centered & symmetrical | Break symmetry: offset margins, mixed aspect ratios, left-aligned headers over centered content |
| 4.2 | Three equal card columns (feature row) | Replace: 2-col zigzag, asymmetric grid, horizontal scroll, or masonry |
| 4.3 | height: 100vh for full-screen sections | Replace with min-height: 100dvh (prevents iOS Safari viewport jump) |
| 4.4 | Complex flexbox percentage math | Replace with CSS Grid for reliable multi-column |
| 4.5 | No max-width container | Add container constraint (~1200-1440px) with auto margins |
| 4.6 | Equal-height cards forced by flexbox | Allow variable heights or use masonry when content varies |
| 4.7 | Uniform border-radius on everything | Vary radius: tighter on inner elements, softer on containers |
| 4.8 | No overlap/depth (flat adjacency) | Use negative margins for layering and visual depth |
| 4.9 | Symmetrical vertical padding (top=bottom always) | Adjust optically - bottom often needs slightly more |
| 4.10 | Dashboard always has left sidebar | Try top nav, floating command menu, or collapsible panel |
| 4.11 | Missing whitespace (cramped) | Double spacing. Let design breathe. Dense = data dashboards only |
| 4.12 | Buttons not bottom-aligned in card groups | Pin CTAs to bottom of each card -> clean horizontal line |
| 4.13 | Feature lists start at different Y positions | Align feature list start across all columns (consistent spacing above) |
| 4.14 | Inconsistent vertical rhythm in side-by-side elements | Align shared elements (titles, descriptions, prices, buttons) across items |
| 4.15 | Mathematical alignment looks optically wrong | Optical adjust 1-2px: icons next to text, play buttons in circles, text in buttons |

---

## Phase 5: Replace Generic Component Patterns

| # | Check | Fix |
|---|-------|-----|
| 5.1 | Generic card (border + shadow + white bg) | Remove border, OR use only bg color, OR use only spacing. Cards only when elevation = hierarchy |
| 5.2 | Always 1 filled + 1 ghost button | Add text links or tertiary styles to reduce visual noise |
| 5.3 | Pill New/Beta badges | Try square badges, flags, or plain text labels |
| 5.4 | Accordion FAQ sections | Side-by-side list, searchable help, or inline progressive disclosure |
| 5.5 | 3-card carousel testimonials with dots | Masonry wall, embedded social posts, or single rotating quote |
| 5.6 | 3-tower pricing table | Highlight recommended tier with color/emphasis, not just extra height |
| 5.7 | Modals for everything | Inline editing, slide-over panels, expandable sections for simple actions |
| 5.8 | Avatar circles exclusively | Try squircles or rounded squares |
| 5.9 | Light/dark toggle = only sun/moon switch | Dropdown, system preference detection, or integrate into settings |
| 5.10 | Footer 4-column link farm | Simplify: main navigational paths + legally required links only |
| 5.11 | Lucide/Feather icons as default | Use Phosphor, Heroicons, Radix, or Tabler. Pick ONE family per project |
| 5.12 | Rocket=Launch, Shield=Security cliches | Replace: bolt, fingerprint, spark, vault |
| 5.13 | Inconsistent icon stroke weights | Audit all icons -> standardize to ONE stroke weight |
| 5.14 | Missing favicon | Always include branded favicon |
| 5.15 | Stock diverse team photos | Real team photos, candid shots, or consistent illustration style |

---

## Phase 6: Loading, Empty, Error States (Makes It Feel Finished)

| # | Check | Fix |
|---|-------|-----|
| 6.1 | No skeleton loaders | Match final layout shape - no generic spinners |
| 6.2 | No composed empty states | Getting started view with illustration + CTA |
| 6.3 | No inline form error messages | Clear, specific, below input. No alerts |
| 6.4 | No toast/error boundary for async failures | Contextual toasts for transient, inline for forms |

---

## Phase 7: Polish Typography Scale & Spacing (Premium Final Touch)

| # | Check | Fix |
|---|-------|-----|
| 7.1 | Type scale lacks clear hierarchy | Define scale: display -> h1 -> h2 -> h3 -> body -> small -> micro. Each step distinct |
| 7.2 | Spacing scale inconsistent | Define spacing tokens: space-1 -> space
