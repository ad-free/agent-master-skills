---
name: bug-hunting
description: |
  Systematic security vulnerability discovery: Recon → Scan → Test → Exploit → Disclose.
  Use for security audits, pre-release reviews, and vulnerability assessments.
  Invoked by: security-auditor, code-reviewer.
version: 1.1.0
preamble-tier: 4
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
triggers:
  - "security audit"
  - "vulnerability scan"
  - "penetration test"
  - "find security issues"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  phases: 5
  proof-required: true
  integrates-with: [code-review-and-quality, verification-before-completion, dev-craft]
---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

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

### Chain Thinking

One bug is good. A chain of bugs is excellent.

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

---

## Phase 2: Agent-Driven Code Scan

The agent scans the codebase by reading files and looking for patterns. No tools needed.

### Secrets & Credentials

The agent reads every file and looks for:

```bash
# Agent: grep for common secret patterns
# REDACTED_SECRET
  --include="*.{ts,js,py,java,go,rb,rs,php,env}" . \
  | grep -v "node_modules\|\.venv\|vendor\|/.md"
```

**For each hit, the agent reads the context and determines:**
- Is this a real secret or a placeholder/test value?
- Is it committed to version control?
- Is it referenced in production config?

**What the agent checks manually (no grep needed):**
- Hardcoded connection strings with credentials: `postgre/db`
- JWT tokens, API keys, OAuth tokens in source
```bash
# EXAMPLE (do not run)
- Private keys (RSA, EC, SSH) embedded in files
```
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
- Read password hashing code: is it bcrypt/scrypt or MD5/SHA1?
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
- Read nginx/Caddy config: are CSP, HSTS, X-Frame-Options set?

**Debug/Info Leakage:**
- Read error handlers: do they return stack traces in production?
- Read `DEBUG=true` or similar in production config
- Read `/docs`, `/graphql?introspection` — are these exposed to unauthenticated users?

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

| Category | Verify | Flag Patterns |
|----------|--------|---------------|
| A02: Cryptographic Failures | Password hashing strength, JWT key & algorithm, TLS version, encryption at rest | `md5()`/`sha1()` for passwords, weak/hardcoded JWT secret, `alg: none`, sensitive data in JWT payload |

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

### A04–A10: Compact Reference

| Category | Verify | Flag Patterns |
|----------|--------|---------------|
| A04: Insecure Design | Rate limiting, account lockout, password reset token entropy, mass assignment protection | No rate limiter, `User.create(req.body)`, predictable reset token (`md5(userId+date)`), no lockout tracking |
| A05: Security Misconfiguration | CORS `*`+cred, security headers (CSP/HSTS/XFO), debug mode, directory listing, stack trace exposure | `origin: *`+`credentials: true`, `DEBUG=true` in prod, full error objects returned |
| A06: Vulnerable Components | Known-vulnerable versions, supply chain attacks, deprecated/unmaintained, version pinning | Log4j < 2.17, jQuery < 3.5, `"latest"` without lockfile |
| A07: Authentication Failures | Login rate limiting, password strength, session rotation, JWT validation (exp/sig/iss/aud), 2FA backup limits | No rate limiter on login, no lockout, JWT without exp/sig, 2FA backup codes reusable |
| A08: Data Integrity Failures | JWT `alg: none`, unsafe deserialization (`pickle`/`ObjectInputStream`), CI/CD security, auto-update signing | `alg: none`, `pickle.loads(user_input)`, unsigned auto-updates |
| A09: Logging & Monitoring Failures | Audit logging for sensitive actions, log content (no secrets), error handling (no silent `except: pass`), alerting for repeated failures | Secrets in logs, `except: pass`, no monitoring for brute force |
| A10: SSRF | URL fetching from user input, server-side URL params, URL scheme/host validation, cloud metadata access | `fetch(req.query.url)`, `requests.get(data.url)` unvalidated, webhook callback from body |

---

## Phase 4: Exploitation — Prove Impact

For each finding, the agent produces evidence by tracing the exact code path.

### Proof Format (No Tools Required)

```markdown
## Vulnerability: [Title]

**CWE:** [CWE-ID]
**Severity:** [Critical/Low]
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

Combine findings for higher severity impact.

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

- Routes without auth middleware
- Raw string concatenation in DB queries
- `exec()`/`shell_exec()` with user data
- Secrets committed to any tracked file

## Outputs / Handoffs

On completion, invokes: `skill("code-review-and-quality")` with context:
  - `findingsPath`: "bug-hunt-report.md"
  - `severityCounts`: {critical: N, high: N, medium: N, low: N}
  - `regressionTests`: [paths]

Then: `skill("verification-before-completion")` to verify fixes
Then: `skill("learn")` to capture security learnings

## Integration

- `dev-craft` HARDEN phase — security scan before shipping
- `code-review-and-quality` — security axis feeds deep dive
- `debugging-and-error-recovery` — systematic bug investigation