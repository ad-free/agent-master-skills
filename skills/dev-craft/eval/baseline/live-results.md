# Live eval results: old (v3.0.0, dev-craft.bak) vs new (v4.0.0)

Method: 8 cases x 2 skill versions = 16 subagent runs (sonnet), each in its own throwaway git repo built from
small fixtures (shop / hrm / hr / perf). Same prompt; only the skill path differed. Headless: agents could not
ask, so "stopped and asked" means no code was written. One run per cell: this is a sample, not statistics.
Fixture flaw: tracked `__pycache__` files made `git status` noisy in every run (ignored when scoring).

| Case | Old v3 | New v4 | Better |
|---|---|---|---|
| G2 bug fix | Fixed, red-green shown, Standard + Bug mode | Same fix, red-green, "Not verified" list, more refs loaded | tie |
| R1 contradiction | Found README rule, stopped, no code, defaults listed | Found it, kept finance rule (409), shipped code + red-green | new (delivers safe default) |
| R4 unverifiable claim | Built, no dedupe; noted missing signature check | Built, added 409 already-paid (flagged), noted signature; did not tag the "exactly-once" claim Unknown | tie, both miss |
| F2 response-shape change | Changed it, updated all 3 consumers, red-green, report/export verified unchanged | Stopped with 3 questions, no code | OLD (new over-asked) |
| F4 FE-only missing field | Stopped, asked 3 questions | Stopped with options A/B/C, cited private-email docstring | new (options) |
| U1 HRM | Stopped; 7 questions; wrote .dev-craft state files | Stopped; 3 questions with defaults; REQs with examples; proposals capped; no design step reached | new (cap/defaults) |
| D1 flawed schema | Built give_raise + salary_history returning only current salary (misleading), flagged missing history | give_raise built; history report withheld; history table + migration proposed as the decision | new |
| D2 slow query | EXPLAIN, migration up/down, tie-order fix, test | Same, plus test that fails when migration is a no-op | tie (slightly new) |

Tally: new better 4, tie 3, old better 1.

## Findings that drive step 3
1. R4: neither version treats a claim about an external system as Unknown. Add it to challenge.md.
2. F2: the new skill over-asks on an explicit instruction with in-repo consumers. Loosen the rule.
3. The old skill was stronger than my static trace predicted (R1, F4, D2). The new skill's measured gain is
   moderate: options-not-questions, question caps with defaults, Not-verified lists, red-green proof, safe
   defaults instead of stopping.
4. U1 never reached the design step; the HRM playbook and design.md remain untested live.

## After step 3 (re-run, new skill with challenge.md/workflow.md edits)
| Case | Before edit (v4.0) | After edit | Result |
|---|---|---|---|
| R4 | Built without questioning the "exactly-once" claim | Named the guarantee Unknown, built what was asked, kept the write idempotent, flagged side-effect risk | fixed |
| F2 | Stopped with 3 questions, no code | Proceeded: format_cents, updated 3 consumers + tests, red-green incl. stashed run, outside-repo clients under Not verified | fixed; now matches old on outcome and adds the Not-verified note |

One run per cell; sample, not proof. Not re-run: the other six cases (edits touch only challenge.md and
workflow.md wording). U1's design step and the UI playbooks are still untested live.

## U1 follow-up: UI design step with the brief pre-approved (new skill, 1 run)
Checked in the run directory, not only from the agent's summary: `design.md` (56 lines) has users/goals, IA,
per-screen composition (12-col grid, rows, breakpoints), concrete design-system choices (Tailwind v4 `@theme`
tokens, slate + one indigo accent, semantic colors, inline SVG icons/charts because nothing is installed, light
mode only, stated), and states (loading skeleton, error + retry, empty per widget, long content). It loaded
frontend-design, checklists/ui, ui-patterns/hrm, tailwind, charts, react-typescript idioms. Test run re-run by me:
4 pass, 0 fail (`node --test --experimental-strip-types src/derive.test.ts`).
Gaps: new tests never failed first (no red-green proof; the agent said so); build/typecheck/screenshots Not
verified (no installs, no browser; `vite.config.ts` imports two packages missing from package.json, flagged).
Verdict: the design step and HRM playbook work as intended. The screenshot critique is still untested live.

## UI Verify step with a real browser (U1 output, new skill's verify.md procedure)
First attempt (subagent): could not start the Playwright MCP browser (Chrome not found), so it reported the
screenshot pass as Not verified instead of faking it. It still caught real build defects in the delivered UI:
`react-dom` missing from package.json, `@vitejs/plugin-react` latest incompatible with the project's Vite 6
(pinned ^4), missing type packages. It also left its dev server running while reporting it stopped (I verified by
port and PID and stopped it).
Second attempt (me, driving Playwright's cached Chromium directly, following verify.md and frontend-design.md
section 4): screenshots at 1440 and 390, viewed, compared with design.md and checklists/ui.md.
- Desktop 1440: matches design (hierarchy, icons, chart with text summary, bars with value and share, badges,
  avatars). Console: one 404 (missing favicon).
- Mobile 390, before: page 437px wide (horizontal overflow; two cards wider than the viewport), truncated approval
  rows, trend chart scaled so small its labels were unreadable.
- Fixes (4 small edits): `grid-cols-1` on the dashboard grids, chart in an `overflow-x-auto` container with a
  minimum width, favicon link. After: scrollWidth 390 = clientWidth 390, console clean at both widths, `tsc` ok,
  confirmed by viewing the new screenshot.
- Remaining: approval subtitles truncate at 390 (full text in `title`); no tests re-run after the fix.
Verdict: the critique pass finds defects that tests and the build cannot (overflow, unreadable chart text), and
the procedure in verify.md is workable. The browser tool is environment-dependent: when it fails, the skill's
"Not verified" path worked as designed.
