# AI Tells — Quick Reference (Banned by Default)

**Source:** taste-skill, image-to-code-skill, redesign-skill  
**Use in:** ui-craft DESIGN/REVIEW phases — mechanical grep check

---

## HARD BANS (Fail Build)

### Visual
- [ ] Neon/outer glows (unless "cyberpunk" brief)
- [ ] Pure `#000000` background
- [ ] Accent saturation > 80%
- [ ] Purple/blue "AI gradient" aesthetic
- [ ] Custom mouse cursors
- [ ] Floating blobs everywhere
- [ ] Random futuristic details without structure
- [ ] Over-rendered noise hiding layout

### Typography
- [ ] `Inter` as default sans (unless "neutral/Linear/public-sector")
- [ ] Serif for dashboards/B2B SaaS (unless editorial/luxury/heritage)
- [ ] `Fraunces` / `Instrument Serif` as default display serif
- [ ] Mixed-family emphasis (random serif word in sans headline)
- [ ] Italic descender clipping (`leading-none` on `y/g/j/p/q`)
- [ ] Eyebrow abuse (> ceil(sections/3))
- [ ] Title Case On Every Header
- [ ] > 3 font moods per page
- [ ] Body text > 65ch line width

### Layout
- [ ] Everything centered & symmetrical
- [ ] Three equal card columns (feature row)
- [ ] `height: 100vh` (use `min-height: 100dvh`)
- [ ] Complex flex percentage math (use CSS Grid)
- [ ] No max-width container
- [ ] Uniform border-radius on everything
- [ ] No overlap/depth (flat adjacency)
- [ ] Symmetrical vertical padding (top=bottom always)
- [ ] Dashboard = left sidebar only
- [ ] Hero overflows viewport (CTA below fold)
- [ ] Hero > 3 lines headline
- [ ] Hero top padding > `pt-24` (6rem) desktop
- [ ] Hero stack > 4 text elements
- [ ] Banned in hero: trust micro-strip, pricing teaser, feature bullets, social proof avatars
- [ ] "Used by" logo wall INSIDE hero
- [ ] Nav wraps to 2 lines desktop
- [ ] Nav height > 80px
- [ ] Bento with empty cells
- [ ] Section layout family repeated > 1x
- [ ] Zigzag (L/R image-text) > 2 consecutive
- [ ] Split-header as default (L headline + R paragraph)
- [ ] Bento: 6 white-on-white text-only cards
- [ ] Mobile collapse not explicit per section

### Interactivity
- [ ] No hover states on buttons
- [ ] No active/pressed feedback
- [ ] 0-duration transitions
- [ ] Missing focus ring
- [ ] Generic circular spinners for loading
- [ ] Dead links (`href="#"`)
- [ ] No active nav indicator
- [ ] Animating `top/left/width/height` (use `transform`+`opacity`)
- [ ] Button text wraps at desktop
- [ ] Duplicate CTA intent on one page
- [ ] Form inputs fail WCAG AA contrast

### Content
- [ ] "John Doe" / "Jane Smith"
- [ ] Fake round numbers: 99.99%, 50%, $100.00
- [ ] "Acme Corp" / "Nexus" / "SmartFlow"
- [ ] AI clichés: Elevate, Seamless, Unleash, Next-Gen, Game-changer, Delve, Tapestry, "In the world of..."
- [ ] Exclamation marks in success messages
- [ ] "Oops!" error messages
- [ ] Lorem Ipsum
- [ ] Quote > 3 lines
- [ ] Em-dashes as design flourish in quotes
- [ ] Straight ASCII quotes `"`
- [ ] Attribution: name only ("- Sarah")

### Components
- [ ] Generic card (border+shadow+white)
- [ ] Always 1 filled + 1 ghost button
- [ ] Pill "New"/"Beta" badges
- [ ] Accordion FAQ
- [ ] 3-card carousel testimonials with dots
- [ ] 3-tower pricing (equal height)
- [ ] Modals for everything
- [ ] Avatar circles exclusively
- [ ] Light/dark = only sun/moon toggle
- [ ] Footer 4-column link farm
- [ ] Lucide/Feather as default icons
- [ ] Rocket=Launch, Shield=Security clichés
- [ ] Inconsistent icon stroke weights
- [ ] Missing favicon
- [ ] Stock "diverse team" photos
- [ ] Div soup (no semantic HTML)
- [ ] Inline styles mixed with CSS classes
- [ ] Hardcoded pixel widths
- [ ] Missing alt on meaningful images
- [ ] Arbitrary `z-index: 9999`
- [ ] Commented dead code
- [ ] Import not in package.json
- [ ] Missing meta tags (title, description, og:image, social)

---

## Premium-Consumer Palette Ban

**If brief = cookware/wellness/artisan/luxury/heritage/DTC home goods:**

| Category | BANNED Hex Families |
|----------|---------------------|
| Backgrounds | `#f5f1ea`, `#f7f5f1`, `#fbf8f1`, `#efeae0`, `#ece6db`, `#faf7f1`, `#e8dfcb` (warm paper/cream/chalk/bone) |
| Accents | `#b08947`, `#b6553a`, `#9a2436`, `#9c6e2a`, `#bc7c3a`, `#7d5621` (brass/clay/oxblood/ochre) |
| Text | `#1a1714`, `#1a1814`, `#1b1814` (espresso/warm near-black) |

**Rotate alternatives (never reuse previous):**
- Cold Luxury: silver-grey + chrome + smoke
- Forest: deep green + bone + amber
- Black & Tan: true off-black + warm tan
- Cobalt + Cream: saturated blue + single neutral
- Terracotta + Slate: warm rust + cool grey
- Olive + Brick + Paper: muted olive + brick accent
- Monochrome + Pop: off-white + off-black + electric blue/emerald/hot pink

**Palette-rotation rule:** If previous premium project used beige+brass, this one MUST use different family.

---

## Strategic Omissions (What AI Forgets)

- [ ] Privacy/Terms links in footer
- [ ] "Back" navigation (no dead ends)
- [ ] Custom 404 page
- [ ] Form validation (email, required, format)
- [ ] Skip-to-content link
- [ ] Cookie consent (if jurisdiction requires)

---

## SOFT BANS (Flag for Discussion)

- Glassmorphism without reason
- `Inter` when premium/consumer
- Accordion FAQ
- 3-card carousel testimonials
- Avatar circles only
- Sun/moon toggle only
- Footer link farm
- Lucide/Feather icons

---

## Usage

**DESIGN Phase:** After design read + dials set, review this list. Any HARD ban = redesign that element.

**REVIEW Phase:** Mechanical grep. Any HARD ban = FAIL. SOFT ban = flag for human discussion.

**Never** use these as defaults. Reach past them deliberately per design read.
