---
name: anti-slop
description: Use when building UI components to enforce anti-generic design rules — no emoji icons, no generic gradients, proper spacing, and motion that follows design principles. Includes Brief Inference, Three Dials (VARIANCE/MOTION/DENSITY), design system mapping, and comprehensive AI-tell prevention.
model: gpt-5-nano
version: 2.0.0
preamble-tier: 1
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "anti slop"
  - "generic design"
  - "ai generated ui"
  - "design quality"
  - "ui consistency"
disable-model-invocation: true
metadata:
  origin: agent-master-skills
  plugin-for: ui-craft
  phase: BUILD
  preferred-model: gpt-5-nano
  ports: taste-skill
---

<!-- TOKEN CEILING: ~4K -->

# Anti-Slop Plugin (v2 — taste-skill port)

## 0. BRIEF INFERENCE (Read the Room Before Anything Else)

Before touching code or tweaking dials, **infer what the user actually wants**. Most LLM design output is bad because the model jumps to a default aesthetic instead of reading the room.

### 0.A Read these signals first
1. **Page kind** — landing (SaaS / consumer / agency / event), portfolio (dev / designer / creative studio), redesign (preserve vs overhaul), editorial / blog.
2. **Vibe words** the user used — "minimalist", "calm", "Linear-style", "Awwwards", "brutalist", "premium consumer", "Apple-y", "playful", "serious B2B", "editorial", "agency-y", "glassy", "dark tech".
3. **Reference signals** — URLs they linked, screenshots they pasted, products they named, brands they're competing with.
4. **Audience** — B2B procurement panel vs. design-conscious consumer vs. recruiter scanning a portfolio. The audience picks the aesthetic, not your taste.
5. **Brand assets that already exist** — logo, color, type, photography. For redesigns, these are starting material, not optional input.
6. **Quiet constraints** — accessibility-first audiences, public-sector, regulated industries, trust-first commerce, kids' products. These constraints OVERRIDE aesthetic preference.

### 0.B Output a one-line "Design Read" before generating
Before any code, state in one line: **"Reading this as: \<page kind> for \<audience>, with a \<vibe> language, leaning toward \<design system or aesthetic family>."**

### 0.C If the brief is ambiguous, ask one question, do not guess
Ask exactly **one** clarifying question — never a multi-question dump — and only when the design read genuinely diverges.

### 0.D Anti-Default Discipline
Do not default to: AI-purple gradients, centered hero over dark mesh, three equal feature cards, generic glassmorphism on everything, infinite-loop micro-animations everywhere, Inter + slate-900. These are the LLM defaults. Reach past them deliberately based on the design read.

---

## 1. THE THREE DIALS (Core Configuration)

After the design read, set three dials. Every layout, motion, and density decision below is gated by these.

* **`DESIGN_VARIANCE: 8`** — 1 = Perfect Symmetry, 10 = Artsy Chaos
* **`MOTION_INTENSITY: 6`** — 1 = Static, 10 = Cinematic / Physics
* **`VISUAL_DENSITY: 4`** — 1 = Art Gallery / Airy, 10 = Cockpit / Packed Data

**Baseline:** `8 / 6 / 4`. Use these unless the design read overrides them.

### 1.A Dial Inference (design read → dial values)
| Signal | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| "minimalist / clean / calm / editorial / Linear-style" | 5-6 | 3-4 | 2-3 |
| "premium consumer / Apple-y / luxury / brand" | 7-8 | 5-7 | 3-4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9-10 | 8-10 | 3-4 |
| "landing page / portfolio / marketing site (default)" | 7-9 | 6-8 | 3-5 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3-4 | 2-3 | 4-5 |
| "redesign - preserve" | match existing | +1 | match existing |
| "redesign - overhaul" | +2 | +2 | match existing |

### 1.B Use-Case Presets
| Use case | VARIANCE | MOTION | DENSITY |
|---|---|---|---|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Landing (Premium consumer) | 7 | 6 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |

---

## 2. BRIEF → DESIGN SYSTEM MAP

Once you have the design read and dials, pick the right foundation.

### 2.A When to reach for a real design system
| Brief reads as… | Reach for |
|---|---|
| Microsoft / enterprise SaaS / dashboards | `@fluentui/react-components` |
| Google-ish UI, Material-flavored product | `@material/web` + Material 3 tokens |
| IBM-style B2B / enterprise analytics | `@carbon/react` + `@carbon/styles` |
| Shopify app surfaces | Polaris web components |
| Atlassian / Jira-style product | `@atlaskit/*` + `@atlaskit/tokens` |
| GitHub-style devtool / community page | `@primer/css` or `@primer/react-brand` |
| Public-sector UK service | `govuk-frontend` |
| US public-sector / trust-first | `uswds` |
| Fast local-business / agency MVP | Bootstrap 5.3 |
| Modern accessible React foundation | `@radix-ui/themes` |
| Modern SaaS where you own the components | shadcn/ui |
| Tailwind-based modern SaaS / AI marketing | Tailwind v4 utilities + `dark:` variant |

**Honesty rule:** if the brief reads as one of the systems above, install and use the **official** package. Do not recreate its CSS by hand.

**One system per project.** Do not mix Fluent React with Carbon in the same tree.

### 2.B When the brief is an aesthetic, not a system
| Aesthetic | Honest implementation |
|---|---|
| Glassmorphism / "frosted glass" | `backdrop-filter`, layered borders, highlight overlays. Provide solid-fill fallback for `prefers-reduced-transparency`. |
| Bento (Apple-style tile grids) | CSS Grid with mixed cell sizes. No single library owns this. |
| Brutalism | Native CSS, monospace, raw borders. No library. |
| Editorial / magazine | Serif type, asymmetric grid, generous whitespace. No library. |
| Dark tech / hacker | Mono + accent neon, terminal motifs. No library. |
| Aurora / mesh gradients | SVG or layered radial gradients. No library. |
| Kinetic typography | Native CSS animations, scroll-driven animations, GSAP for hijacks. No library. |

---

## 3. DEFAULT ARCHITECTURE & CONVENTIONS

Unless the design read picks a real design system, these are the defaults:

### 3.A Stack
* **Framework:** React or Next.js. Default to Server Components (RSC).
* **Styling:** **Tailwind v4** (default). Tailwind v3 only if the existing project demands it.
* **Animation:** **Motion** (`import { motion } from "motion/react"`).
* **Fonts:** Always use `next/font` (Next.js) or self-host with `@font-face` + `font-display: swap`. Never link Google Fonts via `<link>` in production.

### 3.B State
* Local `useState` / `useReducer` for isolated UI.
* Global state ONLY for deep prop-drilling avoidance — Zustand, Jotai, or React context.
* **NEVER** use `useState` to track continuous values driven by user input (mouse position, scroll progress, pointer physics, magnetic hover). Use Motion's `useMotionValue` / `useTransform` / `useScroll`.

### 3.C Icons
* **Allowed libraries (priority order):** `@phosphor-icons/react`, `hugeicons-react`, `@radix-ui/react-icons`, `@tabler/icons-react`.
* **Discouraged:** `lucide-react`. Acceptable only when the user explicitly asks for it or the project already depends on it.
* **NEVER hand-roll SVG icons.** If a glyph is missing, install a second library or compose from primitives.
* **One family per project.** Do not mix Phosphor with Lucide in the same component tree.
* **Standardize `strokeWidth` globally** (e.g. `1.5` or `2.0`).

### 3.D Emoji Policy
Discouraged by default in code, markup, and visible text. Replace symbols with icon-library glyphs. Allow emojis only when the user explicitly asks for a playful / chat-style / social-native vibe.

### 3.E Responsiveness & Layout Mechanics
* Standardize breakpoints (`sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`).
* Contain page layouts using `max-w-[1400px] mx-auto` or `max-w-7xl`.
* **Viewport Stability:** NEVER use `h-screen` for full-height Hero sections. ALWAYS use `min-h-[100dvh]`.
* **Grid over Flex-Math:** NEVER use complex flexbox percentage math. ALWAYS use CSS Grid.

### 3.F Dependency Verification (mandatory)
Before importing ANY 3rd-party library, check `package.json`. If the package is missing, output the install command first. **Never** assume a library exists.

---

## 4. DESIGN ENGINEERING DIRECTIVES (Bias Correction)

LLMs default to clichés. Override these defaults proactively.

### 4.1 Typography
* **Display / Headlines:** Default `text-4xl md:text-6xl tracking-tighter leading-none`.
* **Body / Paragraphs:** Default `text-base text-gray-600 leading-relaxed max-w-[65ch]`.
* **Sans font choice:**
  * **Discouraged as default:** `Inter`. Pick `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`, or a brand-appropriate serif first.
  * **Override:** Inter is acceptable when the user explicitly asks for a neutral / standard / Linear-style feel, or when the brief is a public-sector / accessibility-first site.
* **Pairings to know:** `Geist` + `Geist Mono`, `Satoshi` + `JetBrains Mono`, `Cabinet Grotesk` + `Inter Tight`, `GT America` + `IBM Plex Mono`.

* **SERIF DISCIPLINE (VERY DISCOURAGED AS DEFAULT):**
  * Serif is **very discouraged as the default font for any project.** "It feels creative / premium / editorial" is NOT a reason to reach for serif.
  * **Serif is only acceptable when ONE of these is explicitly true:**
    - The brand brief literally names a serif font, OR
    - The aesthetic family is genuinely editorial / luxury / publication / manuscript / heritage / vintage AND you can articulate why this specific serif fits this specific brand
  * For everything else, **default sans-serif display** (Geist Display, ABC Diatype, Söhne Breit, Cabinet Grotesk Display, Migra Sans, GT Walsheim, Inter Display, PP Neue Montreal).
  * **EMPHASIS RULE:** When you want to emphasize a word within a headline, use **italic or bold of the SAME font**. Do NOT inject a random serif word into a sans headline.
  * **Specifically BANNED as defaults:** `Fraunces` and `Instrument_Serif` (the two LLM-favorite display serifs).

* **ITALIC DESCENDER CLEARANCE (mandatory):** When italic is used in display type and the word contains a descender letter (`y g j p q`), `leading-[1]` or `leading-none` will clip the descender. Use `leading-[1.1]` minimum and add `pb-1` or `mb-1` reserve.

### 4.2 Color Calibration
* Max 1 accent color. Saturation < 80% by default.
* **THE LILA RULE:** The "AI Purple / Blue glow" aesthetic is discouraged as a default. No automatic purple button glows, no random neon gradients. Use neutral bases (Zinc / Slate / Stone) with high-contrast singular accents.
* **One palette per project.** Do not fluctuate between warm and cool grays within the same project.
* **COLOR CONSISTENCY LOCK (mandatory):** Once an accent color is chosen for a page, it is used on the WHOLE page.

* **PREMIUM-CONSUMER PALETTE BAN (mandatory):**
  * For premium-consumer briefs (cookware, wellness, artisan, luxury, heritage craft, DTC home goods, etc.) the LLM default is **warm beige/cream + brass/clay/oxblood/ochre + espresso/ink dark text**. This palette is BANNED as the default.
  * **Default alternatives (rotate, do not reuse):**
    - **Cold Luxury:** silver-grey + chrome + smoke
    - **Forest:** deep green + bone + amber accent
    - **Black and Tan:** true off-black + warm tan, sharp contrast, no beige
    - **Cobalt + Cream:** saturated blue against a single neutral, no brass
    - **Terracotta + Slate:** warm rust against cool grey, no brass
    - **Olive + Brick + Paper:** muted olive plus brick-red accent
    - **Pure monochrome + single saturated pop:** off-white + off-black + one bright accent

### 4.3 Layout Diversification
* **ANTI-CENTER BIAS:** Centered Hero / H1 sections are avoided when `DESIGN_VARIANCE > 4`. Force "Split Screen" (50/50), "Left-aligned content / right-aligned asset", "Asymmetric white-space", or scroll-pinned structures.
* **Override:** centered hero is OK for editorial / manifesto / launch-announcement briefs where the message itself is the design.

### 4.4 Materiality, Shadows, Cards
* Use cards ONLY when elevation communicates real hierarchy. Otherwise group with `border-t`, `divide-y`, or negative space.
* When a shadow is used, tint it to the background hue. No pure-black drop shadows on light backgrounds.
* **SHAPE CONSISTENCY LOCK (mandatory):** Pick ONE corner-radius scale for the page and stick to it.

### 4.5 Interactive UI States
LLMs default to "static successful state only." Always implement full cycles:
* **Loading:** Skeletal loaders matching the final layout's shape. Avoid generic circular spinners.
* **Empty States:** Beautifully composed; indicate how to populate.
* **Error States:** Clear, inline (forms), or contextual (toasts only for transient).
* **Tactile Feedback:** On `:active`, use `-translate-y-[1px]` or `scale-[0.98]` to simulate a physical push.
* **BUTTON CONTRAST CHECK (mandatory, a11y):** Before shipping any button, verify the button text is readable against the button background. WCAG AA min (4.5:1 for body, 3:1 for large text 18px+).
* **CTA BUTTON WRAP BAN (mandatory):** Button text MUST fit on one line at desktop. If a label wraps to 2 or 3 lines, the button is broken. Fix by EITHER shortening the label (3 words max for primary CTAs) OR widening the button.
* **NO DUPLICATE CTA INTENT (mandatory):** Two CTAs with the same intent on one page is a Pre-Flight Fail. Pick ONE label per intent and use it everywhere.
* **FORM CONTRAST CHECK (mandatory, a11y):** Form inputs, placeholder text, focus rings, helper text, and error text all pass WCAG AA contrast against the section background.

### 4.6 Data & Form Patterns
* Label ABOVE input. Helper text optional but present in markup. Error text BELOW input. Standard `gap-2` for input blocks.
* No placeholder-as-label. Ever.

### 4.7 Layout Discipline (Hard Rules)

* **Hero MUST fit in the initial viewport.** Headline max 2 lines on desktop, subtext max **20 words** AND max 3-4 lines, CTAs visible without scroll.
* **Hero font-scale discipline.** Plan font size and image size *together*. Default sensible range: `text-4xl md:text-5xl lg:text-6xl` for most heroes; `text-6xl md:text-7xl` only when the headline is 3-5 words.
* **HERO TOP PADDING CAP (mandatory):** Hero top padding max `pt-24` (≈6rem) at desktop.
* **HERO STACK DISCIPLINE (max 4 text elements).** The hero is a single moment, not a feature list. Allowed text elements, max 4 in total:
  1. Eyebrow (small uppercase label) OR brand strip OR neither — pick zero or one
  2. Headline (max 2 lines, see above)
  3. Subtext (max 20 words, max 4 lines)
  4. CTAs (1 primary + max 1 secondary)
  - **BANNED in the hero:** tiny tagline below CTAs, trust micro-strip, pricing teaser, feature bullet list, social-proof avatar row.
* **"Used by" / "Trusted by" logo wall belongs UNDER the hero, never inside it.**
* **Navigation MUST render on a single line on desktop.** A two-line nav at desktop is broken design.
* **Navigation height cap: 80px max desktop, default 64-72px.**
* **Bento grids MUST have rhythm, not one-sided repetition.**
* **BENTO CELL COUNT RULE (mandatory):** A bento grid has EXACTLY as many cells as you have content for. No empty cells.
* **Section-Layout-Repetition Ban.** Once you use a layout family for a section, that family can appear at most ONCE on the page.
* **ZIGZAG ALTERNATION CAP (mandatory).** Max 2 sections in a row with image+text-split pattern. The 3rd consecutive image+text split is a Pre-Flight Fail.
* **EYEBROW RESTRAINT (mandatory).** Maximum 1 eyebrow per 3 sections. Hero counts as 1.
* **SPLIT-HEADER BAN (mandatory).** The "left big headline + right small explainer paragraph" pattern is banned as default.
* **Bento Background Diversity (mandatory).** At least 2-3 cells in any multi-cell grid need real visual variation.
* **Mobile collapse must be explicit per section.**

### 4.8 Image & Visual Asset Strategy

Landing pages and portfolios are **visual products**. Text-only pages with fake-screenshot divs are slop.

**Priority order for visual assets:**
1. **Image-generation tool first.** If ANY image-gen tool is available, you MUST use it to create section-specific assets.
2. **Real web images second.** Use `https://picsum.photos/seed/{descriptive-seed}/{w}/{h}` for placeholder photography.
3. **Last resort: tell the user.** Leave clearly-labeled placeholder slots and ask for images.

**Even minimalist sites need real images.** A pure-text page is not minimalism.

**Real company logos for social proof.** Use real SVG logos from Simple Icons (`https://cdn.simpleicons.org/{slug}/ffffff`). **LOGO-ONLY rule (mandatory):** logo wall = logos and nothing else. No industry / category labels below each logo.

**Hand-rolled illustrations are strongly discouraged.** Acceptable only when the brief explicitly calls for it.

**Div-based fake screenshots are banned.** A "hand-built product preview" rendered with `<div>` rectangles is a Tell.

**Hero needs a real visual.** Text + gradient blob is not a hero — it's a placeholder.

### 4.9 Content Density

* **Default content shape per section:** short headline (≤ 8 words) + short sub-paragraph (≤ 25 words) + one visual asset OR one CTA.
* **No data-dump sections.** Use top 3-5 highlights + "View full list" link, or marquee / carousel.
* **Long lists need a different UI component, not a longer list.** For > 5 items, reach for: 2-column split, card grid, tabs / accordion, horizontal scroll-snap pills, carousel, or marquee.
* **COPY SELF-AUDIT (mandatory before ship):** Before declaring any task done, re-read every visible string on the page. Flag any string that is grammatically broken, has unclear referents, sounds like AI hallucination, or reads like an LLM trying to sound thoughtful.
* **Fake-precise numbers are flagged.** Numbers like `92%`, `4.1×`, `48k` are banned unless they come from real data or are explicitly labeled as mock.
* **One copy register per page.** Don't mix technical mono, editorial prose, and marketing punch in the same composition.

### 4.10 Quotes & Testimonials
* **Max 3 lines** of quote body.
* Attribution: name + role + (optionally) company. Never name only.
* Quote marks: use real typographic quotes ( " " ) or none at all. Not straight ASCII.

### 4.11 Page Theme Lock (Light / Dark Mode Consistency)
The page has ONE theme. Sections do not invert. Pick light, dark, or auto (`prefers-color-scheme`) at the page level and lock it.

---

## 5. CONTEXT-AWARE PROACTIVITY

These are tools, not defaults. Use them when the design read calls for them.

* **Liquid Glass / Glassmorphism:** Appropriate for premium consumer, Apple-adjacent, luxury brand, or media-overlay vibes. When used, go beyond `backdrop-blur`: add a 1px inner border and a subtle inner shadow. Provide a solid-fill fallback under `prefers-reduced-transparency`.
* **Magnetic Micro-physics:** Use when `MOTION_INTENSITY > 5` AND the brief reads premium / playful / agency. Implement EXCLUSIVELY with Motion's `useMotionValue` / `useTransform` outside the React render cycle.
* **Perpetual Micro-Interactions:** Use when `MOTION_INTENSITY > 5` AND the section actively benefits from motion. Apply Spring Physics — no linear easing.
* **"Motion claimed, motion shown."** If `MOTION_INTENSITY > 4`, the page must actually move. A static page that claims `MOTION_INTENSITY: 7` is broken.
* **MOTION MUST BE MOTIVATED (mandatory).** Before adding any animation, ask: "what does this animation communicate?" Valid answers: hierarchy, storytelling, feedback, state transition. Invalid answer: "it looked cool".
* **MARQUEE MAX-ONE-PER-PAGE (mandatory).** Two or more marquees on the same page reads as lazy filler.
* **GSAP Sticky-Stack Pattern** and **GSAP Horizontal-Pan Pattern** — see canonical skeletons in taste-skill Section 5.A / 5.B.
* **Scroll-Reveal Stagger** — prefer Motion's `whileInView` over GSAP for simple reveals.

### 5.A Forbidden Animation Patterns
* **`window.addEventListener("scroll", ...)`** is banned. Use Motion's `useScroll()`, GSAP's `ScrollTrigger`, IntersectionObserver, or CSS `scroll-driven animations`.
* **Custom scroll progress calculations using `window.scrollY`** in React state. Same reason.
* **`requestAnimationFrame` loops that touch React state.** Use motion values instead.
* **NEVER mix GSAP / Three.js with Motion in the same component tree.** They fight over the same frames.

---

## 6. PERFORMANCE & ACCESSIBILITY GUARDRAILS

### 6.A Hardware Acceleration
* Animate ONLY `transform` and `opacity`. Never animate `top`, `left`, `width`, `height`.

### 6.B Reduced Motion (mandatory)
* **Any motion above `MOTION_INTENSITY > 3` MUST honor `prefers-reduced-motion`.** This is non-negotiable.
* Infinite loops, parallax, scroll-hijack, and magnetic physics MUST collapse to static / instant under reduced motion.

### 6.C Dark Mode (mandatory for any consumer-facing page)
* Design for **both modes from the start**. Never ship light-only or dark-only without explicit user instruction.
* Respect `prefers-color-scheme: dark`. Default to system preference unless the brand insists on one mode.

### 6.D Core Web Vitals Targets
* **LCP** < 2.5s. Hero image must be `next/image priority` or preloaded.
* **INP** < 200ms. Heavy work off main thread.
* **CLS** < 0.1. Reserve space for images, fonts, embeds.
* Run Lighthouse before declaring a page done.

### 6.E DOM Cost
* Apply grain / noise filters EXCLUSIVELY to fixed, `pointer-events-none` pseudo-elements.
* Be aware of bundle size. Lazy-load anything that's not above-the-fold.

### 6.F Z-Index Restraint
NEVER spam arbitrary `z-50` or `z-10`. Use z-index strictly for systemic layer contexts.

---

## 7. DIAL DEFINITIONS (Technical Reference)

### DESIGN_VARIANCE (Level 1-10)
* **1-3 (Predictable):** Symmetrical CSS Grid, equal paddings, centered alignment.
* **4-7 (Offset):** `margin-top: -2rem` overlaps, varied image aspect ratios, left-aligned headers.
* **8-10 (Asymmetric):** Masonry layouts, CSS Grid with fractional units, massive empty zones.
* **MOBILE OVERRIDE:** For levels 4-10, asymmetric layouts above `md:` MUST collapse to strict single-column on viewports `< 768px`.

### MOTION_INTENSITY (Level 1-10)
* **1-3 (Static):** No automatic animations. CSS `:hover` and `:active` states only.
* **4-7 (Fluid CSS):** `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. `animation-delay` cascades.
* **8-10 (Advanced Choreography):** Complex scroll-triggered reveals, parallax, scroll-driven animation.

### VISUAL_DENSITY (Level 1-10)
* **1-3 (Art Gallery):** Lots of white space. Huge section gaps (`py-32` to `py-48`).
* **4-7 (Daily App):** Standard web app spacing (`py-16` to `py-24`).
* **8-10 (Cockpit):** Tight paddings. No card boxes; 1px lines separate data.

---

## 8. DARK MODE PROTOCOL

Dual-mode by default. Never assume light-only unless the brief is print-emulating editorial.

### 8.A Token Strategy (pick one, stick to it)
* **Tailwind `dark:` variant** (default for utility-first projects).
* **CSS variables** (for shadcn/ui, Radix Themes, or component libraries with theming).

### 8.B Do Not Prescribe Specific Colors Here
The brief and brand decide. This skill enforces only:
* **Contrast** — WCAG AA minimum for body text, AAA target for hero copy.
* **Hierarchy parity** — visual hierarchy that works in light must work in dark.
* **Brand fidelity** — primary brand color stays recognisable.
* **No pure `#000000` and no pure `#ffffff`** — use off-black and off-white.

### 8.C Default Mode
Respect `prefers-color-scheme` unless the brand insists. Add a manual toggle if either mode would lose key brand expression.

### 8.D Test in Both Modes Before Finishing
Open the page in both modes during development. Do not ship a page you've only seen in one mode.

---

## 9. AI TELLS (Forbidden Patterns)

### 9.A Visual & CSS
* **NO neon / outer glows** by default. Use inner borders or subtle tinted shadows.
* **NO pure black (`#000000`).** Off-black, zinc-950, or charcoal.
* **NO oversaturated accents.** Desaturate to blend with neutrals.
* **NO excessive gradient text** for large headers.
* **NO custom mouse cursors.** Outdated, accessibility-hostile, perf-hostile.

### 9.B Typography
* **AVOID Inter as default.** See Section 4.1. Override path exists.
* **NO oversized H1s** that just scream. Control hierarchy with weight + color, not raw scale.
* **Serif constraints:** Serif for editorial / luxury / publication. Not for dashboards.

### 9.C Layout & Spacing
* **Mathematically perfect** padding and margins. No floating elements with awkward gaps.
* **NO 3-column equal feature cards.** The generic "three identical cards horizontally" feature row is banned. Use 2-column zig-zag, asymmetric grid, scroll-pinned, or horizontal-scroll alternative.

### 9.D Content & Data ("Jane Doe" Effect)
* **NO generic names.** "John Doe", "Sarah Chan", "Jack Su" → use creative, realistic, locale-appropriate names.
* **NO generic avatars.** No SVG "egg" or Lucide user icons → use believable photo placeholders or specific styling.
* **NO fake-perfect numbers.** Avoid `99.99%`, `50%`, `1234567`. Use organic, messy data (`47.2%`, `+1 (312) 847-1928`).
* **NO startup-slop brand names.** "Acme", "Nexus", "SmartFlow", "Cloudly" → invent contextual, premium names that sound real.
* **NO filler verbs.** "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize" → concrete verbs only.

### 9.E External Resources & Components
* **NO hand-rolled SVG icons.** Use Phosphor / HugeIcons / Radix / Tabler. Lucide on explicit request only.
* **NO div-based fake screenshots.** Never build a fake product UI out of `<div>` rectangles to simulate a screenshot. Use real images, generated images, or skip the preview.
* **NO broken Unsplash links.** Use `https://picsum.photos/seed/{descriptive-string}/{w}/{h}`.
* **shadcn/ui customization:** Allowed, but NEVER in default state.

### 9.F Production-Test Tells (banned outright)

**Hero & top-of-page**
* **NO version labels in the hero.** `V0.6`, `v2.0`, `BETA`, `INVITE-ONLY PREVIEW`, `EARLY ACCESS`, `ALPHA` — banned as default eyebrows.
* **NO "Brand · No. 01"-style sub-eyebrows.**

**Section numbering & micro-labels**
* **NO section-number eyebrows.** `00 / INDEX`, `001 · Capabilities`, `06 · how it works` — banned.
* **NO `01 / 4`-style pagination on images or bento tiles.**
* **NO `Scroll · 001 Capabilities`-style scroll cues.**
* **NO "Index of Work, 2018 - 2026"-style range labels** as eyebrows.

**Separators & dots**
* **The middle-dot (`·`) is rationed.** Maximum 1 per line in metadata strips.
* **NO decorative colored status dots on every list/nav/badge.** Only for actual semantic state.

**Em-dashes & typography flourishes**
* **NO em-dash (`—`) as a design element OR anywhere else.** The em-dash character is forbidden in headlines, eyebrows, pills, body copy, quotes, attribution, captions, button text, and alt text. Use the regular hyphen (`-`).
* **NO `<br>`-broken-and-italicized headlines** as a default "design move."
* **NO vertical rotated text.** Agency-portfolio cliché.
* **NO crosshair / hairline grid lines as decoration.**

**Fake product previews**
* **NO div-based fake product UI in the hero.** It is the #1 LLM-design Tell. Use a real screenshot, a generated image, a real component preview, or none at all.
* **NO fake version footers** inside fake screenshots.

**Marketing-copy Tells**
* **NO "Quietly in use at" / "Quietly trusted by"** social-proof headers. Use "Trusted by", "Used at", or skip the heading.
* **NO "From the field" / "Field notes" / "Currently on the bench" / "On our desks" / "Loose plates" style poetic labels.**
* **NO weather / locale strips** ("LIS 14:23 · 18°C") in headers/footers.
* **NO micro-meta-sentences under eyebrows.**
* **NO generic step labels.** "Stage 1 / Stage 2 / Stage 3" — banned. Use the verb-noun directly.

**Pills, labels and version stamps**
* **NO pills/labels/tags overlaid on images.**
* **NO photo-credit captions as decoration.** Photo credit is allowed ONLY when there is a real photographer being credited.
* **NO version footers on marketing pages.** `v1.4.2`, `Build 0048`, `last sync 4s ago · main` — banned.
* **NO "Reservation 412 of 800"-style live-stock counters** as decoration.

**Decoration text strips**
* **NO decoration text strip at hero bottom.** `BRAND. MOTION. SPATIAL.`, `TYPE / FORM / MOTION` — banned.
* **NO floating top-right sub-text in section headings.**

**Lists, dividers and scoring**
* **NO `border-t` + `border-b` on every row** of a long list / spec table.
* **NO scoring/progress bars with filled background tracks** as comparison visuals.

**Locale, time, scroll cues**
* **Locale / city-name / time / weather strips are banned for 99% of briefs.**
* **Scroll cues are banned.** `Scroll`, `↓ scroll`, `Scroll to explore`.
* **ZERO decorative status dots by default.**

### 9.G EM-DASH BAN (the single most-violated Tell)

**Em-dash (`—`) is COMPLETELY banned.** It is the LLM's signature stylistic crutch and it is the #1 visual Tell in production tests. There is no "limited use" allowance. None.

* **Banned in headlines.** Use a period or a comma.
* **Banned in eyebrows / labels / pills / button text / image captions / nav items.** Replace with line breaks, columns, or hairlines.
* **Banned in body copy.** Restructure the sentence: two sentences with a period, OR a comma, OR parentheses, OR a colon.
* **Banned in quote attribution.** Use a normal hyphen with spaces (` - `) or a line break + smaller-weight name.
* **Banned in en-dash form too (`–`)** when used as a separator. Date ranges (`2018-2026`) use a hyphen. Number ranges (`€40-80k`) use a hyphen.

The ONLY permitted dash characters on the page are:
* Regular hyphen `-` (for compound words, ranges, line dividers in markup)
* Minus sign in math (`-5°C`)

If your output contains a single `—` or `–` anywhere visible to the user, the output fails the Pre-Flight Check and must be rewritten.

---

## 10. REFERENCE VOCABULARY (Pattern Names the Agent Should Know)

### Hero Paradigms
* **Asymmetric Split Hero** — Text on one side, asset on the other, generous white space.
* **Editorial Manifesto Hero** — Large type, no asset, almost-poster.
* **Video / Media Mask Hero** — Type cut out as mask over video background.
* **Kinetic-Type Hero** — Animated typography as the primary visual.
* **Curtain-Reveal Hero** — Hero parts on scroll like a curtain.
* **Scroll-Pinned Hero** — Hero stays pinned while content scrolls behind.

### Navigation & Menus
* **Mac OS Dock Magnification** — Edge nav, icons scale fluidly on hover.
* **Magnetic Button** — Pulls toward cursor.
* **Gooey Menu** — Sub-items detach like viscous liquid.
* **Dynamic Island** — Morphing pill for status / alerts.
* **Contextual Radial Menu** — Circular menu expanding at click point.
* **Floating Speed Dial** — FAB springing into curved secondary actions.
* **Mega Menu Reveal** — Full-screen dropdown, stagger-fade content.

### Layout & Grids
* **Bento Grid** — Asymmetric tile grouping (Apple Control Center).
* **Masonry Layout** — Staggered grid, no fixed row height.
* **Chroma Grid** — Borders / tiles with subtle animating gradients.
* **Split-Screen Scroll** — Two halves sliding in opposite directions.
* **Sticky-Stack Sections** — Sections that pin and stack on scroll.

### Cards & Containers
* **Parallax Tilt Card** — 3D tilt tracking mouse coordinates.
* **Spotlight Border Card** — Borders illuminate under cursor.
* **Glassmorphism Panel** — Frosted glass with inner refraction.
* **Holographic Foil Card** — Iridescent rainbow shift on hover.
* **Tinder Swipe Stack** — Physical card stack, swipe-away.
* **Morphing Modal** — Button expands into its own dialog.

### Scroll Animations
* **Sticky Scroll Stack** — Cards stick and physically stack.
* **Horizontal Scroll Hijack** — Vertical scroll → horizontal pan.
* **Locomotive / Sequence Scroll** — Video / 3D sequence tied to scrollbar.
* **Zoom Parallax** — Central background image zooming on scroll.
* **Scroll Progress Path** — SVG line drawing along scroll.
* **Liquid Swipe Transition** — Page transition like viscous liquid.

### Galleries & Media
* **Dome Gallery** — 3D panoramic gallery.
* **Coverflow Carousel** — 3D carousel with angled edges.
* **Drag-to-Pan Grid** — Boundless draggable canvas.
* **Accordion Image Slider** — Narrow strips expanding on hover.
* **Hover Image Trail** — Mouse leaves popping image trail.
* **Glitch Effect Image** — RGB-channel shift on hover.

### Typography & Text
* **Kinetic Marquee** — Endless text bands reversing on scroll.
* **Text Mask Reveal** — Massive type as transparent window to video.
* **Text Scramble Effect** — Matrix-style decoding on load / hover.
* **Circular Text Path** — Text curving along spinning circle.
* **Gradient Stroke Animation** — Outlined text with running gradient.
* **Kinetic Typography Grid** — Letters dodging the cursor.

### Micro-Interactions & Effects
* **Particle Explosion Button** — CTA shatters into particles on success.
* **Liquid Pull-to-Refresh** — Reload indicator like detaching droplets.
* **Skeleton Shimmer** — Shifting light reflection across placeholders.
* **Directional Hover-Aware Button** — Fill enters from cursor's exact side.
* **Ripple Click Effect** — Wave from click coordinates.
* **Animated SVG Line Drawing** — Vectors drawing themselves in real time.
* **Mesh Gradient Background** — Organic lava-lamp blobs.
* **Lens Blur Depth** — Background UI blurred to focus foreground action.

### Animation Library Choice
* **Motion (`motion/react`)** — default for UI / Bento / state-change motion.
* **GSAP + ScrollTrigger** — for full-page scrolltelling and scroll hijacks.
* **Three.js / WebGL** — for canvas backgrounds and 3D scenes.
* **NEVER mix GSAP / Three.js with Motion in the same component tree.**

---

## 11. FINAL PRE-FLIGHT CHECK

Run this matrix before outputting code. This is the last filter.

**THIS IS NOT OPTIONAL. Run every box. If any box fails, the output is not done.**

- [ ] **Brief inference** declared (Section 0.B one-liner)?
- [ ] **Dial values** explicit and reasoned from the brief?
- [ ] **Design system** chosen from Section 2 if applicable, or aesthetic labeled honestly?
- [ ] **ZERO em-dashes (`—`) anywhere on the page?**
- [ ] **Page Theme Lock**: ONE theme for the whole page?
- [ ] **Color Consistency Lock**: one accent color used identically across all sections?
- [ ] **Shape Consistency Lock**: one corner-radius system applied consistently?
- [ ] **Button Contrast Check**: every CTA text is readable against its background (WCAG AA 4.5:1)?
- [ ] **CTA Button Wrap**: no CTA label wraps to 2+ lines at desktop?
- [ ] **Form Contrast Check**: form inputs, placeholders, focus rings, labels all pass WCAG AA?
- [ ] **Serif discipline**: if a serif is used, it is NOT Fraunces or Instrument_Serif?
- [ ] **Premium-consumer palette check**: if premium-consumer, palette is NOT the AI-default beige+brass?
- [ ] **Italic descender clearance**: every italic word with `y g j p q` has `leading-[1.1]` min + `pb-1` reserve?
- [ ] **Hero fits the viewport**: headline ≤ 2 lines, subtext ≤ 20 words AND ≤ 4 lines, CTA visible?
- [ ] **Hero top padding**: max `pt-24` at desktop?
- [ ] **Hero stack discipline**: max 4 text elements in hero?
- [ ] **EYEBROW COUNT (mechanical)**: count ≤ ceil(sectionCount / 3)?
- [ ] **Split-Header Ban**: no "left big headline + right small explainer paragraph" pattern?
- [ ] **Zigzag Alternation Cap**: no 3+ consecutive sections with the same image+text-split layout?
- [ ] **No Duplicate CTA Intent**: no two CTAs with the same intent?
- [ ] **Logo wall = logo only**: no industry / category labels below logos?
- [ ] **Bento Background Diversity**: at least 2-3 bento cells have real visual variation?
- [ ] **Copy Self-Audit**: every visible string re-read, no grammatically-broken or AI-hallucinated phrases?
- [ ] **Motion motivated**: every animation can be justified in one sentence?
- [ ] **Marquee max-one-per-page**: no two horizontal marquees on the same page?
- [ ] **Navigation on ONE line** at desktop, height ≤ 80px?
- [ ] **Section-Layout-Repetition** check: at least 4 different families across 8 sections?
- [ ] **Bento has rhythm AND exact cell count** (N items → N cells)?
- [ ] **Long lists use the right UI component** (not default `<ul>` with `divide-y` for > 5 items)?
- [ ] **Real images used** — NO div-based fake screenshots, NO hand-rolled decorative SVGs, NO pure-text minimalism?
- [ ] **No pills/labels overlaid on images**?
- [ ] **No photo-credit captions as decoration**?
- [ ] **No version footers** on marketing pages?
- [ ] **No micro-meta-sentences** under eyebrows?
- [ ] **No decoration text strip at hero bottom**?
- [ ] **No floating top-right sub-text** in section headings?
- [ ] **No scoring/progress bars with filled background tracks**?
- [ ] **No locale / city-name / time / weather strips** unless brief is genuinely globally-distributed?
- [ ] **No scroll cues**?
- [ ] **No version labels in hero** unless the brief is a launch?
- [ ] **No section-numbering eyebrows**?
- [ ] **No decorative dots** (zero by default)?
- [ ] **No `border-t` + `border-b` on every row** of long lists / spec tables?
- [ ] **Content density** sane: no 20-row data tables, ≤ 25-word sub-paragraphs by default?
- [ ] **Quotes ≤ 3 lines** of body, attribution clean?
- [ ] **Motion claimed = motion shown**?
- [ ] **No `window.addEventListener('scroll')`** — using Motion useScroll / ScrollTrigger / IntersectionObserver only?
- [ ] **Reduced motion** wrapped for everything `MOTION_INTENSITY > 3`?
- [ ] **Dark mode** tokens defined and tested in both modes?
- [ ] **Mobile collapse** explicit per section?
- [ ] **Viewport stability**: `min-h-[100dvh]`, never `h-screen`?
- [ ] **`useEffect` animations** have strict cleanup functions?
- [ ] **Empty / loading / error** states provided?
- [ ] **Icons** from an allowed library only?
- [ ] **Motion** isolated in client-leaf components with `'use client'`?
- [ ] **No AI Tells** from Section 9?
- [ ] **Core Web Vitals** plausibly hit (LCP < 2.5s, INP < 200ms, CLS < 0.1)?
- [ ] **One design system** per project?

If a single checkbox cannot be honestly ticked, the page is not done. Fix it before delivering.
