# Bug-class checklist

Fallback for `bug-hunting` (see `SKILL.md` §5). Each item is checkable in a diff or by running one input.

## How to hunt
- For each changed function, list its callers; check each still holds.
- Grep the repo for the same pattern: the same bug class often exists elsewhere.
- Write the 3 most likely failing inputs and run them; report only what you reproduced (`review.md` states).

## Inputs
- null/None, empty string and list, zero, negative, very large, whitespace-only, unicode, duplicates, wrong
  type, missing optional fields.

## Boundaries
- Off-by-one; first and last page of pagination; empty result; end-of-month and leap-day dates.
- Time zones and DST; inclusive vs exclusive ranges.

## Numbers
- Money in float; rounding mode and where it is applied; integer overflow; division by zero; mixed currencies.

## State and concurrency
- Double submit; read-modify-write races; missing transaction boundary.
- Lost update (use a version column or row lock); non-idempotent retries; stale cache.
- Ordering assumed without `ORDER BY`.

## Errors
- Swallowed exceptions; partial failure leaving half-written data; missing timeouts.
- Retry of a non-idempotent call; error messages that leak internals.

## Resources
- Unclosed session, file or connection; N+1 queries; unbounded query or loop; unbounded memory on large input.

## Async
- Blocking call inside an async handler; missing `await`; shared mutable state across requests.

## Contract
- Changed response shape or status code; nullable field treated as non-null; enum value added on one side only.

## Frontend
- Stale closures and effect dependency errors; race between two fetches; state set after unmount.
- Missing `key`; uncontrolled-to-controlled input; date/number/currency formatting.
- Missing empty, loading or error state.

## Authorization
- Missing check on a new route; object-level access (IDOR); permission enforced only by hiding UI.
