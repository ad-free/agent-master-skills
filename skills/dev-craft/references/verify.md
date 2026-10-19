# Verify and Finalize

Read before saying "done". The report is incomplete without the Evidence table, because reading code and
reasoning it should work is how unverified claims get through.

## Evidence table

```markdown
## Evidence
| Layer | Claim | Command run | Result (real output, trimmed) |
|---|---|---|---|
| backend | REQ-1 refund works | `pytest tests/test_refund.py -v` | 4 passed |
| frontend | REQ-2 form shows API error | `npm test -- order-form` | 6 passed |
| ui | Dashboard matches design.md | screenshots `shots/dash-1440.png`, `shots/dash-390.png` | reviewed; 2 issues fixed |
| db | Migration safe | `alembic upgrade head && alembic downgrade -1 && alembic upgrade head` | ok |
| contract | Types in sync | `npm run gen:types && git diff --exit-code` | clean |
| e2e | REQ-3 checkout flow | `npx playwright test checkout` | 1 passed |
| all | Nothing else broke | `pytest -q` | 212 passed |

Not verified: <anything not run, and why; manual steps for the user>
```
Include only rows you actually ran. "Not verified" is the honest alternative to overclaiming; use it.

## What counts

- **Strong:** a command run in this session, output shown, produced **after the last edit**. Edit again, re-run.
- **Weak:** reading code. **Invalid:** "should work", "same pattern as elsewhere", output from before the last edit.
- **Red-green proof:** a new test that passed on its first run proves nothing. Show it fails without the change
  (stash the fix or revert it, run, restore).
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

Outcome first, then: files and behavior changed; `REQ` checklist (done / partial / not done, with `path:line`
or test); Evidence table; decisions and assumptions; open proposals (not built); Not verified; risks; new env
vars; branch; proposed commit message. After a Large task add "What was missing from the task". Do not commit.

Worked example of a failing claim caught: "Fixed the 500 on empty cart." -> no output shown -> run
`pytest tests/test_cart.py::test_empty` first; paste "1 passed"; show it failed before the fix.
