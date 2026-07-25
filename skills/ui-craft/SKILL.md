---
name: ui-craft
description: Use when converting UI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/UX
  prompts into design tokens, component code, and visual previews with pipeline state
  in `.ui-craft`.
metadata:
  origin: agent-master-skills
owner: noname.spyware@gmail.com

---

# ui-craft

## Overview

Turns a UI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/UX prompt into production-quality design tokens, component code, and visual previews.
Every phase has a clear goal, exit criteria, and a human checkpoint.
Persists state to `.ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` so work survives across sessions.

**Philosophy:** Design-first, version-aware, human-orchestrated.
Skip any phase. Edit any phase. The pipeline serves you.

## When to Use

- Given a prompt, PLAN.md, or feature request for UI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/UX
- Starting a new project (greenfield)
- Improving existing project's UI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/UX
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

`.ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` directory created on first run:

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
| No `.ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` | Phase 1 if codebase exists, Phase 2 if greenfield |
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
| `npx shadcn@latest` | shadcn${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ui version | v2.0+ |
| User prompt | Manual override | "I want React 18" |

### Version-Aware Rules

| Stack | Version | Use | Avoid |
|-------|---------|-----|-------|
| React | 19 | `useActionState`, `use()`, Server Components | Class components, `UNSAFE_*` |
| React | 18 | `useTransition`, `useDeferredValue`, `Suspense` | `UNSAFE_componentWillMount` |
| Next.js | 15 | App Router, Server Actions, `next${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/navigation` | Pages Router |
| Next.js | 14 | App Router | `getInitialProps` |
| Tailwind | v4 | `@import "tailwindcss"`, CSS-first config | `@tailwind` directives |
| Tailwind | v3 | `tailwind.config.js`, `@tailwind` directives | v1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/v2 syntax |
| shadcn${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ui | v2 | `cn()` helper, new-york style | v1 component API |
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
[0] LOAD → [1] AUDIT → [2] ALIGN → [3] DESIGN → [3.7] REQUIREMENTS-EXTRACTION
    → [4] SOURCE → [5] BUILD → [6] REVIEW → [7] HARDEN → [8] SHIP
```

Each phase:
```
Phase → Output
LOAD → state.json initialized
AUDIT → Health report (remediate first?)
ALIGN → CONTEXT.md (shared language)
DESIGN → Design system + tokens + preview
REQUIREMENTS-EXTRACTION → requirements.md (spec→task traceability matrix)  ← COVERAGE GATE
SOURCE → Fetched docs
BUILD → UI code + tokens + preview + SECURE (incl. regex) per slice
REVIEW → UX + a11y + visual + security audit
HARDEN → Polish + dark mode + responsive + cross-cutting security
SHIP → Commit + ADRs + state complete
```

> **Why REQUIREMENTS-EXTRACTION exists:** ui-craft enforces design discipline, but on its
> own it does not prove the UI plan covers the product spec. UI requirements
> (a11y targets, responsive breakpoints, permission-gated components, i18n, specific
> component libraries) get dropped the same way backend ones do. This phase traces every
> UI requirement to a concrete design${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/component task **before** any component is built.

---

### [0] LOAD — Initialize or Resume

Read `.ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.json`:

**Not found →** Detect existing source code:
- Existing code (src${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/, app${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/, components${PROJECT_ROOT}${PROJECT_ROOT}/) → Phase 1 (AUDIT)
- Greenfield → Phase 2 (ALIGN), skip AUDIT

**Found + complete →** Ask: "New feature? Start fresh?"

**Found + incomplete →** Load context.md, restore slice progress.

Write state after LOAD.

---

### [1] AUDIT — Project UI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/UX Scan

**Goal:** Assess UI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/UX health before adding new code.

**Process:**

1. Scan project for UI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/UX health:

   **Stack Detection:**
   - Read package.json, tsconfig.json, tailwind.config.*
   - Detect exact versions of React, Next.js, Vue, Tailwind
   - Detect CSS approach (Tailwind, CSS Modules, styled-components)

   **Component Inventory:**
   - Scan src${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/, app${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/, components/ for UI files
   - Identify component patterns (shadcn${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ui, custom)
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
   - Detect breakpoints in CSS${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Tailwind config
   - Check for mobile-specific patterns
   - Check for viewport meta tag

   **Version Audit:**
   - Check for deprecated patterns
   - Flag patterns that don't match detected version

2. Surface report:
   ```
   UI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/UX HEALTH REPORT:

   STACK:
   - React 19.0.0 (package.json)
   - Tailwind CSS v4 (CSS-first config)
   - shadcn${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ui v2.0+
   - TypeScript 5.5 (tsconfig.json)

   FINDINGS:
   1. [ACCESSIBILITY] Missing focus states
      → src${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Navbar.tsx:15
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
   - shadcn${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ui v2.0+
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
    python ~${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/analyze.py --image <path> --format json --output .ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/image-analysis.json
    ```
   Use extracted data to:
   - Auto-generate design tokens from extracted colors
   - Create `.ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/MASTER.md` from analysis
   - Skip manual token definition
   - Generate Tailwind config from colors
   Present to user for confirmation.

**Exit criterion:** Human confirms scope with explicit yes.

**State write:** Save stack to state.json. Save context.md. Save image analysis if present.

---

### [3] DESIGN — Design System + Tokens + Preview

**Goal:** Generate design system with tokens, visual preview, ADRs.

**Process:**

 1. Generate design system (requires a screenshot reference):
     ```bash
     python ~${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/analyze.py \
       --image <path> --design-system --output .ui-craft${PROJECT_ROOT}/
     ```
    This writes `design-system.json`, `tokens.css`, `tailwind.config.js`,
    and `DESIGN-SPEC.md` into the output directory.
    If you already have a JSON analysis from Step [2] (`--format json`), you can
    instead run `generate_design_system.py --input .ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/image-analysis.json \
    --output .ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`.

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
   - Light${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/dark mode toggle
   - Responsive preview

5. Validate design system:
   ```bash
   python3 scripts${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/validator.py validate-design-system
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

7. Persist design system to .ui-craft${PROJECT_ROOT}/

 **Exit criterion:** Human reviews and approves.

**State write:** Save plan.md, ADRs, design system.

---

### [3.7] REQUIREMENTS-EXTRACTION — Spec → Task Traceability (COVERAGE GATE)

**Goal:** Guarantee every UI-relevant requirement from the source spec is traced to a
concrete design${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/component task with an acceptance criterion, before any component is
built. This is what stops UI features (a11y, responsive, permission-gating, i18n,
mandated component libraries) from silently falling out of the plan.

**Input:** The source spec (from product-thinking / project-discovery, or `docs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/*.md`).
If no source spec exists, skip this phase.

**Process:**

1. **Extract every UI requirement** from the spec — literal and exhaustive:
   - Component library mandates ("Tailwind + shadcn${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ui only, no Ant Design")
   - Accessibility targets ("contrast ≥ 4.5:1", "touch ≥ 44px")
   - Responsive breakpoints ("375 / 768 / 1024 / 1440")
   - Permission-gated UI (`<HasPermission permission="hrm.payroll.approve">`)
   - i18n ("Interface language: Vietnamese")
   - Design language ("minimalist global SaaS style")
   - Every screen${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/page the spec implies but does not name explicitly
   - Preserve the spec's priority markers (`🔴 [REQUIRED P1]`, `G1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G3`) verbatim.

2. **Assign stable IDs:** `UI-REQ-001`, `UI-REQ-002`, ...

3. **Trace each to a task** in the DESIGN${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/BUILD plan. Every UI requirement must map to
   ≥1 task whose acceptance criteria verify it.

4. **Build the matrix** → `.ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/requirements.md`:
   ```markdown
   # UI Requirements Traceability Matrix — <project>

   | UI-REQ-ID | Priority | Requirement (verbatim) | Traced Task(s) | Status |
   |-----------|----------|------------------------|----------------|--------|
   | UI-REQ-001 | P1 | shadcn${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ui only, no Ant Design | DESIGN tokens | ✅ |
   | UI-REQ-007 | P1 | i18n Vietnamese | A9 i18n setup | ✅ |
   | UI-REQ-012 | G1 | permission-gated components | A10 HasPermission | ⚠️ GAP |
   ```

5. **Self-review** against the spec (do not delegate): re-read each section, confirm a
   row exists and maps to a task. Search for skipped markers.

6. **Present matrix + gaps.** Do not auto-skip.

**Exit criterion (HARD GATE):** Every P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1 UI requirement traced to a task + acceptance
criterion. G2${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G3 gaps deferrable **only with explicit human acknowledgement** (recorded
in state.json `deferredRequirements`). Building UI with unresolved P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1 coverage gaps is
the failure this phase prevents.

**State write:** Save `.ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/requirements.md`; record `requirementsExtracted`,
`coverageGaps`, `deferredRequirements` in state.json.

---

### [4] SOURCE — Version-Aware Doc Verification

**Goal:** Verify framework decisions against official docs.

**Process:**

1. Read exact versions from state.json
2. Fetch specific official docs for each feature
3. Extract patterns, API signatures, deprecation warnings
4. Cite sources inline during BUILD:
   ```typescript
   ${PROJECT_ROOT}/ Source: http${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/useActionState
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
| 2 | Official blog${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/changelog |
| 3 | MDN Web Standards |
| ❌ | Stack Overflow, blog posts |

**Exit criterion:** All dependencies verified.

**State write:** Save source references to state.

---

### [5] BUILD — Generate UI Code + Secure-by-Construction

**Goal:** Generate tokens, component code, and preview per slice. Every UI slice is verified for security as it's written.

**Branch isolation (mandatory):** Every BUILD run starts on a dedicated feature branch — never commit directly to `main`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`develop`. For `multi` topology with `fullstack` scope, the FE branch is created in the FE repo **paired** with the BE branch in the BE repo (see dev-craft SCOPE §0.2 step 5): `fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fe-payroll-142` alongside `fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/be-payroll-142`. Each repo's `state.json` records its own `activeBranch`; `linkedBranches` ties them. A FE-only unit branches only the FE repo.

**Base-branch guard (enforced before every commit):** Treat `main`, `master`, `develop` (and the repo's configured default branch) as protected. If `git branch --show-current` reports a base branch at commit time, STOP and create${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/checkout the feature branch first. Never override this with `--no-verify` or force.

1. **Resolve the branch name** (deterministic, from SCOPE when fullstack, else derived here):
    - `mono`: one `activeBranch` in this repo.
    - `multi`: read `linkedBranches.fe` (this FE repo's branch) from state.
2. **Branch naming convention:**
    ```
    <type>${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/<scope>-<short-description>[-<issue-id>]
    type ∈ { feat, fix, refactor, chore, test, docs }
    scope ∈ { fe, fs }
    examples:
      feat${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fs-login-form        (mono: one branch;  multi: paired be+fe branches)
      fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fe-button-a11y-142
    ```
3. **Ensure the branch actually exists before any code** — verify, don't just record intent:
    ```bash
    BRANCH="$(jq -r '.activeBranch ${PROJECT_ROOT}/ empty' .ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.json)"
    if [ -z "$BRANCH" ]; then
      # derive from SCOPE: <type>${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/<scope>-<short-description>, e.g. feat${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fe-login-form
      BRANCH="<type>${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/<scope>-<short-description>"
      jq --arg b "$BRANCH" '.activeBranch = $b' .ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.json > .ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.tmp \
        && mv .ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.tmp .ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.json
    fi

    if git show-ref --verify --quiet "refs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/$BRANCH"; then
      git checkout "$BRANCH"
    elif [ "$(git branch --show-current)" = "$BRANCH" ]; then
      :
    else
      git checkout -b "$BRANCH"
    fi

    # FAIL LOUDLY if we are not on the feature branch (e.g. checkout failed)
    CURRENT="$(git branch --show-current)"
    case "$CURRENT" in
      main|master|develop) echo "ERROR: still on base branch $CURRENT — branch creation failed"; exit 1 ;;
      "")                  echo "ERROR: detached HEAD — branch creation failed"; exit 1 ;;
      "$BRANCH")           echo "OK: on feature branch $BRANCH" ;;
      *)                   echo "ERROR: on unexpected branch $CURRENT, expected $BRANCH"; exit 1 ;;
    esac
    ```
    Record `activeBranch` in state.json **only after** the branch is confirmed to exist and we are on it. Also register it in `branches` keyed by the unit.
4. **Per-slice commits land on this branch.** Each slice is an atomic commit. The branch is only merged${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/PR'd during SHIP. Re-run the base-branch guard above before each commit.
5. **Resume safety:** On resume, re-run step 3. If the recorded `activeBranch` no longer exists, fall back to deriving a new name (do NOT silently stay on a base branch).

**Scope-aware entry (fe-ticket on existing project):** If this is a frontend-only ticket on a repo that already has a design system (`.ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/MASTER.md` or tokens present), skip ALIGN${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/DESIGN and jump straight to BUILD consuming the existing tokens. Do not regenerate the design system for a one-component fix.

**Consume the API contract (fullstack only):** Before building components that call the BE, read `api-contract.md` from the recorded `apiContract` path (dev-craft's `contractRepo`, or the mirror path for `multi`). If it is missing, STOP and ask dev-craft to produce it — do not invent endpoints.

**Process per component${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/page:**

0a. BRANCH-GUARD — Confirm we are on the feature branch (create${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/switch if needed); abort if on a base branch
1. Generate design token files
2. Generate component code with version-correct patterns:
    - React 19 → `useActionState`, Server Components
    - React 18 → `useTransition`, `Suspense`, `useId`
    - Tailwind v4 → CSS-first config
    - Tailwind v3 → JS config
    - shadcn${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ui v2 → new-york style, `cn()` helper
    - Forms: React Hook Form + Zod validation
    - Tests: Vitest + React Testing Library + jest-axe
    - Icons: lucide-react, heroicons, phosphor, tabler

3. **SECURE** — Agent determines what the UI slice touches, then runs matching checks. Load `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/secure-checks.md` for the full check tree (user data, forms, storage, API calls, regex) and output format.

4. Generate HTML style guide preview
5. Run lint${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/type checks → must pass

**Rules:**
- Version-correct patterns only
- Scope discipline — don't touch code outside slice
- One slice at a time
- Accessibility gates: contrast ≥ 4.5:1, focus visible, touch ≥ 44px
- **SECURE before lint** — Security first, then code quality

**Exit criterion:** All slices implemented, committed, and security-verified.

**State write:** Save `activeBranch` (the current unit's branch), `branches` map, slices, and security notes to state.json.

---

### [6] REVIEW — Multi-Axis Audit

**Goal:** Quality gate before shipping.

**Invoke:** `code-review-and-quality` for backend axes (Correctness, Readability, Architecture, Performance, Security, Testing, Modern Patterns).

**UI-Specific Review (in addition to code-review-and-quality):**
Load `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/review-protocol.md` for the 8 UI-specific axes (UX, accessibility, visual consistency, version pattern, visual regression, testing, UI lint, security), plus the two nested sub-checks (Axis 2b screen-reader testing, Axis 4b readability gate), the finding-categorization labels, and the reality-check discipline. Each axis is a
read-the-actual-diff pass; do not summarize from memory.

**Exit criterion:** All Critical${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Required resolved **with evidence**, and every P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1
requirement in the traceability matrix verified against the built UI.

**State write:** Save review findings.

---

### [7] HARDEN — Polish + Dark Mode + Responsive + Cross-Cutting Security

**Goal:** Polish UI across all dimensions. Catch cross-cutting frontend security issues.

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
- Images have width${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/height
- Fonts preloaded
- No render-blocking resources

**Clean:**
- Remove debug instrumentation
- Delete throwaway prototypes
- Check unused CSS classes

**Cross-Cutting Security Review — agent reads across all UI slices:**
Load the deep reference `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/harden-checks.md` for the 5-point security
audit (third-party scripts${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/deps, auth-token handling, error${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/info leakage, form
security, client-side data exposure) and Axis 9 (BE↔FE contract conformance).
Each point is a read-the-actual-code pass; do not summarize from memory.

**Exit criterion:** Zero findings. Human approves.

**State write:** Update state.

---

### [8] SHIP — Docs + Commit + Finalize

**Goal:** Deliver with full traceability.

**Process:**

1. Update ADRs for BUILD${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/HARDEN decisions
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
    Before committing, re-run the branch-guard: confirm `git branch --show-current`
    is the feature branch, not a base branch. If on a base branch, stop and
    checkout the feature branch first.
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

2. Write handoff to sessions${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/session-YYYYMMDD-N.md:
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
1. PLAN — Decompose into frontend${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/backend slices
2. DESIGN SYSTEM — Run ui-craft for tokens${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/components
3. HANDOFF — Generate API spec
4. BACKEND — Run dev-craft for API${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/auth
5. FRONTEND — Run ui-craft using API spec
6. INTEGRATION — Run both for testing
7. SHIP — Coordinate commits
```

### Cross-Skill Communication

Driven by SCOPE (dev-craft §0.2). The contract artifact is ALWAYS named **`api-contract.md`** (no `api-spec.md` variant), at repo root or `docs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`. Both skills read the same file.

**ui-craft (`scope: fullstack`) needs backend:**
1. If `api-contract.md` already exists (dev-craft produced it), consume it directly — do not regenerate endpoints.
2. If not, generate `api-contract.md` from the UI's data needs; record `crossSkill.backendSliceNeeded: ["auth-api"]`; hand to dev-craft to implement.
3. dev-craft MUST implement only what the contract declares; any new endpoint updates the contract first.

**dev-craft needs UI:**
1. Run CONTRACT (dev-craft §4.5) → write `api-contract.md`.
2. Record `crossSkill.uiSliceNeeded: ["login-form"]`, `apiContract: "api-contract.md"`.
3. ui-craft MUST consume `api-contract.md` and may not invent endpoints.

**Contract conformance (fullstack):** In REVIEW, verify the built UI calls only contract-declared routes with contract-declared request${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/response shapes; surface any divergence as Required.

---

## "What If" Mode

After Phase 3 (DESIGN), user can explore alternatives.

**Trigger:** User says "what if we used [different style${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/font]?"

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
- Lint${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/type checks failing but proceeding
- No ADRs for design decisions
- "Fix it later" for Critical findings
- No .ui-craft/ directory
- Accessibility review skipped
- No visual preview before BUILD
- **Starting BUILD without `.ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/requirements.md` coverage gate passing (P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1 UI gaps unresolved)**
- UI requirement traced to a task but no acceptance criterion verifying it
- Commits made directly to main${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/develop (no feature branch)
- `activeBranch` recorded in state.json but agent is actually on a base branch (branch was never created${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/checked out)

## Verification

- [ ] AUDIT was run (or deferred with approval)
- [ ] .ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.json exists with status: complete
- [ ] All slices implemented and committed
- [ ] All slices committed on a dedicated feature branch (not a base branch)
- [ ] `activeBranch` recorded in state.json and verified to exist before BUILD commits
- [ ] Design token files generated
- [ ] HTML style guide preview generated
- [ ] **`.ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/requirements.md` exists and the COVERAGE GATE passed** (every P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1 UI REQ-ID traced to a task + acceptance criterion)
- [ ] Every P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1 requirement in the matrix verified against the built UI during REVIEW
- [ ] Linter + formatter pass
- [ ] Type checker passes
- [ ] No deprecated patterns
- [ ] Accessibility gates passed
- [ ] Dark mode supported
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] Every slice had SECURE check pass before commit
- [ ] Cross-cutting security review in HARDEN passed
- [ ] No secrets in source code (agent verified by reading all files)
- [ ] No debug tags or temp files
- [ ] ADRs written for decisions
- [ ] CONTEXT.md up to date
- [ ] Human approved every checkpoint

## See Also

- `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ui-patterns.md` — UI-specific pattern guidance
- `image-to-design-spec` — Design token extraction from images
- `bug-hunting` — Security methodology for frontend vulnerability discovery
- `dev-craft` — Backend pipeline with complementary security checks