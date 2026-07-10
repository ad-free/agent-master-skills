---
name: dev-craft
description: Full-stack engineering pipeline with persistent memory. Use when given a prompt, PLAN.md, or feature request — runs ArchScan → Align → Design → Build → Verify → Harden → Ship. Detects stack, scans for existing code smells, enforces modern patterns, runs lint/type/test after every slice, and resumes across sessions via .dev-craft/ state.
---

# dev-craft

## Overview

A single pipeline that turns a prompt into production-quality code. Every phase has a clear goal, exit criteria, and a human checkpoint. The pipeline persists state to `.dev-craft/` so work survives across sessions.

**Philosophy:** Transparent, human-orchestrated, composable. You remain in control. Skip any phase. Edit any phase. The pipeline serves you, not the other way around.

## When to Use

- Given a prompt, PLAN.md, or feature request
- Starting a new project or feature
- A task that spans multiple files or modules
- Resuming work from a previous session
- Any time you need more than a single-file change

**When NOT to use:** Single-line fixes, typo corrections, trivial config changes where the full pipeline is overkill.

## The Memory System

The project's `.dev-craft/` directory is created on first run and persists across sessions:

```
.dev-craft/
├── state.json           # { currentPhase, completed: [], stack: {...}, slices: [...] }
├── plan.md              # Evolving plan from Align → Design
├── context.md           # Domain glossary (shared language)
├── decisions/           # ADRs — key decisions captured
│   └── 001-*.md
├── sessions/            # Handoff docs for context rotation
│   └── session-YYYYMMDD-N.md
└── config.json          # Project config (linter, formatter, test commands)
```

### Resume Logic

| Scenario | Behavior |
|---|---|
| `.dev-craft/` does not exist | Detect existing code: Phase 1 (ARCH-SCAN) if codebase exists, Phase 2 (ALIGN) if greenfield |
| `state.json` exists, `currentPhase > 0` | Load state, skip completed phases, restore glossary |
| `state.json` says all phases complete | Ask "New task on same project?" — preserves context/ADRs |
| Context near limit mid-phase | Generate handoff doc, save slice position, resume next session |

## Stack Detection

Run during Phase 2 (ALIGN). Scan dependency files for exact versions — see Phase 2 for the full detection table.

If a linter or formatter is detected, every slice MUST pass it. If none is detected, surface to the human: *"No linter/formatter found — recommend installing one. Proceed without?"*

## Pipeline Phases

```
[0] LOAD ──→ [1] ARCH-SCAN ──→ [2] ALIGN ──→ [3] DESIGN ──→ [4] SOURCE ──→ [5] BUILD ──→ [6] TEST ──→ [7] REVIEW ──→ [8] HARDEN ──→ [9] SHIP
                   │                  │              │               │              │             │             │               │             │
                   ▼                  ▼              ▼               ▼              ▼             ▼             ▼               ▼             ▼
               Smell report       CONTEXT.md     PLAN.md +      Fetched       Vertical       Test        Code           Clean +      Commit +
               (remediate        (shared        ADRs           docs          slices         output      review         security     ADRs
                first?)           language)
```

---

### [0] LOAD — Initialize or Resume

Read `.dev-craft/state.json`:

- **Not found** → Detect if the project has existing source code:
  - **Existing code** (`src/`, `lib/`, `app/`, or equivalent directories with source files) → Set `stack: {}`, `completed: []`, `currentPhase: 1`. Run ARCH-SCAN first.
  - **Greenfield** (no source files yet) → Set `stack: {}`, `completed: []`, `currentPhase: 2`. Skip ARCH-SCAN — nothing to scan.
- **Found + all phases complete** → Ask human: "New feature? (preserves context/ADRs)" or "Start fresh?"
- **Found + incomplete** → Load `context.md` into working memory. Set `currentPhase` to next uncompleted phase. Restore slice progress if resuming mid-BUILD.

Write state after LOAD.

---

### [1] ARCH-SCAN — Codebase Smell Detection

**Goal:** Assess existing codebase health before adding new code. Surface architecture debt so the human can decide what to remediate first.

**Process:**

1. **Scan the codebase** for Fowler's code smells across the diff-relevant areas:
   - **Mysterious Name** — function/variable/type names that don't reveal intent
   - **Duplicated Code** — same logic shape in more than one place
   - **Feature Envy** — method that reaches into another object's data more than its own
   - **Data Clumps** — same fields travelling together (a type wanting to be born)
   - **Primitive Obsession** — strings/numbers standing in for domain concepts
   - **Repeated Switches** — same `switch`/`if`-cascade on the same type recurring
   - **Shotgun Surgery** — one logical change forcing scattered edits
   - **Divergent Change** — same file edited for multiple unrelated reasons
   - **Speculative Generality** — abstraction for needs that don't exist yet
   - **Message Chains** — long `a.b().c().d()` navigation chains
   - **Middle Man** — class/module that mostly delegates onward
   - **Refused Bequest** — subclass that ignores most of what it inherits
   - **Dead Code** — exports, functions, or components no longer referenced

2. **Surface the report** as a structured list with locations:
   ```
   SMELL REPORT:
   1. [Duplicated Code] src/utils/format.ts:45-52 and src/lib/helpers.ts:12-19
      → Extract shared function into src/lib/format.ts
   2. [Primitive Obsession] src/models/user.ts: user type uses raw strings for roles
      → Create a Role discriminated union
   3. [Shotgun Surgery] Adding a field touches 5+ files across src/
      → Consolidate schema in one source of truth
   ```

3. **Ask the human to prioritize:**
   - "Fix these before proceeding? (Y/n)"
   - "Which ones should I remediate now?"
   - If human says skip → note the findings in `.dev-craft/state.json` for the REVIEW phase

4. **If remediation is approved** — fix each smell one at a time, commit after each fix, re-run tests after each commit. Do NOT proceed to ALIGN until all chosen smells are resolved.

**Resources:** See `references/modern-patterns.md` for language-specific migration patterns. Use Chesterton's Fence before removing anything you don't understand.

**Exit criterion:** Human has reviewed the report and either approved remediation or explicitly deferred.

**State write:** Save found smells to `state.json` for cross-reference in REVIEW. If smells were deferred, REVIEW will check they weren't made worse.

---

### [2] ALIGN — Grill + Detect + Glossary

**Goal:** Surface assumptions, sharpen requirements, build shared language.

**Process:**

1. **Ask one question at a time** — each with your best guess attached. The human reacts faster to a wrong guess than generating from scratch.
2. **Surface assumptions** — before writing anything, list what you're assuming:
   ```
   ASSUMPTIONS:
   1. This is a web app (not native mobile)
   2. Auth uses JWT stored in httpOnly cookies
   3. Database is PostgreSQL
   → Correct me now or I'll proceed with these.
   ```
3. **Define "Out of scope"** — explicitly state what is NOT being built. Half of misalignment is silent disagreement about what is excluded.
4. **Detect stack** — scan dependency files. State explicitly:
   ```
   STACK DETECTED:
   - Python 3.12, FastAPI, SQLAlchemy 2.0 (pyproject.toml)
   - Node 22, React 19, Vite 6 (package.json)
   - Linter: ruff (ruff.toml)
   - Formatter: ruff
   - Type checker: mypy (mypy.ini)
   ```
5. **Build glossary** — extract key terms from the conversation and write them to `context.md`. This becomes the shared language for all subsequent phases.

**Exit criterion:** Human confirms the refined scope with an explicit yes (not "sounds good", not "whatever you think").

**State write:** Save detected stack to `state.json`. Save `context.md`.

---

### [3] DESIGN — Spec + Plan + ADRs

**Goal:** Produce a structured spec, task breakdown, and architecture decisions.

**Process:**

1. **Write spec** covering:
   - **Objective** — what and why. User stories or acceptance criteria.
   - **Commands** — full executable commands (build, test, lint, type, dev)
   - **Project structure** — where source, tests, docs live
   - **Code style** — see references/modern-patterns.md for per-language guidance. Show one real code snippet per language.
   - **Testing strategy** — framework, test locations, coverage expectations
   - **Boundaries** — three tiers:
     - **Always do:** Run lint+type+test before commit, follow project conventions
     - **Ask first:** Database schema changes, adding dependencies, changing CI
     - **Never do:** Commit secrets, edit vendor dirs, remove failing tests without approval

2. **Map dependency graph** — what depends on what. Build foundations first.

3. **Slice vertically** — decompose into vertical slices (one complete feature path per task, not horizontal layers):
   ```
   Slice 1: User can create an item (DB + API + basic UI)
   Slice 2: User can list items (query + API + UI)
   Slice 3: User can edit an item (update + API + UI)
   ```

4. **Write tasks** — each with acceptance criteria, verification step, estimated size (XS/S/M/L — split L).

5. **Write ADRs** — for every architecture decision:
   ```markdown
   # ADR-001: [Title]
   **Status:** Accepted
   **Context:** [Problem and constraints]
   **Decision:** [What we chose]
   **Alternatives:** [What else was considered and why rejected]
   **Consequences:** [Impact on codebase]
   ```

**Exit criterion:** Human reviews spec + plan + ADRs. Explicit approval.

**State write:** Save `plan.md`. Save ADRs to `.dev-craft/decisions/`.

---

### [4] SOURCE — Document Verification

**Goal:** Verify framework decisions against official docs. Training data is stale.

**Process:**

1. Read exact versions from dependency files (already detected in Phase 2).
2. For each framework/library being used, fetch the **specific official documentation page** for the feature being implemented. Not the homepage. Not a tutorial.
3. Extract key patterns, API signatures, and deprecation warnings.
4. Cite sources inline during the BUILD phase:
   ```python
   # Source: https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy
   async with engine.connect() as conn:
       ...
   ```
5. If documentation does not cover a pattern, flag it explicitly:
   ```
   UNVERIFIED: Could not find official docs for this pattern.
   Based on training data — verify before shipping.
   ```

**Source hierarchy:**
| Priority | Source | Example |
|---|---|---|
| 1 | Official docs | python.org, react.dev, fastapi.tiangolo.com |
| 2 | Official blog/changelog | react.dev/blog |
| 3 | Web standards (MDN) | developer.mozilla.org |
| ❌ NOT authoritative | Stack Overflow, blog posts, training data | — |

6. **Present a source summary to the human:**
   ```
   SOURCE VERIFICATION SUMMARY:
   ✅ FastAPI 0.115 — fetched docs/sqlalchemy for model patterns
   ✅ React 19 — fetched react.dev for useActionState
   ❌ Redis — no official docs found for the pattern, flagged UNVERIFIED
   → Any concerns before I proceed to BUILD?
   ```

**Exit criterion:** Official docs fetched and reviewed for ALL framework dependencies used in this specific feature. Any UNVERIFIED pattern is explicitly noted and the human has acknowledged it.

**State write:** Save fetched source references to state for use in BUILD.

---

### [5] BUILD — TDD + Incremental

**Goal:** Implement one vertical slice at a time, red-green-refactor.

**Process:**

For each vertical slice from the plan:

```
1. RED    — Write a failing test that specifies the behavior
2. GREEN  — Write minimal code to make it pass (Rule 0: simplicity first)
3. LINT   — Run linter + formatter on ALL changed files → must pass
4. TYPE   — Run type checker → must pass
5. TEST   — Run test suite (at least the affected test file) → must pass
6. COMMIT — Atomic commit with structured message
```

**Rules:**
- **Rule 0: Simplicity first** — Three similar lines of code is better than a premature abstraction. Avoid speculative generality.
- **Scope discipline** — Do NOT touch code outside the slice. If you spot improvements, note them. Do not fix them now.
- **One slice at a time** — Do not implement multiple slices in one pass. The pipeline loops over slices.
- **TDD seams** — Test at public interfaces only. Agree on seams with the human before writing code. No testing private methods.
- **Mock at boundaries only** — Prefer real implementations > fakes > stubs > mocks. Over-mocking creates tests that pass while production breaks.
- **Feature flags for risky changes** — If the slice modifies production-critical flow, wrap it behind a feature flag. Deploy OFF → enable in staging → gradual rollout. The feature flag lifecycle (create → test → rollout → remove) is documented in the ADR.

**Lint/Type/Tests are gating — every slice leaves the codebase cleaner than you found it.**

**Exit criterion:** All slices implemented. All tests pass. All lint/type checks pass. Every slice committed.

**State write:** Save completed slices to `state.json`. If context is > 80% full, generate handoff doc in `.dev-craft/sessions/`.

---

### [6] TEST — Full Suite + Diagnose

**Goal:** Run the full test suite. Fix every failure using structured diagnosis.

**Process:**

1. **Run full suite** — `npm test` / `pytest` / `cargo test` / equivalent
2. **If all pass** → Proceed to Phase 7
3. **If any fail** → **Stop-the-Line:**
   ```
   STOP adding anything new
   PRESERVE error output
   RUN structured diagnosis:
     1. REPRODUCE  — Make the failure happen reliably
     2. LOCALIZE   — Bisect if regression; isolate the failing component
     3. REDUCE     — Shrink to minimal failing case
     4. FIX        — Fix the root cause (not the symptom)
     5. GUARD      — Add regression test that fails without the fix
     6. VERIFY     — Full suite passes
   ```
4. **Re-run full suite** after every fix to confirm no regressions.

**Prove-It Pattern for bugs:** When a bug is reported during this phase:
1. Write a test that reproduces the bug (it FAILS — confirming the bug)
2. Implement the fix
3. Test PASSES — bug is fixed and guarded

**Exit criterion:** Full test suite passes with zero failures.

**State write:** Update state. If a handoff doc was needed, write it here.

---

### [7] REVIEW — Six-Axis + Modern Audit

**Goal:** Quality gate before shipping. Review across six axes.

**Process:**

Conduct a parallel review of the entire diff (since the last known-good commit or state):

**Axis 1 — Correctness:**
- Does code match the spec and plan?
- Are edge cases handled (null, empty, boundary)?
- Are error paths handled — not just the happy path?

**Axis 2 — Readability:**
- Are names consistent with CONTEXT.md glossary?
- Is control flow straightforward? (No deep nesting, no clever tricks)
- Does each function have a clear single responsibility?

**Axis 3 — Architecture:**
- Does the change follow the ADRs?
- Are module boundaries clean?
- No feature-specific logic leaked into shared modules?
- If ARCH-SCAN found deferred smells: check they were not made worse by this change

**Axis 4 — Performance:**
- Any N+1 query patterns introduced?
- Any unbounded loops or unconstrained data fetches?
- Any synchronous I/O that should be async?
- Any missing pagination on list endpoints?
- Any large objects created on hot paths?

**Axis 5 — Security:**
- Input validated at boundaries?
- Secrets kept out of code/logs?
- Parameterized queries (no string concatenation)?
- Treat external data as untrusted?

**Axis 6 — Modern Patterns (against fetched docs):**
- No deprecated APIs from the migration guide?
- Code follows patterns shown in current-version docs?
- Lint/format/tests pass?
- If source citations exist, are they for the correct version?

**Categorize every finding:**
| Label | Meaning | Action |
|---|---|---|
| Critical | Blocks merge | Must fix |
| _(no prefix)_ | Required | Must address |
| Nit | Minor, optional | Author may ignore |
| Optional | Suggestion | Worth considering |

**Exit criterion:** All Critical and Required findings resolved. Human approves.

**State write:** Save review findings.

---

### [8] HARDEN — Clean + Security + Simplify

**Goal:** Remove scaffolding, close security gaps, simplify without changing behavior.

**Process:**

**Clean:**
- Remove all debug instrumentation (`[DEBUG-*]` tags, temporary logs)
- Delete throwaway prototypes and dead code paths
- Check for zombie code (unused since the change)

**Security:**
- Run dependency audit (`npm audit`, `pip audit`, `cargo audit`)
- Run threat model (STRIDE) against the change
- Verify all secrets, tokens, and connections are in env vars, not code
- Check SSRF, injection, XSS vectors

**Simplify (Chesterton's Fence):**
- Before simplifying anything, understand why it exists
- Simplify one thing at a time, run tests after each change
- Prefer reducing moving pieces over spreading complexity
- Rule of 500: if the clean touches >500 lines, automate it instead

**Exit criterion:** Zero security findings. All debug code removed. Simplifications tested and passing.

**State write:** Update state.

---

### [9] SHIP — Docs + Commit + Finalize

**Goal:** Deliver the work with full traceability.

**Process:**

1. **Update ADRs** — any decisions made during BUILD/HARDEN that weren't captured in Phase 3. Every key decision must have an ADR.
2. **Update CONTEXT.md** — add any new domain terms encountered.
3. **Final verification:**
   - Lint + type + test + build — all must pass
   - Run secrets scanner (`gitleaks` / `trufflehog` / `secretlint`) on the diff — if none installed, do a manual grep for keys, tokens, passwords, and connection strings
   - Dead code removed
4. **Update CHANGELOG** — add an entry summarizing the change, referencing ADRs.
5. **Atomic commit:**
   ```
   type(scope): short imperative description

   - What changed and why
   - Key decisions (reference ADRs)
   - What was intentionally NOT done
   ```
6. **Define rollback strategy** — state the rollback plan in the commit body:
   - Feature flag toggling: `< 1 minute`
   - Code revert: specify the commit to revert
   - Database rollback: migration revert command
7. **Mark state as complete:**
   ```json
   { "status": "complete", "lastRun": "2026-07-10" }
   ```

**Exit criterion:** Clean commit with rollback plan. All tests/lint/type/secrets pass. State marked complete.

---

### [H] HANDOFF — Cross-Session Context (Cross-Cutting)

**When to trigger:** Mid-phase when context is > 80% full, or when the human says "continue later".

**Process:**
1. Save all in-memory state to `.dev-craft/state.json`:
   - Current phase and slice position
   - Incomplete tasks
   - Pending decisions
2. Write a handoff document to `.dev-craft/sessions/session-YYYYMMDD-N.md`:
   - What was accomplished
   - What's in progress
   - What's next
   - Any decisions to be made
   - Known issues or blockers
3. Summarize to the human: "Session saved. Run dev-craft again to resume from the current phase."

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I don't need to grill — I know what they want" | The #1 cause of AI failure is misalignment. Five minutes of grilling saves hours of rework. |
| "Let me just start coding" | Starting without a spec guarantees scope creep, wrong architecture, and rework. Write the spec first. |
| "I'll add tests later" | You won't. And tests written after the fact test implementation, not behavior. |
| "This is too simple to source-verify" | Training data is stale at every level. A two-line API call can use a deprecated signature. |
| "I'll clean up lint after all slices" | Lint debt compounds. Fix it per-slice or you won't fix it at all. |
| "The tests pass, it's good" | Tests are necessary but not sufficient. They don't catch architecture, security, or modern-pattern issues. |
| "I'll commit everything at the end" | Large commits destroy history value. Commit per-slice so each is revertable. |
| "This is a prototype, skip security" | Prototypes become production. Security from day one prevents the "security debt" crisis. |
| "We'll fix architecture later" | Architecture debt compounds faster than any other. Architectural rot after three agent sessions can take weeks to undo. |
| "I'll clean up dead code at the end" | Dead code confuses agents and humans. Clean as you go. |
| "The codebase is fine, skip the arch scan" | Every codebase has accumulated smells. A 2-minute scan prevents 2-hour rework when you discover the architecture doesn't support your change. |
| "I'll fix architecture after I build the feature" | You'll build on a rotten foundation. The feature will inherit every smell the scan would have caught. Fix first, build second. |

## Red Flags

- Skipping ARCH-SCAN on an existing codebase with > 10 files
- Starting implementation without a completed Align phase
- Human checkpoints skipped without explicit approval
- Writing code before fetching current-version docs
- Multiple slices committed in one commit
- Lint/type/tests failing but moving to next phase
- No ADRs for architecture decisions
- "I'll fix it later" accepted for any Critical finding
- No .dev-craft/ directory created (state not persisting)
- Security review skipped on production-bound code
- Commit messages that say "WIP", "fix", or "update"

## Verification

Before declaring the pipeline complete:

- [ ] ARCH-SCAN was run (or explicitly skipped with human approval)
- [ ] `.dev-craft/state.json` exists with `status: "complete"`
- [ ] All planned slices implemented and committed
- [ ] Full test suite passes
- [ ] Linter + formatter pass on all changed files
- [ ] Type checker passes
- [ ] No debug tags, dead code, or temp files remain
- [ ] ADRs written for all architecture decisions
- [ ] CONTEXT.md glossary is up to date
- [ ] Security audit passed (or explicitly deferred with human approval)
- [ ] No secrets in the diff
- [ ] Commit message references ADRs where relevant
- [ ] Human has approved every checkpoint

## See Also

- `references/modern-patterns.md` — Per-language guidance for detecting and enforcing modern coding patterns
- `references/phase-templates.md` — Templates for spec, plan, task, ADR, and handoff documents
