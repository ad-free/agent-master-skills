# Design Dials — ui-craft ALIGN Phase Reference

**Source:** Aggregated from taste-skill/design-taste-frontend  
**Purpose:** Explicit design intent for every project. Set in ALIGN, governs all DESIGN/BUILD decisions.

---

## Three Dials (Global Variables)

| Dial | Range | Default | Meaning |
|------|-------|---------|---------|
| `DESIGN_VARIANCE` | 1–10 | 8 | 1 = Perfect Symmetry / 10 = Artsy Chaos |
| `MOTION_INTENSITY` | 1–10 | 6 | 1 = Static / 10 = Cinematic/Physics |
| `VISUAL_DENSITY` | 1–10 | 4 | 1 = Art Gallery / 10 = Cockpit |

**Usage:** Reference these exact variable names in DESIGN/BUILD. Never invent aliases (`LAYOUT_VARIANCE`, `ANIM_LEVEL`, etc.).

---

## Dial Inference (Design Read → Dial Values)

| Signal | VARIANCE | MOTION | DENSITY |
|--------|----------|--------|---------|
| "minimalist / clean / calm / editorial / Linear-style" | 5–6 | 3–4 | 2–3 |
| "premium consumer / Apple-y / luxury / brand" | 7–8 | 5–7 | 3–4 |
| "playful / wild / Dribbble / Awwwards / experimental / agency" | 9–10 | 8–10 | 3–4 |
| "landing page / portfolio / marketing site (default)" | 7–9 | 6–8 | 3–5 |
| "trust-first / public-sector / regulated / accessibility-critical" | 3–4 | 2–3 | 4–5 |
| "redesign — preserve" | match existing | +1 | match existing |
| "redesign — overhaul" | +2 | +2 | match existing |

---

## Use-Case Presets

| Use Case | VARIANCE | MOTION | DENSITY |
|----------|----------|--------|---------|
| Landing (SaaS, mainstream) | 7 | 6 | 4 |
| Landing (Agency / creative) | 9 | 8 | 3 |
| Landing (Premium consumer) | 7 | 6 | 3 |
| Portfolio (Designer / studio) | 8 | 7 | 3 |
| Portfolio (Developer) | 6 | 5 | 4 |
| Editorial / Blog | 6 | 4 | 3 |
| Public-sector service | 3 | 2 | 5 |
| Redesign — preserve | match | match+1 | match |
| Redesign — overhaul | +2 | +2 | match |

---

## How Dials Drive Output

**DESIGN_VARIANCE**
- 1–3: Symmetrical CSS Grid (12-col, equal fr), equal paddings, centered alignment
- 4–7: Offset margins (`margin-top: -2rem`), varied aspect ratios (4:3 next to 16:9), left-aligned headers over centered data
- 8–10: Masonry, fractional grid (`2fr 1fr 1fr`), massive empty zones (`padding-left: 20vw`)
- **Mobile override (4–10):** Asymmetric layouts above `md:` MUST collapse to strict single-column (`w-full`, `px-4`, `py-8`) on `< 768px`

**MOTION_INTENSITY**
- 1–3: No auto animations. CSS `:hover`/`:active` only. `prefers-reduced-motion` is default
- 4–7: `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. `animation-delay` cascades for load-ins. Focus on `transform`/`opacity`
- 8–10: Complex scroll-triggered reveals, parallax, scroll-driven animation (CSS `animation-timeline` or GSAP ScrollTrigger). Motion hooks. **NEVER `window.addEventListener('scroll')`** — hard ban
- **Reduced motion:** Any motion > 3 MUST honor `prefers-reduced-motion`. Motion: wrap with `useReducedMotion()`. CSS: gate behind `@media (prefers-reduced-motion: no-preference)` or provide `@media (prefers-reduced-motion: reduce)` disable block. Infinite loops, parallax, scroll-hijack, magnetic physics MUST collapse to static/instant

**VISUAL_DENSITY**
- 1–3: Lots of whitespace. Huge section gaps (`py-32` to `py-48`). Expensive, clean
- 4–7: Standard web app spacing (`py-16` to `py-24`)
- 8–10: Tight paddings. No card boxes; 1px lines separate data. **Mandatory: `font-mono` for all numbers**

---

## Design Read (One-Line Declaration)

**Before any code, state in one line:**

> "Reading this as: `<page kind>` for `<audience>`, with a `<vibe>` language, leaning toward `<design system or aesthetic family>`."

Examples:
- "Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind utilities + Geist + restrained motion."
- "Reading this as: Solo designer portfolio for hiring managers, with an editorial/kinetic-type language, leaning toward native CSS + scroll-driven animation + custom typography."
- "Reading this as: Redesign of a public-sector service site, with a trust-first language, leaning toward GOV.UK Frontend or USWDS."

**If brief ambiguous → ask ONE clarifying question.** Never a multi-question dump. Only when design read genuinely diverges.

---

## Anti-Default Discipline

**Do NOT default to:** AI-purple gradients, centered hero over dark mesh, three equal feature cards, generic glassmorphism on everything, infinite-loop micro-animations everywhere, Inter + slate-900.

**These are LLM defaults. Reach past them deliberately based on the design read.**

---

## Decision Log (ALIGN Phase)

Record in `context.md`:

```markdown
## Design Dials
DESIGN_VARIANCE: <value>
MOTION_INTENSITY: <value>
VISUAL_DENSITY: <value>

## Design Read
Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <design system or aesthetic family>.

## Design System Selection
[ ] Official package (Section 2.A) — specify which
[ ] Aesthetic build (Section 2.B) — specify which
```
