# Large-path phases

Load one phase at a time. Each phase lists its steps, its exit criterion, and what it writes to state.
Write state at the phase boundary, not after each step.

## Contents
LOAD · SCOPE · REQUIRE · SCAN · ALIGN · DESIGN · TRACE · SOURCE · CONTRACT · BUILD · TEST · REVIEW · HARDEN ·
SHIP-PREP

## LOAD
1. Load or initialize `.dev-craft/state.json`. Add `.dev-craft/` to `.git/info/exclude` if missing.
2. If every phase was completed, ask "New task on the same project?" before continuing.
3. Create or reuse `session.md` with: date, task summary, tier and scope, expected phases. Record `sessionFile`.

**Exit:** state is valid and `sessionFile` is current.

## SCOPE
1. Classify the layer: `be`, `fe`, or `fullstack`. Classify the mode: `build` (new capability) or `ticket`
   (bounded change in an understood codebase). Record both in state.
2. `fe` only: use the UI rules in `SKILL.md` §6 and `ui-craft` for large UI pipelines. Record a
   `skillOverride` in state if dev-craft is intentionally driving a frontend-only task.
3. `ticket`: follow the ticket short-circuit in `SKILL.md` §4.
4. Multi-repo (`multi` topology): list every repo the scope touches. Branches and checks apply to each.

**Exit:** layer and mode recorded.

## REQUIRE
1. Scan for `PRODUCT.md`, `DOMAIN.md`, `PLAN.md`, and spec files.
2. `PRODUCT.md`: extract domain, modules, features, priorities. `DOMAIN.md`: load directly. Spec files: load
   `project-discovery` or extract manually. None: continue to ALIGN with questions.
3. Validate the domain model with the user.

**Exit:** domain model confirmed (or no specs exist). **State:** `domain.md` content goes into `spec.md`.

## SCAN
Run once. If the stored map's git commit hash matches `HEAD`, reuse it. Otherwise refresh only the changed areas.
1. Directory tree, then the frontend architecture (if any), then the backend architecture (if any).
2. Build the codebase map from `codebase-map-template.md`.
3. Read a representative sample across layers (about 10, enough to confirm conventions). Do not repeat this in
   ALIGN.
4. Record detected conventions (layering, naming, error format, test style) plus the git hash in state.

**Exit:** map and conventions recorded. Present a short summary; it is reviewed at the approval checkpoint, not
separately.

## ALIGN
1. Use the domain model to ask calibrated questions. Without one, ask one question at a time.
2. Surface assumptions. Define "out of scope" explicitly.
3. Detect the stack: framework, linter, formatter, type checker, with exact versions. If there is no linter or
   formatter, tell the user and ask whether to proceed without one.
4. Build the glossary (shared domain language) into `spec.md`.
5. Image analysis, if a screenshot or mockup was provided.

**Exit:** scope and assumptions confirmed. Batch the questions into one message.

## DESIGN
1. Write the spec: objective, commands, project structure, code style, testing strategy, boundaries, **data
   model and migrations** (tables, constraints, indexes, rollback), and **infra/config changes**.
2. Map the dependency graph, then fix the build order (modules in DAG order, slices per module).
3. Slice vertically: one complete feature path per slice.
4. Write tasks with Given-When-Then acceptance criteria (`planning-and-task-breakdown`).
5. Write ADRs for architecture decisions, in `documentation-engineering` format.
6. API surface change: invoke `api-design`. Structural pattern decision: invoke `architecture-patterns`.

**Exit:** a plan ready for the checkpoint. **State:** plan, build order, and ADR summaries in `spec.md`.

## TRACE (coverage gate)
1. Extract every requirement from the source spec, literally and exhaustively.
2. Assign stable IDs (`REQ-001`...) and a priority.
3. Trace each requirement to a plan task with an acceptance criterion. Build the matrix in `spec.md`.
4. Self-review the matrix against the spec. Do not delegate this step.
5. Present the matrix and the gaps together with the brief, plan, and build order (the single checkpoint).

<HARD-GATE>
Every P1 requirement is traced to a task with an acceptance criterion. Lower-priority gaps may be deferred only
with explicit user acknowledgement. Get one explicit approval for the whole package before BUILD.
</HARD-GATE>

**State:** `requirementsExtracted`, `coverageGaps`, `deferredRequirements`.

## SOURCE (only when needed)
Run for new libraries, new APIs, or version-sensitive code. Skip for code that only uses patterns already in
the repo.
1. Read exact versions from dependency files.
2. Fetch the specific official docs for the feature in question. Source hierarchy: official docs, then official
   changelog, then web-standards references. Not forum answers or blog posts.
3. Extract API signatures and deprecation warnings. Cite the source inline while building.

## CONTRACT (fullstack only)
1. Extract the existing API endpoints from source. Do not guess. Extract the existing schema the same way.
2. Add new endpoints to `api-contract.md` tagged `[NEW]`. Record the path in state (`apiContract`).
3. The frontend consumes this file and does not invent endpoints.

**Exit:** `api-contract.md` exists and matches the existing endpoints.

## BUILD
1. Branch guard: confirm you are on a feature branch in every repo the scope touches. Create one with
   `git switch -c <type>/<slug>` if needed.
2. For each slice, in build order: failing test → minimal code → security check → convention match → lint
   (read-only check) → type check → tests. Detail in `build-protocol.md`.
3. **Stage only the intended files** and record the slice in `session.md`. Do not commit; propose a message.
4. UI slices: apply the UI rules and capture screenshots of changed routes before the next slice.

**Exit:** all slices implemented, staged, tested, and convention-matched.

## TEST
1. Run the suites the scope touches (the relevant repo for `multi`).
2. Fullstack: assert that the running app matches `api-contract.md`.
3. On any failure, invoke `debugging-and-error-recovery`, then rerun the relevant suites after each fix.

**Exit:** all relevant suites pass and contract conformance holds.

## REVIEW
1. Invoke `code-review-and-quality` over the full diff on seven axes: correctness, readability, architecture,
   performance, security, testing, modern patterns. Add `bug-hunting` for security-critical code.
2. Run the lint gate from `lint-rules.md`. Cryptic-name hits and listed rule violations are automatic fails.
3. Categorize findings (Critical / Optional) and fix everything Critical.
4. Requirements reality-check: for each P1 row in the matrix, confirm the built code satisfies it, with
   evidence (`path:line`, test, or screenshot). Cap revision cycles at two.

**Exit:** Critical findings resolved with evidence and every P1 requirement verified.

## HARDEN
1. Load `harden-checks.md` and run its eight read-the-code checks: secrets, auth/authz, injection surface,
   dependency CVEs, config/infra, cross-slice audit, BE-FE contract conformance, risk register.
2. Check that the changes follow the documented component hierarchy, API contract, and schema conventions.
   Update the codebase map if it is outdated.
3. Invoke `observability-engineering` (a separate concern from security).

**Exit:** Critical and High findings resolved. Accepted risks are recorded with reasons in `spec.md`.

## SHIP-PREP
1. Update ADRs for decisions made during BUILD and HARDEN. Add new terms to the glossary.
2. Final verification: lint, type check, build, and tests pass; secrets scan run; dead code removed.
3. Define the rollback strategy. For migrations, prove upgrade and rollback in a disposable database.
4. Prepare the handoff: changed files, requirement statuses with evidence, verification commands and results,
   risks and skipped checks, new env vars, and a proposed conventional commit message.
5. Mark the state complete. Do not commit unless the user asks.

**Exit:** a staged, verified change with a rollback plan and a proposed commit message.
