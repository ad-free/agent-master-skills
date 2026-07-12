---
name: ui-craft
description: UI/UX engineering pipeline with persistent memory. Detects stack versions, generates design tokens, component code, and visual preview. Resumes via .ui-craft/ state.
---

# ui-craft

## Overview

Turns a UI/UX prompt into production-quality design tokens, component code, and visual previews.
Every phase has a clear goal, exit criteria, and a human checkpoint.
Persists state to `.ui-craft/` so work survives across sessions.

**Philosophy:** Design-first, version-aware, human-orchestrated.
Skip any phase. Edit any phase. The pipeline serves you.

## When to Use

- Given a prompt, PLAN.md, or feature request for UI/UX
- Starting a new project (greenfield)
- Improving existing project's UI/UX
- Task spans multiple components or pages
- Resuming work from a previous session
- Need more than a single-component change

**When NOT to use:** Single-line CSS fixes, typo corrections, trivial color changes.

## The Iron Law

```
NO UI WITHOUT DESIGN SYSTEM
```

UI without design tokens = inconsistent, inaccessible, unmaintainable code.

## Memory System

`.ui-craft/` directory created on first run:

```
.ui-craft/
├── state.json          # currentPhase, completed, stack, slices
├── plan.md             # Evolving plan from ALIGN → DESIGN
├── context.md          # Domain glossary (shared language)
├── decisions/          # ADRs — key design decisions
│   └── 001-*.md
├── sessions/           # Handoff docs for context rotation
│   └── session-YYYYMMDD-N.md
├── design-system/      # Persisted design system
│   ├── MASTER.md
│   └── pages/
├── preview/            # Generated HTML previews
│   ├── design-system.html
│   └── components.html
└── tokens/             # Generated design token files
    ├── tailwind.config.ts
    ├── tokens.css
    └── theme.ts
```

### Resume Logic

| Scenario | Behavior |
|---|---|
| No `.ui-craft/` | Phase 1 if codebase exists, Phase 2 if greenfield |
| `state.json` exists | Load state, skip completed phases |
| All phases complete | Ask "New feature on same project?" |
| Context near limit | Generate handoff doc, resume next session |

## Stack Detection + Version Resolution

Run during Phase 2 (ALIGN).
Every generated code must match exact framework version.

### Version Detection Sources

| Source | Detects | Example |
|--------|---------|---------|
| `package.json` | React, Next.js, Vue, shadcn, Tailwind | `"react": "^19.0.0"` |
| `tailwind.config.*` | Tailwind v3 (JS) vs v4 (CSS-first) | CSS-first = v4 |
| `tsconfig.json` | TypeScript target | `"target": "ES2022"` |
| `npx shadcn@latest` | shadcn/ui version | v2.0+ |
| User prompt | Manual override | "I want React 18" |

### Version-Aware Rules

| Stack | Version | Use | Avoid |
|-------|---------|-----|-------|
| React | 19 | `useActionState`, `use()`, Server Components | Class components, `UNSAFE_*` |
| React | 18 | `useTransition`, `useDeferredValue`, `Suspense` | `UNSAFE_componentWillMount` |
| Next.js | 15 | App Router, Server Actions, `next/navigation` | Pages Router |
| Next.js | 14 | App Router | `getInitialProps` |
| Tailwind | v4 | `@import "tailwindcss"`, CSS-first config | `@tailwind` directives |
| Tailwind | v3 | `tailwind.config.js`, `@tailwind` directives | v1/v2 syntax |
| shadcn/ui | v2 | `cn()` helper, new-york style | v1 component API |
| TypeScript | 5.x | `satisfies`, `const` type params | legacy enums |

### Version Resolution Flow

```
1. Check package.json → exact version
2. If not found → ask user (default: latest)
3. If "latest" → fetch from npm registry
4. Store in state.json
5. SOURCE: fetch docs for that version
6. BUILD: use only valid patterns
7. REVIEW: flag deprecated patterns
```

---

## Pipeline Phases

```
[0] LOAD → [1] AUDIT → [2] ALIGN → [3] DESIGN → [4] SOURCE
    → [5] BUILD → [6] REVIEW → [7] HARDEN → [8] SHIP
```

Each phase:
```
Phase → Output
LOAD → state.json initialized
AUDIT → Health report (remediate first?)
ALIGN → CONTEXT.md (shared language)
DESIGN → Design system + tokens + preview
SOURCE → Fetched docs
BUILD → UI code + tokens + preview
REVIEW → UX + a11y + visual audit
HARDEN → Polish + dark mode + responsive
SHIP → Commit + ADRs + state complete
```

---

### [0] LOAD — Initialize or Resume

Read `.ui-craft/state.json`:

**Not found →** Detect existing source code:
- Existing code (src/, app/, components/) → Phase 1 (AUDIT)
- Greenfield → Phase 2 (ALIGN), skip AUDIT

**Found + complete →** Ask: "New feature? Start fresh?"

**Found + incomplete →** Load context.md, restore slice progress.

Write state after LOAD.

---

### [1] AUDIT — Project UI/UX Scan

**Goal:** Assess UI/UX health before adding new code.

**Process:**

1. Scan project for UI/UX health:

   **Stack Detection:**
   - Read package.json, tsconfig.json, tailwind.config.*
   - Detect exact versions of React, Next.js, Vue, Tailwind
   - Detect CSS approach (Tailwind, CSS Modules, styled-components)

   **Component Inventory:**
   - Scan src/, app/, components/ for UI files
   - Identify component patterns (shadcn/ui, custom)
   - Count components, pages, layouts

   **Style Analysis:**
   - Detect color usage patterns
   - Detect typography patterns
   - Detect spacing patterns
   - Detect dark mode support

   **Accessibility Scan:**
   - Check for aria labels on interactive elements
   - Check for focus states
   - Check for semantic HTML
   - Check for color contrast
   - Check for touch target sizes

   **Responsive Check:**
   - Detect breakpoints in CSS/Tailwind config
   - Check for mobile-specific patterns
   - Check for viewport meta tag

   **Version Audit:**
   - Check for deprecated patterns
   - Flag patterns that don't match detected version

2. Surface report:
   ```
   UI/UX HEALTH REPORT:

   STACK:
   - React 19.0.0 (package.json)
   - Tailwind CSS v4 (CSS-first config)
   - shadcn/ui v2.0+
   - TypeScript 5.5 (tsconfig.json)

   FINDINGS:
   1. [ACCESSIBILITY] Missing focus states
      → src/components/Navbar.tsx:15
   2. [STYLE] Inconsistent color usage
      → Define single --color-primary token
   3. [DARK MODE] No dark mode support
   4. [VERSION] React 18 patterns, React 19 detected
   ```

3. Ask human to prioritize fixes

**Exit criterion:** Human approves remediation or defers.

**State write:** Save findings to state.json.

---

### [2] ALIGN — Grill + Detect + Glossary

**Goal:** Surface assumptions, detect stack versions, build shared language.

**Process:**

1. Ask one question at a time with best guess attached

2. Surface assumptions:
   ```
   ASSUMPTIONS:
   1. Web app (not native mobile)
   2. Target: C-end consumers
   3. Style: modern, minimal
   4. Platform: responsive web
   → Correct me now or I'll proceed.
   ```

3. Define "Out of scope" explicitly

4. Detect stack + versions:
   ```
   STACK DETECTED:
   - React 19.0.0 (package.json)
   - Tailwind CSS v4 (CSS-first config)
   - shadcn/ui v2.0+
   - TypeScript 5.5
   - Linter: ESLint 9.x
   - Formatter: Prettier 3.x
   ```

5. Route to design style:
   | Project Type | Suggested Style |
   |--------------|-----------------|
   | SaaS / Dashboard | Minimalism |
   | E-commerce | Glassmorphism |
   | Marketing / Landing | Bold Typography |
   | Portfolio / Agency | Editorial |
   | Enterprise / B2B | Neumorphism |
   | Social / Community | Duotone |
   | Mobile-first | Flat Design |
   | Creative / Artistic | 3D / Isometric |

6. Build glossary in context.md

7. **Image analysis** (if screenshot provided):
   ```bash
   python scripts/analyze.py --image <path> --format json --output .ui-craft/image-analysis.json
   ```
   Use extracted data to:
   - Auto-generate design tokens from extracted colors
   - Create `.ui-craft/design-system/MASTER.md` from analysis
   - Skip manual token definition
   - Generate Tailwind config from colors
   Present to user for confirmation.

**Exit criterion:** Human confirms scope with explicit yes.

**State write:** Save stack to state.json. Save context.md. Save image analysis if present.

---

### [3] DESIGN — Design System + Tokens + Preview

**Goal:** Generate design system with tokens, visual preview, ADRs.

**Process:**

1. Generate design system:
   ```bash
   python3 ~/.opencode/skills/ui-ux-pro-max/scripts/search.py \
     "<query>" --design-system -p "Project Name"
   ```

2. Figma integration (if Figma MCP available):
   - Export design tokens from Figma
   - Extract color palette, typography, spacing
   - Generate components from Figma library
   - If no Figma MCP: skip

3. Generate design token files:
   - `tailwind.config.ts` — colors, spacing, fonts
   - `tokens.css` — CSS custom properties
   - `theme.ts` — TypeScript theme object
   - `tokens.json` — Design token JSON

4. Generate HTML style guide preview:
   - Self-contained HTML file
   - Color palette with hex + CSS variables
   - Typography scale (h1-h6, body, small)
   - Component examples (buttons, cards, inputs)
   - Light/dark mode toggle
   - Responsive preview

5. Validate design system:
   ```bash
   python3 scripts/validator.py validate-design-system
   ```

6. Write ADRs for design decisions:
   ```markdown
   # ADR-001: [Title]
   Status: Accepted
   Context: [Problem]
   Decision: [What we chose]
   Alternatives: [What else was considered]
   Consequences: [Impact]
   ```

7. Persist design system to .ui-craft/design-system/

**Exit criterion:** Human reviews and approves.

**State write:** Save plan.md, ADRs, design system.

---

### [4] SOURCE — Version-Aware Doc Verification

**Goal:** Verify framework decisions against official docs.

**Process:**

1. Read exact versions from state.json
2. Fetch specific official docs for each feature
3. Extract patterns, API signatures, deprecation warnings
4. Cite sources inline during BUILD:
   ```typescript
   // Source: https://react.dev/reference/react/useActionState
   const [state, formAction, isPending] = useActionState(fn, initialState)
   ```
5. Flag uncovered patterns:
   ```
   UNVERIFIED: No official docs for this pattern.
   Based on training data — verify before shipping.
   ```

**Source hierarchy:**
| Priority | Source |
|---|---|
| 1 | Official docs |
| 2 | Official blog/changelog |
| 3 | MDN Web Standards |
| ❌ | Stack Overflow, blog posts |

**Exit criterion:** All dependencies verified.

**State write:** Save source references to state.

---

### [5] BUILD — Generate UI Code

**Goal:** Generate tokens, component code, and preview per slice.

**Process per component/page:**

1. Generate design token files
2. Generate component code with version-correct patterns:
   - React 19 → `useActionState`, Server Components
   - React 18 → `useTransition`, `Suspense`, `useId`
   - Tailwind v4 → CSS-first config
   - Tailwind v3 → JS config
   - shadcn/ui v2 → new-york style, `cn()` helper
   - Forms: React Hook Form + Zod validation
   - Tests: Vitest + React Testing Library + jest-axe
   - Icons: lucide-react, heroicons, phosphor, tabler

3. Generate HTML style guide preview
4. Run lint/type checks → must pass

**Rules:**
- Version-correct patterns only
- Scope discipline — don't touch code outside slice
- One slice at a time
- Accessibility gates: contrast ≥ 4.5:1, focus visible, touch ≥ 44px

**Exit criterion:** All slices implemented and committed.

**State write:** Save slices to state.json.

---

### [6] REVIEW — Seven-Axis Audit

**Goal:** Quality gate before shipping.

**Invoke:** `code-review-and-quality` for backend axes (Correctness, Readability, Architecture, Performance, Security, Testing, Modern Patterns).

**UI-Specific Review (in addition to code-review-and-quality):**

Review entire diff across UI-specific axes:

**Axis 1 — UX Best Practices:**
- Interaction patterns consistent?
- Error states handled (empty, loading, error)?
- Navigation intuitive?
- Forms usable (validation, errors, labels)?

**Axis 2 — Accessibility:**
- Color contrast ≥ 4.5:1 body, ≥ 3:1 large text
- Focus states visible on all interactive elements
- Touch targets ≥ 44x44px
- All interactive elements have aria labels
- Semantic HTML (button, nav, main, headings)
- `prefers-reduced-motion` respected

**Axis 2b — Screen Reader Testing:**
- Test with NVDA (Windows) or VoiceOver (macOS)
- All images have alt text
- All form inputs have labels
- All buttons have accessible names
- Page structure with headings (h1 → h2 → h3)
- Dynamic content with aria-live

**Axis 3 — Visual Consistency:**
- Colors match design system tokens
- Typography matches design system
- Spacing follows 4/8dp rhythm
- Shadows/border-radii consistent
- Icons from consistent set

**Axis 4 — Version Pattern Audit:**
- No deprecated APIs for detected version
- Code follows current-version docs
- Source citations for correct version
- Lint/format/tests pass

**Axis 5 — Visual Regression:**
- Run Playwright/Cypress screenshot comparison
- No unintended layout shifts
- No color/typography regressions
- Responsive at 375px, 768px, 1024px, 1440px

**Axis 6 — Testing:**
- Tests exist for new components
- Tests cover edge cases and error states
- Accessibility tests (jest-axe) pass
- Mocks at boundaries only

**Axis 7 — UI Lint:**
- No design system violations
- No unused CSS classes
- No missing responsive utilities
- Run automated UI lint tools

**Categorize findings:**
| Label | Action |
|---|---|
| Critical | Must fix |
| Required | Must address |
| Nit | May ignore |
| Optional | Worth considering |

**Exit criterion:** All Critical/Required resolved.

**State write:** Save review findings.

---

### [7] HARDEN — Polish + Dark Mode + Responsive

**Goal:** Polish UI across all dimensions.

**Dark Mode:**
- All colors have dark mode equivalents
- Contrast verified in both modes
- No hardcoded colors (all use tokens)

**Responsive:**
- Layout at 375px, 768px, 1024px, 1440px
- No horizontal scroll on mobile
- Safe areas respected
- Touch targets ≥ 44px on mobile

**Animation:**
- Micro-interactions: 150-300ms with proper easing
- `prefers-reduced-motion` respected
- No layout-shifting animations

**Performance:**
- No layout shifts (CLS)
- Images have width/height
- Fonts preloaded
- No render-blocking resources

**Clean:**
- Remove debug instrumentation
- Delete throwaway prototypes
- Check unused CSS classes

**Exit criterion:** Zero findings. Human approves.

**State write:** Update state.

---

### [8] SHIP — Docs + Commit + Finalize

**Goal:** Deliver with full traceability.

**Process:**

1. Update ADRs for BUILD/HARDEN decisions
2. Update CONTEXT.md with new terms
3. Generate final HTML style guide preview
4. Final verification:
   - Lint + type + build all pass
   - Run secrets scanner
   - Dead code removed
5. Atomic commit:
   ```
   type(scope): short description

   - What changed and why
   - Key decisions (reference ADRs)
   - What was intentionally NOT done
   ```
6. Define rollback strategy
7. Mark state complete

**Exit criterion:** Clean commit with rollback plan.

---

### [H] HANDOFF — Cross-Session Context

**When:** Context > 80% full, or human says "continue later".

**Process:**

1. Save state to state.json:
   - Current phase and slice position
   - Incomplete tasks
   - Pending decisions

2. Write handoff to sessions/session-YYYYMMDD-N.md:
   - What was accomplished
   - What's in progress
   - What's next
   - Known issues

3. Summarize: "Session saved. Run ui-craft to resume."

---

## Workflow Orchestration

For complex features spanning multiple domains.

### Workflow Types

| Workflow | Pipeline |
|----------|----------|
| SaaS MVP | ui-craft + dev-craft |
| Admin Dashboard | ui-craft + dev-craft |
| E-commerce | ui-craft + dev-craft |
| Landing Page | ui-craft only |
| Design System | ui-craft only |

### Orchestration Pattern

```
1. PLAN — Decompose into frontend/backend slices
2. DESIGN SYSTEM — Run ui-craft for tokens/components
3. HANDOFF — Generate API spec
4. BACKEND — Run dev-craft for API/database/auth
5. FRONTEND — Run ui-craft using API spec
6. INTEGRATION — Run both for testing
7. SHIP — Coordinate commits
```

### Cross-Skill Communication

ui-craft needs backend:
- Note in state.json: `"backendSliceNeeded": ["auth-api"]`
- Generate API spec in api-spec.md
- Resume with dev-craft

dev-craft needs UI:
- Note in state.json: `"uiSliceNeeded": ["login-form"]`
- Generate API contract in api-contract.md
- Resume with ui-craft

---

## "What If" Mode

After Phase 3 (DESIGN), user can explore alternatives.

**Trigger:** User says "what if we used [different style/color/font]?"

**Process:**

1. Save current design system as snapshot
2. Re-run Phase 3 with modified parameters
3. Show diff between old and new
4. Ask: "Keep or revert?"

**Supported variations:**
- "What if warmer palette?" → re-run with color keywords
- "What if glassmorphism?" → re-run with style keywords
- "What if denser?" → adjust density dial
- "What if different font?" → re-run typography search

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I know what they want" | #1 cause of AI failure is misalignment |
| "Just start coding" | No design system = inconsistent UI, rework |
| "Add a11y later" | You won't. Retrofitting is 10x harder |
| "Too simple to verify" | Training data is stale |
| "Clean tokens after slices" | Token debt compounds |
| "UI looks fine, skip audit" | Visual correctness ≠ accessibility |
| "Add dark mode later" | You won't. Retrofitting touches every color |
| "Prototype, skip a11y" | Prototypes become production |
| "Fix responsive at end" | Responsive debt compounds |
| "Design system for reference" | Design system IS source of truth |

## Red Flags

- Skipping AUDIT on codebase with > 10 UI files
- Starting without completed ALIGN phase
- Human checkpoints skipped
- Code before fetching current-version docs
- Multiple slices in one commit
- Lint/type checks failing but proceeding
- No ADRs for design decisions
- "Fix it later" for Critical findings
- No .ui-craft/ directory
- Accessibility review skipped
- No design tokens generated
- No visual preview before BUILD

## Verification

- [ ] AUDIT was run (or deferred with approval)
- [ ] .ui-craft/state.json exists with status: complete
- [ ] All slices implemented and committed
- [ ] Design token files generated
- [ ] HTML style guide preview generated
- [ ] Linter + formatter pass
- [ ] Type checker passes
- [ ] No deprecated patterns
- [ ] Accessibility gates passed
- [ ] Dark mode supported
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No debug tags or temp files
- [ ] ADRs written for decisions
- [ ] CONTEXT.md up to date
- [ ] No secrets in diff
- [ ] Human approved every checkpoint

## See Also

- `references/ui-patterns.md` — UI-specific pattern guidance
- `~/.opencode/skills/ui-ux-pro-max/` — Design database
