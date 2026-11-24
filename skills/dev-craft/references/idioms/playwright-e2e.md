# Playwright end-to-end

Load when writing or fixing an e2e suite (`@playwright/test`). Screenshots for review: `testing-frontend.md`.

- **Disposable data only.** Point the run at a throwaway database the project names (never the dev DB); seed it
  in the run, not by hand. A suite that creates orders or users must refuse any other database.
- **One login per role, reused.** A setup project (`testMatch: '**/*.setup.ts'`) signs in once per role and saves
  `page.context().storageState({ path: 'playwright/.auth/<role>.json' })`; test projects list
  `dependencies: ['setup']`. Pick the role per file or group with `test.use({ storageState: ... })`, or give each
  role its own fixture with `browser.newContext({ storageState })`. Keep `playwright/.auth/` out of git.
- **Every role and locale the change touches.** Loop over roles in a `describe` per role; for locales, set the
  app's language the way a user does (switcher, cookie or `?lng=`) or `test.use({ locale })` when the app reads
  the browser locale. Assert the translated text or a key-free label, and that no raw key (`checkout.title`) shows.
- **Authorization from the outside:** each protected route has a test that a role without access is redirected
  or sees the denied state, and one that the API call returns 403 (`page.request` with that role's state).
- **Locators and waits:** `getByRole` / `getByLabel` / `getByText`; web-first assertions (`await expect(...)
  .toBeVisible()`), never `waitForTimeout`. Wait for the final URL after login before saving state.
- **Isolation:** each test creates the data it needs (API helper, unique names); no order between tests.
- **Proof:** quote the run (`N passed`, the project names); on failure open the trace (`--trace on`) before
  changing a selector. A flaky test is a bug to fix (race, shared data), not a retry to add.
