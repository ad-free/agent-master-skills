---
name: dev-craft
description: Full-stack engineering pipeline with persistent memory. Detects stack, scans code smells, enforces modern patterns, runs lint/type/test per slice. Resumes via .dev-craft/ state.
metadata:
  origin: agent-master-skills
---

# dev-craft

## Overview

Turns a prompt into production-quality code.
Every phase has a clear goal, exit criteria, and a human checkpoint.
Persists state to `.dev-craft/` so work survives across sessions.

**Philosophy:** Transparent, human-orchestrated, composable.
Skip any phase. Edit any phase. The pipeline serves you.

## When to Use

- Given a prompt, PLAN.md, or feature request
- Starting a new project or feature
- Task spans multiple files or modules
- Resuming work from a previous session
- Need more than a single-file change

**When NOT to use:** Single-line fixes, typo corrections, trivial config changes.

## The Iron Law

```
NO CODE WITHOUT DESIGN APPROVAL
```

Implementation without approved spec = wasted hours of rework.

## Memory System

`.dev-craft/` directory created on first run:

```
.dev-craft/
├── state.json       # currentPhase, completed, stack, slices
├── plan.md          # Evolving plan from Align → Design
├── context.md       # Domain glossary (shared language)
├── decisions/       # ADRs — key decisions captured
│   └── 001-*.md
├── sessions/        # Handoff docs for context rotation
│   └── session-YYYYMMDD-N.md
└── config.json      # Project config (linter, formatter, test cmds)
```

### Resume Logic

| Scenario | Behavior |
|---|---|
| No `.dev-craft/` | Phase 1 if codebase exists, Phase 2 if greenfield |
| `state.json` exists | Load state, skip completed phases |
| All phases complete | Ask "New task on same project?" |
| Context near limit | Generate handoff doc, resume next session |

## Stack Detection

Run during Phase 2 (ALIGN).
Scan dependency files for exact versions.

```
Read dependency files (package.json, requirements.txt, go.mod, Cargo.toml, etc.):
│
├── Framework/library found?
│   ├── Version explicit? → use that version for docs/code generation
│   ├── Version range (`^18.0.0`)? → resolve to installed or latest
│   └── No version? → ask user or default to latest
│
├── Linter/formatter detected?
│   ├── Yes → every slice MUST pass lint + format
│   └── No → surface to human:
│       "No linter/formatter — recommend installing one. Proceed without?"
│
└── Type checker detected?
    └── Yes → every slice MUST pass type check
```

## Pipeline Phases

```
[0] LOAD → [1] ARCH-SCAN → [2] ALIGN → [3] DESIGN → [4] SOURCE
    → [5] BUILD → [6] TEST → [7] REVIEW → [8] HARDEN → [9] SHIP
```

Each phase:
```
Phase → Output
LOAD → state.json initialized
ARCH-SCAN → Smell report (remediate first?)
ALIGN → CONTEXT.md (shared language)
DESIGN → PLAN.md + ADRs
SOURCE → Fetched docs
BUILD → Vertical slices (TDD + SECURE + MATCH per slice)
TEST → Test output
REVIEW → Code review
HARDEN → Cross-cutting security verification
SHIP → Commit + ADRs
```

---

### [0] LOAD — Initialize or Resume

Read `.dev-craft/state.json`:

**Not found →** Detect existing source code:
- Existing code (src/, lib/, app/) → Phase 1 (ARCH-SCAN)
- Greenfield → Phase 2 (ALIGN), skip ARCH-SCAN

**Found + complete →** Ask: "New feature? Start fresh?"

**Found + incomplete →** Load context.md, restore slice progress.

Write state after LOAD.

---

### [1] ARCH-SCAN — Codebase Smell Detection

**Goal:** Assess codebase health before adding new code.

**Process:**

1. Scan for Fowler's code smells:
   - Mysterious Name, Duplicated Code, Feature Envy
   - Data Clumps, Primitive Obsession, Repeated Switches
   - Shotgun Surgery, Divergent Change, Speculative Generality
   - Message Chains, Middle Man, Refused Bequest, Dead Code

2. Scan for design system health:
   - Check for tailwind.config.*, tokens.css, theme.ts
   - Check for shadcn/ui components (components/ui/)
   - Check for CSS custom properties (:root { --color-* })
   - Flag inconsistencies

3. Surface report:
   ```
   SMELL REPORT:
   1. [Duplicated Code] src/utils/format.ts:45-52
      → Extract shared function
   2. [Primitive Obsession] src/models/user.ts
      → Create discriminated union
   ```

4. Ask human to prioritize fixes

**Exit criterion:** Human approves remediation or defers.

**State write:** Save smells to state.json for REVIEW.

---

### [2] ALIGN — Grill + Detect + Glossary

**Goal:** Surface assumptions, sharpen requirements.

**Process:**

1. Ask one question at a time with best guess attached

2. Surface assumptions:
   ```
   ASSUMPTIONS:
   1. Web app (not native mobile)
   2. Auth uses JWT in httpOnly cookies
   3. Database is PostgreSQL
   → Correct me now or I'll proceed.
   ```

3. Define "Out of scope" explicitly

4. Detect stack:
   ```
   STACK DETECTED:
   - Python 3.12, FastAPI, SQLAlchemy 2.0
   - Node 22, React 19, Vite 6
   - Linter: ruff, Formatter: ruff
   - Type checker: mypy
   ```

5. Build glossary in context.md

6. **Detect code conventions** from existing source files:
   ```
   CONVENTIONS DETECTED: [read from src/ lib/ or existing files]
   ├── File organization: [features/ modules/ pages/]
   ├── Naming: files=[kebab/camel/snake] functions=[camel/snake] types=[Pascal/I]
   ├── Imports: [absolute/relative] exports=[named/default]
   ├── Error handling: [try-catch / Result types / error boundaries]
   ├── Structure: [single file per feature / split across layers]
   └── Testing: [colocated / __tests__/] style=[describe-it/test()]
   ```
   Read 3-5 existing files to detect patterns. Save to `state.json` for BUILD phase.
   If the project is greenfield (no existing code), skip detection and use sensible defaults based on the detected stack.

7. **Image analysis** (if screenshot provided):
   ```bash
   python scripts/analyze.py --image <path> --format json --output .dev-craft/image-analysis.json
   ```
   Present findings:
   ```
   IMAGE ANALYSIS:
   - Colors: [primary, secondary, accent, background]
   - Layout: [sidebar-main / single-column / grid / dashboard]
   - Mode: [light / dark]
   - Components: [if Gemini available]
   → Confirm these observations.
   ```
   Save to state.json for DESIGN phase reference.

**Exit criterion:** Human confirms scope with explicit yes. Conventions detected for non-greenfield projects.

**State write:** Save stack to state.json. Save context.md. Save image analysis if present. Save detected conventions to state.json (`conventions` key).

---

### [3] DESIGN — Spec + Plan + ADRs

**Goal:** Produce spec, task breakdown, architecture decisions.

**Process:**

1. Write spec covering:
   - Objective (what and why)
   - Commands (build, test, lint, type, dev)
   - Project structure
   - Code style (see references/modern-patterns.md)
   - Testing strategy
   - Boundaries (Always do / Ask first / Never do)

2. Map dependency graph

3. Slice vertically:
   ```
   Slice 1: User can create item (DB + API + UI)
   Slice 2: User can list items (query + API + UI)
   Slice 3: User can edit item (update + API + UI)
   ```

4. Write tasks with acceptance criteria

5. Write ADRs for architecture decisions:
   ```markdown
   # ADR-001: [Title]
   Status: Accepted
   Context: [Problem]
   Decision: [What we chose]
   Alternatives: [What else was considered]
   Consequences: [Impact]
   ```

**Exit criterion:** Human reviews and approves.

**State write:** Save plan.md. Save ADRs to decisions/.

---

### [4] SOURCE — Document Verification

**Goal:** Verify framework decisions against official docs.

**Process:**

1. Read exact versions from dependency files
2. Fetch specific official docs for each feature
3. Extract patterns, API signatures, deprecation warnings
4. Cite sources inline during BUILD:
   ```python
   # Source: https://docs.sqlalchemy.org/en/20/core/
   async with engine.connect() as conn:
       ...
   ```
5. Flag uncovered patterns:
   ```
   UNVERIFIED: No official docs for this pattern.
   Based on training data — verify before shipping.
   ```

**Source hierarchy:**
| Priority | Source |
|---|---|
| 1 | Official docs |
| 2 | Official blog/changelog |
| 3 | MDN Web Standards |
| ❌ | Stack Overflow, blog posts |

**Exit criterion:** All dependencies verified.

**State write:** Save source references to state.

---

### [5] BUILD — TDD + Incremental + Secure-by-Construction

**Goal:** Implement one vertical slice at a time. Every slice is verified for security as it's written — not deferred to a batch scan.

**Process per slice:**

```
1. RED    — Write failing test
2. GREEN  — Write minimal code to pass
3. SECURE — Verify the slice has no security issues
4. MATCH  — Verify code matches existing project conventions
5. LINT   — Run linter + formatter
6. TYPE   — Run type checker
7. TEST   — Run test suite
8. COMMIT — Atomic commit
```

**Step 3 — SECURE: Agent traces what the slice touches, then runs matching checks.**

The agent already knows every file in the slice. Start by reading the slice files to determine which security categories apply, then follow the matching branch:

```
Read the slice's files to determine what it touches:
│
├── AUTH (passwords, sessions, tokens, login, reset)?
│   Read auth code → verify:
│   ├── Passwords hashed with bcrypt/argon2? (cost ≥ 10)
│   ├── Session/JWT in httpOnly cookies, not URL params?
│   ├── JWT signature verified? `alg` restricted to RS256/HS256?
│   ├── Login rate-limited? Account lockout after N failures?
│   └── Password reset token random, single-use, time-limited?
│
├── DATA ACCESS (DB queries, API responses)?
│   Read each query → verify:
│   ├── All queries parameterized (`?`, `$1`, named params)? No string concat?
│   ├── ORM queries accept structured params, not raw SQL?
│   ├── Queries scoped to authenticated user? (`WHERE user_id = ?`)
│   └── List endpoints paginated?
│
├── USER INPUT (forms, params, uploads, headers)?
│   Read input handling → verify:
│   ├── Input validated at boundary (Zod, Pydantic, Joi)?
│   ├── File uploads: type whitelisted? Size limited? Outside web root?
│   ├── User content rendered in HTML? → escaped or safe APIs?
│   └── Any exec/spawn/subprocess with user data? → args array, not shell string
│
├── REGEX (validation, matching, routing)?
│   Read each regex → verify:
│   ├── ReDoS risk: nested quantifiers `(a+)+b`, overlapping `(a|aa)+b`,
│   │   unbounded `(.*a)*`? → rewrite without nesting, use atomic groups
│   ├── Injection: user input embedded in pattern `new RegExp(input)`?
│   │   → escape with re.escape(), never construct from input
│   ├── Anchors: missing `^...$` allows partial match? `/\d+/` matches "abc123def"
│   │   → use fullmatch or anchors for validation
│   ├── Unicode: JS without `u` flag? Python default behavior intended?
│   │   → add `u` flag in JS, use re.A if ASCII-only needed
│   └── Bounds: user-controlled `{m,n}` with large values?
│       → cap bounds, never accept user-controlled counts
│
├── BUSINESS LOGIC (payments, roles, permissions, state machines)?
│   Read authorization → verify:
│   ├── Ownership checked? (User A cannot access User B's data)
│   ├── Role/permission checks before admin operations?
│   ├── Critical actions (delete, role change, payment) logged?
│   └── Rate limiting on sensitive operations?
│
└── EXTERNAL INTEGRATIONS (webhooks, third-party APIs, MCP)?
    Read outbound code → verify:
    ├── URLs from user input? → validate scheme and host
    ├── Secrets read from env vars, not hardcoded?
    └── Webhook payloads signature-verified?
```

**Output per slice:**
```
SECURE CHECK: [slice name]
- Auth: [PASS / FLAG — issue]
- Data Access: [PASS / FLAG — issue]
- User Input: [PASS / FLAG — issue]
- Regex: [PASS / FLAG — issue]
- Business Logic: [PASS / FLAG — issue]
- Integrations: [PASS / FLAG — issue]
→ All PASS or fix FLAGs before MATCH
```

---

**Step 4 — MATCH: Agent verifies the slice matches existing project conventions.**

The agent reads existing code outside the current slice to detect conventions, then verifies the new code follows them.

**Conventions to detect from existing code:**

```
Read 3-5 existing files in the same area (same directory or feature) to detect:
├── File organization
│   - Where do similar files live? (features/ vs modules/ vs pages/)
│   - One component per file or grouped?
│   - Test files: colocated or in __tests__/ directory?
│
├── Naming conventions
│   - Files: camelCase, kebab-case, PascalCase, snake_case?
│   - Functions: fetchUser() vs get_user() vs UserFetcher?
│   - Variables: const or let? (most code uses const?)
│   - Types/Interfaces: IUser vs User vs UserType interface?
│
├── Import patterns
│   - Absolute imports (src/components/...) or relative (../../)?
│   - Index files for re-exports?
│   - Default export or named export?
│
├── Error handling
│   - try/catch blocks or .catch() chains or Result types?
│   - Custom error classes or generic Error?
│   - Error responses: consistent envelope format?
│
├── Code structure
│   - Single file per feature or split across files?
│   - Hooks in separate files or in components?
│   - State management approach?
│
└── Testing patterns
    - describe/it blocks or test()?
    - Assertion style: expect().toBe() or assert.equal()?
    - Mock patterns: jest.mock() or dependency injection?
```

**Verification:**
- For each convention detected, the agent reads the new slice code and flags violations
- Example: `"Existing code uses named exports, but this new file uses default export — fix to match project convention"`
- Example: `"Existing tests use describe/it blocks, new test uses test() — fix to match"`
- Example: `"Existing code imports from src/lib/* (absolute), new file uses relative ../../ — fix"`
- Convention violations are treated as Required severity (must fix before commit)

**MATCH output:**
```
MATCH CHECK: [slice name]
Conventions detected: [fileOrg, naming, imports, errorHandling, testing, structure]
- [count] violations found:
  - [file:line] — [convention violated] → [expected fix]
→ All violations fixed before LINT
```

**Rules:**
- **Simplicity first** — Three similar lines > premature abstraction
- **Scope discipline** — Don't touch code outside slice
- **One slice at a time** — Pipeline loops over slices
- **TDD seams** — Test at public interfaces only
- **Mock at boundaries only** — Real > fakes > stubs > mocks
- **Feature flags** — For risky production changes
- **Form generation** — React Hook Form + Zod (React projects)
- **Design system** — Use tokens, no ad-hoc values
- **SECURE before MATCH, MATCH before LINT** — Security, then consistency, then quality

**Exit criterion:** All slices implemented, committed, security-verified, and convention-matched.

**State write:** Save slices, security notes, and convention profile to state.json.

---

### [6] TEST — Full Suite + Diagnose

**Goal:** Run full test suite. Fix every failure.

**Process:**

1. Run full suite: `npm test` / `pytest` / `cargo test`

2. If all pass → Proceed to Phase 7

3. If any fail → **Invoke:** `debugging-and-error-recovery`
   - This skill handles structured root-cause investigation
   - Do NOT embed debugging procedures here — defer to the skill

4. Re-run full suite after every fix

**Exit criterion:** Full test suite passes.

**State write:** Update state.

---

### [7] REVIEW — Quality Audit

**Goal:** Quality gate before shipping.

**Invoke:** `code-review-and-quality` for seven-axis review. If security-critical code, also invoke `bug-hunting`.

**Process:**

1. Load `code-review-and-quality` skill (and `bug-hunting` for security-sensitive code)
2. Review entire diff across seven axes:
   - Correctness, Readability, Architecture
   - Performance, Security, Testing, Modern Patterns
3. Categorize findings (Critical/Required/Nit/Optional)
4. Fix all Critical/Required findings

**Exit criterion:** All Critical/Required resolved.

**State write:** Save review findings.

**Exit criterion:** All Critical/Required resolved.

**State write:** Save review findings.

---

### [8] HARDEN — Cross-Cutting Security Verification

**Goal:** Verify security across all slices, not within individual slices. Catch cross-cutting issues that per-slice SECURE checks miss.

The agent now has the full codebase in context. It reads across all slices to find issues no single slice could surface.

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

#### Check 7: Generate Risk Register

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

---

### [9] SHIP — Docs + Commit + Finalize

**Goal:** Deliver with full traceability.

**Process:**

1. Update ADRs for any BUILD/HARDEN decisions
2. Update CONTEXT.md with new terms
3. Final verification:
   - Lint + type + test + build all pass
   - Dead code removed
   - HARDEN risk register is clean (no unaddressed Critical/High findings)
4. Update CHANGELOG
5. Atomic commit:
   ```
   type(scope): short description

   - What changed and why
   - Key decisions (reference ADRs)
   - What was intentionally NOT done
   ```
6. Define rollback strategy:
   - Feature flag toggling: < 1 minute
   - Code revert: specify commit
   - Database: migration revert command

**Exit criterion:** Clean commit with rollback plan.

---

### [H] HANDOFF — Cross-Session Context

**When:** Context > 80% full, or human says "continue later".

**Process:**

1. Save state to state.json:
   - Current phase and slice position
   - Incomplete tasks
   - Pending decisions

2. Write handoff to sessions/session-YYYYMMDD-N.md:
   - What was accomplished
   - What's in progress
   - What's next
   - Known issues

3. Summarize: "Session saved. Run dev-craft to resume."

---

## Workflow Orchestration

For complex features spanning multiple domains.

### Workflow Types

| Workflow | Pipeline |
|----------|----------|
| SaaS MVP | dev-craft + ui-craft |
| Admin Dashboard | dev-craft + ui-craft |
| E-commerce | dev-craft + ui-craft |
| API Service | dev-craft only |
| Landing Page | ui-craft only |

### Orchestration Pattern

```
1. PLAN — Decompose into backend/frontend slices
2. BACKEND — Run dev-craft for API/database/auth
3. HANDOFF — Generate API contract
4. FRONTEND — Run ui-craft using API contract
5. INTEGRATION — Run dev-craft for testing
6. SHIP — Coordinate commits
```

### Cross-Skill Communication

dev-craft needs UI:
- Note in state.json: `"uiSliceNeeded": ["login-form"]`
- Generate API contract in api-contract.md
- Resume with ui-craft

ui-craft needs backend:
- Note in state.json: `"backendSliceNeeded": ["auth-api"]`
- Generate API spec in api-spec.md
- Resume with dev-craft

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I know what they want" | #1 cause of AI failure is misalignment |
| "Just start coding" | No spec = scope creep, wrong architecture |
| "Tests later" | You won't. Tests after test implementation |
| "Too simple to verify" | Training data is stale |
| "Lint after slices" | Lint debt compounds |
| "Tests pass, it's good" | Tests don't catch architecture/security |
| "Commit at the end" | Large commits destroy history |
| "Prototype, skip security" | Prototypes become production |
| "Fix architecture later" | Rot compounds fast |
| "Skip arch scan" | 2-min scan prevents 2-hour rework |

## Red Flags

- Skipping ARCH-SCAN on codebase with > 10 files
- Starting without completed Align phase
- Human checkpoints skipped
- Code before fetching current-version docs
- Multiple slices in one commit
- Lint/type/tests failing but proceeding
- No ADRs for decisions
- "Fix it later" for Critical findings
- No .dev-craft/ directory
- Security review skipped
- Commit messages: "WIP", "fix", "update"

## Verification

- [ ] ARCH-SCAN was run (or deferred with approval)
- [ ] .dev-craft/state.json exists with status: complete
- [ ] All slices implemented and committed
- [ ] Full test suite passes
- [ ] Linter + formatter pass
- [ ] Type checker passes
- [ ] No debug tags or temp files
- [ ] ADRs written for decisions
- [ ] CONTEXT.md up to date
- [ ] HARDEN risk register clean (no unaddressed Critical/High findings)
- [ ] Every slice had SECURE check pass before commit
- [ ] Commit references ADRs
- [ ] Human approved every checkpoint

## See Also

- `plugins/security-audit/SKILL.md` — Deep security scan pipeline
- `references/modern-patterns.md` — Per-language guidance
- `references/phase-templates.md` — Templates for documents
