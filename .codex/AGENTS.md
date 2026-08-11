# AGENTS.md — Codex Agent Instructions

Project-level OpenCode config. Extends global `~/.codex/AGENTS.md`.

---

## Quick Reference

| Task Type | Primary Agent | Skill Chain |
|-----------|---------------|-------------|
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

## Development Environment

- **OS / Shell Adaptability:** Auto-detect OS (`uname -s` or `$OSTYPE`) at session start.
  - **Linux / POSIX Environment:** Use standard POSIX/Bash commands (`ls`, `mkdir -p`, `rm -rf`, `systemctl`, native packages).
  - **Windows Environment:** 
    - Shell: Git Bash / Mintty (POSIX compliant, NOT PowerShell/CMD).
    - Executions: Use standard Bash syntax (`rm -rf`, `mkdir -p`), avoiding Windows-native commands like `dir` or `del`.
- **Cross-Platform CLI Guidelines:**
  - Avoid OS-specific hardcoded paths (e.g., use relative paths or `/` instead of `C:\`).
  - Use `npx` / `uv run` for node and python commands across environments.
  - Environment variables: Use `$VAR` syntax across both platforms.

---

## Agent Registry

| Agent | Tier / Strategy | Domain | Key Skills |
|-------|-----------------|--------|------------|
| `triage` | Fast / Routing | routing | prompt-optimizer (pre-routing), agent-router, find-skills, caveman-explore |
| `planner` | Reasoning | planning | product-thinking, planning-and-task-breakdown, grilling, graphify, codegraph, diagram-design |
| `implementer` | Coding / General | implementation | dev-craft, testing-strategies, codegraph, lean-build, safe-refactor, surgical-patch, migration, caveman-commit |
| `debugger` | Fast / Reasoning | debugging | prompt-optimizer (per-agent), debugging-and-error-recovery, codegraph, graphify, investigate-first, surgical-patch, caveman-explore, caveman-review |
| `code-reviewer` | High-Quality | review | prompt-optimizer (per-agent), code-review-and-quality, graphify, codegraph, caveman-explore, caveman-review |
| `frontend-engineer` | Coding / Visual | frontend | prompt-optimizer (per-agent), ui-craft, dev-craft, playwright-skill, diagram-design |
| `verifier` | Fast / Standard | verification | prompt-optimizer (per-agent), verification-before-completion, playwright-skill, verify-and-stop |
| `api-designer` | Standard | api-design | prompt-optimizer (per-agent), api-design, graphify, codegraph |
| `database-engineer` | Standard | data | prompt-optimizer (per-agent), dev-craft, database-migrations, migration, safe-refactor |
| `devops-engineer` | Standard | infrastructure | prompt-optimizer (per-agent), dev-craft, devops-automation, migration |
| `security-auditor` | Standard | security | prompt-optimizer (per-agent), bug-hunting, graphify, codegraph, investigate-first |
| `test-engineer` | Coding | testing | prompt-optimizer (per-agent), testing-strategies, surgical-patch |
| `docs-engineer` | Coding | documentation | prompt-optimizer (per-agent), documentation-engineering |
| `retro-analyst` | Standard | analysis | prompt-optimizer (per-agent), retro, learn |

---

## Skill Chains

**Pre-routing (runs on ALL requests):**
```
prompt-optimizer (pipeline mode) → triage/agent-router → routes to agent
```

**Per-agent (runs in agent's skill chain for specialized agents):**

```
Feature (vague):    product-thinking → planning-and-task-breakdown → grilling → graphify → codegraph → lean-build → dev-craft
                    → (per slice) code-review-and-quality → verification-before-completion
                    → verification-before-completion → ship → learn
                    → (per-agent: code-reviewer, verifier use prompt-optimizer)

Feature (specs):    project-discovery → planning-and-task-breakdown → grilling → graphify → codegraph → dev-craft
                    → (per slice) ...
                    → (per-agent: code-reviewer, verifier use prompt-optimizer)

Bug fix:            investigate-first → codegraph → graphify → debugging-and-error-recovery → surgical-patch → verification-before-completion
                    → (per-agent: debugger uses prompt-optimizer)

Refactoring:        investigate-first → graphify → codegraph → safe-refactor → verification-before-completion
                    → (per-agent: debugger uses prompt-optimizer)

Migration:          migration → graphify → codegraph → dev-craft → verification-before-completion
                    → (per-agent: implementer, database-engineer, devops-engineer)

Code review:        caveman-explore → graphify → codegraph → code-review-and-quality → caveman-review → verification-before-completion
                    → (per-agent: code-reviewer, verifier use prompt-optimizer)

Security audit:     investigate-first → graphify → codegraph → bug-hunting → code-review-and-quality → verification-before-completion
                    → (per-agent: security-auditor uses prompt-optimizer)

Deployment:         ship → caveman-commit → verification-before-completion → learn
                    → (per-agent: shipper uses prompt-optimizer)

Retrospective:      retro → learn
                    → (per-agent: retro-analyst uses prompt-optimizer)
```

**Agents NOT using prompt-optimizer:** `planner`, `implementer` — their skills (`product-thinking`, `planning-and-task-breakdown`, `dev-craft`) handle requirement gathering directly.

---

## Cost Optimization

- **prompt-optimizer** runs at triage (pre-routing, 20-40% savings) and per-agent for specialized agents (15-30% savings)
- **cost-optimizer** tracks savings via `.dev-craft/prompt-optimizer-metrics.jsonl`
- Model routing adjusts complexity thresholds based on optimization savings
- **Agents using prompt-optimizer:** triage, debugger, code-reviewer, verifier, api-designer, frontend-engineer, database-engineer, devops-engineer, security-auditor, test-engineer, docs-engineer, retro-analyst
- **Agents NOT using prompt-optimizer:** planner, implementer

---

## Context Management

- Memory hierarchy: Working (4k) → Project (.dev-craft/) → Skill (on-demand) → Reference (external) → Handoff (archival)
- Rotation at 70%: generate handoff, save state.json, resume from latest
- Cross-agent: sliced context per role, shared = API contract + compressed domain

---

## Dual-Skill Synergy Rules (Graphify + CodeGraph)

To maximize accuracy and efficiency, combine **Graphify** and **CodeGraph** dynamically:

1. **Architecture & Docs (Graphify first):** Use `graphify` when analyzing non-code files (PDF, spec, docx, media) or building high-level system dependency maps.
2. **Symbol & Call-Path Search (CodeGraph first):** Use `codegraph` (`codegraph_explore` or CLI) when navigating actual code files, exact symbol definitions, dynamic dispatch, or function call trees.
3. **Execution Pipeline:**
   - *Architecture/Spec Tasks:* `graphify` (map boundaries) → `codegraph` (pinpoint exact code lines).
   - *Debugging/Trace Tasks:* `codegraph` (locate bug origin) → `graphify` (assess ripple impact on system).

---

## Playwright Skill Auto-Execution Policy

- **Purpose:** Automatically validate UI rendering, user interaction flows, and client-side logic in a real browser.
- **Trigger Rule:** Whenever code in `src/`, `components/`, `pages/`, `app/`, or any frontend file is created, updated, or refactored:
  1. Detect/start the local development server (e.g., `npm run dev` / `http://localhost:3000`).
  2. Invoke `playwright-skill` to navigate to the modified UI route.
  3. Execute automated interactions (e.g., fill input, click buttons) and capture DOM state/screenshots.
  4. Verify no console errors or visual regressions exist before marking the task complete.

## Graphify Auto-Execution Policy

- **Purpose:** Build and query source code & documentation Knowledge Graphs to deeply understand system relationships.
- **Trigger Principles:** Agents proactively execute the `graphify` skill without awaiting explicit user prompts or `/graphify` commands for:
  1. Impact analysis prior to refactoring or fixing major bugs.
  2. Querying cross-domain relationships (e.g., PDF/Spec files matched against code files).
  3. System-level architecture mapping.

---

## Global Graphify Routing Rules

When the user types `/graphify` or asks codebase questions, use the global graphify tool protocols before running raw terminal searches or grep.

### Execution Protocols
- For codebase questions, first run `graphify query "<question>"` when `graphify-out/graph.json` exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If `graphify-out/wiki/index.md` exists, use it for broad navigation instead of raw source browsing.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

---

<!-- CODEGRAPH_START -->
## CodeGraph

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.
<!-- CODEGRAPH_END -->

---

## Auto-Execution Policies for Caveman & Workflow Skills

The following policies instruct agents to invoke these skills automatically based on context — no explicit mention in the user's prompt is required. All skills live in `~/.agents/skills/` (symlinked into `~/.config/opencode/skills/`) and are discovered by the `skill` tool.

### Caveman Communication Mode (`caveman`)

- **Auto-triggers when** the user requests token efficiency: "be brief", "less tokens", "short version", "brief", "concise", "keep it short".
- **Auto-triggers when** the user says "caveman mode", "talk like caveman", "use caveman", or invokes `/caveman`.
- **Intensity levels** (`full` is default): `/caveman lite`, `/caveman ultra`, `/caveman wenyan-lite`, `/caveman wenyan-full`, `/caveman wenyan-ultra`.
- **Deactivate** by saying "stop caveman" or "normal mode".
- **Boundary:** caveman drops to normal prose for security warnings, irreversible-action confirmations, and multi-step sequences where fragment ambiguity risks misread. Resumes after the clear part. Code blocks, error strings, and technical terms stay verbatim in all modes.

### Caveman Commit Messages (`caveman-commit`)

- **Auto-triggers** when changes are staged for commit (i.e., `git add` detected) or when the user requests a commit message ("write a commit", "commit message", "generate commit", `/commit`).
- Produces ultra-compressed Conventional Commits: subject line ≤50 chars, body only when the "why" isn't obvious.
- Does not run `git commit` — outputs the message ready to paste.

### Code Review with Caveman Compression (`caveman-review`)

- **Auto-triggers** when reviewing a pull request, when the user says "review this PR", "code review", "review the diff", or invokes `/caveman-review`.
- Emits one-line comments: `L<line>: <severity>: <problem>. <fix>.`
- Severity prefixes: `🔴 bug:`, `🟡 risk:`, `🔵 nit:`, `❓ q:`.
- Drops to verbose review for security findings (CVE-class) and architectural disagreements; resumes terse afterward.

### Cold-Start Exploration (`caveman-explore`)

- **Auto-triggers** for cold-start exploration of a new codebase, broad cross-file localization, or when a direct search (grep/glob) has failed and the location of code is unknown.
- **Skip** when the issue already names the exact file or symbol, or when a previous turn returned usable `path:line` evidence.
- Read-only: returns only compact `path:line` citations. Uses a low-cost model (haiku). Its tool calls never enter the main conversation — only the citations do.
- **Synergy:** use `caveman-explore` first to locate code, then `codegraph_explore` for exact symbol/source, then `graphify` for relationship impact analysis.

### Find Skills (`find-skills`)

- **Auto-triggers** when the user asks "how do I do X", "find a skill for X", "is there a skill that can do X", or expresses interest in extending capabilities with a phrase like "I wish I had help with X".
- Checks the [skills.sh leaderboard](https://skills.sh/) first, then searches via `npx skills find`. Verifies install count (1K+ preferred), source reputation, and GitHub stars before recommending.
- Does NOT install skills without explicit user confirmation.

### Diagram Design (`diagram-design`)

- **Auto-triggers** when the user asks to create a visual diagram: architecture diagrams, flowcharts, sequence diagrams, ER/data models, timelines, swimlanes, quadrants, org charts, layer stacks, Gantt charts, data flows, security matrices, etc.
- First-run gate: if the style guide (`references/style-guide.md`) still has default tokens, prompts the user to customize from their website, an installed skill, a local folder, or paste tokens manually before generating.
- Produces self-contained HTML files with inline SVG and CSS, no JavaScript required. Complexity budget enforced (max 9 nodes, 12 arrows, 2 coral accents).
- Does NOT auto-export to PNG/SVG — only when explicitly requested.

### Investigate First (`investigate-first`)

- **Auto-triggers** for ambiguous failures before editing product code: unknown root causes, intermittent behavior, performance regressions, or any investigation needing evidence-ranked hypotheses.
- Workflow: (1) separate observed symptom from inferred cause, (2) trace inputs/state transitions/ownership/failure output, (3) rank hypotheses by evidence and cheap falsification, (4) do not edit until one credible mechanism explains the evidence.
- **Synergy with debugger:** `investigate-first` precedes `codegraph` and `graphify` in the bug-fix chain. `surgical-patch` is the fix step that follows once root cause is confirmed.

### Lean Build (`lean-build`)

- **Auto-triggers** for new feature work where overbuilding risk is high: new behavior, product slices, integrations where repository reuse, strict scope, and an explicit stop condition matter.
- Derives observable acceptance criteria and explicit non-goals from the request and repository. Delivers a coherent end-to-end path across responsible layers. Omits config, providers, modes, and polish unless acceptance requires them.
- **Synergy:** `planning-and-task-breakdown` feeds `lean-build` which feeds `dev-craft` in the `implementer` chain.

### Surgical Patch (`surgical-patch`)

- **Auto-triggers** for bug fixes and small behavior changes where regression proof matters: the narrowest responsible-layer fix with preserved surrounding behavior.
- Reproduces failure first when economical; traces symptom to responsible mechanism; changes only the narrowest layer that owns the incorrect behavior. No cleanup, renaming, or abstraction outside the fix.
- Adds only regression proof relevant to the task. Runs focused proof plus nearest affected gate.
- **Synergy:** `investigate-first` → `codegraph`/`graphify` → `surgical-patch` → `verification-before-completion` is the debugger chain for known bugs.

### Safe Refactor (`safe-refactor`)

- **Auto-triggers** for structural refactoring where behavior preservation is critical: extraction, consolidation, ownership moves, or cleanup that must not change behavior.
- Establishes verification before structural edits. Moves one ownership boundary at a time. Preserves public interfaces, failure behavior, ordering, and compatibility. Keeps intermediate states buildable and testable.
- **Synergy:** `graphify` → `codegraph` → `safe-refactor` → `verification-before-completion` is the refactoring chain.

### Migration (`migration`)

- **Auto-triggers** for schema, data, API, protocol, configuration, or dependency migrations requiring rollback and preservation proof.
- Maps current readers, writers, data shape, compatibility window, and ownership before editing. Defines forward path and rollback path. Preserves existing data; makes destructive steps explicit and separately authorized. Sequences expand → migrate → verify → contract.
- **Synergy:** `migration` → `graphify` → `codegraph` → `dev-craft` → `verification-before-completion` is the migration chain, used by `database-engineer` and `devops-engineer`.

### Verify and Stop (`verify-and-stop`)

- **Auto-triggers** for validation-only tasks: "is this done?", "verify this works", completion checks, focused gate runs, last-mile proof.
- Translates acceptance conditions into the smallest sufficient proof set. Reuses still-current results with matching repository state. Runs focused checks before wider gates. Does NOT edit product code (unless the verification request includes fixes). Does not add polish, cleanup, or unrelated tests after criteria pass.
- **Synergy:** `verify-and-stop` → `verification-before-completion` is the verifier chain for "claim done" scenarios.

### Caveman Subagent Delegation (`cavecrew`)

- **Auto-triggers** when the user says "delegate to subagent", "use cavecrew", "spawn investigator/builder/reviewer", "save context", or "compressed agent output".
- Delegates to `cavecrew-investigator` (locate code, ~60% smaller tool results), `cavecrew-builder` (1–2 file edits), or `cavecrew-reviewer` (diff review) instead of doing the work inline.
- **Decision guide:**
  | Task | Use |
  |---|---|
  | "Where is X defined / what calls Y" | `cavecrew-investigator` |
  | Suggestions / architecture commentary | `Explore` (vanilla) |
  | Surgical edit, ≤2 files, scope obvious | `cavecrew-builder` |
  | New feature / 3+ files / cross-cutting refactor | Main thread |
  | Review diff for bugs | `cavecrew-reviewer` |
  | Deep review with rationale | `Code Reviewer` |

---

## Operator-Invoked Caveman Skills (Manual Triggers)

These skills require explicit user invocation — they do NOT auto-trigger from context:

| Skill | Trigger Phrase | What it does |
|-------|---------------|--------------|
| **caveman-setup** | "set up caveman", paste Caveman setup prompt | Wires a repo through the Caveman Cloud gateway for spend observability (record mode only, no optimization) |
| **caveman-learn** | "caveman learn", "lower token cost", "trim CLAUDE.md" | Reviews ranked token sinks from `caveman learn report`, applies cost-lowering fixes with per-edit consent |
| **caveman-discover** | "discover workflows", paste Caveman discovery prompt | Finds and labels every LLM workflow in the repo for Caveman Cloud spend grouping |
| **caveman-evidence-review** | "what did Caveman find", "where does spend go", "trace review", "why cost changed" | Read-only review of Caveman evidence: costs, Cave Score, Cave Plan, workflows, traces |
| **caveman-optimize** | "inspect optimization", "evaluate candidate change" | Turns Caveman report-only observations into a baseline/candidate evaluation pair; requires explicit approval |
| **caveman-manage** | "start experiment", "approve/cancel/promote/roll back" | Manages eval-gated experiment lifecycle; read-first, blocks unsafe mutations |
| **caveman-compress** | `/caveman-compress <file>`, "compress memory file" | Compresses `.md`/`.txt`/`.typ` memory files into caveman prose, saves backup out-of-tree |
| **caveman-stats** | `/caveman-stats` | Shows real token usage and estimated savings from the session log (hook-injected) |
| **caveman-help** | `/caveman-help`, "caveman help", "what caveman commands" | Reference card of all caveman modes, skills, and commands |
