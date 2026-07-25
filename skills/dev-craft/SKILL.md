---
name: dev-craft
description: Use when running a full-stack engineering pipeline with persistent `.dev-craft`
  state for long-lived work and phased delivery.
metadata:
  origin: agent-master-skills
owner: noname.spyware@gmail.com
allowedTools:
- python
- git
- shell

---

# dev-craft

## Overview

Turns a prompt into production-quality code.
Every phase has a clear goal, exit criteria, and a human checkpoint.
Persists state to `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` so work survives across sessions.

**Philosophy:** Transparent, human-orchestrated, composable.
Skip any phase. Edit any phase. The pipeline serves you.

## When to Use

- Given a prompt, PLAN.md, or feature request
- Starting a new project or feature
- Task spans multiple files or modules
- Resuming work from a previous session
- Need more than a single-file change

**When NOT to use:** Single-line fixes, typo corrections, trivial config changes — skip the full pipeline for these. Exception: the **Minimum Bar** still applies (no cryptic names, no legacy idioms) — see `skills${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/SHARED.md` → *Minimum Bar*. The deterministic lint gate in `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/lint-rules.md` is not skipped just because the pipeline is.

## The Iron Law

```
NO CODE WITHOUT DESIGN APPROVAL
```

Implementation without approved spec = wasted hours of rework.

**Standing navigation rule:** After finishing ANY request — a phase, a fix, or an answer — the agent MUST close by stating the current phase and the next valid step (run the `[S] STATUS` protocol). When the human asks for a fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/tweak outside the phase loop, route it through STATUS's resume-after-ad-hoc-fix routing; never silently edit and claim done. This keeps the human oriented and ties every action back to what they asked for.

**Concrete output format** (every response that is not a question to the user MUST end with this):

```
STATUS: Phase <name> [✅${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/⬜]
NEXT: <the single next action the agent will take or expects the user to take>
STATE: sessionFile=<file>, lastBuildFix=<count>
```

Examples:
```
STATUS: Phase SHIP [✅]  NEXT: Awaiting new task.  STATE: session-20260721-001, 1 fix
```
```
STATUS: Phase BUILD (slice 3${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/5) [🔶]  NEXT: Write failing test for payslip export.  STATE: session-20260721-002, 0 fixes
```

If the user's last message was not a request but a question${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/comment, and there is no pending action, end with:
```
STATUS: Awaiting instructions.  NEXT: None.  STATE: session-20260721-001
```

This format is the minimum — add context as needed, but never omit it entirely.

### State Integrity Mandate (non-negotiable)

Every task run — whether `build` or `ticket` — MUST persist its progress to `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`:

1. **Load state before any phase.** If `state.json` exists, read it. Detect `currentPhase`, `lastSession`, and resume logic.
2. **Create a session file before any BUILD work.** Every task must have a corresponding `sessions${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/session-YYYYMMDD-N.md` written BEFORE the first code change, not after. No session file = no BUILD.
3. **Update state.json after every phase.** After each phase completes, write the updated `currentPhase`, `testResults`, `buildFixes`, and `lastSession` to `state.json`. Do not batch updates.
4. **Verify state after ad-hoc fixes.** If the human requests a fix outside the phase loop, update `state.json`'s `buildFixes` and `testResults` before closing.

A simple mental model: *if a context crash happens right now, the next session should resume from the correct phase.* If you can't confidently say that, the state is stale — update it.

---

## Input Quality Handling

Before starting, assess the input:

| Input Type | Action |
|------------|--------|
| Short${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/vague ("Build HRM", "Make me a CRM") | → Do NOT proceed automatically. Ask user: "Your prompt is short — I need more context. Should I load `product-thinking` to refine this into a spec first, or can you provide more details?" |
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

`.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` directory created on first run:

```
.dev-craft/
├── state.json       # currentPhase, completed, stack, slices
├── plan.md          # Evolving plan from Align → Design
├── domain.md        # Domain model (from REQUIRE or project-discovery)
├── build-order.md   # Module dependency sequencing
├── estimation.md    # Cost${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/schedule validation
├── context.md       # Domain glossary (shared language)
├── decisions/       # ADRs — key decisions captured
│   └── 001-*.md
├── sessions/        # Handoff docs for context rotation
│   └── session-YYYYMMDD-N.md
└── config.json      # Project config (linter, formatter, test cmds)
```

### Session Creation Checklist (mandatory)

Every new task MUST go through this checklist before any code is written:

1. **Load or initialize `state.json`.**
2. **Confirm task intent** — if all phases were completed, ask "New task on same project?" before proceeding.
3. **Create session file** at `sessions${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/session-YYYYMMDD-N.md` with at minimum:
   - Date, task summary, scope classification
   - A checklist of the phases you expect to run
4. **Record `sessionFile`** in `state.json`.
5. **After every phase**, append results to the session file and update `state.json`.

> **Rationale:** Without this checklist, agents skip session creation, batch state updates, and lose traceability across context resets. A session file is not optional paperwork — it is the agent's sole recovery point if context crashes mid-pipeline.

### Resume Logic

| Scenario | Behavior |
|---|---|
| No `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` | Phase 0.5 (REQUIRE) — check for spec files |
| DOMAIN.md exists but not loaded | Load into REQUIRE |
| `state.json` exists but `sessionFile` is missing or stale | Treat as suspect — flag to user: *"State file found but no recent session. Verify you want to resume or start fresh."* |
| `state.json` exists and `sessionFile` is current | Load state, skip completed phases |
| All phases complete | Ask "New task on same project?" and create new session |
| Context near limit | Generate handoff doc, resume next session |

## Stack Detection

Run during Phase 2 (ALIGN).
Scan dependency files for exact versions.

```
Read dependency files (package.json, requirements.txt, go.mod, Cargo.toml, etc.):
│
├── Framework${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/library found?
│   ├── Version explicit? → use that version for docs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/code generation
│   ├── Version range (`^18.0.0`)? → resolve to installed or latest
│   └── No version? → ask user or default to latest
│
├── Linter${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/formatter detected?
│   ├── Yes → every slice MUST pass lint + format
│   └── No → surface to human:
│       "No linter${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/formatter — recommend installing one. Proceed without?"
│
└── Type checker detected?
    └── Yes → every slice MUST pass type check
```

## Pipeline Phases

```
[0] LOAD → [0.2] SCOPE (be${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fullstack × build${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ticket) → [0.5] REQUIRE → [1] ARCH-SCAN
    → [2] ALIGN → [3] DESIGN → [3.5] BUILD-ORDER → [3.7] REQUIREMENTS-EXTRACTION
    → [4] SOURCE → [4.5] CONTRACT (fullstack only) → [5] BUILD → [6] TEST
    → [7] REVIEW → [8] HARDEN → [9] SHIP
    → [S] STATUS (anytime: navigation + drift + requirements-coverage aid)
```

> **Ticket mode short-circuits:** when `mode == ticket`, skip REQUIRE${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/REQUIREMENTS-EXTRACTION unless the change alters spec coverage — go LOAD → SCOPE → scoped BUILD → TEST → REVIEW → SHIP. SCOPE decides.

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

> **Why REQUIREMENTS-EXTRACTION exists:** Makes spec coverage a first-class, machine-checkable artifact (see §3.7 for the full rationale).

### Non-Negotiable Gates (applied across ALL phases)

These gates fire at specific points and block progress if not satisfied. They exist because
the pipeline is long and agents routinely skip them without a hard stop:

| Gate | Fires At | Fails If | Action on Failure |
|------|----------|----------|-------------------|
| **State Integrity** | Before every phase transition after SCOPE | `state.json` is missing, stale, or `sessionFile` is empty${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/null | Create${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/update state and session file before proceeding |
| **Skill Alignment** | SCOPE §0.2 step 3a | Classification is `fe` (frontend) but the running skill is dev-craft without a recorded `skillOverride` | Surface to user, get explicit approval or switch to ui-craft |
| **Session Exists** | Before BUILD phase | No `sessions${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/session-YYYYMMDD-N.md` exists for this run | Create session file first (see checklist above) |
| **Standing Navigation** | After ANY request finishes | Agent finishes a response without stating current phase + next step | This is a text-output rule — output MUST include "Current phase: X. Next: Y" or equivalent |

---

### [0.2] SCOPE — Classify the work (BE / FE / Fullstack, Build / Ticket)

**Goal:** One gate that decides the entire downstream shape of the run. Every later phase (REQUIRE, DESIGN, BUILD, TEST, HARDEN, SHIP, cross-skill handoff) reads the scope decision made here. This is what makes dev-craft correct for a backend-only bug ticket, a frontend-only tweak, a fullstack feature, and a greenfield build — without separate pipelines.

**Why this exists:** The skill was originally written as "dev-craft = backend, ui-craft = frontend." That binary breaks two ways: (1) a large existing repo contains BE *and* FE, so building them needs a shared contract; (2) an incoming ticket is often BE-only or FE-only on a codebase mid-build, and forcing the full greenfield pipeline is wasted overhead. SCOPE classifies intent up front so the right phases run.

**Process:**

0. **Detect repo topology** (how the code is laid out — this decides where git${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/contract operations run):
    - `mono`  — BE and FE in ONE repo (e.g. `backend${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` + `frontend${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` dirs, or a single fullstack app).
    - `multi` — separate repos: a BE repo and a FE repo (two checkouts, two remotes).
    Heuristic:
    ```bash
    # mono: backend + frontend signals in the SAME checkout
    has_be=$( test -d backend || grep -q '"fastapi"\|"django"\|"flask"' package.json 2>${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/null && echo y )
    has_fe=$( test -d frontend || grep -q '"react"\|"vue"\|"next"' package.json 2>${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/null && echo y )
    # multi: user passed two repo paths, or only one side exists here and the other is elsewhere
    ```
    If the request names two repo paths (e.g. `~${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/be-api` and `~${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/web-app`), or only BE *or* only FE is present in the current checkout, treat as `multi` and ask the user for the sibling repo path. Record `topology` (`mono`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`multi`).
    For `multi`, record `repos: { be: "<path>", fe: "<path>" }` and a `contractRepo` — the repo that owns `api-contract.md` (default: the BE repo). Every git${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/contract command below is **scoped to the relevant repo(s)** via `cd "<repo>"`.

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
    Heuristic: if the request names an existing module${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/component, or says "fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/hotfix", it is a `ticket`. If it describes something new, it is `build`. When unsure, prefer `ticket` for existing repos (less overhead) but confirm.

3a. **Skill Alignment Check** (do NOT skip after classification):
    - If you loaded this skill (`dev-craft`) because the user asked you to, but the SCOPE classification resolves to `fe` (frontend-only), then dev-craft is the wrong skill for the work — ui-craft owns frontend.
    - **Action:** Surface the mismatch to the user immediately after classification:
      ```
      SCOPE classified this as [fe] + [ticket|build].
      The optimal skill for frontend work is ui-craft, not dev-craft.
      I can:
        1. Switch to ui-craft (recommended)
        2. Continue with dev-craft (you asked for it, but I'll note the override)
      ```
    - If the user chooses to continue with dev-craft despite the mismatch, record in state.json:
      ```json
      "skillOverride": { "requested": "dev-craft", "recommended": "ui-craft", "accepted": true }
      ```
    - This serves as proof that the mismatch was surfaced and the human made an informed choice. Without this record, the pipeline must NOT proceed past SCOPE for an FE-classified task — stop and ask.

4. **Resolve the pipeline shape** from the two axes + topology:

    | TOPOLOGY | DOMAIN  | MODE     | Pipeline                                                                 |
    |----------|---------|----------|--------------------------------------------------------------------------|
    | `mono`   | `be`    | `build`  | full dev-craft (REQUIRE…SHIP), no CONTRACT needed                        |
    | `mono`   | `be`    | `ticket` | LOAD → SCOPE → scoped BUILD slice → TEST → REVIEW → SHIP; skip REQUIREMENTS-EXTRACTION${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/BUILD-ORDER unless spec coverage changes |
    | `mono`   | `fe`    | `build`  | ui-craft full (owns DESIGN${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/tokens); dev-craft not needed                |
    | `mono`   | `fe`    | `ticket` | ui-craft, jump to BUILD consuming existing design system; skip ALIGN${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/DESIGN |
    | `mono`   | `fullstack` | `build` | dev-craft with **CONTRACT** (§4.5) before BUILD; ui-craft consumes `api-contract.md` |
    | `mono`   | `fullstack` | `ticket` | CONTRACT (update touched endpoints) → scoped BE + FE slices → TEST (both) → REVIEW (contract conformance) → SHIP |
    | `multi`  | `be`    | any      | dev-craft in BE repo only; branch in BE repo; FE repo untouched          |
    | `multi`  | `fe`    | any      | ui-craft in FE repo only; branch in FE repo; BE repo untouched          |
    | `multi`  | `fullstack` | any   | BE in BE repo, FE in FE repo, **paired branches** in BOTH repos, one shared `api-contract.md` (in `contractRepo`); cross-repo conformance in HARDEN${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/REVIEW |

5. **State Initialization Gate (run before any branch${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state work):**
    - Before writing any code, creating any branch, or entering any build phase:
      1. If `state.json` does NOT exist → create it with `currentPhase: "SCOPE"` and the classification from steps 1-4.
      2. If `state.json` EXISTS and all phases show `"completed"` → this is a new task on a shipped codebase. Do NOT silently skip session creation. Ask: *"Previous run completed. New task on same project?"* and only proceed after confirmation.
      3. If `state.json` EXISTS with `in_progress` → resume from that phase (do NOT restart).
    - **Session file creation:** After state is initialized and the task is confirmed, immediately create `sessions${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/session-YYYYMMDD-N.md` with:
      ```markdown
      # Session YYYY-MM-DD-N
      Type: [build|ticket]
      Task: <one-line summary>
      Scope: [be|fe|fullstack]
      ```
      This file MUST exist before any BUILD-phase work. It is the agent's checkpoint: if context resets, the session file proves progress.
    - Record the session filename in `state.json` under `sessionFile`.

6. **Branch per unit of work (repo-scoped, never one global branch):**
    - Each `build`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`ticket` gets its **own** branch derived from scope + mode:
      ```
      <type>${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/<scope>-<short-description>[-<issue-id>]
      type ∈ { feat, fix, refactor, chore, test, docs }
      scope ∈ { be, fe, fs }
      examples:
        feat${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fs-user-auth      (mono: one branch;  multi: paired be+fe branches)
        fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/be-payroll-calc-142
        fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fe-login-align
      ```
    - **mono:** create the single branch in the one repo.
    - **multi:** create the branch in **every repo the scope touches**:
      ```bash
      # fullstack ticket across two repos → paired branches
      cd "$beRepo" && git checkout -b "fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/be-payroll-142"
      cd "$feRepo" && git checkout -b "fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fe-payroll-142"
      ```
      Each repo's `state.json` records its own `activeBranch`; the SCOPE record links them via `linkedBranches: { be: "fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/be-payroll-142", fe: "fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fe-payroll-142" }`. A BE-only or FE-only `multi` ticket branches only its own repo.
    - This replaces the single `buildBranch` assumption: a BE hotfix can run on `fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/be-payroll-calc` while a feature branch `feat${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fs-user-auth` is mid-BUILD. Keep a `branches` map of `{unitId: {be?, fe?}}` so units can be resumed and switched.
    - The branch-isolation + base-branch guard from BUILD (§5) applies to **every** per-unit branch, in **every** repo it was created in.

7. **Interrupt / resume between units:** If a `ticket` arrives while a `build` is `in_progress`, do NOT abandon the build:
    - Stash the current phase pointer: `state.suspendedPhase = currentPhase`, `state.suspendedBranch = activeBranch` (and `suspendedBranches` for multi).
    - Do the ticket on its own branch(es) per step 6 (Branch per unit of work).
    - On ticket completion, restore: `git checkout "$suspendedBranch"` in each relevant repo, set `currentPhase = suspendedPhase`. The STATUS protocol (§S) surfaces this automatically.

**State write:** `topology` (`mono`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`multi`), `scope` (`be`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`fullstack`), `mode` (`build`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`ticket`), `repos` (multi only), `contractRepo` (multi only), `activeBranch`, `branches` (map of unitId → {be?, fe?}), `linkedBranches` (multi), `sessionFile` (string, set by State Initialization Gate step 5), `skillOverride` (object, set by Skill Alignment Check step 3a if override occurred), and (if suspended) `suspendedPhase`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`suspendedBranch`(es).

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
   Generate `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/domain.md` from the spec.

3. **If DOMAIN.md found:**
   Load directly into `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/domain.md`.

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
   - Clock in${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/out (G1)
   - Calculate salary (G1)
   ```
   Save to `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/domain.md`.

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
   
   Confirm this model? (Y${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/detail)
   ```
   If user says "n" or "detail", loop back to refine.

**Exit criterion:** Domain model confirmed by user (or no specs available).

**State write:** Save domain model to `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/domain.md`. Update state.json.

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
   - Check for shadcn${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ui components (components${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/)
   - Check for CSS custom properties (:root { --color-* })
   - Flag inconsistencies

3. Surface report:
   ```
   SMELL REPORT:
   1. [Duplicated Code] src${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/format.ts:45-52
      → Extract shared function
   2. [Primitive Obsession] src${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/user.ts
      → Create discriminated union
   ```

4. Ask human to prioritize fixes

**Exit criterion:** Human approves remediation or defers.

**State write:** Save smells to state.json for REVIEW.

---

### [2] ALIGN — Grill + Detect + Glossary

**Goal:** Surface assumptions, sharpen requirements. If REQUIRE phase produced a domain model, use it to ask targeted questions. If not, do basic discovery.

**Process:**

1. **Load domain model** if `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/domain.md` exists:
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
   ├── File organization: [features/ modules/ pages${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/]
   ├── Naming: files=[kebab${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/snake] functions=[camel${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/snake] types=[Pascal${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/I]
   ├── Imports: [absolute${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/relative] exports=[named${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/default]
   ├── Error handling: [try-catch / Result types / error boundaries]
   ├── Structure: [single file per feature / split across layers]
   └── Testing: [colocated / __tests__${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/] style=[describe-it${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/test()]
   ```
   Read 3-5 existing files to detect patterns. Save to `state.json` for BUILD phase.
   If the project is greenfield (no existing code), skip detection and use sensible defaults based on the detected stack.

9. **Image analysis** (if screenshot provided):
    ```bash
    python ~${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/analyze.py --image <path> --format json --output .dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/image-analysis.json
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
   - Code style (see references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/modern-patterns.md)
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

**Cross-skill invocations in this phase:**
- If this change adds${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/reshapes an API surface → invoke `api-design` to decide contract shape (style, versioning, auth, rate-limiting). The resulting contract doc feeds into this phase's spec.
- If this change requires a structural pattern decision → invoke `architecture-patterns` for trade-off analysis. The resulting memo feeds into this phase's spec and ADRs.
- Write resulting ADRs per `documentation-engineering`'s format (MADR in `docs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` with index table).

**Exit criterion:** Human reviews and approves.

**State write:** Save plan.md. Save ADRs to decisions${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/.

---

### Estimation Validation (after DESIGN, before SOURCE)

**Goal:** Catch cost${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/schedule discrepancies between plan and expectations.

Use the template in `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/phase-templates.md` (Estimation Template section). Compare module estimates against any stated budget${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/schedule from domain.md and flag significant gaps.

**Exit:** User reviewed and acknowledged the estimate.

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
   
   Phase 5 (Extended — G2${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G3):
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
   Slice 2: List${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/search employees (query + API + table)
   Slice 3: Edit employee details (update + API + form)
   Slice 4: Document upload (file handling + API + upload UI)
   Slice 5: Delete / deactivate (soft delete + confirm dialog)
   ```

4. **Save build-order.md**

 **Exit criterion:** Build order is documented and user-approved for complex projects.

**State write:** Save `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/build-order.md`.

---

### [3.7] REQUIREMENTS-EXTRACTION — Spec → Task Traceability (COVERAGE GATE)

**Goal:** Guarantee every explicitly stated requirement from the source spec is traced
to a concrete plan task with an acceptance criterion. Catch coverage gaps *before* any
code is written. This is the phase that prevents "the pipeline ran perfectly but we
missed 6 P1 requirements."

**Why this phase exists:** ALIGN captures decisions; DESIGN writes a plan. Neither
mechanically proves the plan covers the spec. A 343-line spec with 12 `[REQUIRED P1]`
markers will lose requirements in summarization. This phase is a line-by-line audit.

**Input:** The source spec (from REQUIRE → `domain.md`, or the original `docs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/*.md` /
PRODUCT.md / DOMAIN.md). If no source spec exists, skip this phase.

**Process:**

1. **Extract every requirement** from the source spec. Be exhaustive and literal:
   - For each paragraph${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/table row that expresses a capability, constraint, or
     non-functional rule, write one requirement row.
   - Preserve the spec's own priority markers verbatim
     (`[REQUIRED P1]`, `🔴 [REQUIRED P1]`, `⚪ [FUTURE PHASE]`, `G1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G3`).
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

4. **Build the traceability matrix** and save to `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/requirements.md`:
   ```markdown
   # Requirements Traceability Matrix — <project>

    Source spec: <path> (<N> lines)
    Extracted: <M> requirements (P1: x, G1: y, G2: z, Future: w)

   | REQ-ID | Priority | Requirement (verbatim clause) | Traced Task(s) | Acceptance Ref | Status |
   |--------|----------|-------------------------------|----------------|----------------|--------|
   | REQ-001 | P1 | `employee_code` auto via PG SEQUENCE | B1, B2 | B1-AC1 | ✅ |
   | REQ-002 | P1 | lockout 5 fails${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/15min + audit_log | A7 | A7-AC2 | ✅ |
   | REQ-011 | P1 | Cross-day shifts UTC+7 display | D1, D2 | D1-AC3 | ⚠️ GAP |
   | REQ-027 | G1 | Leave: full${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/hourly + carry-forward | — | — | ❌ GAP |

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
a task with an acceptance criterion. G2${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G3 gaps may be deferred **only with explicit
human acknowledgement** (record in state.json `deferredRequirements`).

- If gaps exist and are NOT acknowledged → **stop the pipeline**, return to DESIGN and
  add the missing tasks. Do NOT proceed to BUILD.
- This gate is non-negotiable: building with known P1 coverage gaps is the exact failure
  this phase exists to prevent.

**State write:** Save `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/requirements.md`. Record `requirementsExtracted`,
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
   # Source: http${PROJECT_ROOT}/
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
| 2 | Official blog${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/changelog |
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
    - `mono`: repo root or `docs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/api-contract.md` in the one repo.
    - `multi`: in `contractRepo` (the BE repo by default, from SCOPE §0.2 step 0). The other repo references it by absolute path or a symlink; do NOT keep a second copy that can drift. If the sibling repo cannot read it (separate remote, no shared mount), copy it and record `apiContractMirror: "<feRepo>${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/api-contract.md"` so conformance checks read the same content.
    Structure per endpoint:
    ```markdown
    ## POST ${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/login
    Auth: required? (public)
    Request:  { email: string, password: string }
    Response: 200 { token: string, user: User }
             401 { error: "invalid_credentials" }
             429 { error: "rate_limited" }
    Notes: httpOnly cookie set; never return raw password
    ```
    Prefer OpenAPI YAML **content inside** `api-contract.md` when the stack has tooling for it; the canonical filename stays `api-contract.md` (do not rename the file to `openapi.yaml`). Otherwise the markdown table above is the minimum.
2. **Record the contract path** in state.json: `apiContract: "<contractRepo>${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/api-contract.md"` (multi) or `"api-contract.md"` (mono).
3. **Hand to ui-craft:** ui-craft MUST consume this file (not invent endpoints). For `multi`, ui-craft reads it from `contractRepo` (or the recorded mirror). See Cross-Skill Communication below.

**Exit criterion:** `api-contract.md` exists at the canonical location and is recorded; backend BUILD slices trace to it; ui-craft is pointed at it.

---

### [5] BUILD — TDD + Incremental + Secure-by-Construction

**Goal:** Implement one vertical slice at a time. Every slice is verified for security as it's written — not deferred to a batch scan.

**Branch isolation (mandatory):** Every BUILD run starts on a dedicated feature branch — never commit directly to `main`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`develop`. The branch keeps in-progress work isolated and reviewable. For `multi` topology, the branch is created in **every repo the scope touches** (see SCOPE §0.2 step 6 "Branch per unit of work"), and each repo's `state.json` records its own `activeBranch`; the SCOPE record links them via `linkedBranches`. A BE-only or FE-only `multi` unit branches only its own repo.

**Base-branch guard (enforced before every commit, in every repo):** Treat `main`, `master`, `develop` (and each repo's configured default branch) as protected. If `git branch --show-current` reports a base branch at commit time, STOP and create${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/checkout the feature branch first. Never override this with `--no-verify` or force.

1. **Resolve the branch name(s)** (deterministic, from SCOPE §0.2 step 6 "Branch per unit of work"):
    - `mono`: one `activeBranch`.
    - `multi`: read `linkedBranches` for the unit — branch names per repo (`be`, `fe`).
2. **Branch naming convention:**
    ```
    <type>${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/<scope>-<short-description>[-<issue-id>]
    type ∈ { feat, fix, refactor, chore, test, docs }
    scope ∈ { be, fe, fs }
    examples:
      feat${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fs-user-auth        (mono: one branch;  multi: paired be+fe branches)
      fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/be-payroll-calc-142
      fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fe-login-align
    ```
3. **Ensure the branch(es) actually exist before any code** — verify per repo, don't just record intent. Run the branch verification script from `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/build-protocol.md` (Branch Verification Script section) per repo. Record `activeBranch` / `linkedBranches` in state.json **only after** each branch is confirmed to exist and we are on it.
4. **Per-slice commits land on the branch(es).** Each slice is an atomic commit in every repo it touches. Branches are only merged${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/PR'd during SHIP. Re-run the base-branch guard above (per repo) before each commit — never assume the branch is still current.
5. **Resume safety:** On resume, re-run step 3. If a recorded branch no longer exists, fall back to deriving a new name (do NOT silently stay on a base branch). If a different unit was suspended (SCOPE §0.2 step 7 "Interrupt / resume between units"), restore `suspendedBranch`(es) first.

**Process per slice:**

```
0a. BRANCH-GUARD — Confirm we are on the feature branch (create${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/switch if needed); abort if on a base branch
0b. BRANCH — Ensure dedicated feature branch exists (create or resume)
1. RED    — Write failing test
2. GREEN  — Write minimal code to pass
3. SECURE — Verify the slice has no security issues
4. MATCH  — Verify code matches existing project conventions
5. LINT   — Run linter + formatter
6. TYPE   — Run type checker
7. TEST   — Run test suite
8. COMMIT — Atomic commit (re-run per-repo branch-guard from BUILD intro first)
```

**Per-slice deep detail (SECURE tree, MATCH tree, Rules, Git Worktree Mode):**
Load `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/build-protocol.md` when executing a slice — it holds the
per-category security checks, the convention-detection guide, the MATCH${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/SECURE
output formats, and the git worktree isolation workflow. The loop below is the
skeleton; the reference is the step-by-step.

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
    - `be`-only or `fe`-only ticket: run only the touched suite${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/repo — don't force the other.
    - If the layout differs, detect the per-domain test command from its manifest; never assume a single root-level `npm test`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`pytest`.

**Cross-skill invocation in this phase:**
- Before writing tests, invoke `testing-strategies` to decide test type and stated failure mode per test — do not default to unit tests without checking its decision tree.

2. **Contract conformance (fullstack only):** If `api-contract.md` exists, assert the running app matches it — at minimum: every contract route is registered, request${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/response shapes are compatible, and status codes the FE handles are returned by the BE. For `multi`, read the contract from `contractRepo`. A route the FE calls that the BE doesn't expose is a test failure.

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
 3. Categorize findings (Critical${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Optional)
 4. **Run the lint gate** — load `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/lint-rules.md` and execute its ruff
    config + cryptic-name grep. UP007${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/UP045 violations and any cryptic-name
    hit are automatic fails; fix before proceeding.
 5. Fix all Critical${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Required findings

**Reality-Check Discipline (evidence-based QA):** Approach review as a skeptic, not an advocate.
- **Default stance is "needs work."** First-pass implementations typically need 1–3
  revision cycles; do not declare done on the first review.
- **Spec reality-check:** for each P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1 row in `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/requirements.md`, confirm the
  built code actually satisfies it — quote the requirement, cite the file${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/line or test
  that proves it. A requirement marked ✅ without evidence is not verified.
- **Evidence, not assertion:** run the linter, type checker, and full test suite and read
  the output. Do not infer pass${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fail.
- **Automatic-fail triggers:** claiming "zero issues", a perfect score without evidence, or
  treating unverified requirements as complete.

**Exit criterion:** All Critical${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Required resolved **with evidence**, and every P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1
requirement in the traceability matrix verified against the built code.

**State write:** Save review findings.

---

### [8] HARDEN — Cross-Cutting Security Verification

**Goal:** Verify security across all slices, not within individual slices. Catch cross-cutting issues that per-slice SECURE checks miss.

The agent now has the full codebase in context. It reads across all slices to find issues no single slice could surface.

**Process:** Load the deep reference `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/harden-checks.md` for the 8 concrete checks (secrets, auth${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/authz, injection surface, dependency CVE review, config${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/infra, cross-slice audit, BE↔FE contract conformance, risk register). Each check is a read-the-actual-code pass; do not summarize from memory.

**Cross-skill invocation in this phase:**
- Also invoke `observability-engineering` — security hardening and observability are separate concerns; a hardened system that fails silently in production is still a gap.

**Exit criterion:** All Critical${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/High findings resolved. Risk register documents any accepted risks with explicit reasoning.

**State write:** Update state. Save risk register to `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/risk-register.md`.

---

### [9] SHIP — Docs + Commit + Finalize

**Goal:** Deliver with full traceability.

**Process:**

1. Update ADRs for any BUILD${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/HARDEN decisions
2. Update CONTEXT.md with new terms
3. Final verification:
   - Lint + type + test + build all pass
   - Dead code removed
   - HARDEN risk register is clean (no unaddressed Critical${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/High findings)
4. Update CHANGELOG
5. Atomic commit (on the feature branch(es) created in BUILD):
   ```
   type(scope): short description

   - What changed and why
   - Key decisions (reference ADRs)
   - What was intentionally NOT done
   ```
   Before committing, re-run the per-repo branch-guard from BUILD intro (confirm no repo is on a base branch).
6. Merge or open a pull request from the feature branch(es):
   - **mono:** one branch, one PR.
   - **multi:** open a PR in **each repo the scope touched** (paired `fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/be-*` + `fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fe-*` branches), linked by the same issue id. Never ship one side without the other for a `fullstack` unit — they are one change split across repos.
   - **PR (recommended):** Push the branch(es) and open PR(s) for review before merging to the base branch. Never merge unreviewed Critical${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Required findings.
   - **Direct merge (solo${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/small):** Only if no review gate is required:
     ```bash
     cd "$REPO" && git checkout <base-branch> && git merge --no-ff <feature-branch>
     ```
   - Record the merged branch name(s) and PR${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/commit reference in `state.json` (`shippedBranches`, `prUrls` if any).
7. **Cross-skill invocation in this phase:**
   - For the rollback plan and deployment mechanics, invoke `devops-automation` rather than deciding deployment strategy ad hoc.

**Exit criterion:** Feature branch(es) merged (or PR(s) opened) with a clean commit and a rollback plan.

---

### [S] STATUS — Where am I / What's next (on demand)

**Goal:** Give the human an always-available navigation aid. After the pipeline "finishes", after ad-hoc fixes, or when the human loses track of the phase flow, this protocol reconstructs the current position from `state.json` + git and shows the forward path — tied back to what the human actually asked for (the requirements matrix).

**When to run it:**
- The human asks "where are we?", "what now?", "what's next?", "what phase?", or "remind me".
- The human returns after a gap and asks to continue.
- The human asks the agent to fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/change something *outside* the normal phase loop (a bug report, a tweak, a "can you also…").
- The agent finishes ANY request (phase, fix, or answer) and should close by stating the next valid step.

**Process:**

1. **Read position from state:**
    ```bash
    python3 - <<'PY'
    import json
    d = json.load(open('.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.json'))
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
    echo "activeBranch:   $(jq -r .activeBranch .dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.json)"
    echo "linkedBranches: $(jq -r '.linkedBranches ${PROJECT_ROOT}/ {}' .dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.json)"
    echo "branches:       $(jq -r '.branches ${PROJECT_ROOT}/ {}' .dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.json)"
    ```
    - Uncommitted changes in any repo → warn: *"Uncommitted work in `<R>`. The phase loop expects atomic per-slice commits. Commit or stash before moving on."*
    - On a different branch than the recorded branch for that repo → warn: *"You're on `<x>` in `<R>`, not the feature branch `<expected>`. Switch back before committing."*
    - A phase marked `completed` but `git log` shows no commit since it started → flag: *"`<phase>` is marked done but no commit landed — verification may be unrecorded."*

3. **Map to requirements coverage (stay close to what the human expects):**
    - If `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/requirements.md` exists, read it and report:
      - Total requirements, and how many P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1 are traced ✅ vs ⚠️ GAP vs ❌ GAP.
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

5. **Resume-after-ad-hoc-fix routing:** When the human asks for a fix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/tweak *outside* the loop, do NOT silently edit and claim done. Instead:
    - Identify which phase the fix belongs to (bug → re-run TEST + the slice's SECURE; style${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/convention → re-run MATCH${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/LINT; security → HARDEN; spec gap → back to REQUIREMENTS-EXTRACTION).
    - Run that phase's verification on the changed slice, then update state + requirements.md if coverage changed.
    - Close by printing the roadmap (step 4) so the human sees the fix did not skip gates.

**Output contract:** STATUS must always answer three questions for the human:
1. *Where am I?* (phase + completed${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/pending map)
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

2. Write handoff to sessions${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/session-YYYYMMDD-N.md:
   - What was accomplished
   - What's in progress
   - What's next
   - Known issues

3. Summarize: "Session saved. Run dev-craft to resume."

---

## Workflow Orchestration

For complex features spanning multiple domains. Load `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/cross-skill.md` for workflow tables, orchestration patterns, and cross-skill communication protocols.

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|---|
| "I know what they want" | #1 cause of AI misalignment |
| "Just start coding" | No spec → scope creep, wrong architecture |
| "Tests later / lint after slices" | You won't; debt compounds |
| "Tests pass, it's good" | Tests don't catch architecture${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/security |
| "Commit at the end / to main" | Destroys history; always branch → review |
| "Prototype, skip security" | Prototypes become production |
| "Fix architecture later" | Rot compounds fast |
| "Skip arch scan" | 2-min scan prevents 2-hour rework |

## Red Flags

- Skipping ARCH-SCAN (>10 files)
- Starting BUILD without completed ALIGN
- Code before SOURCE (current-version docs)
- Lint${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/tests failing but proceeding
- Multiple slices in one commit; commits to main${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/develop
- No ADRs, no .dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/, no domain model for multi-module
- "Fix it later" for Critical findings; security review skipped
- `activeBranch` mismatch (recorded branch ≠ actual HEAD)
- Vague prompt accepted; REQUIRE skipped when spec files exist
- Wrong dependency order; no build-order.md for complex projects
- BUILD without passing `requirements.md` coverage gate (P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1 gaps unresolved)
- Ad-hoc fix outside phase loop without re-running verification
- Plan tasks with AC that can't map to a REQ-ID

## Verification

- [ ] ARCH-SCAN was run (or deferred with approval)
- [ ] .dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/state.json exists with status: complete
- [ ] All slices implemented and committed on a dedicated feature branch
- [ ] `activeBranch` recorded in state.json and verified to exist before BUILD commits
- [ ] Feature branch merged or PR opened during SHIP (not committed to base)
- [ ] Full test suite passes
- [ ] Linter + formatter pass
- [ ] Type checker passes
- [ ] No debug tags or temp files
- [ ] ADRs written for decisions
- [ ] CONTEXT.md up to date
- [ ] HARDEN risk register clean (no unaddressed Critical${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/High findings)
- [ ] Every slice had SECURE check pass before commit
- [ ] Commit references ADRs
- [ ] Human approved every checkpoint
- [ ] Input was assessed (vague prompts redirected to product-thinking)
- [ ] REQUIRE phase completed (or skipped with valid reason)
- [ ] Domain model exists in .dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/domain.md (for multi-module projects)
- [ ] Build order documented in .dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/build-order.md (for complex projects)
- [ ] Module dependencies respected during build
- [ ] **`requirements.md` exists and the COVERAGE GATE passed** (every P1${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/G1 REQ-ID traced to a task + acceptance criterion)
- [ ] Any ad-hoc fix was routed through STATUS and re-ran the owning phase's verification
- [ ] Agent closed its last turn by stating current phase + next valid step (STATUS)
- [ ] No uncommitted drift warning left unaddressed before claiming a phase complete

## See Also

- `plugins${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/SKILL.md` — Deep security scan pipeline
- `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/modern-patterns.md` — Per-language guidance
- `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/lint-rules.md` — Forbidden patterns + ruff gate (Optional[], single-char names)
- `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/phase-templates.md` — Templates for documents
- `product-thinking` — Refine vague ideas into structured specs
- `project-discovery` — Extract domain model from existing documents
- `agent-orchestration` — Multi-agent parallel builds with git worktree
- `quality-gates` — Layered validation pipeline