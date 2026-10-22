---
name: imagegen
description: Use when you need to generate premium frontend images for website design references, hero sections, illustrations, or product shots. Creates one separate horizontal image per section with consistent palette, typography scale, and CTA family.
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
  - "image gen"
  - "generate image"
  - "design reference"
  - "section image"
  - "website comp"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
---

# Image Generation Skill

Generate premium website design reference images that developers or coding models can accurately recreate.

---

## HARD OUTPUT RULE

**Generate one separate horizontal image PER section. Always. No exceptions.**

- 1 section → 1 image
- 4 sections → 4 images
- 8 sections → 8 images
- 12 sections → 12 images
- "landing page" with no count → default to 6 sections → 6 images
- "full website template" → default to 8 sections → 8 images

Each image is one section, generated as its own image call. Never combine multiple sections into one frame.

---

## HERO COMPOSITION BIAS

The default left-text / right-image hero is the most overused AI pattern. Before reaching for it, consider:

- Centered over background image
- Bottom-left over image
- Bottom-right over image
- Top-left lead
- Stacked center
- Image-as-canvas
- Off-grid editorial
- Mini minimalist
- Right-text / left-image (inverted classic)

Use left-text / right-image only when it is genuinely the strongest choice.

---

## 1. ACTIVE BASELINE CONFIGURATION

- DESIGN_VARIANCE: 8
- VISUAL_DENSITY: 4
- ART_DIRECTION: 8
- IMPLEMENTATION_CLARITY: 9
- IMAGE_USAGE_PRIORITY: 9
- SPACING_GENEROSITY: 8
- LAYOUT_VARIATION: 8
- CONVERSION_DISCIPLINE: 8

### Brief-to-direction mapping

**"minimalist" / "clean" / "typography-only" / "swiss":**
- Hero Scale: Mini Minimalist
- Background Mode: solid surfaces, subtle texture
- Gradients: skip or softest tonal
- Composition: stacked center, generous negative space

**"editorial" / "magazine" / "art-directed":**
- Hero Scale: Mid Editorial or Giant Statement
- Background Mode: editorial side-image, duotone treated
- Composition: off-grid editorial offset

**"cinematic" / "atmospheric" / "premium" / "luxury":**
- Hero Scale: Giant Statement
- Background Mode: full-bleed image with tonal overlay
- Composition: bottom-left over background image

**"SaaS" / "product" / "dashboard":**
- Hero Scale: Mid Editorial
- Background Mode: solid + inline asset
- Composition: clear product framing

**"agency" / "creative studio" / "portfolio":**
- Hero Scale: Giant Statement OR Mini Minimalist
- Background Mode: vary boldly
- Composition: off-grid, poster-like

---

## 2. THE COMBINATORIAL VARIATION ENGINE

### Theme Paradigm (pick 1)
1. Pristine Light Mode — Off-white / cream / paper tones
2. Deep Dark Mode — Charcoal / graphite / zinc
3. Bold Studio Solid — Strong controlled color fields
4. Quiet Premium Neutral — Bone, sand, taupe, stone

### Background Character (pick 1)
1. Subtle technical grid / dotted field
2. Pure solid field with soft ambient gradient depth
3. Full-bleed cinematic imagery with contrast control
4. Quiet textured paper / material feel

### Typography Character (pick 1)
1. Satoshi-like clean grotesk
2. Neue-Montreal-like refined grotesk
3. Cabinet / Clash-like expressive display
4. Monument-like compressed statement
5. Elegant editorial serif + sans pairing
6. Swiss rational sans with strong hierarchy

### Hero Architecture (pick 1)
1. Cinematic Centered Minimalist
2. Asymmetric Split Hero
3. Floating Polaroid Scatter
4. Inline Typography Behemoth
5. Editorial Offset Composition
6. Massive Image-First Hero with restrained text

### Section System (pick 1)
1. Strict modular bento rhythm
2. Alternating editorial blocks
3. Poster-like stacked storytelling
4. Gallery-led visual cadence
5. Swiss grid discipline
6. Asymmetric premium marketing flow

### Signature Components (pick exactly 4)
- Diagonal Staggered Square Masonry
- 3D Cascading Card Deck
- Hover-Accordion Slice Layout
- Pristine Gapless Bento Grid
- Infinite Brand Marquee Strip
- Turning Polaroid Arc
- Vertical Rhythm Lines
- Off-Grid Editorial Layout
- Product UI Panel Stack
- Split Testimonial Quote Wall
- Oversized Metrics Strip
- Layered Image Crop Frames

### Motion-Implied Language (pick exactly 2)
- Scrubbing text reveal energy
- Pinned narrative section energy
- Staggered float-up energy
- Parallax image drift energy
- Smooth accordion expansion energy
- Cinematic fade-through energy

### Composition Anchor (per-section, vary across page)
- Centered statement
- Top-left lead, support bottom-right
- Bottom-left text over background image
- Bottom-right CTA cluster
- Left-third caption + right-two-thirds visual (use sparingly)
- Right-third caption + left-two-thirds visual
- Centered low (text in lower 40%)
- Off-grid editorial offset
- Stacked center
- Image-as-canvas with text overlaid

### Background Mode (per-section, vary across page)
- Solid surface with inline asset
- Subtle texture / paper / grid
- Full-bleed image background with tonal overlay
- Editorial side-image (50/50, 60/40, 40/60)
- Image as entire visual + text overlaid
- Flat color block + detail crop as accent
- Cinematic tonal gradient
- Atmospheric photo with color grade
- Duotone treated image
- Soft radial vignette + product crop
- Micro-noise gradient over solid
- Color-blocked diptych

### CTA Variation
- Classic primary pill
- Outline / ghost
- Underlined inline link with arrow
- Banner-style full-width CTA
- Oversized headline + tiny CTA hint
- CTA as caption under a strong visual

### Hero Scale (per-page, pick 1)
- Giant Statement Hero — massive type, large image, dominant viewport
- Mid Editorial Hero — balanced type/image, cinematic
- Mini Minimalist Hero — tiny logo + short statement + thin CTA, lots of negative space

### Narrative / Concept Spine (pick 1, thread through the page)
- Artifact / collectible
- Journey / pilgrimage
- Tool / precision instrument
- Living system / garden
- Stage / spotlight
- Archive / dossier

### Second-Read Moment (pick exactly 1, place once)
- Asymmetric bleed that respects hierarchy
- One oversized punctuation or numeral serving structure
- Single unexpected material switch
- Narrow vertical side-rail editorial note style
- Macro crop that carries brand color naturally

---

## 3. FRONTEND REFERENCE RULE

Every generated image must clearly communicate:
- Layout and section hierarchy
- Spacing and typography scale
- Visual rhythm
- CTA priority
- Component styling
- Image treatment
- Overall design system

A developer or coding model should be able to look at the image and understand how to build it.

---

## 4. HERO MINIMALISM RULES

- Hero must feel like a strong opening scene
- Keep composition clean, do not overcrowd
- Main headline: 5-10 strong words, not a paragraph
- Keep supporting text concise
- Prioritize negative space and contrast
- Avoid stuffing with pills, fake stats, badges, tiny logos

### Typography Execution
Prefer: medium / normal / light elegance, tight tracking, controlled line count, strong scale contrast
Avoid: random extra-bold shouting, gradient text as lazy premium effect, 6-line headings

---

## 5. IMAGE COUNT & PAGE SLICING

### Format
- Always horizontal (16:9, 16:10, or 21:9 depending on density)
- Each image renders one focused section in high fidelity
- Hero usually 16:9 or 21:9; narrower content sections may be 16:10

### Continuity Rule
Across all per-section images, enforce:
- Same palette and accent logic
- Same typography family and scale
- Same CTA family
- Same border radius language
- Same image treatment (color grade, materials, framing)
- Same tonal voice in any short copy

---

## 6. CREATIVITY ESCALATION RULE

Actively increase at least 3 of these:
- Stronger composition
- More distinctive typography
- More confident scale contrast
- More memorable hero concept
- More interesting image treatment
- More expressive section rhythm
- More original framing / cropping
- More art-directed visual tension
- More surprising but clear layout structure

---

## 7. ANTI-AI-SLOP RULES

### Layout slop
- Endless centered sections
- Identical card rows repeated section after section
- Cloned left-text/right-image blocks
- Perfect but lifeless symmetry everywhere

### Visual slop
- Default purple/blue AI gradients
- Too many glowing edges
- Floating spheres / blobs everywhere
- Glassmorphism stacked without reason

### Typography slop
- Giant heading + weak tiny subcopy
- Too many font moods
- Gradient headline as shortcut for "premium"

### Content slop
- "Unleash", "Elevate", "Revolutionize", "Next-Gen", "Seamless"
- "Acme", "Nexus", "Flowbit", "Quantumly", "NovaCore"

### Density slop
- Over-packed sections
- Card overload
- Tiny spacing between major sections

---

## 8. COLOR & MATERIAL RULES

### Palette Discipline
- 1 primary (brand anchor)
- 1 secondary (supporting tone)
- 1 accent (used sparingly for CTA / highlight)
- A neutral scale (background, surface, text, hairline)

### Gradient Discipline
Allowed: low-chroma palette-matched tonal gradients, single-hue atmospheric grades, soft vignettes, noise-textured gradients
Banned: rainbow / mesh blob gradients, purple-to-blue "AI" defaults, pink-to-orange "creator" defaults

---

## 9. MULTI-IMAGE CONSISTENCY RULE

Across all per-section frames enforce:
- Same brand world
- Same type scale logic
- Same spacing discipline
- Same CTA family
- Same icon or illustration mood
- Same image treatment
- Same tonal language in any copy

Variation IS allowed in composition anchor, background mode, section size and density.

---

## 10. CLARITY CHECK

Before finalizing, verify:

1. Is the hierarchy obvious?
2. Is the hero clean enough?
3. Is the design visually distinctive?
4. Is it free of obvious AI tells?
5. Is it premium rather than template-like?
6. Can someone code from this?
7. Do multiple images clearly belong together?
8. Is imagery used strongly enough?
9. Does the page breathe?
10. Is there enough spacing between sections?
11. Is composition varied across sections?
12. Is the hero scale chosen and executed cleanly?
13. Is there a clear conversion path?
14. Is the palette consistent across all images?
15. Is each image horizontal and one-section-only?
16. Is the total number of images equal to the number of sections?
17. Is the hero using a varied composition?

---

## 11. DEFAULT SITE PACKS

### 4-section pack
1. Hero
2. Features
3. Social proof / testimonial
4. CTA

### 8-section pack
1. Hero
2. Trust bar
3. Features
4. Product showcase
5. Benefits / use cases
6. Testimonials
7. Pricing
8. CTA

### 12-section pack
1. Hero
2. Trust bar
3. Feature grid
4. Product preview
5. Problem / solution
6. Benefits
7. Workflow
8. Metrics / proof / integration
9. Testimonials
10. Pricing
11. FAQ
12. CTA + footer
