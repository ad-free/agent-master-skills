---
name: bug-hunting
description: Systematic vulnerability discovery methodology. Agent-driven code inspection for security audits, penetration testing, and responsible disclosure. No external tools required.
metadata:
  origin: agent-master-skills
---

# Bug Hunting

## Overview

Systematic methodology for finding, validating, and reporting security vulnerabilities. Every check is done by the agent reading, analyzing, and reasoning about code — no external tools required. Tools are mentioned only as optional accelerators if available.

**Philosophy:** The agent is the most powerful analysis engine. It can read every file, trace every data flow, and reason about every vulnerability class. Tools are shortcuts, not prerequisites.

## When to Use

- Security audit of codebase or application
- Pre-release security review
- After architecture changes (regression testing)
- When code handles auth, payments, PII, or user data
- Before deploying to production

**When NOT to use:** General feature development, UI polish, documentation.

## The Iron Law

```
NO VULNERABILITY CLAIM WITHOUT REPRODUCIBLE PROOF
```

"Probably a bug" is noise. "Here's the exact code path and the request that proves it" is evidence.

---

## The Bug Hunter's Mindset

### Attack Surface Thinking

Every feature is an attack surface. Every input is an entry point. Every integration is a trust boundary.

```
INPUT → PROCESSING → STORAGE → OUTPUT
  │          │          │        │
  ├──        ├──        ├──      ├──
Injection  Logic     Injection  XSS
XSS        Flaws     XSS        Info Leak
Path       Auth      Path       Path
Traversal  Bypass    Traversal  Traversal
```

### Chain Thinking

One bug is good. A chain of bugs is excellent.

```
Low: Debug endpoint exposed
  ↓
Medium: Debug endpoint leaks internal IPs
  ↓
High: Internal IPs bypass WAF restrictions
  ↓
Critical: Direct DB access from bypassed WAF
```

**Don't stop at the first finding.** Ask: "What can I do from here?"

---

## Phase 1: Reconnaissance — Read the Codebase

Understand the attack surface by reading the code, not running tools.

### Step 1: Read the routes/endpoints

```bash
# Agent: Read all route definition files to understand every entry point
grep -rn "router\.\(get\|post\|put\|delete\|patch\)\|@\(Get\|Post\|Put\|Delete\|Patch\)\|app\.\(get\|post\)" --include="*.{ts,js,py,java,go}" .
```

For each endpoint, note:
- Does it require authentication?
- Does it accept user input? (path params, query params, body)
- What does it return?
- Is there rate limiting?

### Step 2: Read the auth/authorization logic

Files to inspect:
- `middleware/auth*`, `middleware/auth*.ts`
- Any JWT validation, session handling, permission checks
- Password hashing, reset flows

### Step 3: Read database access layer

Files that construct SQL/queries:
- Raw SQL strings, ORM queries
- Parameterized vs concatenated
- Migrations for existing data

### Step 4: Read configuration files

- `.env`, `config/*`: secrets, DB URLs, API keys
- `Dockerfile`, `docker-compose.yml`: exposed ports, environment
- `nginx.conf`, `Caddyfile`: HTTP headers, CORS
- `package.json`, `requirements.txt`, `go.mod`: dependency versions

### Step 5: Build attack surface map

```
TARGET:
├── Endpoints: [read from routes]
├── Auth: [read from auth code]
├── Database: [read from DB layer]
├── Config: [read from config files]
├── Dependencies: [read from package files]
└── Integrations: [read from API client code]
```

---

## Phase 2: Agent-Driven Code Scan

The agent scans the codebase by reading files and looking for patterns. No tools needed.

### Secrets & Credentials

The agent reads every file and looks for:

```bash
# Agent: grep for common secret patterns
grep -rn "api_key\|API_KEY\|secret\|SECRET\|password\|PASSWORD\|token\|TOKEN\|auth_token\|private_key\|PRIVATE_KEY" \
  --include="*.{ts,js,py,java,go,rb,rs,php,env}" . \
  | grep -v "node_modules\|\.venv\|vendor\|/test\|/spec\|example\|sample\|\.md"
```

**For each hit, the agent reads the context and determines:**
- Is this a real secret or a placeholder/test value?
- Is it committed to version control?
- Is it referenced in production config?

**What the agent checks manually (no grep needed):**
- Hardcoded connection strings with credentials: `postgres://user:pass@host/db`
- JWT tokens, API keys, OAuth tokens in source
- Private keys (RSA, EC, SSH) embedded in files
- `.env` files committed to repo
- Secrets in Dockerfiles, CI configs, build scripts

### Injection Vulnerabilities

The agent reads data-flow paths from input → processing → output:

**SQL Injection: read every database query construction:**
- Raw SQL with string concatenation: `"SELECT * FROM users WHERE id = " + userId`
- ORM methods that accept raw SQL
- Stored procedures with dynamic queries
- NoSQL queries with unescaped input: `{ "username": req.body.name }`

**Command Injection: read every OS command execution:**
- `exec()`, `spawn()`, `system()`, `shell_exec()`, `Runtime.getRuntime().exec()`
- `child_process.execSync()`, `subprocess.run(shell=True)`
- Template literals/path construction with user input: `exec('ls ' + filename)`

**XSS: read every place user data reaches HTML:**
- `dangerouslySetInnerHTML`, `v-html`, `innerHTML`, `document.write`
- Template engines (Jinja2, Pug, EJS) without autoescaping
- API responses that include user input without Content-Type safety
- `href` attributes with user-controlled values

**Path Traversal: read file operations with user input:**
- `fs.readFile(userInput)`, `open(userInput)`
- `sendFile()`, `download()` with user-controlled paths
- Image/file upload paths constructed from user data

**SSTI: read template rendering with user input:**
- `render_template_string(userInput)`, `Template(userInput).render()`
- Template engines with user-controlled template names

### Authentication & Authorization

The agent reads the auth flow end-to-end:

**Password handling:**
- Read password hashing code: is it bcrypt/argon2/scrypt or MD5/SHA1?
- Read password reset: is the token random? Single-use? Time-limited?

**Session/JWT:**
- Read JWT verification: is the signature verified? Is `alg` constrained?
- Read session storage: httpOnly cookie vs localStorage vs URL param
- Read token expiry: is there a reasonable TTL?

**Authorization:**
- Read every protected endpoint: is there actually a permission check?
- Read the authorization logic: does it verify ownership or just role?
- Look for IDOR: are resources fetched by user ID without ownership check?

### Security Misconfigurations

The agent reads config files directly:

**CORS:**
- Read backend CORS config: is origin `*` in production?
- Read middleware: does it allow credentials with permissive origins?

**HTTP Headers:**
- Read nginx/apache/Caddy config: are CSP, HSTS, X-Frame-Options set?

**Debug/Info Leakage:**
- Read error handlers: do they return stack traces in production?
- Read `DEBUG=true` or similar in production config
- Read `/api/docs`, `/graphql?introspection` — are these exposed to unauthenticated users?

**Cloud/Infrastructure:**
- Read IaC configs (Terraform, CloudFormation): S3 bucket public access? Security groups open to `0.0.0.0/0`?
- Read Dockerfile: is the app running as root? Exposed ports?

### Dependency Vulnerabilities

The agent reads dependency files and reasons about risk:

**What to check (by reading package files, no tools):**
- Read `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`
- Flag known-vulnerable versions the agent knows about (old React, jQuery, Log4j, etc.)
- Flag packages that are unmaintained (> 2 years since last release, per agent knowledge)
- Flag packages with excessive permissions or access

**Fallback (if tools available):**
```bash
# Optional — only if npm/pip available
npm audit --audit-level=high
pip-audit
```

---

## Phase 3: Deep Manual Testing — OWASP Top 10

The agent now traces through each vulnerability class by reading the actual code paths.

### A01: Broken Access Control

**Agent reads code to verify:**
1. Read route definitions — which routes have auth middleware?
2. Read the auth middleware — what does it actually check? Does it bail early?
3. Read each data access method — does it scope queries by the current user?
4. Read admin endpoints — is there an admin role check before the handler?

**Code patterns to flag:**
- Data fetched by `id` from URL without checking `userId` from session
- Admin routes that only check if user exists, not if user has admin role
- APIs that return all records when no filter is provided
- UUID-based access without additional ownership verification

### A02: Cryptographic Failures

**Agent reads code to verify:**
1. Read password hashing — bcrypt/argon2 rounds ≥ 10, or plain MD5?
2. Read JWT — is the signing key strong? Is algorithm restricted?
3. Read TLS config (if available) — minimum TLS 1.2?
4. Read how sensitive data is stored — encrypted at rest?

**Code patterns to flag:**
- `md5()`, `sha1()` for passwords
- `jwt.verify(token, 'secret')` with a weak/hardcoded secret
- `alg: 'none'` allowed in JWT library config
- Sensitive data in JWT payload (not encrypted, just base64)

### A03: Injection

**Agent traces data flow for each injection type:**

*SQLi check:*
- Find all `db.query()`, `db.execute()`, `cursor.execute()` calls
- Are they using parameterized queries (`?`, `$1`, `%s` with cursor.execute args)?
- Or string concatenation: `f"SELECT * FROM users WHERE id = {user_id}"`
- Check stored procedures too

*NoSQLi check:*
- Find all MongoDB/NoSQL queries: `collection.find({ username: req.body.name })`
- Are they accepting objects from the request body directly?
- Check for `$where`, `$gt`, `$ne` operator injection

*XSS check:*
- Find where user input enters the response HTML
- In React: `dangerouslySetInnerHTML`, `dangerouslySetInnerHTML={{ __html: userContent }}`
- In Vue: `v-html`, `v-bind` with URL params
- In APIs: responses that include user input with `text/html` content type

*Command injection check:*
- Find `exec`, `spawn`, `system`, `shell_exec`, `subprocess.run(shell=True)`
- Is user input part of the command string?
- Is there any validation/sanitization before execution?

*SSTI check:*
- Find template render calls with user input: `render_template_string(template)`
- In Jinja2: `Template(user_input).render()`
- In Pug/EJS: `res.render('page', { name: req.query.name })` — safe (data, not template)

### A04: Insecure Design

**Agent reads code to verify:**
1. Rate limiting: read middleware — is there a rate limiter? Is it applied to auth routes?
2. Account lockout: read login handler — does it track failed attempts?
3. Password reset: read the reset flow — is the token unpredictable? Single-use?
4. Mass assignment: read create/update handlers — are fields whitelisted or is the entire body passed to the DB?

**Code patterns to flag:**
- No rate limiter middleware
- `User.create(req.body)` or `db.users.insert(req.body)` — mass assignment
- Password reset token is `md5(userId + date)` — predictable
- Login always returns success, no lockout tracking

### A05: Security Misconfiguration

**Agent reads config files to verify:**
1. CORS: `Access-Control-Allow-Origin: *` with `credentials: true`?
2. Headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options present?
3. Debug mode: `DEBUG=true`, `NODE_ENV=development`, `DJANGO_DEBUG=True` in production config?
4. Directory listing: static file server without `index` fallback?
5. Stack traces: error handler returns full error objects in production?

### A06: Vulnerable Components

**Agent reads dependency files and checks:**
1. Known-vulnerable versions from agent knowledge (Log4j < 2.17, jQuery < 3.5, etc.)
2. Packages with known supply chain attacks
3. Deprecated packages no longer maintained
4. Version mismatch (package.json says "latest" with no lockfile)

### A07: Authentication Failures

**Agent reads auth code to verify:**
1. Login rate limiting? (Read route handler)
2. Password strength validation? (Read registration handler)
3. Session/Token rotation on login? (Read login — old session invalidated?)
4. JWT validation — is expiry checked? Signature verified? `iss`/`aud` validated?
5. 2FA implementation — is backup code single-use? Rate-limited OTP?

### A08: Data Integrity Failures

**Agent reads code to verify:**
1. JWT `alg: none` allowed? (Read JWT config)
2. Serialization — Python `pickle.loads(user_input)`, Java `ObjectInputStream.readObject()`?
3. CI/CD — are pipeline configs modifiable by PRs from forks?
4. Auto-update — is the update mechanism verifying signatures?

### A09: Logging & Monitoring Failures

**Agent reads code to verify:**
1. Audit logging — are sensitive actions (deletion, role change) logged?
2. Log content — are passwords, tokens, or PII being logged?
3. Error handling — are errors silently swallowed? (`except: pass`)
4. Alerting — is there any monitoring for repeated failures?

### A10: SSRF

**Agent reads code to verify:**
1. URL fetching — `axios.get(userUrl)`, `requests.get(url)`, `fetch(userInput)`
2. Are there URL parameters in the API that get fetched server-side?
3. Is there any validation on URL schemes/hosts?
4. Cloud metadata endpoints accessible via fetched URLs?

**Code patterns to flag:**
- `fetch(req.query.url)`, `requests.get(data.url)` without validation
- Webhook handlers that fetch callback URLs from request body
- Image/file fetching from user-provided URLs

---

## Phase 4: Exploitation — Prove Impact

For each finding, the agent produces evidence by tracing the exact code path.

### Proof Format (No Tools Required)

```markdown
## Vulnerability: [Title]

**CWE:** [CWE-ID]
**Severity:** [Critical/High/Medium/Low]
**Location:** `file.ts:42`

### Code Path (Agent Traced)
1. Input enters at `routes/users.ts:15` — `req.params.id`
2. No auth check before handler
3. Passed to `services/userService.getUser(id)` at `services/userService.ts:22`
4. Query: `db.query("SELECT * FROM users WHERE id = " + id)`
5. Returns full user object including `password_hash` and `email`

### Impact
Attacker can enumerate all users, extract PII, and potentially escalate with password data.

### Suggested Fix
1. Add auth middleware to route
2. Scope query to current user: `WHERE id = ? AND user_id = ?`
3. Never return `password_hash` in responses
```

### Chain Building

Combine findings for higher severity impact:

```
LOW: No rate limiting on login endpoint
LOW: No account lockout after failures
COMBINED: Credential stuffing attack possible → HIGH
```

---

## Phase 5: Remediation & Verification

### Fix Guidance

For each finding, the agent:
1. Reads the vulnerable code path
2. Implements the fix using the correct pattern
3. Verifies no other instances of the same pattern exist
4. Writes a regression test for the vulnerability

### Fix Patterns (No Tools Needed)

| Vulnerability | Fix Pattern |
|---------------|-------------|
| SQL Injection | Replace string concat with parameterized queries: `?` or `$1` placeholders |
| XSS | Replace `innerHTML` with `textContent` or use DOMPurify |
| Command Injection | Use execFile/spawn with args array, not shell string |
| Secrets in code | Move to env vars, check .gitignore, rotate the secret |
| Missing Auth | Add auth middleware to route definition |
| Weak Password Hash | Use bcrypt (cost=12) or argon2 |
| Missing CSP | Add helmet/secure-headers middleware |
| Mass Assignment | Whitelist allowed fields explicitly |

### Verification

After each fix:
1. Re-read the fixed code to confirm the pattern is correct
2. Read related code to catch identical patterns elsewhere
3. Run the test suite: `npm test` / `pytest` / etc.
4. Confirm the specific vulnerability path is closed

---

## OWASP Top 10 (2021) — Agent Coverage Map

| # | Category | Agent checks by reading |
|---|----------|------------------------|
| A01 | Broken Access Control | Route middleware, auth logic, query scoping |
| A02 | Cryptographic Failures | Password hashing, JWT config, TLS settings |
| A03 | Injection | SQL/NoSQL/Command/XSS/SSTI data flow tracing |
| A04 | Insecure Design | Rate limiting, lockout, mass assignment |
| A05 | Security Misconfiguration | CORS, headers, debug mode, error handlers |
| A06 | Vulnerable Components | Dependency versions from package files |
| A07 | Authentication Failures | Login flow, session handling, JWT validation |
| A08 | Data Integrity Failures | Serialization, JWT alg, CI/CD config |
| A09 | Logging Failures | Log sensitive data, silent error suppression |
| A10 | SSRF | URL fetching, webhook handlers, image fetch |

---

## Optional Tool Accelerators

If the development environment happens to have these tools, they can speed up specific checks:

| Check | Tool (if available) | Agent Alternative |
|-------|--------------------|--------------------|
| Secrets | `trufflehog`, `gitleaks` | Grep for patterns + agent reads every hit context |
| SAST | `semgrep`, `bandit`, `gosec` | Agent traces every data-flow path manually |
| SQLi | `sqlmap` | Agent reads every query construction pattern |
| Dependencies | `npm audit`, `pip-audit` | Agent reads package files and checks known CVEs |
| DAST | `zap`, `nuclei` | Agent traces HTTP request/response logic by reading route handlers |

**The agent always does the check.** Tools only make it faster.

---

## Bug Bounty Checklist

Before submitting a report:

- [ ] Can I reproduce it reliably? (traced the exact code path)
- [ ] What's the actual impact? (not theoretical)
- [ ] Is this in scope? (was this code modified in this change?)
- [ ] Have I chained it with other findings for higher severity?
- [ ] Is the fix correct? (read the fixed code to confirm)
- [ ] Are there more instances of the same pattern?
- [ ] Do tests still pass after the fix?

---

## Common Rationalizations

| Rationalization | Agent's Reality Check |
|----------------|----------------------|
| "That endpoint is authenticated" | Read the middleware. Is the middleware actually applied to that route? Verify by reading the route definition. |
| "We use parameterized queries" | Read the database calls. Are ALL of them parameterized? Check for string interpolation in edge cases. |
| "We don't have secrets in code" | Read every file. Secrets hide in config files, tests, comments, docs, and Dockerfiles. Don't assume. |
| "The framework handles XSS" | Read the raw HTML output. Frameworks protect template data, not `dangerouslySetInnerHTML`. |
| "Our dependencies are safe" | Read the version numbers. Log4j, Spring4Shell, and other CVEs affect specific versions. Cross-reference with agent knowledge. |
| "We validate input on the frontend" | Read the API handler. Frontend validation is UX, not security. What does the backend actually receive and process? |

## Red Flags

- Routes defined without any middleware/reference to auth
- Raw string concatenation in database queries
- Any `exec()` / `shell_exec()` / `subprocess.run(shell=True)` with user data
- `dangerouslySetInnerHTML` / `v-html` / `innerHTML` with user content
- Secrets (API keys, passwords, connection strings) in any tracked file
- CORS with `origin: *` and `credentials: true`
- `process.env.NODE_ENV !== 'production'` or `DEBUG=true` in production config
- `.env` file tracked in version control
- Login endpoint without rate limiting
- JWT library configured allowing `alg: 'none'`

## Integration

**Use with:**
- `dev-craft` Phase 8 (HARDEN) — agent-driven security scan before shipping
- `code-review-and-quality` — security axis feeds into this skill for deep dive
- `debugging-and-error-recovery` — security bugs found here are debugged systematically
- `verification-before-completion` — verify security fixes before claiming done
