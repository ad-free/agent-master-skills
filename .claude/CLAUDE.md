# CLAUDE.md — Claude Code Agent Instructions

Cross-project rules for every Claude Code session. Extends global `~/.claude/CLAUDE.md`.

---

## Core Principles

- **Scope discipline.** Do the minimum necessary to satisfy the task: no speculative refactors, no unrequested features, no exploring more hypotheses than the evidence calls for. `lean-build` and `surgical-patch` are the default posture, not the exception.
- **Test at completion, not per-line.** Implement the full slice/fix first, then run tests once against the complete change. Do not run a test after every single edit.
  - Exception: a failing reproduction test required by `investigate-first` / `debugging-and-error-recovery` *before* writing a fix, and explicit TDD requests.
  - `verify-and-stop` and `verification-before-completion` are the single gating checks before declaring a task done — not a loop run after each change.
  - The full suite can be slow to run mid-task. If it's known or estimated to take longer than 10 minutes, the agent must not run it automatically — ask the user first whether to run it now. If they decline (or don't respond), run only the tests covering the changed/updated code, note in the handoff that the full suite was skipped and why, and let the user run it manually and report the results back.
- **Route once.** Use the table below to pick one agent + skill chain per task. Don't re-route mid-task unless scope genuinely changes.
- **Branch before coding.** Before any file edit, an agent must create and check out a new branch off the current base (`git checkout -b <type>/<short-desc>`, e.g. `fix/login-timeout`, `feat/export-csv`). Never edit or commit on the branch the session started on. Applies to every agent that touches code: `implementer`, `debugger`, `frontend-engineer`, `database-engineer`, `devops-engineer`, `security-auditor`, `test-engineer`, `api-designer`. Read-only agents (`triage`, `planner`, `code-reviewer`, `verifier`, `retro-analyst`, `docs-engineer` when only reading) are exempt unless they start writing files. If already on a non-default, non-protected branch for this task, reuse it instead of branching again. For multi-step work (e.g. `safe-refactor`), commit per logical step on that one branch rather than one giant commit at the end.
- **Escalate before high-risk actions.** Pause and ask the user for confirmation before: changing more than 25 files in one task, deleting or dropping data, force-pushing, or bumping a dependency's major version. Exception: a `safe-refactor` confined to a single module/directory (e.g. a rename or mechanical pattern change) doesn't count toward the file threshold, since interface preservation is already guaranteed — but escalate if that refactor spans multiple modules/services. (Adjust these thresholds in this file if they don't fit your workflow.)

---

## Routing Table

| Task Type | Agent | Skill Chain |
|---|---|---|
| Vague idea / brainstorming | `planner` | product-thinking → planning-and-task-breakdown → grilling → graphify → codegraph → dev-craft |
| Spec files (xlsx/csv/md/pdf) | `planner` | project-discovery → planning-and-task-breakdown → grilling → graphify → codegraph → dev-craft |
| New feature / project | `implementer` | planning-and-task-breakdown → lean-build → dev-craft → codegraph |
| Bug / failing test | `debugger` | investigate-first → codegraph → graphify → debugging-and-error-recovery → surgical-patch → verification-before-completion |
| Refactoring (behavior-preserving) | `debugger` / `implementer` | investigate-first → graphify → codegraph → safe-refactor → verification-before-completion |
| Migration (schema, API, deps) | `database-engineer` / `devops-engineer` | migration → graphify → codegraph → dev-craft → verification-before-completion |
| Dependency upgrade (minor/patch, no schema/API change) | `implementer` / `devops-engineer` | dev-craft → verification-before-completion |
| Revert / rollback a change | `implementer` | investigate-first → surgical-patch → verification-before-completion |
| Frontend / UI work | `frontend-engineer` | prompt-optimizer (pre-routing) → ui-craft → playwright-skill → verification-before-completion |
| Screenshot / image reference | `frontend-engineer` | prompt-optimizer (pre-routing) → image-to-design-spec → ui-craft |
| Create a diagram | `frontend-engineer` / `planner` | diagram-design |
| Code review | `code-reviewer` | caveman-explore → graphify → codegraph → code-review-and-quality → caveman-review → verification-before-completion |
| Security audit | `security-auditor` | prompt-optimizer (pre-routing) → investigate-first → graphify → codegraph → bug-hunting → verification-before-completion |
| API design / contract change | `api-designer` | prompt-optimizer (pre-routing) → api-design → graphify → codegraph |
| Writing / adding tests | `test-engineer` | prompt-optimizer (pre-routing) → testing-strategies → surgical-patch |
| Documentation | `docs-engineer` | prompt-optimizer (pre-routing) → documentation-engineering |
| Retrospective / postmortem | `retro-analyst` | prompt-optimizer (pre-routing) → retro → learn |
| Validation / "done" check (incl. claims of "done") | `verifier` | prompt-optimizer (pre-routing) → verify-and-stop → verification-before-completion |
| Merge / PR-ready check | `verifier` | verify-and-stop → verification-before-completion (confirms rebased on base, no conflicts, CI/tests green) |
| Commit message | `implementer` | caveman-commit (auto-triggers on staging) |
| Find a skill for X | `triage` | find-skills |
| Infra / IaC / deploy | `devops-engineer` | prompt-optimizer (pre-routing) → dev-craft → devops-automation → verification-before-completion |
| Large multi-module work | `orchestrator` | dev-craft + agent-orchestration + graphify + codegraph |
| Multiple independent tasks | `orchestrator` | dispatching-parallel-agents |

`triage`, `planner`, and `orchestrator` route; all others execute. `Strategy` per agent (Fast/Reasoning/Coding/Visual/High-Quality/Standard) is implicit in its skill chain above — no separate registry needed.

---

## Environment & Cost

- **OS detection:** `uname -s` / `$OSTYPE`. Linux/POSIX → standard Bash. Windows → Git Bash/Mintty with POSIX syntax; avoid native `CMD`/`PowerShell`.
- **Cross-platform:** relative paths, `/` separators, `$VAR`, `npx` / `uv run`.
- **prompt-optimizer:** runs pre-routing (20–40% savings) and per-agent (15–30% savings), except for `planner` and `implementer` (they gather requirements natively). Metrics in `.dev-craft/prompt-optimizer-metrics.jsonl`.
- **Context rotation:** Working (4k) → Project (`.dev-craft/`) → Skill → Reference → Handoff. Rotate at 70% capacity via `state.json`.

---

## Search & Graph Protocols

- **Graphify first:** non-code inputs — PDFs, specs, media, system-level dependency maps.
- **CodeGraph first:** code symbols, function definitions, call trees. Check for `.codegraph/`; if present use `codegraph_explore` / `codegraph explore "<symbol>"` before `grep`/`find`. Skip if absent.
- **Combined flow:** Spec/Arch → graphify → codegraph. Trace/Debug → codegraph → graphify.
- **Graphify commands:** `graphify query "<question>"`, `graphify path "<A>" "<B>"`, `graphify explain "<concept>"`, `graphify update .` (run once at task completion — not after every individual file edit). Use `graphify-out/wiki/index.md` to navigate; read `GRAPH_REPORT.md` only for full architecture reviews.

---

## Auto-Triggered Workflow Skills

| Skill | Trigger | Policy |
|---|---|---|
| `branch-before-code` | First file edit of a coding task | Create/check out a new branch off the current base before touching any file; skip only if already on a dedicated non-default branch for this task. |
| `playwright-skill` | UI change in `src/`, `components/`, `pages/`, `app/` | Start local dev server, navigate the modified route, run interaction checks once change is complete, verify no console errors. On large apps, scope checks to the modified route(s) rather than a full site crawl unless asked. |
| `graphify` | Pre-refactor, bug investigation, cross-domain spec matching | Build/query proactively, no explicit prompt needed. On large repos where a full rebuild is slow, ask before rebuilding and prefer `graphify query`/`update .` scoped to the changed area. |
| `caveman` | "be brief" / "caveman mode" / `/caveman` | Ultra-concise output; reverts to normal prose for security warnings or critical confirmations. |
| `caveman-commit` | Staged changes or commit request | Conventional commit, subject ≤50 chars. Does not run `git commit`. |
| `caveman-review` | PR review or `/caveman-review` | One-line comments: `L<line>: <severity>: <problem>. <fix>.` |
| `caveman-explore` | Cold-start exploration when the relevant file/symbol location is unknown | Read-only haiku search; compact `path:line` citations. Once the location is found, hand off to `investigate-first` — don't run both on the same question. |
| `find-skills` | "find a skill for X" | Query `skills.sh`/`npx skills find`, validate install count >1k, confirm before install. |
| `diagram-design` | Requests for charts, sequence/ER diagrams | Check `references/style-guide.md`; output self-contained HTML, max 9 nodes. |
| `investigate-first` | Ambiguous bug or perf regression | Separate symptom from root cause; rank hypotheses by evidence before editing. |
| `lean-build` | Scope-heavy feature work | Minimal viable slice against observable criteria; no unneeded config/polish. |
| `surgical-patch` | Targeted bug fix | Narrowest fix + regression proof; no unrelated cleanup. |
| `safe-refactor` | Structural refactor | Preserve public interfaces/behavior; verify before structural edits. |
| `migration` | DB/API/dependency migration | expand → migrate → verify → contract; preserve data; include rollback. |
| `verify-and-stop` | "is this done?" | Minimal sufficient proof set; zero product-code edits unless a fix is requested. |
| `cavecrew` | "delegate to subagent" | Sub-tasks: `investigator` (search), `builder` (≤2 file edit), `reviewer` (diff check). |

---

## Manual Operator Commands

| Command | Action |
|---|---|
| "set up caveman" | Connect repo to Caveman Cloud for spend tracking. |
| "caveman learn" / "lower token cost" | Review usage hotspots; apply cost-reduction edits with consent. |
| "discover workflows" | Label repo LLM workflows for analytics grouping. |
| "what did Caveman find" | Read-only cost/trace/optimization report. |
| "inspect optimization" | Evaluate candidate vs. baseline changes. |
| "start/approve/cancel experiment" | Manage eval-gated experiment lifecycle. |
| `/caveman-compress <file>` | Compress `.md`/`.txt`/`.typ` to caveman format, with backup. |
| `/caveman-stats` | Session token usage and estimated savings. |
| `/caveman-help` | Reference card for all caveman skills/modes. |
