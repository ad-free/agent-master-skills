# Edge cases, boundaries, flaky tests

Folded from the former `qa-and-edge-case-tester` skill. Use it to list the failure modes before writing tests;
each item that applies becomes a test with its own failure-mode line.

## Boundaries to walk for every input and state

| Kind | Check |
|---|---|
| Input range | min, max, min-1, max+1, exactly at a limit (off-by-one) |
| Type | null / undefined / missing key, empty string, zero, negative, very large, wrong type (coercion) |
| Collections | empty, one item, many, duplicates, unsorted |
| Text | very long, unicode, whitespace-only, leading/trailing spaces |
| Money / time | rounding, currency precision, time zones, DST, end of month, leap day |
| UI state | initial, loading, empty, error, partial, full / overflow |
| Timing | double click, slow network, timeout, retry, out-of-order responses |
| Concurrency | two writers, stale read then write, optimistic update rolled back |
| Trust | unauthenticated, wrong role, other tenant's id, injection in every string field |

## Flaky test causes and fixes

| Cause | Fix |
|---|---|
| Timing (`sleep`, animation, polling) | Wait for an explicit condition, never a fixed delay |
| Non-deterministic data (random, now(), ordering) | Seed it, freeze the clock, sort before asserting |
| Shared state between tests | Isolate setup/teardown; fresh fixture per test |
| Real external service | Stub at the boundary; keep one contract test for the real shape |

Quarantine a test that fails more than 1 in 20 runs, find the root cause, then re-enable. Never delete or
weaken a test to get green output.

## Test quality

- Coverage is a floor, not a goal; a test that cannot fail is padding.
- Two tests that fail for the same reason are one test.
- Test code meets the same lint and type rules as production code.
