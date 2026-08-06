# AGENTS.md — OpenCode Agent Instructions (Project: agent-master-skills)

Project-level OpenCode config. Extends global `~/.config/opencode/AGENTS.md`.

---

## Quick Reference

| Task Type | Primary Agent | Skill Chain |
|-----------|---------------|-------------|
| Vague idea / brainstorming | `planner` | product-thinking → planning-and-task-breakdown → dev-craft → graphify → codegraph |
| Spec files (xlsx/csv/md/pdf) | `planner` | project-discovery → planning-and-task-breakdown → dev-craft → graphify → codegraph |
| New feature / project | `implementer` | planning-and-task-breakdown → dev-craft / ui-craft → codegraph |
| Bug / failing test | `debugger` | prompt-optimizer (pre-routing) → codegraph → graphify → debugging-and-error-recovery → verification-before-completion → prompt-optimizer (per-agent) |
| Frontend / UI work | `frontend-engineer` | prompt-optimizer (pre-routing) → ui-craft → playwright-skill → verification-before-completion → prompt-optimizer (per-agent) |
| Screenshot / image reference | `frontend-engineer` | prompt-optimizer (pre-routing) → image-to-design-spec → ui-craft |
| Infra / IaC / deploy | `devops-engineer` | prompt-optimizer (pre-routing) → dev-craft → devops-automation → verification-before-completion → prompt-optimizer (per-agent) |
| Large multi-module | `orchestrator` | dev-craft + agent-orchestration + graphify + codegraph |
| Multiple independent tasks | `orchestrator` | dispatching-parallel-agents |
| Code review | `code-reviewer` | prompt-optimizer (pre-routing) → graphify → codegraph → code-review-and-quality → verification-before-completion → prompt-optimizer (per-agent) |
| Security audit | `security-auditor` | prompt-optimizer (pre-routing) → graphify → codegraph → bug-hunting → verification-before-completion → prompt-optimizer (per-agent) |
| Claim "done" | `verifier` | prompt-optimizer (pre-routing) → verification-before-completion (mandatory) → prompt-optimizer (per-agent) |

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
| `triage` | Fast / Routing | routing | prompt-optimizer (pre-routing), agent-router |
| `planner` | Reasoning | planning | product-thinking, planning-and-task-breakdown, grilling, graphify, codegraph |
| `implementer` | Coding / General | implementation | dev-craft, testing-strategies, codegraph |
| `debugger` | Fast / Reasoning | debugging | prompt-optimizer (per-agent), debugging-and-error-recovery, codegraph, graphify |
| `code-reviewer` | High-Quality | review | prompt-optimizer (per-agent), code-review-and-quality, graphify, codegraph |
| `frontend-engineer` | Coding / Visual | frontend | prompt-optimizer (per-agent), ui-craft, dev-craft, playwright-skill |
| `verifier` | Fast / Standard | verification | prompt-optimizer (per-agent), verification-before-completion, playwright-skill |
| `api-designer` | Standard | api-design | prompt-optimizer (per-agent), api-design, graphify, codegraph |
| `database-engineer` | Standard | data | prompt-optimizer (per-agent), dev-craft, database-migrations |
| `devops-engineer` | Standard | infrastructure | prompt-optimizer (per-agent), devops-automation |
| `security-auditor` | Standard | security | prompt-optimizer (per-agent), bug-hunting, graphify, codegraph |
| `test-engineer` | Coding | testing | prompt-optimizer (per-agent), testing-strategies |
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
Feature (vague):    product-thinking → planning-and-task-breakdown → grilling → graphify → codegraph → dev-craft
                    → (per slice) code-review-and-quality → verification-before-completion
                    → verification-before-completion → ship → learn
                    → (per-agent: code-reviewer, verifier use prompt-optimizer)

Feature (specs):    project-discovery → planning-and-task-breakdown → grilling → graphify → codegraph → dev-craft
                    → (per slice) ...
                    → (per-agent: code-reviewer, verifier use prompt-optimizer)

Bug fix:            codegraph → graphify → debugging-and-error-recovery → implementer → verification-before-completion
                    → (per-agent: debugger uses prompt-optimizer)

Code review:        graphify → codegraph → code-review-and-quality → verification-before-completion → verification-before-completion
                    → (per-agent: code-reviewer, verifier use prompt-optimizer)

Security audit:     graphify → codegraph → bug-hunting → code-review-and-quality → verification-before-completion → verification-before-completion
                    → (per-agent: security-auditor uses prompt-optimizer)

Deployment:         ship → verification-before-completion → verification-before-completion → learn
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
## CodeGraph Integration

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.
<!-- CODEGRAPH_END -->
