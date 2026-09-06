# AGENTS.md — Canonical Agent Policy

This file is the single source of truth for coding agents working in this repository.

Supported targets:
- Codex
- OpenCode
- Oh-my-pi (OMP)
- Claude Code via a thin `CLAUDE.md` wrapper containing `@AGENTS.md`

Priority order when instructions conflict:
1. Platform/system instructions.
2. The user's current request and explicit acceptance criteria.
3. A nested `AGENTS.md` closer to the files being touched (see §10) overrides this root file for that subtree.
4. This root file.

---

## 1. Core Operating Contract

1. **Make the smallest correct change.**
   Satisfy the requested behavior. Do not add speculative features, unrelated refactors, abstractions, dependencies, or cleanup.

2. **Current truth beats historical context.**
   Resolve conflicts in this order: current user request/acceptance criteria → current code/tests/schemas/config/runtime evidence → current git state and authoritative project docs → historical notes, handoffs, memory.

3. **Read before edit.**
   Reuse existing types, helpers, components, conventions before creating new ones. Prefer modifying the established path over a parallel implementation.

4. **Plan proportionally.**
   Small/local/reversible: state intent briefly and proceed. Cross-module, risky, ambiguous, migration, security-sensitive, or contract-changing: write a plan before implementing.

5. **Ask only when the user owns the decision** — destructive/irreversible, changes a public contract, risks data loss, requires a product trade-off, or would take substantial work to unwind. Otherwise pick the safest established default and verify it.

6. **Root cause over symptom.**
   Establish reproduction/evidence before editing when practical. Fix the narrowest verified cause. Never mask failures with retries, broad exception handling, disabled validation, or weakened tests unless the design explicitly calls for it.

7. **Evidence before completion.**
   Never claim a task is done from memory or inference — report verification actually performed, fresh.

8. **No hidden destructive actions.** Full list and rules in §8. Never commit/push/merge/deploy/reset data without explicit instruction.

9. **Verify before invoking — never guess a tool into existence.**
   Every named skill, subagent, MCP connector, or plugin in this document (claude-mem, CodeGraph, Graphify, `planner`/`implementer`/etc., `dev-craft`, `caveman`, `ponytail`, ...) is a *candidate*, not a guarantee. Before calling one:
   - Confirm it is actually available in the current session's tool/skill list.
   - If unavailable, do not fabricate its name, parameters, or output — fall back immediately to the plain/lightweight method listed as its escalation path (raw search, direct file read, manual reasoning), and say in the handoff that the preferred tool wasn't available.
   - A failed guess costs more tokens than checking first (a bad call, a retry, and a correction) — checking availability is the cheaper path, not the slower one.

---

## 2. Context & Cost Discipline

This section applies to every task, regardless of which tools from §§3–5 turn out to be available.

**Default retrieval flow**
1. Understand the task and acceptance criteria.
2. Decide whether historical context materially matters.
3. Choose **one** retrieval mechanism first (see table below); do not run multiple systems speculatively.
4. Read only what that result surfaces.
5. Expand only for a specific unresolved dependency.
6. Stop once there's enough evidence to implement safely.

**Choose the source by question**

| Need | First choice | Escalate only when needed |
|---|---|---|
| Previous decisions, prior fixes, rationale, session continuity | claude-mem (if available) | git history, current source verification |
| Exact symbol, definition, caller/callee, code path | CodeGraph (if available) | targeted source read, `rg` |
| Architecture, cross-module relationships, spec-to-code mapping | Graphify (if available) | CodeGraph for exact symbols |
| Exact string, error text, config key, filename | `rg` / targeted read | graph tools |
| Current behavior | source + tests + runtime evidence | history only for rationale |

**Budget (defaults, not hard limits)**
- Initial source reads: ~5 relevant files.
- Memory search results: 5–8 compact entries; full observations: 2–4.
- One focused graph query before broad traversal.
- Don't reread unchanged files unless new evidence invalidates prior assumptions.
- Don't copy full tool outputs into another prompt — pass conclusions, identifiers, and `path:line` evidence instead.
- Don't run a graph/memory system merely because it's installed and available.

**Cost postures** (apply throughout implementation, review, and handoff — not a separate step):
- **Ponytail** (default implementation stance): reuse before create, no new abstraction without repeated need, no new dependency when an existing capability suffices, minimal surface area.
- **Caveman** (default communication stance): concise exploration notes, review comments, commit messages, handoffs, subagent summaries — but never compress away security implications, migration risk, failed verification, or acceptance criteria.

---

## 3. claude-mem Protocol *(skip entirely if claude-mem is not installed/available)*

**Automatic behavior:** let lifecycle hooks capture/inject recent context. Do not manually query memory merely because the plugin exists.

**Explicitly query memory when:** the user says "continue"/"last time"/"we already decided"; resuming after context rotation or a long gap; a design's rationale isn't discoverable from current code/docs; investigating a recurring regression; preparing a handoff; comparing current implementation against an earlier decision.

**Progressive disclosure:**
1. `search` — focused query, prefer 5–8 compact results.
2. `timeline` — only when chronology matters.
3. `get_observations` — filtered IDs only, batched, normally 2–4 full observations.

**Safety rules:**
- Memory is historical evidence, not source of truth — validate against current code/tests/config before editing.
- Search across agents by default; filter by platform only when platform-specific history itself matters.
- Never paste large memory dumps into prompts, plans, handoffs, or any `AGENTS.md`/`CLAUDE.md`.
- Never intentionally persist secrets, tokens, credentials, keys, customer-sensitive data, or large raw logs.
- If claude-mem is unavailable or returns nothing useful, continue from repository evidence — memory is an optimization, never a blocker.
- Keep claude-mem auto-generated folder-level instruction files disabled unless the user explicitly opts in.

---

## 4. CodeGraph / Graphify / Raw Search

**CodeGraph** *(only if `.codegraph/` exists)* — for symbol definitions, caller/callee chains, exact implementation paths, code-level impact tracing. One focused `codegraph_explore` query before broad grep. If no index exists, skip it unless the user explicitly asks to build one.

**Graphify** *(only if available)* — for architecture maps, cross-module relationships, spec/doc-to-code alignment, broad dependency analysis. Prefer scoped `query`/`path`/`explain` over a full report. Update its index once near completion if code changed materially — not after every edit.

**Raw search** (`rg`, targeted reads) — default for exact strings, error messages, config keys, filenames, and any small/local question. Do not invoke a graph system merely because one is available.

**Escalation rule:** CodeGraph → Graphify (or reverse) is optional escalation, not a mandatory chain. Only escalate when you can state the specific unanswered question the second tool is expected to resolve.

---

## 5. Agent Routing & Skills

This table applies **only where the current platform actually supports named subagents/skills** (verify per §1.9 — currently most reliable on Claude Code with subagents configured). On platforms without subagent support, treat the "Primary agent" column as role framing for a single agent, not a literal dispatch target.

| Task | Primary agent | Start with | Add only when needed |
|---|---|---|---|
| Vague feature / product idea | `planner` | product-thinking, planning-and-task-breakdown | grilling |
| Spec-driven work | `planner` → `implementer` | project-discovery, planning-and-task-breakdown | dev-craft |
| Small/new feature | `implementer` | dev-craft | planning-and-task-breakdown |
| Bug / failing test | `debugger` | debugging-and-error-recovery | surgical-patch |
| Behavior-preserving refactor | `debugger` / `implementer` | debugging-and-error-recovery, refactor-and-cleanup | |
| DB/schema migration | `database-engineer` | database-migrations | dev-craft |
| API/contract change | `api-designer` | api-design | |
| Frontend/UI | `frontend-engineer` | ui-craft | ui-pattern-extractor, image-to-code, playwright-skill |
| Tech stack research | `frontend-engineer` / `implementer` | tech-advisor | ui-craft, dev-craft |
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

Route once per task unless scope materially changes. Skills are capabilities loaded on demand — never preload every skill file at session start.

**Skill notes (only where the skill exists in this environment — see §1.9):**
- `dev-craft` — default implementation posture (Ponytail: reuse first, minimal footprint).
- `debugging-and-error-recovery` + `surgical-patch` — targeted bugs/regressions, investigate first.
- `refactor-and-cleanup` — behavior-preserving structural changes only.
- `database-migrations` — schema/API/dependency migrations; preserve data and rollback path.
- `verification-before-completion` / `verify-gate` — run once the implementation slice is coherent, not after every edit.
- `playwright-skill` — frontend behavior needing live interaction validation.
- `tech-advisor` — research alternatives before implementation; mandatory before UI/frontend work on existing codebases.
- `ui-pattern-extractor` — extract existing UI patterns/tokens/conventions; mandatory before writing UI code on existing codebases.
- `caveman` / `caveman-evidence-review` — compact exploration, reviews, commits, handoffs (see Caveman posture, §2) — never at the cost of correctness or warnings.
- `prompt-optimizer` — only for large/noisy/ambiguous prompts where compression preserves requirements; skip for already-precise tasks.

---

## 6. Standard Execution Workflow

1. **Scope** — concrete goal, acceptance criteria, explicit non-goals; separate required work from optional improvements.
2. **Recover context** — per §2's retrieval flow; use claude-mem only if history matters (§3); avoid broad reconnaissance unless genuinely required.
3. **Git safety** — inspect `git status`; preserve unrelated dirty work; reuse an existing dedicated task branch or have the primary writer create one (`git switch -c <type>/<short-slug>`); agents sharing a worktree don't switch branches independently.
4. **Implement** — per §1 (smallest correct change, reuse existing patterns, root-cause fix, preserve public interfaces unless explicitly changing them).
5. **Verify** — smallest fresh proof set that covers the changed behavior (§7).
6. **Self-review** — check the diff for accidental changes, missed edge cases, security/authorization boundaries, data/migration risk, stale generated artifacts, weakened tests, unrelated formatting.
7. **Handoff** — per §12.

---

## 7. Verification Policy

Task-scoped — never run every possible gate for every task.

- **Bug fix:** reproduce/establish a failing proof → implement fix → run the regression test → run directly affected tests.
- **Backend/code change:** relevant lint, type-check, focused unit/integration tests, directly affected module tests.
- **Frontend/UI change:** targeted tests; one live browser/Playwright validation when the app can be run; check relevant interaction state and console errors.
- **Migration:** upgrade path, downgrade/rollback path, constraints, data preservation/backfill, compatibility during transition — as applicable.
- **Docs/config-only:** syntax, config parsing, links, generated output where applicable — don't run unrelated product suites.
- **Review/analysis-only:** don't edit product code unless a fix is requested; run tests only to validate a finding.

**Full suite:** run only when explicitly requested, at a release/merge/completion gate, or when the change surface is too broad for targeted verification to give adequate confidence. If it's known/estimated to take >10 minutes and isn't explicitly required: don't auto-start it, run targeted verification instead, state that the full suite wasn't run, and give the exact command for the operator.

Never weaken, delete, skip, or rewrite a relevant failing test merely to obtain green output.

---

## 8. Branch, Commit, and Infrastructure Safety

The canonical destructive-action list (referenced from §1.8):

- Never commit, push, amend, merge, open a PR, deploy, reset/drop data, or apply destructive infrastructure changes without explicit user instruction.
- Inspect `git status` and `git diff` before staging or handoff.
- Never commit secrets, `.env` values, credentials, private keys, or tokens.
- Assume pre-existing dirty changes belong to the user; never discard unrelated work.
- For migrations, IaC, and destructive operations: inspect/show the plan or diff, identify the target environment, preserve a rollback path, require explicit approval before destructive execution.

---

## 9. Multi-Agent Contract

Parallelize only work that is genuinely independent. **Apply the full contract below only for actual parallel/independent dispatch — skip it for single-agent sequential work.**

**Before dispatch**, define per subagent: one concrete goal, minimal relevant context, expected deliverable, file/interface ownership, acceptance criteria, read-only vs. may-edit. Avoid overlapping edits; use isolated worktrees for parallel writers when appropriate.

**Pass only:** relevant contract/data shape, relevant symbols/files, relevant acceptance criteria, unresolved questions.
**Never pass:** the entire conversation, full memory history, full graph reports, unrelated project documentation.

**Subagent return format:** Findings/Changes · Evidence (`path:line`) · Risks/Unknowns · Verification.

The primary agent owns integration, conflict resolution, final diff review, final verification, and final user handoff.

**Context rotation** (when active context becomes too large): create a compact handoff (goal, decisions, changed files, verification, unresolved issues) → store only durable conclusions in memory → resume from the handoff plus current repository truth. Never carry raw logs, full transcripts, or complete graph reports across rotations.

---

## 10. Project Instruction Hierarchy

Keep repository policy modular:

```text
repo/
├── AGENTS.md             # canonical cross-agent policy (this file)
├── CLAUDE.md             # thin wrapper: @AGENTS.md
├── backend/
│   └── AGENTS.md         # only backend-specific rules
├── frontend/
│   └── AGENTS.md         # only frontend-specific rules
└── infra/
    └── AGENTS.md         # only infra-specific rules
```

- A nested `AGENTS.md` overrides this root file for files within its subtree when they conflict; it should contain only rules specific to that subtree, never a duplicate of root rules.
- Avoid platform-specific policy copies unless a platform truly requires behavior that can't be expressed here.

---

## 11. Environment Defaults

- Detect the current environment rather than assuming one; use the commands/paths for the OS actually running the agent, not ones copied from another platform.
- Prefer portable relative paths and `/` separators in repository instructions.
- Prefer project-managed tooling over globally installed ad-hoc dependencies; follow the repo's existing package/runtime manager.
- Do not install dependencies, modify global configuration, or mutate developer tooling unless required by the task or explicitly requested.

---

## 12. Completion Handoff

**Changed** — concise summary of files/behavior modified.
**Verified** — exact checks run and their results.
**Risk** — only remaining uncertainty that materially matters.
**Skipped** — material checks intentionally not run, and why.

Do not repeat the full plan, tool transcripts, memory history, unchanged source, or entire test logs.

A task is complete when the requested behavior is implemented, task-relevant verification is fresh, the diff has been reviewed, and any remaining risk is clearly disclosed.
