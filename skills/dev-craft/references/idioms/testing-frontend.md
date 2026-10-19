# Testing frontend

- **Vitest + Testing Library:** test behavior as the user sees it (roles, labels, text), not internals.
- **MSW:** mock the API at the network boundary, with handlers derived from the contract or generated types so
  mocks cannot drift; also cover error responses (401, 403, 409, 422, 500).
- **Playwright:** end-to-end for the acceptance flows and for screenshots at desktop and mobile widths; run
  against the real backend for the "done" claim.
- Each `REQ` has a test; states (loading, empty, error) are tested, not just the happy path.
- Traps: asserting on class names, snapshot spam, mocks that return shapes the backend never sends.
