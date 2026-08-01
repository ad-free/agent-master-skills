---
name: ui-craft
description: |
  Run the 10-phase frontend development pipeline with persistent `.ui-craft`
  state. Use for UI/UX features, design system work, component libraries, or
  resuming sessions. Invoked by: planner → frontend-engineer → verifier.
model: big-pickle
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - Task
triggers:
  - "build this UI"
  - "run ui-craft"
  - "design this component"
  - "implement the design"
  - "create design tokens"
metadata:
  origin: agent-master-skills
  phase-count: 10
  plugins: [design-intelligence, anti-slop]
  preferred-model: big-pickle
  version: 2.0.0
  domain: frontend
  integrates-with: [dev-craft, design-system-validate, accessibility-deep]
---

TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# ui-craft

## Relationship to existing skills

- `dev-craft` — backend pipeline; ui-craft consumes `api-contract.md` from dev-craft for fullstack work
- `design-system-validate` — validates UI code against design system tokens and component contracts; this skill enforces those standards
- `accessibility-deep` — WCAG 2.2 AAA compliance auditing; this skill integrates the AA checklist at every phase
- `image-to-design-spec` — extracts design tokens from screenshots; used in ALIGN phase
- `bug-hunting` — security methodology for frontend vulnerability discovery

## When to Use

- Given a prompt, PLAN.md, or feature request for UI/UX
- Starting a new project (greenfield)
- Improving existing project's UI/UX
- Task spans multiple components or pages
- Resuming work from a previous session
- Need more than a single-component change

**When NOT to use:** Single-line CSS fixes, typo corrections, trivial color changes.

## The Iron Law

<HARD-GATE>
```
NO UI WITHOUT DESIGN SYSTEM
```

UI without design tokens = inconsistent, inaccessible, unmaintainable code.
</HARD-GATE>

## Memory System

`.ui-craft/` directory created on first run. Structure: `state.json`, `plan.md`, `context.md`, `decisions/`, `sessions/`, `design-system/`, `preview/`, `tokens/`.

### Resume Logic

| Scenario | Behavior |
|---|---|
| No `.ui-craft/` | Phase 1 if codebase exists, Phase 2 if greenfield |
| `state.json` exists | Load state, skip completed phases |
| All phases complete | Ask "New feature on same project?" |
| Context near limit | Generate handoff doc, resume next session |

## Stack Detection + Version Resolution

Run during Phase 2 (ALIGN). Every generated code must match exact framework version.

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

## Design Token Usage Alignment

Every component must consume design tokens, not hardcoded values:

- **Colors:** Use `color-primary`, `color-surface`, `color-text` tokens — never hex/rgb literals in component code
- **Spacing:** Use `space-xs`, `space-sm`, `space-md`, `space-lg`, `space-xl` tokens
- **Typography:** Use `font-size-body`, `font-size-heading`, `line-height`, `font-weight` tokens
- **Radii:** Use `radius-sm`, `radius-md`, `radius-lg` tokens
- **Shadows:** Use `shadow-sm`, `shadow-md`, `shadow-lg` tokens
- **Breakpoints:** Use `breakpoint-sm`, `breakpoint-md`, `breakpoint-lg`, `breakpoint-xl` tokens

**Component contract rule:** If a component accepts a `className` prop, it must forward it. If it accepts a `variant` prop, it must map to design tokens — never inline styles for variants.

## WCAG 2.1 AA Accessibility Checklist

Every component must pass these checks before BUILD completes:

- [ ] **Color contrast:** All text meets 4.5:1 contrast ratio (3:1 for large text)
- [ ] **Focus indicators:** All interactive elements have visible focus states
- [ ] **Keyboard navigation:** All interactive elements reachable and operable via keyboard
- [ ] **ARIA labels:** Interactive elements have descriptive `aria-label` or visible text
- [ ] **Semantic HTML:** Use appropriate elements (`button`, `nav`, `main`, `article`, etc.)
- [ ] **Heading hierarchy:** Headings follow h1 → h2 → h3 order, no skipping levels
- [ ] **Touch targets:** All interactive elements have minimum 44x44px touch target
- [ ] **Text resize:** Text scales to 200% without loss of content or functionality
- [ ] **Reduced motion:** `prefers-reduced-motion` respected; no essential animations blocked
- [ ] **Screen reader:** Content makes sense when read in DOM order; no `aria-hidden` on interactive elements
- [ ] **Error handling:** Form errors are associated with fields via `aria-describedby`; error messages are programmatically linked
- [ ] **Landmarks:** Page has `main`, `nav`, and `aside` landmarks where appropriate

## Component Contract Standards

Every component must adhere to these contracts (from `design-system-validate`):

1. **Props interface:** All props typed with an explicit interface, no `any`
2. **Default props:** All optional props have sensible defaults
3. **Children:** Components that accept children must handle `undefined` gracefully
4. **Event handlers:** All event handlers are optional unless the component requires them
5. **Ref forwarding:** Components that need DOM access forward refs via `React.forwardRef`
6. **Test contract:** Every component has a test file that validates the contract (props, rendering, events, accessibility)
7. **Story contract:** Every component has a Storybook story that demonstrates all variants

## Workflow

### Phase 0: LOAD — Initialize or Resume

Read `.ui-craft/state.json`:

**Not found →** Detect existing source code:
- Existing code (src/, app/, components/) → Phase 1 (AUDIT)
- Greenfield → Phase 2 (ALIGN), skip AUDIT

**Found + complete →** Ask: "New feature? Start fresh?"

**Found + incomplete →** Load context.md, restore slice progress.

Write state after LOAD.

### Phase 1: AUDIT — Project UI/UX Scan

**Goal:** Assess UI/UX health before adding new code.

**Process:**

1. Scan project for UI/UX health:
   - **Stack Detection:** Read package.json, tsconfig.json, tailwind.config.*
   - **Component Inventory:** Scan src/, app/, components/ for UI files
   - **Style Analysis:** Detect color, typography, spacing, dark mode patterns
   - **Accessibility Scan:** Check aria labels, focus states, semantic HTML, color contrast, touch targets
   - **Responsive Check:** Detect breakpoints, mobile patterns, viewport meta tag
   - **Version Audit:** Check for deprecated patterns, flag version mismatches

2. Surface report with findings and severity
3. Ask human to prioritize fixes

**Exit criterion:** Human approves remediation or defers.

**State write:** Save findings to state.json.

### Phase 2: ALIGN — Grill + Detect + Glossary

**Goal:** Surface assumptions, detect stack versions, build shared language.

**Process:**

1. Ask one question at a time with best guess attached
2. Surface assumptions (platform, audience, style, responsiveness)
3. Set Design Dials (variance, motion, density) — reference `references/design-dials.md`
4. Declare Design Read (one line, before any code)
5. Detect stack + versions (React, Tailwind, shadcn, TypeScript, linter, formatter)
6. Route to design style (SaaS → Minimalism, E-commerce → Glassmorphism, etc.)
7. Build glossary in context.md
8. Image analysis (if screenshot provided) — reference `image-to-design-spec` skill

**Exit criterion:** Human confirms scope with explicit yes.

**State write:** Save stack to state.json. Save context.md. Save image analysis if present.

### Phase 3: DESIGN — Design System + Tokens + Preview

**Goal:** Generate design system with tokens, visual preview, ADRs.

**Process:**

1. Generate design system (requires a screenshot reference)
2. Figma integration (if Figma MCP available)
3. Generate design token files: `tailwind.config.ts`, `tokens.css`, `theme.ts`, `tokens.json`
4. Generate HTML style guide preview (colors, typography, components, light/dark toggle, responsive)
5. Validate design system
6. Write ADRs for design decisions
7. Persist design system to `.ui-craft/`

**Exit criterion:** Human reviews and approves.

**State write:** Save plan.md, ADRs, design system.

### Phase 3.7: REQUIREMENTS-EXTRACTION — Spec → Task Traceability (COVERAGE GATE)

**Goal:** Guarantee every UI-relevant requirement from the source spec is traced to a concrete design/component task with an acceptance criterion, before any component is built.

**Input:** The source spec (from product-thinking / project-discovery, or `docs/*.md`). If no source spec exists, skip this phase.

**Process:**

1. Extract every UI requirement from the spec — literal and exhaustive
2. Assign stable IDs: `UI-REQ-001`, `UI-REQ-002`, ...
3. Trace each to a task in the DESIGN/BUILD plan
4. Build the matrix → `.ui-craft/requirements.md`
5. Self-review against the spec (do not delegate)
6. Present matrix + gaps

<HARD-GATE>
**Exit criterion:** Every P1/G1 UI requirement traced to a task + acceptance criterion. G2/G3 gaps deferrable **only with explicit human acknowledgement** (recorded in state.json `deferredRequirements`).
</HARD-GATE>

**State write:** Save `.ui-craft/requirements.md`; record `requirementsExtracted`, `coverageGaps`, `deferredRequirements` in state.json.

### Phase 4: SOURCE — Version-Aware Doc Verification

**Goal:** Verify framework decisions against official docs.

**Process:**

1. Read exact versions from state.json
2. Fetch specific official docs for each feature
3. Extract patterns, API signatures, deprecation warnings
4. Cite sources inline during BUILD
5. Flag uncovered patterns

**Source hierarchy:** Official docs > Official blog/changelog > MDN Web Standards > ❌ Stack Overflow, blog posts

**Exit criterion:** All dependencies verified.

**State write:** Save source references to state.

### Phase 5: BUILD — Generate UI Code + Secure-by-Construction

**Goal:** Generate tokens, component code, and preview per slice. Every UI slice is verified for security as it's written.

<HARD-GATE>
**Branch isolation (mandatory):** Every BUILD run starts on a dedicated feature branch — never commit directly to `main`/`develop`. For `multi` topology with `fullstack` scope, the FE branch is created in the FE repo paired with the BE branch in the BE repo. Each repo's `state.json` records its own `activeBranch`; `linkedBranches` ties them. A FE-only unit branches only the FE repo.

**Base-branch guard (enforced before every commit):** Treat `main`, `master`, `develop` as protected. If `git branch --show-current` reports a base branch at commit time, STOP and create/checkout the feature branch first. Never override this with `--no-verify` or force.
</HARD-GATE>

1. Resolve the branch name (deterministic, from SCOPE when fullstack, else derived here)
2. Branch naming convention: `<type>/<scope>-<short-description>[-<issue-id>]`
3. Ensure the branch exists before any code — run `scripts/branch-guard.sh`
4. Per-slice commits land on this branch
5. Resume safety: On resume, re-run step 3. If the recorded `activeBranch` no longer exists, fall back to deriving a new name

**Scope-aware entry:** If this is a frontend-only ticket on a repo that already has a design system, skip ALIGN/DESIGN and jump straight to BUILD consuming the existing tokens.

**Consume the API contract (fullstack only):** Before building components that call the BE, read `api-contract.md`. If it is missing, STOP and ask dev-craft to produce it — do not invent endpoints.

**Process per component/page:**

1. Generate design token files
2. Generate component code with version-correct patterns
3. **SECURE** — Run matching security checks from `references/secure-checks.md`
4. Generate HTML style guide preview
5. Run lint/type checks → must pass

### Phase 6: REVIEW — Multi-Axis Audit

**Goal:** Quality gate before shipping.

**Invoke:** `code-review-and-quality` for backend axes (Correctness, Readability, Architecture, Performance, Security, Testing, Modern Patterns).

**UI-Specific Review:**
- AI Tells Check: Load `references/ai-tells-banned.md` and grep for HARD bans
- Review 8 UI-specific axes (UX, accessibility, visual consistency, version pattern, visual regression, testing, UI lint, security)
- Each axis is a read-the-actual-diff pass; do not summarize from memory

**Exit criterion:** All Critical/Required resolved **with evidence**, and every P1/G1 requirement in the traceability matrix verified against the built UI.

**State write:** Save review findings.

### Phase 7: HARDEN — Polish + Dark Mode + Responsive + Cross-Cutting Security

**Goal:** Polish UI across all dimensions. Catch cross-cutting frontend security issues.

**Dark Mode:** All colors have dark mode equivalents, contrast verified in both modes, no hardcoded colors.

**Responsive:** Layout at 375px, 768px, 1024px, 1440px. No horizontal scroll on mobile. Safe areas respected. Touch targets ≥ 44px.

**Animation:** Micro-interactions 150-300ms with proper easing. `prefers-reduced-motion` respected. No layout-shifting animations.

**Performance:** No layout shifts (CLS). Images have width/height. Fonts preloaded. No render-blocking resources.

**Cross-Cutting Security Review:** Load `references/harden-checks.md` for the 5-point security audit (third-party scripts/deps, auth-token handling, error/info leakage, form security, client-side data exposure).

**Exit criterion:** Zero findings. Human approves.

**State write:** Update state.

### Phase 8: SHIP — Docs + Commit + Finalize

**Goal:** Deliver with full traceability.

**Process:**

1. Update ADRs for BUILD/HARDEN decisions
2. Update CONTEXT.md with new terms
3. Generate final HTML style guide preview
4. Final verification: lint + type + build all pass, run secrets scanner, dead code removed
5. Atomic commit with conventional message format
6. Define rollback strategy
7. Mark state complete

**Exit criterion:** Clean commit with rollback plan.

## Quality Gates

- [ ] Design system generated with all token files
- [ ] WCAG 2.1 AA checklist passed for every component
- [ ] Component contracts validated (props interface, default props, children, event handlers, ref forwarding, test contract, story contract)
- [ ] Design tokens consumed, no hardcoded values in component code
- [ ] `requirements.md` exists and COVERAGE GATE passed
- [ ] All slices committed on a feature branch (not base branch)
- [ ] No secrets, debug tags, or temp files remain
- [ ] Lint + type + build all pass
- [ ] Accessibility scan passed (no Critical/High findings)
- [ ] Visual regression check passed (if applicable)

## Error Handling

| Failure Mode | Response |
|--------------|----------|
| Design tokens missing for a value | Define the token before using it; never hardcode |
| Accessibility check fails | Fix before proceeding; do not defer Critical findings |
| Component contract violation | Fix the component to match the contract standard |
| Branch already exists | Use the existing branch; do not create a duplicate |
| API contract missing (fullstack) | STOP and ask dev-craft to produce it |
| Build fails after slice commit | Fix the slice, re-run lint/type, recommit |

## References

- `references/ui-craft-rules.md` — Design token usage, WCAG 2.1 AA checklists, component contract standards (extracted from this skill)
- `references/design-dials.md` — Design variance, motion intensity, visual density dials
- `references/secure-checks.md` — Security check tree for UI slices
- `references/harden-checks.md` — Cross-cutting frontend security audit
- `references/ai-tells-banned.md` — Banned AI-generated UI patterns
- `references/review-protocol.md` — 8 UI-specific review axes and finding categorization
- `references/redesign-audit.md` — 100+ prioritized audit checks for existing projects
- `references/image-first-workflow.md` — Image-first design workflow for visual tasks