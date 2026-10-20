# Verify and Finalize

Read before saying "done". The report is incomplete without the Evidence table, because reading code and
reasoning it should work is how unverified claims get through.

## Evidence table

```markdown
## Evidence
| Layer | Claim | Command run | Result (real output, trimmed) | Verified by |
|---|---|---|---|---|
| backend | REQ-1 refund works | `pytest tests/test_refund.py -v` | 4 passed | main; Verifier, re-run by main: yes |
| frontend | REQ-2 form shows API error | `npm test -- order-form` | 6 passed | main |
| ui | Dashboard matches design.md | screenshots `shots/dash-1440.png`, `shots/dash-390.png` | reviewed; 2 issues fixed | UI Verifier |
| db | Migration safe | `alembic upgrade head && alembic downgrade -1 && alembic upgrade head` | ok | main |
| contract | Types in sync | `npm run gen:types && git diff --exit-code` | clean | main |
| e2e | REQ-3 checkout flow | `npx playwright test checkout` | 1 passed | main |
| all | Nothing else broke | `pytest -q` | 212 passed | main |

Not verified: <anything not run, and why; manual steps for the user>
```
Include only rows you actually ran. "Not verified" is the honest alternative to overclaiming; use it.
Subagent results follow the reconciliation rule in `test-agent.md`: no command output means Weak, and the main
agent re-runs the key command.

## What counts

- **Strong:** a command run in this session, output shown, produced **after the last edit**. Edit again, re-run.
- **Weak:** reading code. **Invalid:** "should work", "same pattern as elsewhere", output from before the last edit.
- **Red-green proof:** a new test that passed on its first run proves nothing. Show it fails without the change
  (stash the fix or revert it, run, restore). For a bug fix it must fail on the assertion, with the failure message
  stated. For a new function or signature, a missing-feature error (ImportError, TypeError, stub) is an
  acceptable first red; say so, and the mutation spot check supplies the assertion-level proof.
- **Oracles, strongest first** (expected values never come from the implementation's own output): user-provided
  values; existing repo behavior; independent checks (a hand calculation the user can redo); invariants;
  characterization/differential comparison; mutation spot check (revert or alter the fix, confirm a test
  fails, restore); a real end-to-end run; screenshots against `design.md`.
- Each `REQ` maps to at least one test; list the mapping. Cover edge cases and error paths, not only the happy
  path. Never delete, skip, or loosen a failing test to get green; if it looks wrong, say so and ask. Do not
  mock the thing under test.

## By kind of change

- **UI:** run the app, screenshot each key screen at desktop and mobile widths, *look at them*, compare with
  `design.md` and `checklists/ui.md`, fix, include screenshots. At least one critique-and-fix pass. If the
  browser cannot run, "Not verified" plus the preview commands.
- **DB:** migration up, down, up on a copy with sample data; `EXPLAIN` on the key queries (`data-modeling.md`).
- **2+ sides:** backend tests, frontend tests/type-check/lint, a contract check, one real end-to-end run per
  acceptance criterion, every contract error exercised once. UI ran against a mock = "backend not verified".
- **Scope:** say which scope you verified and which side you did not.

## Pre-completion self-check

1. Did I run the code, not just read it? 2. Did I re-run everything after my last edit? 3. Does every `REQ` have
a test and a result? 4. Did I touch anything out of scope? 5. What would a skeptical reviewer ask? 6. Am I
claiming anything I have not shown?

## Final report

Outcome first, then: files and behavior changed; requirement matrix; Evidence table; decisions and
assumptions; **Needs your confirmation** (every `Assumption` and `Business rule`); open proposals (not
built); Not verified; risks; new env vars; branch; proposed commit message; demo script. After a Large task add
"What was missing from the task". Do not commit.

**Requirement matrix** (Large, risk-flagged, or when asked; otherwise a plain REQ list is enough. One row per
`REQ` and per invariant):
```markdown
| REQ | Example (source) | Test | Result | Independent check | Status |
|---|---|---|---|---|---|
| REQ-2 | 5-3=2 (Hand calc) | test_approve_leave | 1 passed | mutation spot check | done |
| INV-1 | balance = accruals - usages | test_ledger_invariant | 1 passed | none | done (lower confidence) |
```
`Independent check`: `Test Designer test`, `Verifier run`, `invariant`, `characterization/differential`,
`mutation spot check`, `e2e run`, `screenshot`, `user demo`, `none`. A `none` row is shown as lower confidence.

**Demo script** (Large, UI, or when asked; skip for small Standard tasks): end with steps the user can run in about 5 minutes: seed command, exact commands or URLs, and
what to observe per `REQ` (UI: route, viewport, what to see). Run it once yourself; its output is Evidence.

Worked example of a failing claim caught: "Fixed the 500 on empty cart." -> no output shown -> run
`pytest tests/test_cart.py::test_empty` first; paste "1 passed"; show it failed before the fix.
