# Test-quality checklist

Fallback for `testing-strategies` (see `SKILL.md` §5). Each item is checkable in a diff or a test run.

## Requirements
- Every `REQ` maps to at least one test; the mapping is listed in the report.
- Expected values come from a `Source:` tag (user, document, repo behavior, hand calculation), never copied
  from what the implementation currently returns.
- Invariants from the brief have their own test or constraint (debits equal credits; on-hand equals the sum of
  movements).
- Changing existing logic: characterization tests of current behavior first, then show which differences are
  intentional.

## Test design
- Test behavior through the public interface, not private details; one behavior per test; the name states it.
- A new test was seen failing for the right reason before the fix, output shown (red-green proof: `verify.md`).
- Cover happy path, edge cases, error paths, authorization (401 vs 403) and validation errors (422 for FastAPI).
- Deterministic: time, randomness and network controlled; no order dependence; no shared mutable state.
- Mock only external boundaries (third-party service, clock, email); never the unit under test.
- Prefer real Postgres (for example testcontainers) for query, constraint and migration tests.
- Data from factories or builders, not copy-pasted literals; realistic values.

## Stack specifics
- Backend: pytest fixtures; `httpx` client with `dependency_overrides` reset after use; pagination, filter and
  sort params tested; Alembic up/down/up on a disposable database.
- Frontend: query by role or label (Testing Library); MSW handlers generated from the contract; Playwright only
  for critical end-to-end flows and screenshots.

## Discipline
- Never delete, skip or loosen a failing test to get green (rule in `verify.md`).
- Flaky test: reproduce and fix the cause, or quarantine with a ticket note; never retry until green.
- Coverage is a signal, not a goal; report which `REQ`s and error paths are not covered.
