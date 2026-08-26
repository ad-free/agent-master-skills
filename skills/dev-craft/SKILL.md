---
name: dev-craft
description: |
  Run the 15-phase full-stack engineering pipeline with persistent `.dev-craft`
  state. Use for new features, refactoring, multi-module work, or resuming
  sessions. Invoked by: planner → implementer → verifier.
model: big-pickle
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - Task
triggers:
  - "build this feature"
  - "run dev-craft"
  - "start a new feature"
  - "resume my work"
  - "implement the plan"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  phase-count: 15
  topology-support: [mono, multi]
  domain: fullstack
  integrates-with: [planning-and-task-breakdown, verification-before-completion, verification-before-completion, debugging-and-error-recovery]
---

TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# dev-craft

## Relationship to existing skills

- `planning-and-task-breakdown` — produces PLAN.md that feeds into this skill's REQUIRE phase
- `verification-before-completion` — layered validation before merge; dev-craft's REVIEW phase invokes this
- `verification-before-completion` — evidence gates before claiming done; invoked at every phase exit
- `debugging-and-error-recovery` — invoked during TEST phase when suites fail
- `code-review-and-quality` — 8-axis review protocol used in REVIEW phase
- `bug-hunting` — security-focused debugging for security-sensitive code
- `testing-strategies` — decides WHAT kind of test to write; invoked before TEST phase

## When to Use

- Given a prompt, PLAN.md, or feature request
- Starting a new project or feature
- Task spans multiple files or modules
- Resuming work from a previous session
- Need more than a single-file change

**When NOT to use:** Single-line fixes, typo corrections, trivial config changes — skip the full pipeline for these. Exception: the **Minimum Bar** still applies (no cryptic names, no legacy idioms) — see `skills/SHARED.md` → *Minimum Bar*. The deterministic lint gate in `references/lint-rules.md` is not skipped just because the pipeline is.

## The Iron Law

<HARD-GATE>
```
NO CODE WITHOUT DESIGN APPROVAL
```

Implementation without approved spec = wasted hours of rework.
</HARD-GATE>

After ANY request, output STATUS (phase, next step, state). When the human gives ad-hoc fixes, route through STATUS resume — never silently edit.

```
STATUS: Phase <name> [✅/⬜]
NEXT: <single next action>
STATE: sessionFile=<file>, lastBuildFix=<count>
```

If no pending action: `STATUS: Awaiting instructions. NEXT: None. STATE: ...`

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

## Memory System

`.dev-craft/` directory created on first run:

```
.dev-craft/
├── state.json       # currentPhase, completed, stack, slices
├── plan.md          # Evolving plan from Align → Design
├── domain.md        # Domain model (from REQUIRE or project-discovery)
├── build-order.md   # Module dependency sequencing
├── estimation.md    # Cost/schedule validation
├── context.md       # Domain glossary (shared language)
├── decisions/       # ADRs — key decisions captured
│   └── 001-*.md
├── sessions/        # Handoff docs for context rotation
│   └── session-YYYYMMDD-N.md
└── config.json      # Project config (linter, formatter, test cmds)
```

### Session Creation Checklist (mandatory)

Every new task MUST go through this checklist before any code is written:

1. Load or initialize `state.json`.
2. Confirm task intent — if all phases were completed, ask "New task on same project?" before proceeding.
3. Create session file at `sessions/session-YYYYMMDD-N.md` with at minimum: Date, task summary, scope classification, checklist of expected phases.
4. Record `sessionFile` in `state.json`.
5. After every phase, append results to the session file and update `state.json`.

> **Rationale:** Without this checklist, agents skip session creation, batch state updates, and lose traceability across context resets. A session file is not optional paperwork — it is the agent's sole recovery point if context crashes mid-pipeline.

### Resume Logic

| Scenario | Behavior |
|---|---|
| No `.dev-craft/` | Phase 0.5 (REQUIRE) — check for spec files |
| DOMAIN.md exists but not loaded | Load into REQUIRE |
| `state.json` exists but `sessionFile` is missing or stale | Treat as suspect — flag to user |
| `state.json` exists and `sessionFile` is current | Load state, skip completed phases |
| All phases complete | Ask for new task, create session |
| Context near limit | Generate handoff doc |

## Stack Detection

Run during Phase 2 (ALIGN). Scan dependency files for exact versions.

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
│   └── No → surface to human: "No linter/formatter — recommend installing one. Proceed without?"
│
└── Type checker detected?
    └── Yes → every slice MUST pass type check
```

## Pipeline Phases

```
[0] LOAD → [0.2] SCOPE (be/fullstack × build/ticket) → [0.5] REQUIRE → [1] ARCH-SCAN
    → [2] ALIGN → [3] DESIGN → [3.5] BUILD-ORDER → [3.7] REQUIREMENTS-EXTRACTION
    → [4] SOURCE → [4.5] CONTRACT (fullstack only) → [5] BUILD → [6] TEST
    → [7] REVIEW → [8] HARDEN → [9] SHIP
    → [S] STATUS (anytime: navigation + drift + requirements-coverage aid)
```

> **Ticket mode short-circuits:** when `mode == ticket`, skip REQUIRE/REQUIREMENTS-EXTRACTION unless the change alters spec coverage — go LOAD → SCOPE → scoped BUILD → TEST → REVIEW → SHIP. SCOPE decides.

Each phase:
```
Phase → Output
LOAD → state.json initialized
REQUIRE → domain.md (domain model, features, priorities)
ARCH-SCAN → Smell report
ALIGN → CONTEXT.md (shared language)
DESIGN → PLAN.md + ADRs
BUILD-ORDER → build-order.md (module dependency sequencing)
REQUIREMENTS-EXTRACTION → requirements.md (spec→task traceability matrix)  ← COVERAGE GATE
SOURCE → Fetched docs
BUILD → Vertical slices (TDD + SECURE + MATCH per slice)
TEST → Test output
REVIEW → Code review
HARDEN → Cross-cutting security + risk register
SHIP → Commit + ADRs + rollback plan
```

## Clean Code Patterns (from ECC backend-patterns)

Every slice must follow these clean code patterns:

### Naming
- Variables: descriptive, no abbreviations unless universally understood (`id`, `url`, `err`)
- Functions: verb-noun format (`getUserById`, `validateEmail`), no ambiguous names (`process`, `handle`, `doStuff`)
- Types/interfaces: PascalCase, noun-based (`User`, `CreateUserRequest`, `UserService`)
- Constants: SCREAMING_SNAKE_CASE for true constants, camelCase for config values
- Files: kebab-case for modules, PascalCase for components/types

### Structure
- One function per responsibility (Single Responsibility Principle)
- Functions under 20 lines; extract helpers if longer
- Files under 200 lines; split if larger
- Imports sorted: stdlib → third-party → internal, with blank lines between groups
- No unused imports, no wildcard imports

### Error Handling
- Every function that can fail returns a `Result<T, E>` type or throws a typed error — never returns `null`/`undefined` for failure
- Errors are typed, not strings — define error classes/enums for each domain
- Error messages are actionable: what failed, why, and how to fix
- Never swallow errors silently — always log, re-throw, or handle explicitly
- Defensive programming: validate all external inputs at boundaries (API handlers, DB queries, file I/O)

### Defensive Programming
- Validate all inputs at function entry (guard clauses, not nested ifs)
- Assert invariants at the start of critical functions
- Use `never` type for exhaustive switch/enum handling
- Handle all branches — no `else` that silently does nothing
- Fail fast: throw early, fail loudly, recover gracefully
- Null safety: never use `null` or `undefined` where a value is expected; use `Option<T>`/`X | None` patterns

### Type Safety
- Strict mode enabled (`strict: true` in tsconfig, `mypy --strict` for Python)
- No `any` types — use `unknown` with type narrowing
- No `@ts-ignore` or `# type: ignore` — fix the type instead
- All function signatures have explicit return types
- All public API surfaces have type definitions

## Non-Negotiable Gates (applied across ALL phases)

<HARD-GATE>
These gates fire at specific points and block progress if not satisfied. They exist because the pipeline is long and agents routinely skip them without a hard stop:

| Gate | Fires At | Fails If | Action on Failure |
|------|----------|----------|-------------------|
| **State Integrity** | Before every phase transition after SCOPE | `state.json` is missing, stale, or `sessionFile` is empty/null | Create/update state and session file before proceeding |
| **Skill Alignment** | SCOPE §0.2 step 3a | Classification is `fe` (frontend) but the running skill is dev-craft without a recorded `skillOverride` | Surface to user, get explicit approval or switch to ui-craft |
| **Session Exists** | Before BUILD phase | No `sessions/session-YYYYMMDD-N.md` exists for this run | Create session file first (see checklist above) |
| **Standing Navigation** | After ANY request finishes | Agent finishes a response without stating current phase + next step | This is a text-output rule — output MUST include "Current phase: X. Next: Y" or equivalent |
</HARD-GATE>

## Quality Gates (per-slice, enforced during BUILD)

Every slice must pass these gates before it is committed:

1. **Lint gate:** `ruff check` / `eslint` — 0 errors
2. **Type gate:** `mypy --strict` / `tsc --noEmit` — 0 errors
3. **Test gate:** relevant test suite — all pass
4. **Convention gate:** code matches project conventions (detected in ALIGN)
5. **Security gate:** no hardcoded secrets, no `eval`, no `innerHTML`, no `__proto__` manipulation
6. **Clean code gate:** no cryptic names, no legacy idioms, no `any`/`Object` types

**Automatic fail triggers:** claiming "zero issues" without evidence, a perfect score without running the tools, or treating unverified requirements as complete.

## Workflow

### Phase 0.5: REQUIRE — Domain Discovery

1. Scan for existing specs (PRODUCT.md, DOMAIN.md, PLAN.md, spec files)
2. If PRODUCT.md found → extract domain, modules, features, priorities
3. If DOMAIN.md found → load directly
4. If spec files found → load `project-discovery` or manually extract
5. If no specs found → proceed to ALIGN with questions
6. Validate domain model with user

**Exit criterion:** Domain model confirmed by user (or no specs available).

**State write:** Save domain model to `.dev-craft/domain.md`. Update state.json.

### Phase 1: ARCH-SCAN — Codebase Understanding & Mapping

1. Full directory tree scan
2. Frontend architecture scan (if FE exists)
3. Backend architecture scan (if BE exists)
4. Build the codebase map using the template in `references/codebase-map-template.md`
5. Read at least 10-20 files across layers to confirm conventions
6. Present summary to human

**Exit criterion:** Codebase map confirmed by human.

**State write:** `state.json.codebaseMap = ".dev-craft/codebase-map.md"`.

### Phase 2: ALIGN — Grill + Detect + Glossary

1. Load domain model if `.dev-craft/domain.md` exists
2. Domain-calibrated questions (use domain model to scope questions)
3. If no domain model, do basic discovery (one question at a time)
4. Surface assumptions
5. Define "Out of scope" explicitly
6. Detect stack (framework, linter, formatter, type checker versions)
7. Build glossary in context.md
8. Detect code conventions from existing source files (read 10-20 files across layers)
9. Image analysis (if screenshot provided)

**Exit criterion:** Human confirms scope with explicit yes. Conventions detected for non-greenfield projects.

**State write:** Save stack to state.json. Save context.md. Save image analysis if present. Save detected conventions to state.json.

### Phase 3: DESIGN — Spec + Plan + ADRs

1. Write spec covering: objective, commands, project structure, code style, testing strategy, boundaries
2. Map dependency graph
3. Slice vertically (one complete feature path per slice)
4. Write tasks with Given-When-Then acceptance criteria (see `planning-and-task-breakdown`)
5. Write ADRs for architecture decisions

**Cross-skill invocations in this phase:**
- If this change adds/reshapes an API surface → invoke `api-design`
- If this change requires a structural pattern decision → invoke `architecture-patterns`
- Write resulting ADRs per `documentation-engineering`'s format

**Exit criterion:** Human reviews and approves.

**State write:** Save plan.md. Save ADRs to decisions/.

### Phase 3.5: BUILD-ORDER — Module Dependency Sequencing

1. Load module list from domain.md or plan.md
2. Build sequence respecting DAG dependencies
3. Assign slices per module
4. Save build-order.md

**Exit criterion:** Build order documented and user-approved for complex projects.

### Phase 3.7: REQUIREMENTS-EXTRACTION — Spec → Task Traceability (COVERAGE GATE)

1. Extract every requirement from the source spec (exhaustive, literal)
2. Assign stable IDs: REQ-001, REQ-002, ...
3. Trace each requirement to a plan task
4. Build the traceability matrix → `.dev-craft/requirements.md`
5. Self-review the matrix against the spec (do not delegate)
6. Present matrix + gaps to the human

<HARD-GATE>
**Exit criterion:** Every `[REQUIRED P1]` and `G1` requirement is traced to a task with an acceptance criterion. G2/G3 gaps may be deferred **only with explicit human acknowledgement**.
</HARD-GATE>

**State write:** Save `.dev-craft/requirements.md`. Record `requirementsExtracted`, `coverageGaps`, `deferredRequirements` in state.json.

### Phase 4: SOURCE — Document Verification

1. Read exact versions from dependency files
2. Fetch specific official docs for each feature
3. Extract patterns, API signatures, deprecation warnings
4. Cite sources inline during BUILD
5. Flag uncovered patterns

**Source hierarchy:** Official docs > Official blog/changelog > MDN Web Standards > ❌ Stack Overflow, blog posts

**Exit criterion:** All dependencies verified.

### Phase 4.5: CONTRACT — API contract (fullstack only)

1. If codebase has API endpoints — extract from actual source files, do not guess
2. For new endpoints, add to contract with `[NEW]` tag
3. Write `api-contract.md` (single canonical name)
4. Record path in state.json (`apiContract`)
5. Hand to ui-craft — it must consume this file, not invent endpoints

**Exit criterion:** `api-contract.md` exists, accurately reflects existing endpoints.

### Phase 5: BUILD — TDD + Incremental + Secure-by-Construction

**Branch isolation (mandatory):** Every BUILD run starts on a dedicated feature branch. For `multi` topology, the branch is created in every repo the scope touches.

**Base-branch guard:** Treat `main`, `master`, `develop` as protected. If `git branch --show-current` reports a base branch at commit time, STOP and create/checkout the feature branch first.

**Process per slice:**

```
0a. BRANCH-GUARD — Confirm we are on the feature branch
0b. BRANCH — Ensure dedicated feature branch exists
1. RED    — Write failing test
2. GREEN  — Write minimal code to pass
3. SECURE — Verify the slice has no security issues
4. MATCH  — Verify code matches existing project conventions
5. LINT   — Run linter + formatter
6. TYPE   — Run type checker
7. TEST   — Run test suite
8. COMMIT — Atomic commit (re-run per-repo branch-guard from BUILD intro first)
```

**Per-slice deep detail (SECURE tree, MATCH tree, Rules, Git Worktree Mode):** Load `references/build-protocol.md` when executing a slice.

**Exit criterion:** All slices implemented, committed, security-verified, and convention-matched.

### Phase 6: TEST — Full Suite + Diagnose

1. Run suites per scope (run what the scope touches; for `multi`, run in the relevant repo)
2. Contract conformance (fullstack only): assert running app matches `api-contract.md`
3. If all pass → Proceed to Phase 7
4. If any fail → **Invoke:** `debugging-and-error-recovery`
5. Re-run the relevant suites after every fix

**Exit criterion:** All relevant suites pass; for fullstack, contract conformance holds.

### Phase 7: REVIEW — Quality Audit

**Invoke:** `review-orchestrator` to spawn parallel specialized subagents (security, style, issues/debug, performance). If security-critical code, also invoke `bug-hunting`.

**Process:**
1. Load `review-orchestrator` skill — spawns `review-subagents` in parallel:
   - `security-reviewer` (or `bug-hunting` patterns for deep security audit)
   - `style-reviewer` (uses `language-rules` plugin)
   - `issues-debug-reviewer` (logic bugs, edge cases, error paths)
   - `performance-reviewer` (algorithms, queries, resource usage)
2. Each subagent returns findings to `.dev-craft/review-findings/<name>.json`
3. `review-orchestrator` aggregates, deduplicates, and scores findings
4. Load `code-review-and-quality` skill — consumes subagent findings for 8-axis scoring
5. Review entire diff across all axes: Correctness, Readability, Architecture, Performance, Security, Testing, Modern Patterns
6. Categorize findings (Critical/Optional)
7. Run the lint gate — load `references/lint-rules.md` and execute its ruff config + cryptic-name grep. UP007/UP045 violations and any cryptic-name hit are automatic fails
8. Fix all Critical/Required findings

**Subagent Integration:** Each review subagent focuses on one domain with a specialized prompt, running in parallel. Findings are structured as JSON with file, line, severity, category, message, and fix. This parallel pattern reduces review time from ~21s (sequential) to ~8s (parallel).

**Reality-Check Discipline:**
- Default stance is "needs work" — first-pass implementations typically need 1-3 revision cycles
- Spec reality-check: for each P1/G1 row in `.dev-craft/requirements.md`, confirm the built code actually satisfies it
- Evidence, not assertion — run the linter, type checker, and full test suite and read the output
- Automatic-fail triggers: claiming "zero issues", a perfect score without evidence, or treating unverified requirements as complete

**Exit criterion:** All Critical/Required resolved **with evidence**, and every P1/G1 requirement in the traceability matrix verified against the built code.

### Phase 8: HARDEN — Cross-Cutting Security Verification

**Goal:** Verify security across all slices, not within individual slices. Catch cross-cutting issues that per-slice SECURE checks miss.

**Process:** Load `references/harden-checks.md` for the 8 concrete checks (secrets, auth/authz, injection surface, dependency CVE review, config/infra, cross-slice audit, BE↔FE contract conformance, risk register). Each check is a read-the-actual-code pass.

**Cross-ref against codebase map:** Do changes follow the documented component hierarchy, API contract, and schema conventions? Update the map if outdated.

**Cross-skill invocation:** Also invoke `observability-engineering` — security hardening and observability are separate concerns.

**Exit criterion:** All Critical/High findings resolved. Risk register documents any accepted risks with explicit reasoning.

**State write:** Update state. Save risk register to `.dev-craft/risk-register.md`.

### Phase 9: SHIP — Automated Release Workflow

1. Update ADRs for BUILD/HARDEN decisions
2. Update CONTEXT.md with new terms
3. Generate final HTML style guide preview
4. Final verification: lint + type + build all pass, run secrets scanner, dead code removed
5. Atomic commit with conventional message format
6. Define rollback strategy
7. Mark state complete

**Exit criterion:** Clean commit with rollback plan.

## Quality Gates

- [ ] State integrity maintained (state.json + session file updated every phase)
- [ ] Codebase map current and confirmed by human
- [ ] Domain model confirmed by user
- [ ] Stack versions detected and code matches exact versions
- [ ] Every slice has Given-When-Then acceptance criteria
- [ ] Every slice passes lint + type + test gates
- [ ] No cryptic names, no legacy idioms, no `any`/`Object` types
- [ ] All errors are typed and handled (no swallowed errors)
- [ ] All inputs validated at boundaries (defensive programming)
- [ ] Security scan passed (no Critical/High findings)
- [ ] Contract conformance verified (fullstack)
- [ ] P1/G1 requirements verified against built code
- [ ] Rollback strategy defined and tested
- [ ] ADRs written for all architecture decisions

## Error Handling

| Failure Mode | Response |
|--------------|----------|
| State file missing or stale | Create/update state and session file before proceeding |
| Test suite fails | Invoke `debugging-and-error-recovery` |
| Lint/type check fails | Fix the issue, re-run, do not skip |
| Security scan finds Critical/High | Block deploy, remediate before proceeding |
| Contract conformance fails | Fix the implementation to match the contract |
| Context near limit | Generate handoff doc, resume next session |
| 3+ failed fix attempts (during TEST) | Stop, invoke `debugging-and-error-recovery` |

## References

- `references/build-protocol.md` — Per-slice deep detail: SECURE tree, MATCH tree, branch verification, git worktree isolation
- `references/harden-checks.md` — 8-point cross-cutting security audit
- `references/lint-rules.md` — Ruff config, cryptic-name grep, deterministic lint gate
- `references/modern-patterns.md` — Clean code patterns, defensive programming, error-handling paradigms (from ECC backend-patterns)
- `references/codebase-map-template.md` — Template for ARCH-SCAN codebase map