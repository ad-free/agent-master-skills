---
name: dev-craft
description: Full-stack engineering pipeline with persistent memory. Detects stack, scans code smells, enforces modern patterns, runs lint/type/test per slice. Resumes via .dev-craft/ runs (indexed, per-task state).
metadata:
  origin: agent-master-skills
---

# dev-craft

## Overview

Turns a prompt into production-quality code.
Every phase has a clear goal, exit criteria, and a human checkpoint.
Persists state to `.dev-craft/` (per-task run folders, tracked in `index.json`) so work survives across sessions.

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

---

## Input Quality Handling

Before starting, assess the input:

| Input Type | Action |
|------------|--------|
| Short/vague ("Build HRM", "Make me a CRM") | → Do NOT proceed automatically. Ask user: "Your prompt is short — I need more context. Should I load `product-thinking` to refine this into a spec first, or can you provide more details?" |
| Has spec files attached (xlsx, csv, md, pdf) | → Suggest or auto-load `project-discovery` to extract domain model |
| Has PRODUCT.md from product-thinking | → Load it into REQUIRE phase |
| Has DOMAIN.md from project-discovery | → Load it into REQUIRE phase |
| Clear spec text or PLAN.md | → Proceed to ALIGN |
| "Just build it, I'll know it when I see it" | → DO NOT proceed. Explain: "Without a written spec, there's a 90% chance I build the wrong thing. 10 minutes of `product-thinking` saves hours of rework." |

### The Clarification Protocol

When input is too vague:

1. Say: "I need to understand the project before I can build it. Do you have:
   - A spec document? → I'll use project-discovery
   - A vague idea? → I'll use product-thinking to refine it
   - A PLAN.md? → I'll load it directly"
2. Based on answer, invoke the right skill or ask the user for more detail.

---

## Memory System

`.dev-craft/` directory created on first run. State is **scoped per task/run** so every
PLAN.md, prompt, or Jira ticket gets its own isolated workspace — and history is preserved
for later skill improvement.

```
.dev-craft/
├── index.json           # Registry of all runs (audit trail / skill-improvement log)
├── active               # Symlink → runs/<slug> of the currently active run
└── runs/
    └── <slug>/          # One folder per task (slug from input, see [0] LOAD)
        ├── state.json   # currentPhase, completed, stack, slices, source
        ├── plan.md      # Evolving plan from Align → Design
        ├── domain.md    # Domain model (from REQUIRE or project-discovery)
        ├── build-order.md  # Module dependency sequencing
        ├── estimation.md   # Cost/schedule validation
        ├── context.md   # Domain glossary (shared language)
        ├── risk-register.md  # HARDEN output
        ├── decisions/   # ADRs — key decisions captured
        │   └── 001-*.md
        ├── sessions/    # Handoff docs for context rotation
        │   └── session-YYYYMMDD-N.md
        └── config.json  # Project config (linter, formatter, test cmds)
```

**Slug rules** (how `<slug>` is derived — full logic in [0] LOAD):

| Input type | Slug source |
|---|---|
| Jira ID (`PROJ-123`) | the ID verbatim → `PROJ-123` |
| `PLAN.md` given | filename stem, or slug of its `#` title → `add-auth-flow` |
| Free-form prompt | auto-derived from keywords, **overrideable** by the user |

`index.json` is the single source of truth for "what has this project run through dev-craft".
It lets you later review past runs (inputs, outcomes, durations) to improve the skill itself.

### Resume Logic

| Scenario | Behavior |
|---|---|
| No `.dev-craft/` | Create it (with `index.json`). Phase 0.5 (REQUIRE) — check for spec files |
| Input matches an existing run slug | Load that run's `state.json`, skip completed phases |
| Input is new (new slug) | Create `runs/<slug>/`, preserve all prior runs |
| DOMAIN.md exists but not loaded | Load into REQUIRE |
| `state.json` exists (in the matched run) | Load state, skip completed phases |
| All phases complete | Ask "New task on same project?" → new slug or re-run |
| Context near limit | Generate handoff doc in the run's `sessions/`, resume next session |

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
[0] LOAD → [0.5] REQUIRE → [1] ARCH-SCAN → [2] ALIGN → [3] DESIGN
    → [3.5] BUILD-ORDER → [4] SOURCE → [5] BUILD → [6] TEST
    → [7] REVIEW → [8] HARDEN → [9] SHIP
```

Each phase:

```
Phase → Output
LOAD → runs/<slug>/state.json initialized
REQUIRE → domain.md (domain model, feature list, priorities)
ARCH-SCAN → Smell report
ALIGN → CONTEXT.md (shared language)
DESIGN → PLAN.md + ADRs
BUILD-ORDER → build-order.md (module dependency sequencing)
SOURCE → Fetched docs
BUILD → Vertical slices (TDD + SECURE + MATCH per slice)
TEST → Test output
REVIEW → Code review
HARDEN → Cross-cutting security + risk register
SHIP → Commit + ADRs + rollback plan
```

---

### [0] LOAD — Initialize or Resume

**Step 0.1 — Resolve the task slug from the input.** Every run gets an isolated
`runs/<slug>/` folder. Derive the slug:

1. **Jira ID** in the prompt or as the input (regex `[A-Z][A-Z0-9]+-\d+`, e.g. `PROJ-123`)
   → slug = the ID verbatim.
2. **`PLAN.md` provided** → slug from:
   - the filename stem if not the generic `PLAN` (`plan-add-auth` → `add-auth`), or
   - the slug of the first `#` heading, else `plan-<date>`.
3. **Free-form prompt** → auto-derive a short slug from keywords (e.g. "build a billing
   service" → `billing-service`). Then **ask the user to confirm or override**:
   ```
   I'll track this as run "<slug>". OK, or give it a different short name?
   ```
   This keeps history readable when reviewing past runs.

**Step 0.2 — Look up or create the run.**

- Read `.dev-craft/index.json` (create `{"runs":[]}` if absent).
- **Slug already registered** → load `runs/<slug>/state.json`:
  - complete → Ask: "Re-run this task, or start a new one?"
  - incomplete → Load `context.md`, restore slice progress.
- **Slug new** → create `runs/<slug>/`, register it in `index.json` with
  `{ slug, source, createdAt, status:"in_progress" }`.
- Point `.dev-craft/active` symlink at `runs/<slug>` (best-effort; skip on filesystems
  without symlink support and rely on `index.json` `activeSlug` instead).

**Step 0.3 — Detect existing source code** (only when starting fresh in this run):
- Existing code (src/, lib/, app/) → Phase 0.5 (REQUIRE)
- Greenfield → Phase 0.5 (REQUIRE)

Write state after LOAD.

---

### [0.5] REQUIRE — Domain Discovery

**Goal:** Ingest existing requirements (specs, files, domain model) before any design or code decisions.

**Process:**

1. **Scan for existing specs:**
   - Check for PRODUCT.md (from product-thinking)
   - Check for DOMAIN.md (from project-discovery)
   - Check for PLAN.md (from planning-and-task-breakdown)
   - Check for spec files (xlsx, csv, md, pdf, txt)

 2. **If PRODUCT.md found:**
    Extract domain, modules, features, priorities, dependencies.
    Generate `.dev-craft/runs/<slug>/domain.md` from the spec.

 3. **If DOMAIN.md found:**
    Load directly into `.dev-craft/runs/<slug>/domain.md`.

4. **If spec files found (xlsx, csv, etc.):**
   If `project-discovery` skill is available, load it to extract domain model.
   Otherwise, manually scan and extract:
   ```
   ENTITIES FOUND:
   - Employee, Department, Attendance, Payroll...

   MODULES FOUND:
   - Employee Management (G1)
   - Attendance (G1) → depends on: Employee
   - Payroll (G1) → depends on: Employee, Attendance

   FEATURES FOUND:
   - CRUD employee records (G1)
   - Clock in/out (G1)
   - Calculate salary (G1)
   ```
    Save to `.dev-craft/runs/<slug>/domain.md`.

5. **If no specs found:**
   Proceed to ALIGN. ALIGN will ask clarifying questions.

6. **Validate domain model:**
   Present to user:
   ```
   Domain Model Summary
   ─────────────────────
   Modules: [N]
   Features: [N]
   G1: [N] features
   G2: [N] features
   G3: [N] features
   Dependencies: [N] module links
   
   Confirm this model? (Y/n/detail)
   ```
   If user says "n" or "detail", loop back to refine.

**Exit criterion:** Domain model confirmed by user (or no specs available).

**State write:** Save domain model to `.dev-craft/runs/<slug>/domain.md`. Update state.json.

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

**Goal:** Surface assumptions, sharpen requirements. If REQUIRE phase produced a domain model, use it to ask targeted questions. If not, do basic discovery.

**Process:**

 1. **Load domain model** if `.dev-craft/runs/<slug>/domain.md` exists:
   ```
   DOMAIN MODEL LOADED:
   - Modules: [list from domain.md]
   - Features: [count per module]
   - Priorities: G1=[count], G2=[count], G3=[count]
   - Dependencies: [module links]
   
   I'll use this to ask targeted questions about each module.
   ```

2. **Domain-calibrated questions** (instead of generic ones):
   - If HRM domain: "For Attendance module, do you need GPS check-in, QR code, or biometric?"
   - If E-commerce domain: "For Checkout, do you need one-page checkout or multi-step?"
   - If CRM domain: "For Pipeline, how many stages do you typically have?"
   
   **Use the domain model to scope questions to the actual modules being built.**

3. **If no domain model** (no REQUIRE phase), do basic discovery:
   - Ask one question at a time with best guess attached
   - Detect domain from keywords
   - Build glossary in context.md

4. Surface assumptions:
   ```
   ASSUMPTIONS:
   1. Web app (not native mobile)
   2. Auth uses JWT in httpOnly cookies
   3. Database is PostgreSQL
   → Correct me now or I'll proceed.
   ```

5. Define "Out of scope" explicitly

6. Detect stack:
   ```
   STACK DETECTED:
   - Python 3.12, FastAPI, SQLAlchemy 2.0
   - Node 22, React 19, Vite 6
   - Linter: ruff, Formatter: ruff
   - Type checker: mypy
   ```

7. Build glossary in context.md

8. **Detect code conventions** from existing source files:
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

9. **Image analysis** (if screenshot provided):
   ```bash
    python skills/image-to-design-spec/scripts/analyze.py --image <path> --format json --output .dev-craft/runs/<slug>/image-analysis.json
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

### Estimation Validation (after DESIGN, before SOURCE)

**Goal:** Catch cost/schedule discrepancies between plan and expectations.

**Process:**

1. Review each module's estimated effort:
   ```
   MODULE ESTIMATION:
   Employee Profile: ~3 days (5 slices × 0.5 day)
   Attendance: ~5 days (7 slices × 0.75 day)
   Payroll: ~8 days (complex: tax rules, calculations)
   Mobile App: ~10 days (native iOS + Android or RN)
   ```

2. Compare against any stated budget/schedule from domain.md:
   ```
   ESTIMATION CHECK:
   Module        Expected (from spec)   My estimate     Delta
   Attendance    4.5                    5.0             ~10%
   Payroll       5.2                    8.0             ⚠ ~35% (tax complexity)
   Mobile App    6.85                   10.0            ⚠ ~31%
   
   Total: 34.55 (spec) vs 40.0 (estimate) → ⚠ ~13% gap
   
   Flag any significant discrepancies for user review.
   ```

3. **Ask user:** "Total estimated effort is ~40 days. Does this match your expectations? Want me to descope some G2/G3 features?"

---

### [3.5] BUILD-ORDER — Module Dependency Sequencing

**Goal:** Determine optimal build sequence based on module dependencies and priorities.

**Only needed when:** Project has 3+ modules or complex cross-module dependencies.

**Process:**

1. **Load module list** from domain.md or plan.md:
   ```
   MODULES:
   1. Auth (G1) — no dependencies
   2. Employee Profile (G1) — depends on: Auth
   3. Attendance (G1) — depends on: Employee, Shift
   4. Shift (G1) — depends on: Employee
   5. Payroll (G1) — depends on: Employee, Attendance, Tax
   6. KPI (G2) — depends on: Employee
   ```

2. **Build sequence respecting dependencies:**
   ```
   Phase 1 (Foundation — G1):
     Auth ← no deps, required by everything
     Employee Profile ← only needs Auth
     Shift ← only needs Employee
   
   Phase 2 (Transactions — G1):
     Attendance ← needs Employee + Shift
     Leave ← needs Employee
   
   Phase 3 (Processing — G1):
     Payroll ← needs Employee + Attendance + Tax Config
     Tax Config ← no deps, but needed by Payroll
   
   Phase 4 (Evaluation — G2):
     KPI ← needs Employee
     Evaluation ← needs Employee + KPI
   
   Phase 5 (Extended — G2/G3):
     Recruitment ← needs Employee (for conversion)
     Onboarding ← needs Employee + Recruitment
     Internal Comms ← needs Employee
   
   Phase 6 (Mobile — G2):
     Mobile App ← needs all core API endpoints stable
   ```

3. **Assign slices per module:**
   Each module gets its own set of vertical slices.
   Example for Employee Profile:
   ```
   Module: Employee Profile (G1)
   Slice 1: Create employee record (DB schema + API + form)
   Slice 2: List/search employees (query + API + table)
   Slice 3: Edit employee details (update + API + form)
   Slice 4: Document upload (file handling + API + upload UI)
   Slice 5: Delete / deactivate (soft delete + confirm dialog)
   ```

4. **Save build-order.md**

**Exit criterion:** Build order is documented and user-approved for complex projects.

**State write:** Save `.dev-craft/runs/<slug>/build-order.md`.

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

#### Git Worktree Mode (for large/multi-module projects)

When a project has 3+ modules or needs parallel backend + frontend development,
use git worktree isolation:

```bash
git worktree add ../project-api api-slice     # Backend agent
git worktree add ../project-web web-slice      # Frontend agent
git worktree add ../project-mobile mobile-slice # Mobile agent
```

**Workflow:**
1. Define API contract first (OpenAPI spec)
2. Each agent works in its own worktree on its own branch
3. Backend implements API from contract
4. Frontend consumes API contract, builds UI
5. Mobile builds against same contract
6. Master agent merges worktrees via integration branch

**When to use worktree mode:**
- Project has separate backend + frontend
- Multiple developers/agents working simultaneously
- Module count > 5
- Estimated total effort > 2 weeks

**When NOT to use:** Single-module project, solo development, prototype/exploration.

**Cleanup:**
```bash
git worktree list
git worktree remove ../project-api
```

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
2. Review entire diff across all axes defined in `code-review-and-quality`:
   - Correctness, Readability, Architecture
   - Performance, Security, Testing, Modern Patterns
   (Conventions are already validated during BUILD MATCH step)
3. Categorize findings (Critical/Required/Nit/Optional)
4. Fix all Critical/Required findings

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

**State write:** Update state. Save risk register to `.dev-craft/runs/<slug>/risk-register.md`.

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

 1. Save state to `.dev-craft/runs/<slug>/state.json`:
    - Current phase and slice position
    - Incomplete tasks
    - Pending decisions

 2. Write handoff to `.dev-craft/runs/<slug>/sessions/session-YYYYMMDD-N.md`:
    - What was accomplished
    - What's in progress
    - What's next
    - Known issues

 3. Summarize: "Session saved under run '<slug>'. Run dev-craft to resume."

---

## Workflow Orchestration

For complex features spanning multiple domains.

### Workflow Types

| Workflow | Pipeline | When |
|----------|----------|------|
| SaaS MVP | product-thinking → planning-and-task-breakdown → dev-craft + ui-craft | New SaaS product |
| Admin Dashboard | dev-craft + ui-craft | Internal tool |
| E-commerce | product-thinking → planning-and-task-breakdown → dev-craft + ui-craft | Online store |
| API Service | dev-craft only | Backend API |
| Mobile App | dev-craft (backend) + agent-orchestration (mobile) | Mobile with backend |
| Landing Page | ui-craft only | Marketing site |
| Multi-module | product-thinking → planning-and-task-breakdown → dev-craft + agent-orchestration | Large project |

### Orchestration Pattern

```
1. THINK — If prompt is vague → product-thinking for PRODUCT.md
2. DISCOVER — If spec files exist → project-discovery for DOMAIN.md
3. PLAN — planning-and-task-breakdown for PLAN.md
4. REQUIRE — Load PRODUCT.md / DOMAIN.md into dev-craft
5. ALIGN — Domain-calibrated questions
6. DESIGN — Spec + ADRs + task list
7. BUILD-ORDER — Dependency-based sequencing
8. SOURCE — Official docs verification
9. BUILD — For large projects: agent-orchestration with git worktree
   For small projects: single-agent vertical slices
10. TEST — Full suite
11. REVIEW — code-review-and-quality
12. HARDEN — Cross-cutting security
13. SHIP — Commit + docs
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

dev-craft needs mobile:
- Note in state.json: `"mobileSliceNeeded": ["api-endpoints"]`
- Generate API contract in api-contract.md
- Resume with agent-orchestration

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
- No .dev-craft/ directory or index.json
- Security review skipped
- Commit messages: "WIP", "fix", "update"
- Vague prompt accepted without clarification
- Skipping REQUIRE when spec files exist
- Building modules in wrong dependency order
- No domain model for multi-module project
- No worktree isolation for parallel agents
- Starting BUILD without build-order.md for complex projects

## Verification

- [ ] ARCH-SCAN was run (or deferred with approval)
- [ ] .dev-craft/runs/<slug>/state.json exists with status: complete
- [ ] .dev-craft/index.json registers this run
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
- [ ] Input was assessed (vague prompts redirected to product-thinking)
- [ ] REQUIRE phase completed (or skipped with valid reason)
- [ ] Domain model exists in .dev-craft/runs/<slug>/domain.md (for multi-module projects)
- [ ] Build order documented in .dev-craft/runs/<slug>/build-order.md (for complex projects)
- [ ] Module dependencies respected during build

## See Also

- `plugins/security-audit/SKILL.md` — Deep security scan pipeline
- `references/modern-patterns.md` — Per-language guidance
- `references/phase-templates.md` — Templates for documents
- `product-thinking` — Refine vague ideas into structured specs
- `project-discovery` — Extract domain model from existing documents
- `agent-orchestration` — Multi-agent parallel builds with git worktree
- `quality-gates` — Layered validation pipeline
