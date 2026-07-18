# HARDEN — Cross-Cutting Security Review (UI)

Deep reference for ui-craft `[7] HARDEN`. The main `SKILL.md` states the
polish goal and exit criterion; load this file only when executing the
cross-cutting security portion of HARDEN. The UI-specific listing here parallels
dev-craft `[8] HARDEN` Check 6/7 — read both sides when `scope == fullstack`.

**Cross-Cutting Security Review — agent reads across all UI slices:**

1. **Third-party scripts & dependencies:**
   - Read package.json: any known-vulnerable frontend deps? (old jQuery, Moment.js, deprecated plugins)
   - Read next.config / vite.config: are env vars with NEXT_PUBLIC_ / VITE_ leaking secrets to client?
   - Read index.html / layout: external scripts have integrity hashes (SRI)?
   - Read service worker: intercepting sensitive URLs? Caching auth responses?

2. **Auth token handling consistency:**
   - Read all API client calls: same auth header/token pattern everywhere?
   - Read token storage: localStorage (avoid) vs httpOnly cookie (prefer)?
   - Read token refresh logic: rotated securely? Old token invalidated?
   - Read logout: clears all client-side state? Invalidates server session?

3. **Error handling & info leakage:**
   - Read error boundaries / catch handlers: sensitive data in error UI?
   - Read API error interceptor: stack traces or internal details shown to user?
   - Read data fetching: auth errors handled (redirect to login) vs silently ignored?

4. **Form security consistency:**
   - Read all forms: CSRF token included in state-changing requests?
   - Read password fields: autocomplete attr set correctly?
   - Read file upload components: type validation on client before submit?

5. **Client-side data exposure:**
   - Read analytics/tracking code: PII sent to third-party analytics?
   - Read console.log / debug code left in production components?
   - Read Sentry/error tracking: sensitive data in error reports?
   - Read state management: user data stored in Redux/Vuex persists in devtools?

**Axis 9 — API Contract Conformance (fullstack only):**

When `api-contract.md` exists, verify the UI honors it (the BE side is checked in dev-craft HARDEN Check 7):

- Every route the UI calls is declared in `api-contract.md` (no invented endpoints).
- Request bodies the UI sends match the contract's `Request` shape.
- The UI reads response fields the contract's `Response` actually returns (no `.items` when BE returns `.data`).
- The UI handles the status codes the contract lists (e.g. 401, 429) — none silently unhandled.
- Base URL / CORS origin matches what the BE serves.

Any divergence is a Required finding: the UI "works" in isolation but breaks against the real API.
