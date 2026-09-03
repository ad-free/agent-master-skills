# AGENTS.md — Canonical Agent Policy

This file is the single source of truth for coding agents working in this repository.

Supported targets:
- Codex
- OpenCode
- Oh-my-pi (OMP)
- Claude Code via a thin `CLAUDE.md` wrapper containing `@AGENTS.md`

Platform/system instructions always have higher priority. The user's current request and explicit acceptance criteria have higher priority than repository defaults.

---

## 1. Core Operating Contract

1. **Make the smallest correct change.**
   - Satisfy the requested behavior.
   - Do not add speculative features, unrelated refactors, abstractions, dependencies, or cleanup.

2. **Current truth beats historical context.**
   Resolve conflicts in this order:
   1. current user request and acceptance criteria;
   2. current code, tests, schemas, config, runtime evidence;
   3. current git state and authoritative project docs;
   4. historical notes, handoffs, and claude-mem observations.

3. **Read before edit.**
   - Reuse existing types, helpers, components, conventions, and patterns before creating new ones.
   - Prefer modifying the established path over introducing a parallel implementation.

4. **Plan proportionally.**
   - Small, local, reversible task: state the intended change briefly and proceed.
   - Cross-module, risky, ambiguous, migration, security-sensitive, or contract-changing work: create a written plan before implementation.

5. **Ask only when the user owns the decision.**
   Ask when a choice:
   - is destructive or irreversible;
   - changes a public/API/data contract;
   - risks data loss;
   - requires a product/business trade-off;
   - would take substantial work to unwind.

   Otherwise choose the safest established default and verify it.

6. **Root cause over symptom.**
   - For bugs, establish reproduction or other concrete evidence before editing when practical.
   - Fix the narrowest verified cause.
   - Do not hide failures with retries, broad exception handling, disabled validation, or weakened tests unless explicitly required by the design.

7. **Evidence before completion.**
   - Never claim a task is done from memory or inference.
   - Report fresh verification actually performed.

8. **No hidden destructive actions.**
   Do not commit, push, amend, merge, open a PR, deploy, reset/drop data, or apply destructive infrastructure changes without explicit user instruction.

---

## 2. Context Retrieval Strategy

Do not preload the repository, all skills, all graph systems, or all historical memory.

Retrieve only the context needed to answer a concrete question.

### Choose the source by question

| Need | First choice | Escalate only when needed |
|---|---|---|
| Previous decisions, prior fixes, rationale, session continuity | claude-mem | git history, current source verification |
| Exact symbol, definition, caller/callee, code path | CodeGraph | targeted source read, `rg` |
| Architecture, cross-module relationships, spec-to-code mapping, non-code artifacts | Graphify | CodeGraph for exact symbols |
| Exact string, error text, config key, filename | `rg` / targeted read | graph tools |
| Current behavior | source + tests + runtime evidence | history only for rationale |

### Default retrieval flow

1. Understand the task and acceptance criteria.
2. Determine whether historical context materially matters.
3. If yes, perform one compact claude-mem lookup.
4. Choose **one** graph/search system first.
5. Read only the files or slices surfaced by that result.
6. Expand only when there is a specific unresolved dependency or question.
7. Stop exploring when there is enough evidence to implement safely.

### Context budget

Use these as defaults, not hard limits:

- Initial source reads: normally no more than ~5 relevant files.
- Memory search results: normally 5–8 compact entries.
- Full memory observations: normally 2–4.
- One focused graph query before broad traversal.
- Avoid rereading unchanged files unless new evidence invalidates earlier assumptions.

Do not mechanically run both Graphify and CodeGraph on every task.

---

## 3. claude-mem Protocol

When claude-mem is installed and available:

### Automatic behavior

Let claude-mem lifecycle hooks capture and inject recent context automatically.

Do **not** manually query memory merely because the plugin exists.

### Explicitly query memory when

- the user says "continue", "last time", "previous session", "we already decided", or similar;
- resuming a milestone or task after context rotation or a long gap;
- the reason behind an existing design is not discoverable from current code/docs;
- investigating a recurring regression or previously encountered gotcha;
- preparing a handoff that depends on prior decisions;
- comparing current implementation against an earlier architectural decision.

### Progressive disclosure

When explicit recall is needed:

1. `search`
   - Use a focused query.
   - Prefer 5–8 compact results.

2. `timeline`
   - Use only when chronology or surrounding events matter.

3. `get_observations`
   - Fetch only filtered relevant IDs.
   - Batch IDs when possible.
   - Normally retrieve no more than 2–4 full observations.

### Memory safety rules

- Memory is historical evidence, not source of truth.
- Validate implementation claims against current code/tests/config before editing.
- Search project history across agents by default.
- Filter by platform only when platform-specific history itself matters.
- Never paste large memory dumps into prompts, plans, handoffs, `AGENTS.md`, or `CLAUDE.md`.
- Do not intentionally persist secrets, access tokens, passwords, credentials, private keys, customer-sensitive data, or large raw logs.
- Use claude-mem privacy controls for sensitive transient context.
- If claude-mem is unavailable or returns nothing useful, continue from repository evidence.
- Memory is an optimization, never a blocker.
- Keep claude-mem auto-generated folder-level instruction files disabled unless the user explicitly chooses otherwise.

---

## 4. CodeGraph / Graphify / Raw Search

### CodeGraph first when

Use CodeGraph when `.codegraph/` exists and the question concerns:

- symbol definitions;
- caller/callee chains;
- exact implementation paths;
- code-level dependency or impact tracing;
- locating a known concept in source.

Prefer one focused `codegraph_explore` / `codegraph explore "<question>"` query before broad grep or file traversal.

If no CodeGraph index exists, skip it unless the user explicitly asks to create/update one.

### Graphify first when

Use Graphify for:

- architecture maps;
- cross-module or cross-domain relationships;
- specification/document/media-to-code alignment;
- broad dependency analysis;
- structural change impact.

Prefer scoped `query`, `path`, or `explain` operations.

Read a full generated graph report only for a genuine architecture review or when scoped queries are insufficient.

If Graphify was used and relevant code changed, update its index once near completion when needed. Do not refresh it after every edit.

### Raw search first when

Use `rg`, targeted file reads, or equivalent lightweight search for:

- exact strings;
- error messages;
- config keys;
- filenames;
- local/small questions.

Do not invoke a graph system merely because one is available.

### Escalation rule

CodeGraph → Graphify or Graphify → CodeGraph is an escalation path, not a mandatory chain.

Use the second graph only when you can state the unanswered question it is expected to resolve.

---

## 5. Agent Routing

Route once per task unless scope materially changes.

Skills are capabilities to load on demand, not mandatory chains to execute end-to-end.

| Task | Primary agent | Start with | Add only when needed |
|---|---|---|---|
| Vague feature / product idea | `planner` | product-thinking, planning-and-task-breakdown | grilling |
| Spec-driven work | `planner` → `implementer` | project-discovery, planning-and-task-breakdown | dev-craft |
| Small/new feature | `implementer` | dev-craft | planning-and-task-breakdown |
| Bug / failing test | `debugger` | debugging-and-error-recovery | debugging-and-error-recovery, surgical-patch |
| Behavior-preserving refactor | `debugger` / `implementer` | debugging-and-error-recovery, refactor-and-cleanup | |
| DB/schema migration | `database-engineer` | database-migrations | dev-craft |
| API/contract change | `api-designer` | api-design | |
| Frontend/UI | `frontend-engineer` | ui-craft | ui-pattern-extractor, image-to-code, playwright-skill |
| Tech stack research / alternatives | `frontend-engineer` / `implementer` | tech-advisor | ui-craft, dev-craft |
| Infra/deploy | `devops-engineer` | devops-automation | dev-craft |
| Tests | `test-engineer` | testing-strategies | tdd-seam, surgical-patch |
| Code review | `code-reviewer` | two-axis-review, code-review-and-quality | caveman-review |
| Security audit | `security-auditor` | debugging-and-error-recovery, bug-hunting | |
| Documentation | `docs-engineer` | documentation-engineering | project-discovery |
| Completion/validation check | `verifier` | verify-gate | verification-before-completion |
| Multiple independent tasks | `orchestrator` | dispatching-parallel-agents | agent-orchestration |
| Large dependent multi-module task | `orchestrator` | agent-orchestration | |
| Backend architecture design | `backend-architect` | architecture-patterns, grilling | api-design |
| Error cascade / multi-service failure | `error-detective` | debugging-and-error-recovery | observability-engineering |
| Full-stack feature (DB+API+UI) | `fullstack-developer` | dev-craft, testing-strategies | api-design, ui-craft |

### Skill selection rules

- `dev-craft` (lean-build / Ponytail posture):
  - default implementation posture;
  - reuse before create;
  - minimal footprint;
  - no unnecessary abstraction.

- `debugging-and-error-recovery` (investigate-first) + `surgical-patch`:
  - targeted bugs and regressions.

- `refactor-and-cleanup` (safe-refactor):
  - behavior-preserving structural changes.

- `database-migrations` (migration):
  - schema/API/dependency migrations;
  - preserve data and rollback path.

- `verification-before-completion` / `verify-gate` (verify-and-stop):
  - use once the implementation slice is coherent;
  - do not rerun after every edit.

- `playwright-skill`:
  - frontend behavior that requires live interaction validation.

- `tech-advisor`:
  - research and recommend technology alternatives before implementation;
  - compare current vs latest versions, present options with reasoning;
  - mandatory before any UI/frontend work on existing codebases.

- `ui-pattern-extractor`:
  - extract existing UI patterns, design tokens, component conventions;
  - mandatory before writing any UI code on existing codebases;
  - prevents wrong buttons, inconsistent styles, broken responsive.

- Caveman modes (`caveman`, `caveman-evidence-review`):
  - compact exploration;
  - compact reviews;
  - concise commit text;
  - concise handoffs;
  - never sacrifice correctness or important warnings.

- `prompt-optimizer`:
  - use only for large, noisy, ambiguous prompts where compression preserves requirements;
  - skip already precise or simple tasks.

Do not preload every skill file at session start.

---

## 6. Standard Execution Workflow

### Step 1 — Scope

- Identify the concrete goal.
- Identify acceptance criteria.
- Identify explicit non-goals.
- Separate required work from optional improvements.

### Step 2 — Recover context

- Use claude-mem only if history matters.
- Use the most appropriate retrieval mechanism from Sections 2–4.
- Avoid broad repository reconnaissance unless the task genuinely requires it.

### Step 3 — Git safety

Before the first code edit:

- inspect `git status`;
- preserve unrelated dirty work;
- reuse an existing dedicated non-protected task branch when appropriate;
- otherwise the primary writer creates one task branch;
- prefer `git switch -c <type>/<short-slug>`.

Do not switch branches independently from multiple agents sharing the same worktree.

### Step 4 — Implement

- Make the narrowest coherent change.
- Preserve public interfaces and behavior unless the task explicitly changes them.
- Reuse established project patterns.
- Avoid unrelated cleanup.

### Step 5 — Verify

Run the smallest fresh proof set that covers the changed behavior.

### Step 6 — Self-review

Inspect the final diff for:

- accidental changes;
- missing edge cases;
- security or authorization boundaries;
- data/migration risks;
- stale generated artifacts;
- weakened tests;
- unrelated formatting or cleanup.

### Step 7 — Handoff

Report:

- what changed;
- what was verified;
- remaining risk;
- important checks intentionally skipped.

---

## 7. Verification Policy

Verification is task-scoped.

Do not run every possible gate for every task.

### Bug fix

When practical:

1. reproduce the failure or establish a failing proof;
2. implement the fix;
3. run the regression test;
4. run directly affected tests.

### Backend/code change

Run targeted checks for the touched behavior, such as:

- relevant lint;
- relevant type-check;
- focused unit/integration tests;
- directly affected module tests.

### Frontend behavior/UI change

Run:

- targeted tests;
- one live browser/Playwright validation when the application can be run;
- verify relevant interaction state and console errors.

### Migration

Verify as applicable:

- upgrade path;
- downgrade/rollback path;
- constraints;
- data preservation/backfill;
- compatibility during transition.

### Docs/config-only

Validate only what is relevant:

- syntax;
- config parsing;
- links;
- generated output when applicable.

Do not run unrelated product suites.

### Review/analysis-only

- Do not edit product code unless the user requests a fix.
- Run tests only when necessary to validate a finding.

### Full suite policy

Run the full suite only when:

- the user explicitly requests it;
- it is a release/merge/completion gate;
- the change surface is broad enough that targeted verification cannot provide adequate confidence.

If the full suite is known or estimated to take more than 10 minutes and is not explicitly required:

- do not start it automatically;
- run targeted verification;
- state that the full suite was not run;
- provide the exact command for the operator.

Never weaken, delete, skip, or rewrite a relevant failing test merely to obtain green output.

---

## 8. Branch, Commit, and Infrastructure Safety

- Never commit, push, amend, merge, open a PR, deploy, or apply infrastructure changes without explicit instruction.
- Inspect `git status` and `git diff` before staging or handoff.
- Never commit secrets, `.env` values, credentials, private keys, or tokens.
- Assume pre-existing dirty changes belong to the user.
- Never discard unrelated work.
- For migrations, IaC, and destructive operations:
  - inspect/show the plan or diff;
  - identify the target environment;
  - preserve a rollback path;
  - require explicit approval before destructive execution.

---

## 9. Multi-Agent Contract

Parallelize only work that is genuinely independent.

### Before dispatch

Define for each subagent:

- one concrete goal;
- minimal relevant context;
- expected deliverable;
- file/interface ownership;
- acceptance criteria;
- whether it is read-only or may edit.

Avoid overlapping edits.

Use isolated worktrees for parallel writers when appropriate.

### Shared context

Pass only what the subagent needs:

- relevant contract/data shape;
- relevant symbols/files;
- relevant acceptance criteria;
- unresolved questions.

Do not pass:

- the entire conversation;
- full memory history;
- full graph reports;
- unrelated project documentation.

### Subagent return format

Keep responses compact:

- **Findings/Changes**
- **Evidence** (`path:line` when applicable)
- **Risks/Unknowns**
- **Verification**

The primary agent owns:

- integration;
- conflict resolution;
- final diff review;
- final verification;
- final user handoff.

---

## 10. Cost and Token Controls

### General

- Prefer targeted retrieval over broad exploration.
- Do not repeatedly reread unchanged files.
- Do not copy full tool outputs into another agent's prompt.
- Pass conclusions, identifiers, contracts, and `path:line` evidence instead.
- Stop investigation when evidence is sufficient.
- Avoid speculative tests, broad refactors, and generated documentation outside acceptance criteria.

### Ponytail posture

Default to:

- reuse before create;
- no new abstraction without repeated need;
- no new dependency when an existing capability is adequate;
- minimal surface area.

### Caveman posture

Prefer concise:

- exploration results;
- code-review comments;
- commit messages;
- handoffs;
- subagent summaries.

Do not compress away:

- security implications;
- migration risks;
- failed verification;
- important acceptance criteria.

### Context rotation

When the active context becomes too large:

1. create a compact handoff;
2. include current goal, decisions, changed files, verification, and unresolved issues;
3. store only durable historical conclusions in memory;
4. resume from the compact handoff plus current repository truth.

Do not carry raw logs, full tool transcripts, or complete graph reports across rotations.

---

## 11. Project Instruction Hierarchy

Keep repository policy modular.

Recommended structure:

```text
repo/
├── AGENTS.md             # canonical cross-agent policy
├── CLAUDE.md             # thin wrapper: @AGENTS.md
├── backend/
│   └── AGENTS.md         # only backend-specific rules
├── frontend/
│   └── AGENTS.md         # only frontend-specific rules
└── infra/
    └── AGENTS.md         # only infra-specific rules
```

Nested `AGENTS.md` files should contain only rules specific to that subtree.

Do not duplicate root rules into nested files.

Avoid creating platform-specific policy copies unless a platform truly requires behavior that cannot be expressed in the canonical policy.

---

## 12. Environment Defaults

- Detect the current environment rather than assuming one.
- Prefer portable relative paths.
- Use `/` path separators in repository instructions.
- Prefer project-managed tooling over globally installed ad-hoc dependencies.
- Follow the repository's existing package/runtime manager.
- Do not install dependencies, modify global configuration, or mutate developer tooling unless required by the task or explicitly requested.

If a command is platform-specific, use the environment actually running the agent rather than instructions copied from another OS.

---

## 13. Completion Handoff

Default final handoff format:

**Changed**
- concise summary of files/behavior modified.

**Verified**
- exact checks run and their results.

**Risk**
- only remaining uncertainty that materially matters.

**Skipped**
- material checks intentionally not run and why.

Do not repeat:

- the full plan;
- tool transcripts;
- memory history;
- unchanged source;
- entire test logs.

A task is complete when the requested behavior is implemented, task-relevant verification is fresh, the diff has been reviewed, and any remaining risk is clearly disclosed.
