# Review

Use for the REVIEW step, for "review this diff", and for incoming PR/MR comments. Review `git diff` as if
someone else wrote it, then try to break it. For large work prefer a fresh subagent or session that sees only
the spec and the diff.

## Axes

Seven always: correctness, security, tests, design, performance, readability, scope (anything outside the
brief or write scope). Add when relevant: **boundary** (`fullstack.md` boundary checks), **UI**
(`checklists/ui.md`), **schema** (`data-modeling.md`). Bug classes and security: `bug-hunting`,
`harden-checks.md`. Full eight-axis scoring: `code-review-and-quality`. Do not restate their checklists here.

## Try to break it

List the 3 inputs or situations most likely to break the change (empty, huge, concurrent, unauthorized, bad
format, retry) and run them. Check the same bug class elsewhere in the repo.

## Findings format

```markdown
1. [High | confidence: high] src/orders.py:88 - refund ignores partial shipments, so customers are over-refunded.
   Fix: subtract shipped quantity (see `orders.py:61`); add test `test_partial_refund`.
## Questions (low confidence)
- src/cart.py:40 - is `None` price intended for gifts?
```
- Severity High / Medium / Low; confidence high / low. Cap at about 10, grouped by severity. Every finding has
  `file:line` and a concrete fix. Low-confidence items go under Questions, not as findings.
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
