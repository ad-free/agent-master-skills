---
name: fe-visual-loop
description: |
  Show-before-build visual loop for any UI-visible task. Produces 2-3
  screenshotted direction mocks, gets an explicit human pick, builds to the
  winner, then screenshot-verifies the build against it. Use for page builds,
  redesigns, and component work too big to free-style but smaller than a full
  ui-craft run. Invoked by: frontend-engineer, ui-craft (Phases 2/3/8).
model: big-pickle
version: 1.0.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "show me options"
  - "visual direction"
  - "mockup first"
  - "redesign this page"
  - "build this page"
  - "design options"
  - "pick a design"
  - "screenshot the design"
metadata:
  origin: agent-master-skills
  domain: frontend
  integrates-with: [ui-craft, ui-pattern-extractor, anti-slop, image-to-design-spec, playwright-skill, visual-regression, verification-before-completion]
---

# FE Visual Loop v1.0

## Iron Law

```
NO BUILD WITHOUT A PICKED DIRECTION. NO SHIP WITHOUT A SCREENSHOT.
```

Inferred taste is not agreement. The agent shows; the human picks; then the agent builds.

## When to Use

- Any UI-visible task above a trivial tweak (new page, section, redesign, component set).
- Inside `ui-craft` Phases 2/3 (direction gate) and 8 (proof gate).
- Standalone for mid-size tasks that don't justify a full 10-phase `ui-craft` run.

**When NOT to use:** Single-line CSS fixes, typo/color tweaks, non-visual work.

## The Loop

### Step 1: Brief (minutes, not phases)

- Collect references if given (screenshots, URLs, design system). If provided, run them through `image-to-design-spec` → tokens + style notes.
- If no references: load `anti-slop` Brief Inference + set VARIANCE/MOTION/DENSITY dials, declare the one-line Design Read.
- Output: 2–3 sentence direction candidates (e.g. "A: editorial minimal, B: dense SaaS, C: warm boutique"). Do NOT build yet.

### Step 2: Mock (live HTML, not AI images)

- Build each direction as a small static HTML mock in a scratch dir (real layout, real type scale, palette applied — lorem content is fine).
- Screenshot every mock with `playwright-skill` (desktop + one mobile width).
- Present screenshots side by side with a one-line read per direction.

### Step 3: Pick (hard gate)

- Ask the human to pick a winner (or combine: "B with A's hero").
- Record the pick + screenshot paths in state (or session notes for standalone runs).
- **Phase 5 BUILD (or any implementation) is blocked until a pick is recorded.** No exceptions.

### Step 4: Build to the Winner

- Implement against the picked mock's tokens, spacing, and composition. Deviations need a stated reason.
- Reuse `ui-pattern-extractor` output on existing codebases so the new UI matches surrounding patterns.

### Step 5: Proof (hard gate)

- Screenshot the built UI at the same widths as the mock.
- Self-critique: layout vs. mock, spacing rhythm, type scale, `anti-slop` tells (emoji icons, generic gradients, default hero), responsive breaks, console errors.
- Fix and re-screenshot until match, or record an explicit waiver with reason.
- Present winner-vs-build side by side at handoff.

## Integration

- `ui-craft` Phase 2 exit = Step 3 pick recorded. Phase 3 preview = Step 2 mocks. Phase 8 SHIP = Step 5 proof.
- Evidence from Steps 3/5 feeds `verification-before-completion` (no LLM-judge pass without proof screenshots or a recorded waiver).
