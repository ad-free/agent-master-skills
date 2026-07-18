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

**Standing navigation rule:** After finishing ANY request — a phase, a fix, or an answer — the agent MUST close by stating the current phase and the next valid step (run the `[S] STATUS` protocol). When the human asks for a fix/tweak outside the phase loop, route it through STATUS's resume-after-ad-hoc-fix routing; never silently edit and claim done. This keeps the human oriented and ties every action back to what they asked for.

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

### Resume Logic

| Scenario | Behavior |
|---|---|
| No `.dev-craft/` | Phase 0.5 (REQUIRE) — check for spec files |
| DOMAIN.md exists but not loaded | Load into REQUIRE |
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
[0] LOAD → [0.2] SCOPE (be/fe/fullstack × build/ticket) → [0.5] REQUIRE → [1] ARCH-SCAN
    → [2] ALIGN → [3] DESIGN → [3.5] BUILD-ORDER → [3.7] REQUIREMENTS-EXTRACTION
    → [4] SOURCE → [4.5] CONTRACT (fullstack only) → [5] BUILD → [6] TEST
    → [7] REVIEW → [8] HARDEN → [9] SHIP
    → [S] STATUS (anytime: navigation + drift + requirements-coverage aid)
```

> **Ticket mode short-circuits:** when `mode == ticket`, skip REQUIRE/DESIGN/BUILD-ORDER/REQUIREMENTS-EXTRACTION unless the change alters spec coverage — go LOAD → SCOPE → scoped BUILD → TEST → REVIEW → SHIP. SCOPE decides.

Each phase:

```
Phase → Output
LOAD → state.json initialized
REQUIRE → domain.md (domain model, feature list, priorities)
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

> **Why REQUIREMENTS-EXTRACTION exists:** This pipeline enforces *process* discipline
> (phases, checkpoints, TDD) but, on its own, does NOT guarantee *feature completeness*.
> A dense 300-line spec can be "planned" while 6 P1 requirements silently fall through
> the cracks. This phase makes spec coverage a first-class, machine-checkable artifact.

---

### [0.2] SCOPE — Classify the work (BE / FE / Fullstack, Build / Ticket)

**Goal:** One gate that decides the entire downstream shape of the run. Every later phase (REQUIRE, DESIGN, BUILD, TEST, HARDEN, SHIP, cross-skill handoff) reads the scope decision made here. This is what makes dev-craft correct for a backend-only bug ticket, a frontend-only tweak, a fullstack feature, and a greenfield build — without separate pipelines.

**Why this exists:** The skill was originally written as "dev-craft = backend, ui-craft = frontend." That binary breaks two ways: (1) a large existing repo contains BE *and* FE, so building them needs a shared contract; (2) an incoming ticket is often BE-only or FE-only on a codebase mid-build, and forcing the full greenfield pipeline is wasted overhead. SCOPE classifies intent up front so the right phases run.

**Process:**

0. **Detect repo topology** (how the code is laid out — this decides where git/state/contract operations run):
    - `mono`  — BE and FE in ONE repo (e.g. `backend/` + `frontend/` dirs, or a single fullstack app).
    - `multi` — separate repos: a BE repo and a FE repo (two checkouts, two remotes).
    Heuristic:
    ```bash
    # mono: backend + frontend signals in the SAME checkout
    has_be=$( test -d backend || grep -q '"fastapi"\|"django"\|"flask"' package.json 2>/dev/null && echo y )
    has_fe=$( test -d frontend || grep -q '"react"\|"vue"\|"next"' package.json 2>/dev/null && echo y )
    # multi: user passed two repo paths, or only one side exists here and the other is elsewhere
    ```
    If the request names two repo paths (e.g. `~/be-api` and `~/web-app`), or only BE *or* only FE is present in the current checkout, treat as `multi` and ask the user for the sibling repo path. Record `topology` (`mono`/`multi`).
    For `multi`, record `repos: { be: "<path>", fe: "<path>" }` and a `contractRepo` — the repo that owns `api-contract.md` (default: the BE repo). Every git/state/contract command below is **scoped to the relevant repo(s)** via `cd "<repo>"`.

1. **Detect what exists** (don't ask if the filesystem answers):
    ```bash
    # backend signals (mono: cwd; multi: $repos.be)
    # frontend signals (mono: cwd; multi: $repos.fe)
    ```
    Record `repoHasBE`, `repoHasFE`.

2. **Classify DOMAIN** (what this run touches):
    - `be`     — backend code only (API, services, DB, workers)
    - `fe`     — frontend code only (components, pages, styles, client state)
    - `fullstack` — both, and they must agree (FE consumes a BE API)
    Derive from the request; if ambiguous and the repo has both, ask: *"Is this BE, FE, or fullstack?"* Never assume.

3. **Classify MODE** (how much process is warranted):
    - `build`  — new feature / greenfield / multi-file change → full pipeline.
    - `ticket` — scoped change on an existing codebase (bug fix, small enhancement, config) → reduced pipeline (see routing below).
    Heuristic: if the request names an existing module/file/endpoint/component, or says "fix/adjust/ticket/bug/hotfix", it is a `ticket`. If it describes something new, it is `build`. When unsure, prefer `ticket` for existing repos (less overhead) but confirm.

4. **Resolve the pipeline shape** from the two axes + topology:

    | TOPOLOGY | DOMAIN  | MODE     | Pipeline                                                                 |
    |----------|---------|----------|--------------------------------------------------------------------------|
    | `mono`   | `be`    | `build`  | full dev-craft (REQUIRE…SHIP), no CONTRACT needed                        |
    | `mono`   | `be`    | `ticket` | LOAD → SCOPE → scoped BUILD slice → TEST → REVIEW → SHIP; skip REQUIREMENTS-EXTRACTION/DESIGN/BUILD-ORDER unless spec coverage changes |
    | `mono`   | `fe`    | `build`  | ui-craft full (owns DESIGN/tokens); dev-craft not needed                |
    | `mono`   | `fe`    | `ticket` | ui-craft, jump to BUILD consuming existing design system; skip ALIGN/DESIGN |
    | `mono`   | `fullstack` | `build` | dev-craft with **CONTRACT** (§4.5) before BUILD; ui-craft consumes `api-contract.md` |
    | `mono`   | `fullstack` | `ticket` | CONTRACT (update touched endpoints) → scoped BE + FE slices → TEST (both) → REVIEW (contract conformance) → SHIP |
    | `multi`  | `be`    | any      | dev-craft in BE repo only; branch in BE repo; FE repo untouched          |
    | `multi`  | `fe`    | any      | ui-craft in FE repo only; branch in FE repo; BE repo untouched          |
    | `multi`  | `fullstack` | any   | BE in BE repo, FE in FE repo, **paired branches** in BOTH repos, one shared `api-contract.md` (in `contractRepo`); cross-repo conformance in HARDEN/REVIEW |

5. **Branch per unit of work (repo-scoped, never one global branch):**
    - Each `build`/`ticket` gets its **own** branch derived from scope + mode:
      ```
      <type>/<scope>-<short-description>[-<issue-id>]
      type ∈ { feat, fix, refactor, chore, test, docs }
      scope ∈ { be, fe, fs }
      examples:
        feat/fs-user-auth      (mono: one branch;  multi: paired be+fe branches)
        fix/be-payroll-calc-142
        fix/fe-login-align
      ```
    - **mono:** create the single branch in the one repo.
    - **multi:** create the branch in **every repo the scope touches**:
      ```bash
      # fullstack ticket across two repos → paired branches
      cd "$beRepo" && git checkout -b "fix/be-payroll-142"
      cd "$feRepo" && git checkout -b "fix/fe-payroll-142"
      ```
      Each repo's `state.json` records its own `activeBranch`; the SCOPE record links them via `linkedBranches: { be: "fix/be-payroll-142", fe: "fix/fe-payroll-142" }`. A BE-only or FE-only `multi` ticket branches only its own repo.
    - This replaces the single `buildBranch` assumption: a BE hotfix can run on `fix/be-payroll-calc` while a feature branch `feat/fs-user-auth` is mid-BUILD. Keep a `branches` map of `{unitId: {be?, fe?}}` so units can be resumed and switched.
    - The branch-isolation + base-branch guard from BUILD (§5) applies to **every** per-unit branch, in **every** repo it was created in.

6. **Interrupt / resume between units:** If a `ticket` arrives while a `build` is `in_progress`, do NOT abandon the build:
    - Stash the current phase pointer: `state.suspendedPhase = currentPhase`, `state.suspendedBranch = activeBranch` (and `suspendedBranches` for multi).
    - Do the ticket on its own branch(es) per step 5.
    - On ticket completion, restore: `git checkout "$suspendedBranch"` in each relevant repo, set `currentPhase = suspendedPhase`. The STATUS protocol (§S) surfaces this automatically.

**State write:** `topology` (`mono`/`multi`), `scope` (`be`/`fe`/`fullstack`), `mode` (`build`/`ticket`), `repos` (multi only), `contractRepo` (multi only), `activeBranch`, `branches` (map of unitId → {be?, fe?}), `linkedBranches` (multi), and (if suspended) `suspendedPhase`/`suspendedBranch`(es).

**Exit criterion:** DOMAIN and MODE are decided and recorded; downstream phases know which shape to run.

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
   Generate `.dev-craft/domain.md` from the spec.

3. **If DOMAIN.md found:**
   Load directly into `.dev-craft/domain.md`.

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
   Save to `.dev-craft/domain.md`.

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

**State write:** Save domain model to `.dev-craft/domain.md`. Update state.json.

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

1. **Load domain model** if `.dev-craft/domain.md` exists:
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
    python skills/image-to-design-spec/scripts/analyze.py --image <path> --format json --output .dev-craft/image-analysis.json
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

**State write:** Save `.dev-craft/build-order.md`.

---

### [3.7] REQUIREMENTS-EXTRACTION — Spec → Task Traceability (COVERAGE GATE)

**Goal:** Guarantee every explicitly stated requirement from the source spec is traced
to a concrete plan task with an acceptance criterion. Catch coverage gaps *before* any
code is written. This is the phase that prevents "the pipeline ran perfectly but we
missed 6 P1 requirements."

**Why this phase exists:** ALIGN captures decisions; DESIGN writes a plan. Neither
mechanically proves the plan covers the spec. A 343-line spec with 12 `[REQUIRED P1]`
markers will lose requirements in summarization. This phase is a line-by-line audit.

**Input:** The source spec (from REQUIRE → `domain.md`, or the original `docs/*.md` /
PRODUCT.md / DOMAIN.md). If no source spec exists, skip this phase.

**Process:**

1. **Extract every requirement** from the source spec. Be exhaustive and literal:
   - For each paragraph/bullet/table row that expresses a capability, constraint, or
     non-functional rule, write one requirement row.
   - Preserve the spec's own priority markers verbatim
     (`[REQUIRED P1]`, `🔴 [REQUIRED P1]`, `⚪ [FUTURE PHASE]`, `G1/G2/G3`).
   - Capture CONCRETE constraints as requirements, not prose:
     e.g. "JWT payload contains only `user_id`, `company_id`, `permission_version`" →
     a row, not a footnote.
   - Do NOT paraphrase away detail. Quote the operative clause.

2. **Assign each requirement a stable ID:**
   ```
   REQ-001  [REQUIRED P1]  employee_code auto-generated via PG SEQUENCE (NV0001...)
   REQ-002  [REQUIRED P1]  login lockout after 5 failures / 15 min + audit_log
   REQ-003  ⚪ [FUTURE]     AWS deployment
   ```

3. **Trace each requirement to a plan task.** Map REQ-ID → task ID in PLAN.md
   (DESIGN phase). Every requirement must resolve to at least one task whose
   acceptance criteria verify it.

4. **Build the traceability matrix** and save to `.dev-craft/requirements.md`:
   ```markdown
   # Requirements Traceability Matrix — <project>

   Source spec: docs/hansa_global.md (343 lines)
   Extracted: 47 requirements (12 P1, 9 G1, 18 G2, 8 G3/Future)

   | REQ-ID | Priority | Requirement (verbatim clause) | Traced Task(s) | Acceptance Ref | Status |
   |--------|----------|-------------------------------|----------------|----------------|--------|
   | REQ-001 | P1 | `employee_code` auto via PG SEQUENCE | B1, B2 | B1-AC1 | ✅ |
   | REQ-002 | P1 | lockout 5 fails/15min + audit_log | A7 | A7-AC2 | ✅ |
   | REQ-011 | P1 | Cross-day shifts UTC+7 display | D1, D2 | D1-AC3 | ⚠️ GAP |
   | REQ-027 | G1 | Leave: full/half/hourly + carry-forward | — | — | ❌ GAP |

   ## Gaps (must resolve before BUILD)
   - REQ-011: no task covers UTC+7 presentation conversion
   - REQ-027: Leave module not in plan at all
   ```

5. **Self-review the matrix against the spec** (do not delegate this):
   - Re-read the spec section by section. For each requirement you extracted, confirm
     a row exists. For each row, confirm a task + acceptance ref exists.
   - Search the spec for priority markers you may have skipped:
     `grep -nE "REQUIRED P1|🔴|G1|Must have|must implement" <spec>`.
   - Any P1 / G1 requirement with no traced task = a blocking gap.

6. **Present the matrix + gaps to the human.** Do not auto-skip gaps.

**Exit criterion (HARD GATE):** Every `[REQUIRED P1]` and `G1` requirement is traced to
a task with an acceptance criterion. G2/G3 gaps may be deferred **only with explicit
human acknowledgement** (record in state.json `deferredRequirements`).

- If gaps exist and are NOT acknowledged → **stop the pipeline**, return to DESIGN and
  add the missing tasks. Do NOT proceed to BUILD.
- This gate is non-negotiable: building with known P1 coverage gaps is the exact failure
  this phase exists to prevent.

**State write:** Save `.dev-craft/requirements.md`. Record `requirementsExtracted`,
`coverageGaps`, and `deferredRequirements` in state.json. Set
`phases.REQUIREMENTS_EXTRACTION = "completed"` only after the gate passes.

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

### [4.5] CONTRACT — API contract (fullstack only)

**Goal:** For `fullstack` scope, produce ONE source-of-truth contract that the backend implements and the frontend consumes, so the two never silently diverge. Skipped for `be`-only and `fe`-only scope.

**When to run:** Only when `scope == fullstack` (from SCOPE §0.2). For `build` mode, run before BUILD. For `ticket` mode, update only the endpoints the ticket touches.

**Process:**

1. **Write `api-contract.md`** — the single canonical name (no `api-spec.md` variant). Location depends on topology:
    - `mono`: repo root or `docs/api-contract.md` in the one repo.
    - `multi`: in `contractRepo` (the BE repo by default, from SCOPE §0.2 step 0). The other repo references it by absolute path or a symlink; do NOT keep a second copy that can drift. If the sibling repo cannot read it (separate remote, no shared mount), copy it and record `apiContractMirror: "<feRepo>/api-contract.md"` so conformance checks read the same content.
    Structure per endpoint:
    ```markdown
    ## POST /api/auth/login
    Auth: required? (public)
    Request:  { email: string, password: string }
    Response: 200 { token: string, user: User }
             401 { error: "invalid_credentials" }
             429 { error: "rate_limited" }
    Notes: httpOnly cookie set; never return raw password
    ```
    Prefer OpenAPI YAML **content inside** `api-contract.md` when the stack has tooling for it; the canonical filename stays `api-contract.md` (do not rename the file to `openapi.yaml`). Otherwise the markdown table above is the minimum.
2. **Record the contract path** in state.json: `apiContract: "<contractRepo>/api-contract.md"` (multi) or `"api-contract.md"` (mono).
3. **Hand to ui-craft:** ui-craft MUST consume this file (not invent endpoints). For `multi`, ui-craft reads it from `contractRepo` (or the recorded mirror). See Cross-Skill Communication below.

**Exit criterion:** `api-contract.md` exists at the canonical location and is recorded; backend BUILD slices trace to it; ui-craft is pointed at it.

---

### [5] BUILD — TDD + Incremental + Secure-by-Construction

**Goal:** Implement one vertical slice at a time. Every slice is verified for security as it's written — not deferred to a batch scan.

**Branch isolation (mandatory):** Every BUILD run starts on a dedicated feature branch — never commit directly to `main`/`master`/`develop`. The branch keeps in-progress work isolated and reviewable. For `multi` topology, the branch is created in **every repo the scope touches** (see SCOPE §0.2 step 5), and each repo's `state.json` records its own `activeBranch`; the SCOPE record links them via `linkedBranches`. A BE-only or FE-only `multi` unit branches only its own repo.

**Base-branch guard (enforced before every commit, in every repo):** Treat `main`, `master`, `develop` (and each repo's configured default branch) as protected. If `git branch --show-current` reports a base branch at commit time, STOP and create/checkout the feature branch first. Never override this with `--no-verify` or force.

1. **Resolve the branch name(s)** (deterministic, from SCOPE §0.2 step 5):
    - `mono`: one `activeBranch`.
    - `multi`: read `linkedBranches` for the unit — branch names per repo (`be`, `fe`).
2. **Branch naming convention:**
    ```
    <type>/<scope>-<short-description>[-<issue-id>]
    type ∈ { feat, fix, refactor, chore, test, docs }
    scope ∈ { be, fe, fs }
    examples:
      feat/fs-user-auth        (mono: one branch;  multi: paired be+fe branches)
      fix/be-payroll-calc-142
      fix/fe-login-align
    ```
3. **Ensure the branch(es) actually exist before any code** — verify per repo, don't just record intent:
    ```bash
    # mono: single repo
    REPOS=(".")
    # multi fullstack: both repos; multi be/fe: only the touched repo
    # REPOS=("$beRepo" "$feRepo")  # adjust by scope

    for R in "${REPOS[@]}"; do
      BRANCH="$(jq -r --arg r "$R" '.linkedBranches[$r] // .activeBranch // empty' .dev-craft/state.json)"
      if [ -z "$BRANCH" ]; then
        BRANCH="<type>/<scope>-<short-description>"
        jq --arg r "$R" --arg b "$BRANCH" '.linkedBranches[$r] = $b' .dev-craft/state.json > .dev-craft/state.tmp \
          && mv .dev-craft/state.tmp .dev-craft/state.json
      fi
      ( cd "$R" && {
        if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
          git checkout "$BRANCH"
        elif [ "$(git branch --show-current)" = "$BRANCH" ]; then
          :
        else
          git checkout -b "$BRANCH"
        fi
        CURRENT="$(git branch --show-current)"
        case "$CURRENT" in
          main|master|develop) echo "ERROR[$R]: still on base branch — branch creation failed"; exit 1 ;;
          "")                  echo "ERROR[$R]: detached HEAD — branch creation failed"; exit 1 ;;
          "$BRANCH")           echo "OK[$R]: on $BRANCH" ;;
          *)                   echo "ERROR[$R]: on $CURRENT, expected $BRANCH"; exit 1 ;;
        esac
      } )
    done
    ```
    Record `activeBranch` / `linkedBranches` in state.json **only after** each branch is confirmed to exist and we are on it.
4. **Per-slice commits land on the branch(es).** Each slice is an atomic commit in every repo it touches. Branches are only merged/PR'd during SHIP. Re-run the base-branch guard above (per repo) before each commit — never assume the branch is still current.
5. **Resume safety:** On resume, re-run step 3. If a recorded branch no longer exists, fall back to deriving a new name (do NOT silently stay on a base branch). If a different unit was suspended (SCOPE §0.2 step 6), restore `suspendedBranch`(es) first.

**Process per slice:**

```
0a. BRANCH-GUARD — Confirm we are on the feature branch (create/switch if needed); abort if on a base branch
0b. BRANCH — Ensure dedicated feature branch exists (create or resume)
1. RED    — Write failing test
2. GREEN  — Write minimal code to pass
3. SECURE — Verify the slice has no security issues
4. MATCH  — Verify code matches existing project conventions
5. LINT   — Run linter + formatter
6. TYPE   — Run type checker
7. TEST   — Run test suite
8. COMMIT — Atomic commit (on the feature branch; re-run branch-guard first)
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

**State write:** Save `activeBranch` (the current unit's branch), `branches` map, slices, security notes, and convention profile to state.json.

---

### [6] TEST — Full Suite + Diagnose

**Goal:** Run the relevant test suites for the scope. Fix every failure.

**Process:**

1. **Run suites per scope** (run what the scope touches; for `multi`, run in the relevant repo):
    - `be` / `fullstack` backend:
      - `mono`: `cd backend && pytest` (or the project's BE test cmd)
      - `multi`: `cd "$beRepo" && <be test cmd>`
    - `fe` / `fullstack` frontend:
      - `mono`: `cd frontend && npm test` (or `vitest` / the project's FE test cmd)
      - `multi`: `cd "$feRepo" && <fe test cmd>`
    - `be`-only or `fe`-only ticket: run only the touched suite/repo — don't force the other.
    - If the layout differs, detect the per-domain test command from its manifest; never assume a single root-level `npm test`/`pytest`.
2. **Contract conformance (fullstack only):** If `api-contract.md` exists, assert the running app matches it — at minimum: every contract route is registered, request/response shapes are compatible, and status codes the FE handles are returned by the BE. For `multi`, read the contract from `contractRepo`. A route the FE calls that the BE doesn't expose is a test failure.
3. If all pass → Proceed to Phase 7
4. If any fail → **Invoke:** `debugging-and-error-recovery`
    - This skill handles structured root-cause investigation
    - Do NOT embed debugging procedures here — defer to the skill
5. Re-run the relevant suites after every fix

**Exit criterion:** All relevant suites pass; for fullstack, contract conformance holds.

**State write:** Update state with suites run and results.

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
 4. **Run the lint gate** — load `references/lint-rules.md` and execute its ruff
    config + cryptic-name grep. UP007/UP035/UP045 violations and any cryptic-name
    hit are automatic fails; fix before proceeding.
 5. Fix all Critical/Required findings

**Reality-Check Discipline (evidence-based QA):** Approach review as a skeptic, not an advocate.
- **Default stance is "needs work."** First-pass implementations typically need 1–3
  revision cycles; do not declare done on the first review.
- **Spec reality-check:** for each P1/G1 row in `.dev-craft/requirements.md`, confirm the
  built code actually satisfies it — quote the requirement, cite the file/line or test
  that proves it. A requirement marked ✅ without evidence is not verified.
- **Evidence, not assertion:** run the linter, type checker, and full test suite and read
  the output. Do not infer pass/fail.
- **Automatic-fail triggers:** claiming "zero issues", a perfect score without evidence, or
  treating unverified requirements as complete.

**Exit criterion:** All Critical/Required resolved **with evidence**, and every P1/G1
requirement in the traceability matrix verified against the built code.

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
  5. Atomic commit (on the feature branch(es) created in BUILD):
     ```
     type(scope): short description

     - What changed and why
     - Key decisions (reference ADRs)
     - What was intentionally NOT done
     ```
    Before committing, re-run the branch-guard **in every repo the unit touched** (per SCOPE topology): confirm `git branch --show-current` is the feature branch, not a base branch. If on a base branch in any repo, stop and checkout the feature branch first.
  6. Merge or open a pull request from the feature branch(es):
     - **mono:** one branch, one PR.
     - **multi:** open a PR in **each repo the scope touched** (paired `fix/be-*` + `fix/fe-*` branches), linked by the same issue id. Never ship one side without the other for a `fullstack` unit — they are one change split across repos.
     - **PR (recommended):** Push the branch(es) and open PR(s) for review before merging to the base branch. Never merge unreviewed Critical/Required findings.
     - **Direct merge (solo/small):** Only if no review gate is required:
       ```bash
       cd "$REPO" && git checkout <base-branch> && git merge --no-ff <feature-branch>
       ```
     - Record the merged branch name(s) and PR/commit reference in `state.json` (`shippedBranches`, `prUrls` if any).
  7. Define rollback strategy:
    - Feature flag toggling: < 1 minute
    - Code revert: specify commit (per repo for multi)
    - Database: migration revert command

**Exit criterion:** Feature branch(es) merged (or PR(s) opened) with a clean commit and a rollback plan.

---

### [S] STATUS — Where am I / What's next (on demand)

**Goal:** Give the human an always-available navigation aid. After the pipeline "finishes", after ad-hoc fixes, or when the human loses track of the phase flow, this protocol reconstructs the current position from `state.json` + git and shows the forward path — tied back to what the human actually asked for (the requirements matrix).

**When to run it:**
- The human asks "where are we?", "what now?", "what's next?", "what phase?", or "remind me".
- The human returns after a gap and asks to continue.
- The human asks the agent to fix/change something *outside* the normal phase loop (a bug report, a tweak, a "can you also…").
- The agent finishes ANY request (phase, fix, or answer) and should close by stating the next valid step.

**Process:**

1. **Read position from state:**
    ```bash
    python3 - <<'PY'
    import json
    d = json.load(open('.dev-craft/state.json'))
    ph = d.get('phases', {})
    print("currentPhase:", d.get('currentPhase'))
    for name in ["LOAD","REQUIRE","ARCH_SCAN","ALIGN","DESIGN","BUILD_ORDER",
                 "SOURCE","BUILD","TEST","REVIEW","HARDEN","SHIP"]:
        st = ph.get(name, "—")
        mark = {"completed":"✅","in_progress":"🔶","pending":"⬜","failed":"❌"}.get(st, "·")
        print(f"  {mark} {name}")
    PY
    ```

2. **Detect drift (is state out of sync with reality?):**
    ```bash
    # For multi topology, loop over each repo in state.repos; for mono, just cwd
    for R in "${REPOS[@]}"; do
      ( cd "$R" && {
        echo "[$R] status:"; git status --porcelain | head
        echo "[$R] current branch: $(git branch --show-current)"
      } )
    done
    echo "activeBranch:   $(jq -r .activeBranch .dev-craft/state.json)"
    echo "linkedBranches: $(jq -r '.linkedBranches // {}' .dev-craft/state.json)"
    echo "branches:       $(jq -r '.branches // {}' .dev-craft/state.json)"
    ```
    - Uncommitted changes in any repo → warn: *"Uncommitted work in `<R>`. The phase loop expects atomic per-slice commits. Commit or stash before moving on."*
    - On a different branch than the recorded branch for that repo → warn: *"You're on `<x>` in `<R>`, not the feature branch `<expected>`. Switch back before committing."*
    - A phase marked `completed` but `git log` shows no commit since it started → flag: *"`<phase>` is marked done but no commit landed — verification may be unrecorded."*

3. **Map to requirements coverage (stay close to what the human expects):**
    - If `.dev-craft/requirements.md` exists, read it and report:
      - Total requirements, and how many P1/G1 are traced ✅ vs ⚠️ GAP vs ❌ GAP.
      - Explicitly name any open GAPs — these are the human-facing "not done yet" list.
    - If it does not exist but the human expects feature completeness, say so:
      *"No coverage gate has been run yet. We cannot claim the spec is covered. Run REQUIREMENTS-EXTRACTION before SHIP."*

4. **Print the forward path** as a short, ordered checklist ending at the next actionable step:
    ```
    ROADMAP (from current position):
      ✅ LOAD  ✅ REQUIRE  ✅ ALIGN  ✅ DESIGN  🔶 BUILD  ⬜ TEST  ⬜ REVIEW  ⬜ HARDEN  ⬜ SHIP
    NEXT: TEST — run full suite, fix failures via debugging-and-error-recovery
    THEN: REVIEW → HARDEN → SHIP
    OPEN GAPS: REQ-011 (UTC+7), REQ-027 (Leave module)  ← must close before SHIP
    DRIFT: 3 uncommitted files — commit before TEST
    ```

5. **Resume-after-ad-hoc-fix routing:** When the human asks for a fix/tweak *outside* the loop, do NOT silently edit and claim done. Instead:
    - Identify which phase the fix belongs to (bug → re-run TEST + the slice's SECURE; style/convention → re-run MATCH/LINT; security → HARDEN; spec gap → back to REQUIREMENTS-EXTRACTION).
    - Run that phase's verification on the changed slice, then update state + requirements.md if coverage changed.
    - Close by printing the roadmap (step 4) so the human sees the fix did not skip gates.

**Output contract:** STATUS must always answer three questions for the human:
1. *Where am I?* (phase + completed/pending map)
2. *Am I drifting?* (uncommitted / wrong branch / unverified-completed)
3. *What does the human still expect?* (open requirement gaps + next phase)

**Exit criterion:** Human has a current-position readout, a next-step, and a clear list of what remains vs. what was asked.

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

Driven by the SCOPE gate (§0.2). The contract artifact is ALWAYS named **`api-contract.md`** (no `api-spec.md` variant) and lives at repo root or `docs/`. This is the single source of truth both skills read.

**dev-craft (`scope: fullstack`) needs UI:**
1. Run CONTRACT (§4.5) → write `api-contract.md` (in `contractRepo` for `multi`).
2. Record in state.json: `crossSkill.uiSliceNeeded: ["login-form"]`, `apiContract: "<path>"` (the canonical location; for `multi` that's in the BE repo / `contractRepo`).
3. Hand off to ui-craft: ui-craft MUST consume `api-contract.md` (read from `contractRepo` or the recorded mirror) and may not invent endpoints.
4. On ui-craft return, run HARDEN Check 7 (contract conformance) before SHIP.

**ui-craft (`scope: fullstack`) needs backend:**
1. If `api-contract.md` already exists (dev-craft produced it), consume it directly — for `multi`, read it from `contractRepo` (or the recorded mirror path). Do not regenerate.
2. If not, generate `api-contract.md` from the UI's data needs, record `crossSkill.backendSliceNeeded: ["auth-api"]` and its path, hand to dev-craft to implement.
3. dev-craft MUST implement only what the contract declares; any new endpoint updates the contract first.

**dev-craft needs mobile (agent-orchestration):**
1. Produce `api-contract.md`; record `crossSkill.mobileSliceNeeded: ["api-endpoints"]`; hand to agent-orchestration.

**Verification before switching skills:** confirm `api-contract.md` exists at its recorded path and is readable from the consuming repo (for `multi`, the mirror is in sync). Never switch with an implied/unwritten contract.

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
| "Commit straight to main" | Always work on a feature branch, merge via review |
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
- Commits made directly to main/master/develop (no feature branch)
- `activeBranch` recorded in state.json but agent is actually on a base branch (branch was never created/checked out)
- Commit messages: "WIP", "fix", "update"
- Vague prompt accepted without clarification
- Skipping REQUIRE when spec files exist
- Building modules in wrong dependency order
- No domain model for multi-module project
- No worktree isolation for parallel agents
- Starting BUILD without build-order.md for complex projects
- **Starting BUILD without `requirements.md` coverage gate passing** (P1/G1 gaps unresolved)
- P1/G1 requirement with no traced task silently deferred without human acknowledgement
- Ad-hoc fix made outside the phase loop without re-running the owning phase's verification (TEST/SECURE/MATCH/HARDEN)
- Plan tasks whose acceptance criteria cannot be mapped back to a REQ-ID

## Verification

- [ ] ARCH-SCAN was run (or deferred with approval)
- [ ] .dev-craft/state.json exists with status: complete
- [ ] All slices implemented and committed on a dedicated feature branch
- [ ] `activeBranch` recorded in state.json and verified to exist before BUILD commits
- [ ] Feature branch merged or PR opened during SHIP (not committed to base)
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
- [ ] Domain model exists in .dev-craft/domain.md (for multi-module projects)
- [ ] Build order documented in .dev-craft/build-order.md (for complex projects)
- [ ] Module dependencies respected during build
- [ ] **`requirements.md` exists and the COVERAGE GATE passed** (every P1/G1 REQ-ID traced to a task + acceptance criterion)
- [ ] Any ad-hoc fix was routed through STATUS and re-ran the owning phase's verification
- [ ] Agent closed its last turn by stating current phase + next valid step (STATUS)
- [ ] No uncommitted drift warning left unaddressed before claiming a phase complete

## See Also

- `plugins/security-audit/SKILL.md` — Deep security scan pipeline
- `references/modern-patterns.md` — Per-language guidance
- `references/lint-rules.md` — Forbidden patterns + ruff gate (Optional[], single-char names)
- `references/phase-templates.md` — Templates for documents
- `product-thinking` — Refine vague ideas into structured specs
- `project-discovery` — Extract domain model from existing documents
- `agent-orchestration` — Multi-agent parallel builds with git worktree
- `quality-gates` — Layered validation pipeline
