# AGENTS.md — Codex Agent Instructions

Project-level OpenCode configuration. Extends global `~/.config/opencode/AGENTS.md`.

---

## Quick Reference & Routing

| Task Type | Primary Agent | Skill Chain Sequence |
|-----------|---------------|----------------------|
| Vague idea / brainstorming | `planner` | product-thinking → planning-and-task-breakdown → grilling → graphify → codegraph → dev-craft |
| Spec files (xlsx/csv/md/pdf) | `planner` | project-discovery → planning-and-task-breakdown → grilling → graphify → codegraph → dev-craft |
| New feature / project | `implementer` | planning-and-task-breakdown → lean-build → dev-craft → codegraph |
| Bug / failing test | `debugger` | investigate-first → codegraph → graphify → debugging-and-error-recovery → surgical-patch → verification-before-completion |
| Refactoring (behavior-preserving) | `debugger` / `implementer` | investigate-first → graphify → codegraph → safe-refactor → verification-before-completion |
| Migration (reversible) | `database-engineer` / `devops-engineer` | migration → graphify → codegraph → dev-craft → verification-before-completion |
| Frontend / UI work | `frontend-engineer` | prompt-optimizer (pre-routing) → ui-craft → playwright-skill → verification-before-completion |
| Screenshot / image reference | `frontend-engineer` | prompt-optimizer (pre-routing) → image-to-design-spec → ui-craft |
| Create a diagram | `frontend-engineer` / `planner` | diagram-design |
| Code review | `code-reviewer` | caveman-explore → graphify → codegraph → code-review-and-quality → caveman-review → verification-before-completion |
| Security audit | `security-auditor` | prompt-optimizer (pre-routing) → investigate-first → graphify → codegraph → bug-hunting → verification-before-completion |
| Validation / "done" check | `verifier` | verify-and-stop → verification-before-completion |
| Commit message | `implementer` | caveman-commit (auto-triggers on staging) |
| Find a skill for X | `triage` | find-skills |
| Infra / IaC / deploy | `devops-engineer` | prompt-optimizer (pre-routing) → dev-craft → devops-automation → verification-before-completion |
| Large multi-module | `orchestrator` | dev-craft + agent-orchestration + graphify + codegraph |
| Multiple independent tasks | `orchestrator` | dispatching-parallel-agents |
| Claim "done" | `verifier` | prompt-optimizer (pre-routing) → verification-before-completion |

---

## Environment & Cost Optimization

- **OS Auto-Detection:** Detect OS via `uname -s` or `$OSTYPE`.
  - **Linux / POSIX:** Standard POSIX/Bash commands (`ls`, `mkdir -p`, `rm -rf`, `systemctl`).
  - **Windows:** Use Git Bash / Mintty environment with standard POSIX syntax. Avoid native `CMD`/`PowerShell` commands (`dir`, `del`).
- **Cross-Platform CLI:** Use relative paths, `/` path separators, `$VAR` syntax, and `npx` / `uv run` for Node/Python execution.
- **Cost Management:**
  - `prompt-optimizer` runs pre-routing (20-40% savings) and per-agent (15-30% savings). Metrics tracked in `.dev-craft/prompt-optimizer-metrics.jsonl`.
  - **Excluded from prompt-optimizer:** `planner`, `implementer` (gather requirements natively).
- **Context Rotation:** Memory hierarchy: Working (4k) → Project (`.dev-craft/`) → Skill → Reference → Handoff. Rotate at 70% capacity via `state.json`.

---

## Agent Registry

| Agent | Strategy | Domain | Key Skills |
|-------|----------|--------|------------|
| `triage` | Fast / Routing | Routing | prompt-optimizer, agent-router, find-skills, caveman-explore |
| `planner` | Reasoning | Planning | product-thinking, planning-and-task-breakdown, grilling, graphify, codegraph, diagram-design |
| `implementer` | Coding | Implementation | dev-craft, testing-strategies, codegraph, lean-build, safe-refactor, surgical-patch, migration, caveman-commit |
| `debugger` | Reasoning | Debugging | prompt-optimizer, debugging-and-error-recovery, codegraph, graphify, investigate-first, surgical-patch, caveman-explore, caveman-review |
| `code-reviewer` | High-Quality | Review | prompt-optimizer, code-review-and-quality, graphify, codegraph, caveman-explore, caveman-review |
| `frontend-engineer` | Visual | Frontend | prompt-optimizer, ui-craft, dev-craft, playwright-skill, diagram-design |
| `verifier` | Standard | Verification | prompt-optimizer, verification-before-completion, playwright-skill, verify-and-stop |
| `api-designer` | Standard | API | prompt-optimizer, api-design, graphify, codegraph |
| `database-engineer` | Standard | Database | prompt-optimizer, dev-craft, database-migrations, migration, safe-refactor |
| `devops-engineer` | Standard | Infrastructure | prompt-optimizer, dev-craft, devops-automation, migration |
| `security-auditor` | Standard | Security | prompt-optimizer, bug-hunting, graphify, codegraph, investigate-first |
| `test-engineer` | Coding | Testing | prompt-optimizer, testing-strategies, surgical-patch |
| `docs-engineer` | Coding | Docs | prompt-optimizer, documentation-engineering |
| `retro-analyst` | Standard | Analysis | prompt-optimizer, retro, learn |

---

## Search & Graph Synergy Protocols

### Graphify + CodeGraph Synergy
- **Non-code files / Systems (Graphify First):** Use `graphify` for PDF, specs, media, or high-level system dependency maps.
- **Code Symbols / Functions (CodeGraph First):** Use `codegraph` (`codegraph_explore` or CLI) for code files, symbol definitions, and function call trees.
- **Execution:** Spec/Arch → `graphify` → `codegraph`. Trace/Debug → `codegraph` → `graphify`.

### Global Graphify Protocol (`/graphify`)
1. Query via `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"`.
2. Use `graphify-out/wiki/index.md` for navigation.
3. Read `graphify-out/GRAPH_REPORT.md` only for broad architecture reviews.
4. Run `graphify update .` post-code modifications.

### CodeGraph Protocol
- Check for `.codegraph/` root directory. If present, use `codegraph_explore` or CLI `codegraph explore "<symbol>"` before running `grep` or `find`. Skip if directory is absent.

---

## Workflow Auto-Execution Policies

| Skill | Trigger Condition | Execution Policy |
|-------|-------------------|------------------|
| `playwright-skill` | UI code changes in `src/`, `components/`, `pages/`, `app/` | Auto-start local dev server, navigate modified route, run automated interaction checks, verify no console errors. |
| `graphify` | Pre-refactor, bug investigation, cross-domain spec matching | Proactively build/query Knowledge Graphs without waiting for explicit prompt. |
| `caveman` | "be brief", "concise", "caveman mode", `/caveman` | Ultra-concise output. Reverts to normal prose for security warnings or critical confirmations. |
| `caveman-commit` | Staged changes (`git add`) or commit request | Emits conventional commit (subject ≤50 chars). Does not execute `git commit`. |
| `caveman-review` | Pull request reviews or `/caveman-review` | One-line comments: `L<line>: <severity>: <problem>. <fix>.` |
| `caveman-explore` | Cold-start code exploration, missing symbol location | Read-only search using haiku. Returns compact `path:line` citations. |
| `find-skills` | "how do I do X", "find a skill for X" | Queries `skills.sh` / `npx skills find`. Validates install count (>1k). Prompts user before installing. |
| `diagram-design` | Requests for visual charts, sequence/ER diagrams | Gate-checks style guide (`references/style-guide.md`). Outputs self-contained HTML (max 9 nodes). |
| `investigate-first` | Ambiguous bugs or performance regressions | Separate symptoms from root causes; formulate and rank evidence-based hypotheses before editing code. |
| `lean-build` | Scope-heavy feature implementations | Delivers minimal viable slices based on observable criteria; strictly excludes unneeded config/polish. |
| `surgical-patch` | Targeted bug fixes | Applies narrowest layer fix with regression proof. No unrelated cleanup or refactoring. |
| `safe-refactor` | Structural refactoring | Preserves public interfaces and behavior; verifies before structural edits. |
| `migration` | Database, API, or dependency migrations | Sequence: expand → migrate → verify → contract. Preserves existing data; includes rollback paths. |
| `verify-and-stop` | Task completion checks ("is this done?") | Runs minimal sufficient proof set. Makes zero product code edits unless fix requested. |
| `cavecrew` | "delegate to subagent", "use cavecrew" | Delegates sub-tasks: `investigator` (search), `builder` (≤2 file edit), or `reviewer` (diff check). |

---

## Operator-Invoked Commands (Manual Only)

| Skill | Command / Trigger | Action |
|-------|-------------------|--------|
| **caveman-setup** | "set up caveman" | Connects repo to Caveman Cloud gateway for spend tracking. |
| **caveman-learn** | "caveman learn", "lower token cost" | Reviews token usage hotspots; applies cost-reduction edits with consent. |
| **caveman-discover** | "discover workflows" | Labels repo LLM workflows for analytics grouping. |
| **caveman-evidence-review** | "what did Caveman find" | Read-only analysis of costs, traces, and optimization metrics. |
| **caveman-optimize** | "inspect optimization" | Evaluates candidate baseline vs optimization changes. |
| **caveman-manage** | "start experiment", "approve/cancel" | Manages lifecycle for eval-gated experiments. |
| **caveman-compress** | `/caveman-compress <file>` | Compresses `.md`/`.txt`/`.typ` files into caveman format with backup. |
| **caveman-stats** | `/caveman-stats` | Displays session token usage and estimated savings. |
| **caveman-help** | `/caveman-help` | Displays reference card for all caveman skills and modes. |
