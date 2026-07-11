---
name: ui-craft
description: UI/UX engineering pipeline with persistent memory. Use when given a prompt, PLAN.md, or feature request — runs LOAD → AUDIT → ALIGN → DESIGN → SOURCE → BUILD → REVIEW → HARDEN → SHIP. Detects stack versions, generates design tokens + component code + visual preview, enforces accessibility gates, and resumes across sessions via .ui-craft/ state.
---

# ui-craft

## Overview

A single pipeline that turns a UI/UX prompt into production-quality design tokens, component code, and visual previews. Every phase has a clear goal, exit criteria, and a human checkpoint. The pipeline persists state to `.ui-craft/` so work survives across sessions.

**Philosophy:** Design-first, version-aware, human-orchestrated. You remain in control. Skip any phase. Edit any phase. The pipeline serves you, not the other way around.

## When to Use

- Given a prompt, PLAN.md, or feature request for UI/UX work
- Starting a new project or feature (greenfield)
- Improving an existing project's UI/UX (existing codebase)
- A task that spans multiple components or pages
- Resuming work from a previous session
- Any time you need more than a single-component change

**When NOT to use:** Single-line CSS fixes, typo corrections, trivial color changes where the full pipeline is overkill.

## The Memory System

The project's `.ui-craft/` directory is created on first run and persists across sessions:

```
.ui-craft/
├── state.json              # { currentPhase, completed: [], stack: {...}, slices: [...] }
├── plan.md                 # Evolving plan from ALIGN → DESIGN
├── context.md              # Domain glossary (shared language)
├── decisions/              # ADRs — key design decisions captured
│   └── 001-*.md
├── sessions/               # Handoff docs for context rotation
│   └── session-YYYYMMDD-N.md
├── design-system/          # Persisted design system (Master + Overrides)
│   ├── MASTER.md
│   └── pages/
├── preview/                # Generated HTML previews
│   ├── design-system.html
│   └── components.html
└── tokens/                 # Generated design token files
    ├── tailwind.config.ts
    ├── tokens.css
    └── theme.ts
```

### Resume Logic

| Scenario | Behavior |
|---|---|
| `.ui-craft/` does not exist | Detect existing code: Phase 1 (AUDIT) if codebase exists, Phase 2 (ALIGN) if greenfield |
| `state.json` exists, `currentPhase > 0` | Load state, skip completed phases, restore glossary |
| `state.json` says all phases complete | Ask "New feature on same project?" — preserves design system/ADRs |
| Context near limit mid-phase | Generate handoff doc, save slice position, resume next session |

## Stack Detection + Version Resolution

Run during Phase 2 (ALIGN). This is a critical differentiator — every piece of generated code must match the exact framework version.

### Version Detection Sources

| Source | Detects | Example |
|--------|---------|---------|
| `package.json` | React, Next.js, Vue, shadcn, Tailwind | `"react": "^19.0.0"` |
| `tailwind.config.*` | Tailwind v3 (JS) vs v4 (CSS-first) | CSS-first = v4 |
| `tsconfig.json` | TypeScript target | `"target": "ES2022"` |
| `npx shadcn@latest` | shadcn/ui version | v2.0+ |
| User prompt | Manual override | "I want React 18" |

### Version Resolution Logic

```
1. Check package.json / dependency files → exact version
2. If not found → ask user with default = latest stable
3. If "latest" → fetch from npm registry (npm view <package> version)
4. Store exact version in state.json
5. During SOURCE phase, fetch docs for that exact version
6. During BUILD, use only patterns valid for that version
7. During REVIEW, flag any deprecated patterns
```

### Version-Aware Code Generation Rules

| Stack | Version | Patterns to Use | Patterns to Avoid |
|-------|---------|-----------------|-------------------|
| **React** | 19 | `useActionState`, `use()`, Server Components, `useOptimistic` | Class components, legacy context, `UNSAFE_*` |
| **React** | 18 | `useTransition`, `useDeferredValue`, `Suspense`, `useId` | `UNSAFE_componentWillMount`, legacy lifecycle |
| **Next.js** | 15 | App Router, Server Actions, `next/navigation` | Pages Router, `getServerSideProps` |
| **Next.js** | 14 | App Router, `getServerSideProps` | `getInitialProps`, `next/router` |
| **Tailwind** | v4 | `@import "tailwindcss"`, CSS-first config | `@tailwind` directives, JS config |
| **Tailwind** | v3 | `tailwind.config.js`, `@tailwind` directives | v1/v2 syntax |
| **shadcn/ui** | v2 | `cn()` helper, new-york style, `npx shadcn add` | v1 component API |
| **TypeScript** | 5.x | `satisfies`, `const` type params, decorators | legacy enum patterns |

### Version Resolution Flow

```
1. Check package.json / dependency files → exact version
2. If not found → ask user: "What version of [framework]?" with default = latest
3. If "latest" → fetch from npm registry (npm view <package> version)
4. Store in state.json
5. During SOURCE phase, fetch docs for that exact version
6. During BUILD, use only patterns valid for that version
7. During REVIEW, flag any deprecated patterns
```

---

## Pipeline Phases

```
[0] LOAD ──→ [1] AUDIT ──→ [2] ALIGN ──→ [3] DESIGN ──→ [4] SOURCE ──→ [5] BUILD ──→ [6] REVIEW ──→ [7] HARDEN ──→ [8] SHIP
                  │              │              │               │              │             │               │             │
                  ▼              ▼              ▼               ▼              ▼             ▼               ▼             ▼
              Health         CONTEXT.md     Design system   Fetched       UI code +    UX + a11y     Polish +      Commit +
              report         (shared        + tokens +      docs          tokens +     audit +       dark mode +   ADRs +
              (remediate      language)      preview                      preview      version       responsive    state
               first?)                                                               audit                      complete
```

---

### [0] LOAD — Initialize or Resume

Read `.ui-craft/state.json`:

- **Not found** → Detect if the project has existing source code:
  - **Existing code** (`src/`, `app/`, `components/`, or equivalent directories with source files) → Set `stack: {}`, `completed: []`, `currentPhase: 1`. Run AUDIT first.
  - **Greenfield** (no source files yet) → Set `stack: {}`, `completed: []`, `currentPhase: 2`. Skip AUDIT — nothing to audit.
- **Found + all phases complete** → Ask human: "New feature on same project? (preserves design system/ADRs)" or "Start fresh?"
- **Found + incomplete** → Load `context.md` into working memory. Set `currentPhase` to next uncompleted phase. Restore slice progress if resuming mid-BUILD.

Write state after LOAD.

---

### [1] AUDIT — Project UI/UX Scan

**Goal:** Assess existing project's UI/UX health before adding new code. Surface design debt, accessibility issues, and deprecated patterns so the human can decide what to remediate first.

**Process:**

1. **Scan the project** for UI/UX health across these dimensions:

   **Stack Detection:**
   - Read `package.json`, `tsconfig.json`, `tailwind.config.*`, `next.config.*`, `vite.config.*`
   - Detect exact versions of React, Next.js, Vue, Tailwind, shadcn/ui, TypeScript
   - Detect CSS approach (Tailwind, CSS Modules, styled-components, vanilla CSS)

   **Component Inventory:**
   - Scan `src/`, `app/`, `components/` for UI component files
   - Identify component patterns (shadcn/ui, custom, library-based)
   - Count components, pages, layouts

   **Style Analysis:**
   - Detect color usage patterns (hex values, CSS variables, Tailwind classes)
   - Detect typography patterns (font families, sizes)
   - Detect spacing patterns (consistent or random)
   - Detect dark mode support

   **Accessibility Scan:**
   - Check for aria labels on interactive elements
   - Check for focus states
   - Check for semantic HTML
   - Check for color contrast (basic hex analysis)
   - Check for touch target sizes

   **Responsive Check:**
   - Detect breakpoints in CSS/Tailwind config
   - Check for mobile-specific patterns
   - Check for viewport meta tag

   **Version Audit:**
   - Check for deprecated patterns in existing code
   - Flag patterns that don't match the detected version

2. **Surface the report** as a structured list with locations:
   ```
   UI/UX HEALTH REPORT:
   
   STACK:
   - React 19.0.0 (package.json)
   - Tailwind CSS v4 (CSS-first config detected)
   - shadcn/ui v2.0+ (npx shadcn add)
   - TypeScript 5.5 (tsconfig.json)
   
   COMPONENTS: 12 components found in src/components/
   - 8 custom components
   - 4 shadcn/ui components
   
   FINDINGS:
   1. [ACCESSIBILITY] Missing focus states on 3 interactive elements
      → src/components/Navbar.tsx:15, src/components/Card.tsx:42
   2. [STYLE] Inconsistent color usage — 5 different blue hex values found
      → Define a single --color-primary token
   3. [DARK MODE] No dark mode support detected
   4. [RESPONSIVE] No breakpoints defined in tailwind.config
   5. [VERSION] React 18 patterns used but React 19 detected
      → Migrate to useActionState instead of manual form handling
   ```

3. **Ask the human to prioritize:**
   - "Fix these before proceeding? (Y/n)"
   - "Which ones should I remediate now?"
   - If human says skip → note the findings in `.ui-craft/state.json` for the REVIEW phase

4. **If remediation is approved** — fix each finding one at a time, re-run audit after each fix. Do NOT proceed to ALIGN until all chosen findings are resolved.

**Exit criterion:** Human has reviewed the report and either approved remediation or explicitly deferred.

**State write:** Save findings to `state.json` for cross-reference in REVIEW.

---

### [2] ALIGN — Grill + Detect + Glossary

**Goal:** Surface assumptions, sharpen requirements, detect stack versions, build shared language.

**Process:**

1. **Ask one question at a time** — each with your best guess attached. The human reacts faster to a wrong guess than generating from scratch.

2. **Surface assumptions:**
   ```
   ASSUMPTIONS:
   1. This is a web app (not native mobile)
   2. Target audience: C-end consumers
   3. Style direction: modern, minimal
   4. Platform: responsive web
   → Correct me now or I'll proceed with these.
   ```

3. **Define "Out of scope"** — explicitly state what is NOT being built.

4. **Detect stack + versions:**
   - For existing projects: read dependency files for exact versions
   - For new projects: ask user with default = latest stable
   - If "latest" → fetch from npm registry (`npm view <package> version`)
   - State explicitly:
   ```
   STACK DETECTED:
   - React 19.0.0 (package.json)
   - Tailwind CSS v4 (CSS-first config detected)
   - shadcn/ui v2.0+ (npx shadcn add)
   - TypeScript 5.5 (tsconfig.json)
   - Linter: ESLint 9.x
   - Formatter: Prettier 3.x
   ```

5. **Route to design style** — based on project type and user intent, suggest a UI style:
   | Project Type | Suggested Style | Description |
   |--------------|-----------------|-------------|
   | SaaS / Dashboard | Minimalism | Clean, functional, data-focused |
   | E-commerce | Glassmorphism | Modern, layered, visually rich |
   | Marketing / Landing | Bold Typography | Strong headlines, high contrast |
   | Portfolio / Agency | Editorial | Magazine-style, asymmetric layouts |
   | Enterprise / B2B | Neumorphism | Soft shadows, subtle depth |
   | Social / Community | Duotone | Two-color palette, striking visuals |
   | Mobile-first | Flat Design | Simple, fast-loading, clean |
   | Creative / Artistic | 3D / Isometric | Depth, dimension, creative flair |
   
   Ask user: "I suggest [style] for this project. Choose a different style or proceed?"

6. **Build glossary** — extract key terms from the conversation and write them to `context.md`.

**Exit criterion:** Human confirms the refined scope with an explicit yes.

**State write:** Save detected stack + versions to `state.json`. Save `context.md`.

---

### [3] DESIGN — Design System + Tokens + Preview

**Goal:** Generate a complete design system with design tokens, visual preview, and architecture decisions.

**Process:**

1. **Run design system generation** using the existing search engine:
    ```bash
    python3 ~/.opencode/skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system -p "Project Name"
    ```

2. **Figma integration** (if Figma MCP is available):
   - Export design tokens from Figma file
   - Extract color palette, typography, spacing from Figma styles
   - Generate components from Figma component library
   - Sync design decisions back to Figma
   - If no Figma MCP: skip and generate from scratch

3. **Generate design token files:**
   - `tailwind.config.ts` — colors, spacing, fonts, shadows, breakpoints
   - `tokens.css` — CSS custom properties
   - `theme.ts` — TypeScript theme object
   - `tokens.json` — Design token JSON

3. **Generate HTML style guide preview:**
   - Self-contained HTML file
   - Color palette with hex + CSS variable names
   - Typography scale rendered (h1-h6, body, small)
   - Component examples (buttons, cards, inputs, modals)
   - Light/dark mode toggle
   - Responsive preview with device frames

4. **Validate design system** for accessibility, contrast, and consistency:
    ```bash
    python3 scripts/validator.py validate-design-system
    ```

5. **Write ADRs** for every design decision:
    ```markdown
    # ADR-001: [Title]
    **Status:** Accepted
    **Context:** [Problem and constraints]
    **Decision:** [What we chose]
    **Alternatives:** [What else was considered and why rejected]
    **Consequences:** [Impact on codebase]
    ```

6. **Persist design system** to `.ui-craft/design-system/` (Master + Overrides pattern)

**Exit criterion:** Human reviews design system + tokens + preview. Explicit approval.

**State write:** Save `plan.md`. Save ADRs to `.ui-craft/decisions/`. Save design system to `.ui-craft/design-system/`.

---

### [4] SOURCE — Version-Aware Doc Verification

**Goal:** Verify framework decisions against official docs for the exact detected version. Training data is stale.

**Process:**

1. Read exact versions from `state.json` (detected in Phase 2).
2. For each framework/library being used, fetch the **specific official documentation page** for the feature being implemented. Not the homepage. Not a tutorial.
3. Extract key patterns, API signatures, and deprecation warnings.
4. Cite sources inline during the BUILD phase:
    ```typescript
    // Source: https://react.dev/reference/react/useActionState
    const [state, formAction, isPending] = useActionState(fn, initialState)
    ```
5. If documentation does not cover a pattern, flag it explicitly:
    ```
    UNVERIFIED: Could not find official docs for this pattern.
    Based on training data — verify before shipping.
    ```

**Source hierarchy:**
| Priority | Source | Example |
|---|---|---|
| 1 | Official docs | react.dev, tailwindcss.com, nextjs.org |
| 2 | Official blog/changelog | react.dev/blog |
| 3 | Web standards (MDN) | developer.mozilla.org |
| ❌ NOT authoritative | Stack Overflow, blog posts, training data | — |

6. **Present a source summary to the human:**
    ```
    SOURCE VERIFICATION SUMMARY:
    ✅ React 19 — fetched react.dev for useActionState, Server Components
    ✅ Tailwind v4 — fetched tailwindcss.com for CSS-first config
    ✅ shadcn/ui v2 — fetched ui.shadcn.com for component API
    ❌ No official docs found for this pattern — flagged UNVERIFIED
    → Any concerns before I proceed to BUILD?
    ```

**Exit criterion:** Official docs fetched and reviewed for ALL framework dependencies. Any UNVERIFIED pattern is explicitly noted and the human has acknowledged it.

**State write:** Save fetched source references to state for use in BUILD.

---

### [5] BUILD — Generate UI Code

**Goal:** Generate design token files, component code, and visual preview — one vertical slice at a time.

**Process:**

For each component/page from the plan:

1. **Generate design token files:**
   - `tailwind.config.ts` — colors, spacing, fonts, shadows, breakpoints
   - `tokens.css` — CSS custom properties
   - `theme.ts` — TypeScript theme object
   - `tokens.json` — Design token JSON

2. **Generate component code** using version-correct patterns:
   - React 19 → `useActionState`, Server Components, `use()` hook
   - React 18 → `useTransition`, `Suspense`, `useId`
   - Tailwind v4 → CSS-first config (`@import "tailwindcss"`)
   - Tailwind v3 → JS config (`tailwind.config.js`)
   - shadcn/ui v2 → new-york style, `cn()` helper
   - **Forms**: React Hook Form + Zod validation patterns
     - Login, signup, contact, settings, password reset
   - **Pages**: Landing, dashboard-layout, auth, settings, 404
   - **Tests**: Component testing (Vitest + React Testing Library + jest-axe)
     - button, card, input, modal, navbar tests
   - **Icons**: lucide-react, heroicons, phosphor, tabler, react-icons
     - Auto-detection + wrapper component generation
   - **Page templates**: Complete page layouts with navigation, content, and footer

3. **Generate HTML style guide preview** — self-contained HTML with all components

4. **Run lint/type checks** on all generated files → must pass

**Rules:**
- **Version-correct patterns only** — no deprecated APIs for the detected version
- **Scope discipline** — Do NOT touch code outside the slice. If you spot improvements, note them. Do not fix them now.
- **One slice at a time** — Do not implement multiple slices in one pass. The pipeline loops over slices.
- **Accessibility gates** — every component must pass: contrast ≥ 4.5:1, focus states visible, touch targets ≥ 44px, aria labels present

**Lint/Type checks are gating — every slice leaves the codebase cleaner than you found it.**

**Exit criterion:** All slices implemented. All lint/type checks pass. Every slice committed.

**State write:** Save completed slices to `state.json`. If context is > 80% full, generate handoff doc in `.ui-craft/sessions/`.

---

### [6] REVIEW — UX + Accessibility + Visual + Version Audit

**Goal:** Quality gate before shipping. Review across four axes.

**Process:**

Conduct a parallel review of the entire diff:

**Axis 1 — UX Best Practices:**
- Are interaction patterns consistent?
- Are error states handled (empty, loading, error, edge cases)?
- Is navigation intuitive?
- Are forms usable (inline validation, clear errors, proper labels)?
- Are animations meaningful (not gratuitous)?

**Axis 2 — Accessibility:**
- Color contrast ≥ 4.5:1 for body text, ≥ 3:1 for large text
- Focus states visible on all interactive elements
- Touch targets ≥ 44x44pt (iOS) / ≥ 48x48dp (Android)
- All interactive elements have aria labels
- Semantic HTML used (button, nav, main, heading hierarchy)
- `prefers-reduced-motion` respected
- Screen reader focus order matches visual order

**Axis 2b — Screen Reader Testing:**
- Test with NVDA (Windows) or VoiceOver (macOS)
- Verify all images have alt text
- Verify all form inputs have labels
- Verify all buttons have accessible names
- Verify page structure with headings (h1 → h2 → h3)
- Verify dynamic content updates with aria-live
- Verify modal focus trap and return focus

**Axis 3 — Visual Consistency:**
- Colors match the design system tokens (no ad-hoc hex values)
- Typography matches the design system (fonts, sizes, weights)
- Spacing follows the 4/8dp rhythm
- Shadows are consistent
- Border radii are consistent
- Icons come from a consistent set

**Axis 4 — Version Pattern Audit:**
- No deprecated APIs for the detected version
- Code follows patterns shown in current-version docs
- If source citations exist, they are for the correct version
- Lint/format/tests pass

**Axis 5 — Visual Regression:**
- Run Playwright/Cypress screenshot comparison against baseline
- Verify no unintended layout shifts
- Verify no color/typography regressions
- Verify responsive behavior at 375px, 768px, 1024px, 1440px
- If no baseline exists: capture screenshots as new baseline

**Axis 6 — UI Lint:**
- Check for design system violations (ad-hoc colors, inconsistent spacing)
- Check for unused CSS classes
- Check for missing responsive utilities
- Check for inconsistent border-radius/shadows
- Run automated UI lint tools (if available): `eslint-plugin-jsx-a11y`, `stylelint`

**Categorize every finding:**
| Label | Meaning | Action |
|---|---|---|
| Critical | Blocks merge | Must fix |
| _(no prefix)_ | Required | Must address |
| Nit | Minor, optional | Author may ignore |
| Optional | Suggestion | Worth considering |

**Exit criterion:** All Critical and Required findings resolved. Human approves.

**State write:** Save review findings.

---

### [7] HARDEN — Polish + Dark Mode + Responsive + Performance

**Goal:** Polish the UI across all dimensions without changing behavior.

**Process:**

**Dark Mode:**
- Ensure all colors have dark mode equivalents
- Verify contrast in both light and dark modes
- Test that no colors are hardcoded (all use tokens)

**Responsive:**
- Verify layout at 375px, 768px, 1024px, 1440px
- Check no horizontal scroll on mobile
- Check safe areas are respected
- Check touch targets ≥ 44px on mobile

**Animation:**
- Micro-interactions: 150-300ms with proper easing
- `prefers-reduced-motion` respected
- No layout-shifting animations
- Exit animations faster than enter animations

**Performance:**
- No layout shifts (CLS)
- Images have width/height attributes
- Fonts are preloaded
- No render-blocking resources

**Clean:**
- Remove all debug instrumentation
- Delete throwaway prototypes
- Check for unused CSS classes

**Exit criterion:** Zero findings. All polish applied. Human approves.

**State write:** Update state.

---

### [8] SHIP — Docs + Commit + Finalize

**Goal:** Deliver the work with full traceability.

**Process:**

1. **Update ADRs** — any decisions made during BUILD/HARDEN that weren't captured in Phase 3.
2. **Update CONTEXT.md** — add any new domain terms encountered.
3. **Generate final HTML style guide preview** — comprehensive preview of all components.
4. **Final verification:**
   - Lint + type + build — all must pass
   - Run secrets scanner on the diff
   - Dead code removed
   - Pre-delivery checklist verified
5. **Atomic commit:**
   ```
   type(scope): short imperative description

   - What changed and why
   - Key decisions (reference ADRs)
   - What was intentionally NOT done
   ```
6. **Define rollback strategy** — state the rollback plan in the commit body.
7. **Mark state as complete:**
   ```json
   { "status": "complete", "lastRun": "2026-07-11" }
   ```

**Exit criterion:** Clean commit with rollback plan. All lint/type/secrets pass. State marked complete.

---

### [H] HANDOFF — Cross-Session Context (Cross-Cutting)

**When to trigger:** Mid-phase when context is > 80% full, or when the human says "continue later".

**Process:**
1. Save all in-memory state to `.ui-craft/state.json`:
   - Current phase and slice position
   - Incomplete tasks
   - Pending decisions
2. Write a handoff document to `.ui-craft/sessions/session-YYYYMMDD-N.md`:
   - What was accomplished
   - What's in progress
   - What's next
   - Any decisions to be made
   - Known issues or blockers
3. Summarize to the human: "Session saved. Run ui-craft again to resume from the current phase."

---

## Workflow Orchestration

For complex features that span multiple domains (UI + backend + infrastructure), use workflow orchestration to coordinate multiple pipeline runs.

### Workflow Types

| Workflow | Description | Pipeline |
|----------|-------------|----------|
| **SaaS MVP** | Full-stack SaaS with auth, billing, dashboard | ui-craft (frontend) + dev-craft (backend) |
| **Admin Dashboard** | Data-heavy admin panel with CRUD operations | ui-craft (dashboard UI) + dev-craft (API) |
| **E-commerce** | Product catalog, cart, checkout, payments | ui-craft (storefront) + dev-craft (backend) |
| **Landing Page** | Marketing site with forms | ui-craft only |
| **Design System** | Shared component library | ui-craft only |

### Orchestration Pattern

```
1. PLAN — Decompose feature into frontend and backend slices
2. DESIGN SYSTEM FIRST — Run ui-craft to create design tokens and components
3. HANDOFF — Generate API spec from design system needs
4. BACKEND — Run dev-craft for API/database/auth slices
5. FRONTEND — Run ui-craft for UI slices using API spec
6. INTEGRATION — Run both pipelines for integration testing
7. SHIP — Coordinate commits across both pipelines
```

### Cross-Skill Communication

When ui-craft needs backend work:
- Note in `.ui-craft/state.json`: `"backendSliceNeeded": ["auth-api", "data-endpoint"]`
- Generate API spec in `.ui-craft/api-spec.md`
- Resume with dev-craft: "Run dev-craft for API spec in `.ui-craft/api-spec.md`"

When dev-craft needs UI work:
- Note in `.dev-craft/state.json`: `"uiSliceNeeded": ["login-form", "dashboard"]`
- Generate API contract in `.dev-craft/api-contract.md`
- Resume with ui-craft: "Run ui-craft for API contract in `.dev-craft/api-contract.md`"

---

## "What If" Mode

After Phase 3 (DESIGN), the user can trigger "What If" mode to explore alternatives:

**Trigger:** User says "what if we used [different style/color/font]?"

**Process:**
1. Save current design system as a snapshot in `.ui-craft/design-system/snapshots/`
2. Re-run Phase 3 with the modified parameters
3. Show a diff between old and new design system
4. Ask: "Keep this version or revert?"

**Supported "What If" variations:**
- "What if we used a warmer palette?" → re-run with different color keywords
- "What if we tried glassmorphism?" → re-run with different style keywords
- "What if we made it denser?" → adjust density dial
- "What if we used a different font?" → re-run typography search
- "What if we made it more playful?" → adjust variance dial

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I don't need to grill — I know what they want" | The #1 cause of AI failure is misalignment. Five minutes of grilling saves hours of rework. |
| "Let me just start coding" | Starting without a design system guarantees inconsistent UI, rework, and accessibility issues. |
| "I'll add accessibility later" | You won't. And retrofitting a11y is 10x harder than building it in. |
| "This is too simple to source-verify" | Training data is stale at every level. A two-line React component can use a deprecated hook. |
| "I'll clean up design tokens after all slices" | Token debt compounds. Fix it per-slice or you won't fix it at all. |
| "The UI looks fine, skip the audit" | Visual correctness ≠ accessibility. A beautiful UI can be completely unusable. |
| "I'll add dark mode later" | You won't. And retrofitting dark mode means touching every color in every file. |
| "This is a prototype, skip accessibility" | Prototypes become production. Accessibility from day one prevents the "a11y debt" crisis. |
| "I'll fix responsive at the end" | Responsive debt compounds. A component built without responsive in mind often needs a full rewrite. |
| "The design system is just for reference" | The design system IS the source of truth. Every ad-hoc color or font is debt. |

## Red Flags

- Skipping AUDIT on an existing codebase with > 10 UI files
- Starting implementation without a completed ALIGN phase
- Human checkpoints skipped without explicit approval
- Writing code before fetching current-version docs
- Multiple slices committed in one commit
- Lint/type checks failing but moving to next phase
- No ADRs for design decisions
- "I'll fix it later" accepted for any Critical finding
- No `.ui-craft/` directory created (state not persisting)
- Accessibility review skipped on production-bound code
- Commit messages that say "WIP", "fix", or "update"
- Using deprecated patterns for the detected framework version
- No design tokens generated (ad-hoc colors/fonts)
- No visual preview generated before BUILD

## Verification

Before declaring the pipeline complete:

- [ ] AUDIT was run (or explicitly skipped with human approval for greenfield)
- [ ] `.ui-craft/state.json` exists with `status: "complete"`
- [ ] All planned slices implemented and committed
- [ ] Design token files generated (tailwind.config.ts, tokens.css, theme.ts)
- [ ] HTML style guide preview generated
- [ ] Linter + formatter pass on all changed files
- [ ] Type checker passes
- [ ] No deprecated patterns for the detected framework version
- [ ] Accessibility gates passed (contrast, focus, touch targets, aria labels)
- [ ] Dark mode supported
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No debug tags, dead code, or temp files remain
- [ ] ADRs written for all design decisions
- [ ] CONTEXT.md glossary is up to date
- [ ] No secrets in the diff
- [ ] Human has approved every checkpoint

## See Also

- `references/ui-patterns.md` — UI-specific pattern guidance and best practices
- `~/.opencode/skills/ui-ux-pro-max/` — Design database and search engine (reused by ui-craft)
