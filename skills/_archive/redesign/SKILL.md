---
name: redesign
description: Use when you need to upgrade existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-end design standards without breaking functionality. Works with any CSS framework or vanilla CSS.
model: nemotron-3-ultra-free
version: 1.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
triggers:
  - "redesign"
  - "upgrade design"
  - "fix design"
  - "audit design"
  - "improve ui"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
---

# Redesign Skill

Upgrades existing websites and apps to premium quality without breaking functionality.

---

## HOW THIS WORKS

1. **Scan** — Read the codebase. Identify the framework, styling method (Tailwind, vanilla CSS, styled-components, etc.), and current design patterns.
2. **Diagnose** — Run through the audit below. List every generic pattern, weak point, and missing state.
3. **Fix** — Apply targeted upgrades working with the existing stack. Do not rewrite from scratch. Improve what's there.

---

## DESIGN AUDIT

### Typography

- **Browser default fonts or Inter everywhere.** Replace with a font that has character: `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`.
- **Headlines lack presence.** Increase size for display text, tighten letter-spacing, reduce line-height.
- **Body text too wide.** Limit paragraph width to roughly 65 characters. Increase line-height.
- **Only Regular (400) and Bold (700) weights used.** Introduce Medium (500) and SemiBold (600).
- **Numbers in proportional font.** Use monospace or enable tabular figures.
- **Missing letter-spacing adjustments.** Use negative tracking for large headers, positive tracking for small caps.
- **All-caps subheaders everywhere.** Try lowercase italics, sentence case, or small-caps.
- **Orphaned words.** Fix with `text-wrap: balance` or `text-wrap: pretty`.

### Color and Surfaces

- **Pure `#000000` background.** Replace with off-black, dark charcoal, or tinted dark.
- **Oversaturated accent colors.** Keep saturation below 80%.
- **More than one accent color.** Pick one. Remove the rest.
- **Mixing warm and cool grays.** Stick to one gray family.
- **Purple/blue "AI gradient" aesthetic.** Replace with neutral bases and a single accent.
- **Generic `box-shadow`.** Tint shadows to match the background hue.
- **Flat design with zero texture.** Add subtle noise, grain, or micro-patterns.
- **Random dark sections in a light mode page.** Commit to one theme.
- **Empty, flat sections with no visual depth.** Add high-quality background imagery, subtle patterns, or ambient gradients. Use `https://picsum.photos/seed/{name}/1920/1080` when real assets unavailable.

### Layout

- **Everything centered and symmetrical.** Break symmetry with offset margins, mixed aspect ratios.
- **Three equal card columns as feature row.** Replace with 2-column zig-zag, asymmetric grid, horizontal scroll, or masonry.
- **Using `height: 100vh` for full-screen sections.** Replace with `min-height: 100dvh`.
- **Complex flexbox percentage math.** Replace with CSS Grid.
- **No max-width container.** Add container constraint (~1200-1440px) with auto margins.
- **Uniform border-radius on everything.** Vary the radius.
- **Missing whitespace.** Double the spacing. Let the design breathe.
- **Buttons not bottom-aligned in card groups.** Pin buttons to the bottom of each card.
- **Inconsistent vertical rhythm in side-by-side elements.** Align shared elements across all items.

### Interactivity and States

- **No hover states on buttons.** Add background shift, slight scale, or translate on hover.
- **No active/pressed feedback.** Add `scale(0.98)` or `translateY(1px)` on press.
- **Instant transitions with zero duration.** Add smooth transitions (200-300ms).
- **Missing focus ring.** Ensure visible focus indicators for keyboard navigation.
- **No loading states.** Replace circular spinners with skeleton loaders.
- **No empty states.** Design a composed "getting started" view.
- **No error states.** Add clear, inline error messages for forms.
- **Dead links.** Buttons that link to `#` — either link to real destinations or disable them.
- **No indication of current page in navigation.** Style the active nav link differently.
- **Animations using `top`, `left`, `width`, `height`.** Switch to `transform` and `opacity`.

### Content

- **Generic names like "John Doe".** Use diverse, realistic-sounding names.
- **Fake round numbers.** Use organic, messy data: `47.2%`, `$99.00`.
- **Placeholder company names.** Invent contextual, believable brand names.
- **AI copywriting cliches.** Never use "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer".
- **Exclamation marks in success messages.** Remove them.
- **"Oops!" error messages.** Be direct: "Connection failed. Please try again."
- **Lorem Ipsum.** Never use placeholder latin text.

### Component Patterns

- **Generic card look.** Remove the border, or use only background color, or use only spacing.
- **Always one filled button + one ghost button.** Add text links or tertiary styles.
- **Pill-shaped "New" and "Beta" badges.** Try square badges, flags, or plain text labels.
- **Accordion FAQ sections.** Use a side-by-side list, searchable help, or inline progressive disclosure.
- **3-card carousel testimonials with dots.** Replace with a masonry wall or single rotating quote.
- **Pricing table with 3 towers.** Highlight the recommended tier with color and emphasis.
- **Modals for everything.** Use inline editing, slide-over panels, or expandable sections.
- **Avatar circles exclusively.** Try squircles or rounded squares.

### Iconography

- **Lucide or Feather icons exclusively.** Use Phosphor, Heroicons, or a custom set.
- **Rocketship for "Launch", shield for "Security".** Replace cliche metaphors with less obvious icons.
- **Inconsistent stroke widths across icons.** Standardize to one stroke weight.

### Code Quality

- **Div soup.** Use semantic HTML: `<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`.
- **Inline styles mixed with CSS classes.** Move all styling to the project's styling system.
- **Hardcoded pixel widths.** Use relative units (`%`, `rem`, `em`, `max-width`).
- **Missing alt text on images.** Describe image content for screen readers.
- **Arbitrary z-index values like `9999`.** Establish a clean z-index scale.
- **Commented-out dead code.** Remove all debug artifacts before shipping.
- **Import hallucinations.** Check that every import actually exists in `package.json`.
- **Missing meta tags.** Add proper `<title>`, `description`, `og:image`.

### Strategic Omissions (What AI Typically Forgets)

- **No legal links.** Add privacy policy and terms of service in the footer.
- **No "back" navigation.** Every page needs a way back.
- **No custom 404 page.** Design a branded "page not found" experience.
- **No form validation.** Add client-side validation for emails, required fields.
- **No "skip to content" link.** Essential for keyboard users.
- **No cookie consent.** If required by jurisdiction, add a compliant consent banner.

---

## UPGRADE TECHNIQUES

### Typography Upgrades
- **Variable font animation.** Interpolate weight or width on scroll or hover.
- **Outlined-to-fill transitions.** Text starts as a stroke outline and fills with color.
- **Text mask reveals.** Large typography as a window to video behind it.

### Layout Upgrades
- **Broken grid / asymmetry.** Elements that deliberately ignore column structure.
- **Whitespace maximization.** Aggressive negative space to force focus.
- **Parallax card stacks.** Sections that stick and physically stack during scroll.
- **Split-screen scroll.** Two halves sliding in opposite directions.

### Motion Upgrades
- **Smooth scroll with inertia.** Decouple scrolling from browser defaults.
- **Staggered entry.** Elements cascade in with slight delays.
- **Spring physics.** Replace linear easing with spring-based motion.
- **Scroll-driven reveals.** Content entering through expanding masks or draw-on SVG paths.

### Surface Upgrades
- **True glassmorphism.** Add 1px inner border and subtle inner shadow.
- **Spotlight borders.** Card borders that illuminate dynamically under cursor.
- **Grain and noise overlays.** Fixed, pointer-events-none overlay with subtle noise.
- **Colored, tinted shadows.** Shadows that carry the hue of the background.

---

## FIX PRIORITY

Apply changes in this order for maximum impact with minimum risk:

1. **Font swap** — biggest instant improvement, lowest risk
2. **Color palette cleanup** — remove clashing or oversaturated colors
3. **Hover and active states** — makes the interface feel alive
4. **Layout and spacing** — proper grid, max-width, consistent padding
5. **Replace generic components** — swap cliche patterns for modern alternatives
6. **Add loading, empty, and error states** — makes it feel finished
7. **Polish typography scale and spacing** — the premium final touch

---

## RULES

- Work with the existing tech stack. Do not migrate frameworks or styling libraries.
- Do not break existing functionality. Test after every change.
- Before importing any new library, check the project's dependency file first.
- If the project uses Tailwind, check the version (v3 vs v4) before modifying config.
- If the project has no framework, use vanilla CSS.
- Keep changes reviewable and focused. Small, targeted improvements over big rewrites.
