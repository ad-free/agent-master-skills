# HARDEN — Cross-Cutting Security Checks

Deep reference for dev-craft `[8] HARDEN`. The main `SKILL.md` states the
goal and exit criterion; load this file only when executing HARDEN so the 8
checks don't sit in context during earlier phases.

**Goal of the phase:** Verify security across all slices, not within individual
slices. Catch cross-cutting issues that per-slice SECURE checks miss. The agent
now has the full codebase in context and reads across all slices to find issues
no single slice could surface.

---

#### Check 1: Secrets Across the Codebase

The agent reads every file it has written or modified, looking for:

```
Secrets check — agent reads every file for:
- API keys, tokens, passwords, connection strings with credentials
- Private keys (RSA, EC, SSH, PGP) embedded in source
- .env files, credentials in config commits
- Hardcoded JWT secrets, signing keys, encryption keys
- Cloud provider secrets (AWS_ACCESS_KEY, GCP service account, etc.)
- OAuth tokens, webhook secrets, webhook signing secrets
- Any string matching pattern: /key|secret|token|password|credential/i with a literal value

For each potential secret found:
1. Is it a real credential or a placeholder/test value?
2. Is it in a file tracked by version control?
3. Does it need rotation? (if it was just committed, yes)
```

**If any real secret found** → move to env var, add to `.gitignore`, rotate the secret if exposed.

---

#### Check 2: Auth & Authorization Across All Endpoints

The agent reads every route handler and checks for consistent auth:

```
Auth verification — agent reads:
- Every route definition: does it have auth middleware?
- Admin routes: is there an admin role check?
- Public routes: is it INTENTIONALLY public? (landing, docs, health)
- Authorization: does every user-specific route scope by the authenticated user?

Look for inconsistencies:
- Route A has auth middleware, Route B (same resource) doesn't
- GET is public, but POST/PUT/DELETE require auth
- Admin routes exist without admin checks
- User-scoped data can be accessed by changing ?id= in URL
```

---

#### Check 3: Data Flow Analysis — Injection Surface

The agent traces every path from user input → processing → output/output, reading the actual code:

```
Injection check — agent traces:
INPUT ENTRY POINTS (read all):
├── Route params: /users/:id
├── Query params: ?search=...
├── Request body: POST JSON/form data
├── Headers: Authorization, X-*, cookies
├── File uploads
└── Webhook payloads

↓ Agent traces each to:

DATABASE QUERIES (read all):
├── SQL: parameterized with ? / $1? or string concat?
├── NoSQL: accepts objects or safe operators only?
└── Stored procedures: safely called?

OS COMMANDS (read all):
├── exec/spawn/system calls found?
├── User input in command string? → must use args array
└── File paths from user input? → validated and restricted?

OUTPUT RENDERING (read all):
├── User input in HTML/response? → escaped/sanitized?
├── API JSON responses: no secrets in response bodies?
└── Error responses: no stack traces leaking internals?
```

---

#### Check 4: Dependency & Version Review

The agent reads the package/dependency files:

```
Dependency check:
- Read package.json, requirements.txt, go.mod, Cargo.toml, pom.xml
- For each dependency, reason about known CVEs from training knowledge:
  - Log4j < 2.17.0? → critical RCE
  - jQuery < 3.5.0? → XSS vulnerabilities
  - Express < 4.18? → known middleware bypasses
  - Django < 4.2? → multiple CVEs per version
  - Older versions of lodash, moment.js, etc.
- Flag unmaintained packages (> 2 years since last release, per agent knowledge)
- Flag devDependencies in production Dockerfile
- Check for duplicate or conflicting dependency versions

If the agent is uncertain about a specific version's CVE status:
Flag it: "CVE status unknown for [package]@[version] — recommend manual check"
```

---

#### Check 5: Configuration & Infrastructure

The agent reads config files to find deployment-time vulnerabilities:

```
Config check — read:
- CORS config: origin whitelist? Not * with credentials?
- HTTP security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options set?
- Rate limiting: configured on auth and paid endpoints?
- Error handling: production error handler returns generic messages, not stack traces?
- Environment: DEBUG/NODE_ENV=development set for production?
- HTTPS: server config enforces TLS redirect?
- File storage: uploads stored outside web root? Access controlled?
- Docker: non-root user? No unnecessary exposed ports? No secrets in image layers?
- CI/CD: deploy secrets from environment, not checked into repo?
```

---

#### Check 6: Cross-Slice Interaction Audit

Issues that span multiple slices — these are the most dangerous and the hardest for per-slice checks to catch:

```
1. Are there hardcoded values in one slice that should be env vars shared across slices?
   (API URLs, service endpoints, shared secrets)

2. Do two slices implement the same auth check differently? (inconsistent patterns)
   (One uses middleware, another checks inline — both correct? Any bypass vector?)

3. Does the order of middleware matter?
   (Auth before body parser? Rate limiter before auth?)

4. Are error responses consistent?
   (One route returns {error: "message"}, another returns stack trace)

5. Are there any "TODO: fix security" or "FIXME: add auth" comments?
   (These are deferred vulnerabilities — surface them)

  6. Does every new feature flag have a removal path?
    (Feature flags left on = permanent bypass)
```

---

#### Check 7: BE ↔ FE Contract Conformance (fullstack only)

When `scope == fullstack` and `api-contract.md` exists, verify the two sides actually agree — this is the gap per-slice checks cannot see:

```
1. ROUTE MATCH — For every endpoint the FE calls, does the BE expose it?
   (FE fetches /api/v2/users but BE only serves /api/users → break)
2. SHAPE MATCH — Does the BE request schema accept what the FE sends,
   and does the BE response shape match what the FE consumes?
   (BE returns {data:[...]}; FE reads .items → break)
3. STATUS MATCH — Does the BE return the status codes the FE handles?
   (BE sends 429 on rate-limit; FE only handles 401/500 → unhandled)
4. AUTH MATCH — Does the FE send auth the BE expects (header vs cookie),
   and does CORS origin == the FE's deployment origin?
5. CONTRACT DRIFT — Is any endpoint implemented/consumed but NOT in
   api-contract.md? → either the contract is stale or the code diverged.
```

Any mismatch is a Critical finding: the build "passes" per-slice but the app is broken end-to-end.

---

#### Check 8: Generate Risk Register

Consolidate all findings into a risk register:

```markdown
## Risk Register

### Critical (Must Fix Before Deploy)
| # | Issue | Location | Reasoning |
|---|-------|----------|-----------|
| 1 | SQL injection | src/users.ts:42 | String concat: `WHERE id = ${id}` |

### High (Should Fix Before Deploy)
| # | Issue | Location | Reasoning |
|---|-------|----------|-----------|
| 1 | Missing rate limit | src/auth.ts:15 | Login endpoint has no rate limiting |

### Medium (Document and Schedule)
| # | Issue | Location | Acceptance |
|---|-------|----------|------------|
| 1 | Deprecated package | package.json | safe:moment.js@2.29 — schedule replacement |

### Low (Informational)
| # | Issue | Location | Note |
|---|-------|----------|------|
| 1 | Unused dependency | package.json | lodash remains from earlier refactor |

### Summary
- Critical: [count]
- High: [count]
- Medium: [count]
- Low: [count]
- Fixed during HARDEN: [count]
```

**Simplify:**
- Understand before simplifying (Chesterton's Fence)
- Simplify one thing at a time
- Run tests after each change
- Rule of 500: >500 lines → automate

**Exit criterion:** All Critical/High findings resolved. Risk register documents any accepted risks with explicit reasoning.

**State write:** Update state. Save risk register to `.dev-craft/risk-register.md`.
