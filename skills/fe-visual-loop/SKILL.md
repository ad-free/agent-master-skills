---
name: fe-visual-loop
description: >-
  Use when building a new screen or page, a redesign, or component work too big to free-style but smaller than
  a full ui-craft run. Reference-first loop: starts from real reference sites the user picks (the agent finds
  3-5 when none is given), extracts their structure into DESIGN.md, fills real content, mocks from the
  reference, gets an explicit pick, builds, then has ui-verifier compare build and reference at the same
  widths. Invoked by: dev-craft (Design step), ui-craft (Phases 2/3/8).
metadata:
  version: 2.1.0
  origin: agent-master-skills
  domain: frontend
  integrates-with: [ui-craft, anti-slop, image-to-design-spec, ui-verifier, verification-before-completion]
---

# FE Visual Loop v2

## Iron Law

```
NO MOCK WITHOUT A PICKED REFERENCE. NO BUILD WITHOUT A PICKED MOCK. NO SHIP WITHOUT A SIDE-BY-SIDE PROOF.
```

Directions invented from adjectives ("editorial minimal", "warm boutique") come out generic; designs improve when
they copy the structure of a real, finished site. The agent finds references and shows them; the human picks.

## When to Use

- New page, new screen, new section set, or a redesign.
- Inside `ui-craft` Phases 2/3 (reference and direction gate) and 8 (proof gate).

**When NOT to use:** a tweak inside an existing screen (spacing, a field, a colour fix): follow the screen's
existing pattern and `dev-craft/references/frontend-design.md`.

## Design lock (once per project; check it first)

Measured: on the same "improve this page" task, a locked hand-over scored 7.9/10 blind against 6.9 for the
same model with skills alone, and 5.6 for a stronger model with skills alone. A stronger model or more skill text
does not replace a designer's hand-over; the lock does. The model keeps re-inventing a look when nothing pins it.

- **Lock exists** (`DESIGN.md` marked `Status: locked`, with theme tokens and `design/` pattern screenshots):
  it is the spec. Implement the screen against it with the repo's components; skip Steps 1-5; no new look, no
  new tokens. A rule the lock does not cover: follow its nearest pattern and add the gap to the handoff.
- **No lock and the task is a new screen, a redesign, or "make it look professional"**: build the lock first
  with Steps 1-5, then record it once:
  - `DESIGN.md`: `Status: locked`, the picked references, tokens (font, type scale of 4-5 sizes, spacing scale,
    radius, one accent, status colours as soft pills), page frame (top bar, header with one filled primary),
    and each core pattern spelled out (list: KPI cards, status tabs with counts, table rules, row menu with
    confirm on destroy, footer count; form; detail), each with its 390 behaviour stated (row cards instead of
    a table, tabs that scroll or turn into a select, no horizontal page scroll) and a short Do-not list.
  - Theme tokens in the project's theme file (CSS variables / Tailwind `@theme`, MUI `createTheme`), so code
    can only use the locked values.
  - `design/<pattern>.html` plus `-1440.png` and `-390.png` for each core pattern, approved by the user (Step 5).
  Later screens reuse the lock: they cost one implementation, not another reference loop.

## The Loop

### Step 1: Reference (hard gate)

- The user gave references (URLs, screenshots, a template, a competitor): use them, go to Step 2.
- None given: find 3 to 5 real sites or template demos in the same category and audience (a PPE shop -> live
  industrial-supply shops and storefront template demos; an HR app -> real HR products' public screens). Prefer
  finished, popular, current sites over award showcases.
- Screenshot each with the Playwright MCP at 1440 and 390 (above the fold plus one full page), saved under the
  state folder (`.dev-craft/refs/` or `.ui-craft/refs/`). Visit only the candidate URLs.
- A site blocks the browser (403, CAPTCHA): skip it without trying to get around it and try the next candidate.
  Template demo stores (Shopify theme demos, marketplace live previews) rarely block; try 8 candidates before
  giving up.
- Present them side by side with one line each: what it does well for this brief, what to avoid.
- **Stop and wait for a pick** ("B", or "B's layout with D's product cards"). Record the pick, URLs and
  screenshot paths in state (`.ui-craft/` or `.dev-craft/`, or session notes when standalone).
- No browser or no network: say so, ask the user for 1 to 3 reference URLs or screenshots, and wait. Never fall
  back to inventing directions.

### Step 2: Extract

From the picked reference, write to the project's `DESIGN.md` (create it if missing, under a `## Reference`
heading; keep existing tokens, they win):

- Section inventory in order (e.g. header, promo bar, hero, category tiles, best sellers, trust row, footer).
- Grid: container width, columns, gutters, at 1440 and 390.
- Type scale: sizes, weights, line heights, font family (nearest licensed or free equivalent).
- Spacing rhythm: section padding, card gaps.
- Colour roles: background, surface, text, muted, one accent, status colours.
- Image treatment: aspect ratios, crop, background, how products or people are shown.
- Density: items per row, how much text per card.

Use `image-to-design-spec` on the screenshots for the measurable parts.

### Step 3: Content (hard gate)

Real content before layout: the layout is judged with the content it will hold.

- Use the project's real data if it exists (seed files, CMS export, product feed, API).
- Otherwise write realistic content for the domain: for a shop at least 12 distinct products with real-sounding
  names, prices, variants and categories; real category names; trust content (certifications, shipping, returns,
  reviews with names and dates).
- Never repeat one item to fill a grid, never "Lorem ipsum", "Product 1" or placeholder grey boxes where an image
  belongs (use a licensed or generated product-style image, or a labelled image slot the user must fill).

### Step 4: Mock (live HTML, not AI images)

- Build the page as a static HTML mock in a scratch dir that follows the extracted structure and tokens, with the
  Step 3 content. At most 2 variants, and only where the reference leaves a real choice open.
- Screenshot each at 1440 and 390, next to the reference at the same widths.

### Step 5: Pick (hard gate)

- Show reference and mock side by side; ask the human to pick or name changes.
- Record the pick and screenshot paths in state. **Implementation is blocked until a pick is recorded.**

### Step 6: Build to the pick

- Implement with the project's stack, components and tokens; follow the mock's structure, spacing and content.
  Deviations need a stated reason.
- Spend boldness in one place: one memorable element, everything around it quiet. Before Proof, remove one
  decoration that does not serve the brief.

### Step 7: Proof (hard gate)

- Dispatch the `ui-verifier` agent with the brief, run command, routes, the picked reference and mock
  screenshots, and `DESIGN.md`. It compares build and reference side by side at 1440 and 390.
- Fix every high-severity defect, then run `ui-verifier` again. Done only when a second pass returns no
  high-severity visual defect, or the user records a waiver with a reason.
- Hand off reference, mock and build screenshots side by side.

## Redesign rule

A redesign starts from a new reference (Step 1), and the new mock is a new file. A rejected mock is never edited
into the next attempt: patching a rejected design keeps its structure, which is what was rejected.

## Licence

A template or site is a reference for structure, rhythm and density. Copying its code, images, icons, fonts or
copy needs a licence the user holds; say which assets the reference uses that the project may not, and use
licensed or free equivalents.

## Integration

- `dev-craft` Design step: new screen or redesign runs this loop; the user approves screenshots, not a text
  `design.md`.
- `ui-craft`: Phase 2 exit = Step 1 reference picked and Step 5 mock picked; Phase 3 preview = Step 4 mocks;
  Phase 8 SHIP = Step 7 proof.
- `anti-slop` sets dials and bans LLM defaults; the reference wins where they disagree, except accessibility.
- Evidence from Steps 5 and 7 feeds `verification-before-completion` (no pass without proof screenshots or a
  recorded waiver).
