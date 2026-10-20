# Review

Use for the REVIEW step, for "review this diff", and for incoming PR/MR comments. Review `git diff` as if
someone else wrote it, then try to break it. For large work prefer a fresh subagent or session that sees only
the spec and the diff.

## Axes

Seven always: correctness, security, tests, design, performance, readability, scope (anything outside the
brief or write scope). Add when relevant: **boundary** (`fullstack.md` boundary checks), **UI**
(`checklists/ui.md`), **schema** (`data-modeling.md`). Bug classes: `bug-hunting`, else `checklists/bugs.md`.
Security: `checklists/security.md` (deep pass: `harden-checks.md`). Test quality: `checklists/testing.md`.
If the named skill is available use it and skip the inline file. Full eight-axis scoring:
`code-review-and-quality`. Do not restate checklist content here.

## Try to break it

List the 3 inputs or situations most likely to break the change (empty, huge, concurrent, unauthorized, bad
format, retry) and run them. Check the same bug class elsewhere in the repo.

## Findings format

```markdown
1. [High | confidence: high | Confirmed] orders.py:88 refund over-refunds partial shipments.
   Repro: pytest tests/test_refund.py::test_partial -> FAILED, expected 40.00, got 100.00
   Fix: subtract shipped quantity (see `orders.py:61`).
2. [Medium | confidence: low | Cited] cart.py:52 total may skip the discount when `coupon` is empty string.
   Likely issue; please verify at cart.py:52. Tried: 2 inputs, no failure reproduced (High downgraded).
## Questions (Suspected)
- src/cart.py:40 - is `None` price intended for gifts?
```

| State | Meaning | Allowed wording |
|---|---|---|
| Confirmed | Reproduced: command, input and real output, or a failing test | "bug", "issue", "problem" |
| Cited | `file:line` with a traced reason, not run | "likely issue; please verify at path:line" |
| Suspected | Reasoning only (basis Logic or Unknown) | a question, not an issue |

- Only Confirmed items may be called a bug, issue or problem. Before reporting a High finding, try to reproduce
  it (failing test or command, time-boxed); if you cannot, downgrade it and say what you tried. Claiming "the
  test is wrong" or "the requirement is wrong" needs the contradicting source cited. The same states apply to
  PR-comment assessments, HARDEN findings and subagent returns (`test-agent.md`).
- Severity High / Medium / Low; confidence high / low. Cap at about 10, grouped by severity. Every finding has
  `file:line` and a concrete fix. Suspected items go under Questions, not as findings.
- Do not flag: anything the linter or formatter enforces, pure preference, pre-existing code outside the diff
  (mention once as scope drift if serious).
- Spec gaps found in review go back to the brief; do not patch around them.

## Incoming PR/MR comments

Validate each comment against the code before acting. Do not apply feedback blindly.
For each: **fix** (it is right), **push back** (cite code or test showing why it is wrong), or **ask**
(ambiguous or a product decision). Reply per comment, in one line, with the evidence. Re-run the relevant
tests after fixes and include the output. A wrong comment is answered politely and not implemented.

## Review stance

Assume the first pass needs work, cap revision cycles at two, then summarize and ask. Never report "zero issues"
without having run the tools. Large REVIEW also does a requirements reality-check: each P1 row has `path:line`,
a test, or a screenshot.
