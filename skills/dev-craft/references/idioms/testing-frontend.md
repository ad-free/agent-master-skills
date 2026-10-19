# Testing frontend

- **Vitest + Testing Library:** test behavior as the user sees it (roles, labels, text), not internals.
- **MSW (v2 API):** `http.get(...)` returning `HttpResponse.json(...)`, served with `setupServer` from `msw/node`. Mock the API at the network boundary, with handlers derived from the contract or generated types so
  mocks cannot drift; also cover error responses (401, 403, 409, 422, 500).
- **Playwright:** end-to-end for the acceptance flows and for screenshots at desktop and mobile widths (set
  `viewport` with `test.use`; `toHaveScreenshot` compares against stored snapshots and only works in the Playwright
  test runner, so a one-off look uses `page.screenshot()`); run
  against the real backend for the "done" claim.
- Each `REQ` has a test; states (loading, empty, error) are tested, not just the happy path.
- Traps: asserting on class names, snapshot spam, mocks that return shapes the backend never sends.
