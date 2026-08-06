# CLAUDE.md — Claude Code Agent Instructions

Cross-project rules for every Claude Code session. Project-level `CLAUDE.md` extends/overrides these.

## Quick Reference

| Task Type | Primary Agent | Skill Chain |
|-----------|---------------|-------------|
| Vague idea / brainstorming | `planner` | product-thinking → planning-and-task-breakdown → dev-craft → graphify → codegraph |
| Spec files (xlsx/csv/md/pdf) | `planner` | project-discovery → planning-and-task-breakdown → dev-craft → graphify → codegraph |
| New feature / project | `implementer` | planning-and-task-breakdown → dev-craft / ui-craft → codegraph |
| Bug / failing test | `debugger` | prompt-optimizer (pre-routing) → codegraph → graphify → debugging-and-error-recovery → verification-before-completion → prompt-optimizer (per-agent) |
Frontend / UI work:  prompt-optimizer (pre-routing) → ui-craft → playwright-skill → verification-before-completion → prompt-optimizer (per-agent) |
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

--

## Core Principles (Iron Laws)

1. **Plan before code** — No implementation without written, approved plan
2. **Evidence before done** — Fresh lint/type/test/E2E browser output required, never assume from memory
3. **Root cause fixes** — Patch causes, not symptoms
4. **Quality gates** — No merge without green lint, typecheck, tests
5. **Self-review required** — No code shipped without review evidence
6. **Contract for parallel work** — Verified independence + written contract
7. **Active security probing** — Assumption ≠ verification
8. **Never weaken tests** — Flag suspect tests, wait for decision
9. **Confirm APIs exist** — Check docs/CLI/live version before calling
10. **Reuse before create** — Check existing types/helpers/components first (Ponytail plugin)
11. **Python via uv only** — `uv run pytest`, `uv run python script.py`; bare python/pip forbidden
12. **Project-scoped inspection** — Depth ≤ 3, Glob/Grep/CodeGraph/Graphify
13. **Latest stable versions** — No hardcoded/deprecated major versions
14. **Explicit approval for destructive actions** — Show diff/plan first
15. **Frontend Auto-Validation** — Any frontend edit MUST be verified live in-browser using `playwright-skill` before completion

---

## Operating Principles

- **Plan → Code → Verify** — Lint → typecheck → test in order, read actual output
- **Read before edit** — Match existing naming, structure, conventions
- **Minimal footprint** — Diff-only edits, one concern per change
- **Dual-Skill Code Inspection (Graphify + CodeGraph)** —
  - **Graphify:** Cross-modal knowledge graph (Specs + Code + Media). Auto-invoke for system architecture mapping, spec-to-code alignment, and high-level dependency analysis.
  - **CodeGraph:** Code-level symbol graph. Must use `codegraph_explore` or `codegraph explore` BEFORE grep/find when locating code definitions or tracing exact function call paths.
  - **Synergy Strategy:** High-level scoping via Graphify → Exact symbol tracing via CodeGraph.
- **Ambiguity handling** — Small gap: assume inline. Large gap: ask one question
- **Resume sessions** — Check `.dev-craft/`, `.ui-craft/`, `PLAN.md`, `git log`, `.graphify/`, `.codegraph/`
- **Readable code** — Self-documenting names, comments explain *why*, no dense one-liners

---

## Definition of Done (All Required)

- [ ] Lint, type-check, tests pass — output shown
- [ ] No tests weakened/skipped/deleted to force pass
- [ ] Change addresses request; no unrelated regressions
- [ ] Edge cases handled (null/empty/boundary)
- [ ] Clean style: no cryptic names, consistent imports, one concern
- [ ] Self-review complete (`code-review-and-quality`) — no open issues
- [ ] No stray TODO/FIXME uncaptured in issue
- [ ] Frontend changes verified in live browser via `playwright-skill` (screenshots/interaction pass)

---

## Escalation Guide

**Ask first when:**
- Genuinely ambiguous direction
- Trade-off user should own (perf vs readability, speed vs correctness)
- Large/irreversible action (deletions, migrations, API changes, merges, deploys)
- Root cause unclear after 2 rounds — escalate with ruled-out items

**Proceed when:**
- Obvious low-risk default — state it and move on
- Established pattern in codebase
- Asking costs more than trying + verifying

**Rule:** Wrong guess > 5 min to unwind → ask first

---

## Multi-Agent Work

**Parallel tasks** (`dispatching-parallel-agents`): shared contract (data shapes, file ownership) before dispatch; no overlapping edits; join and verify consistency.

**Multi-module** (`agent-orchestration`): DAG order, stages, written handoff summaries — never silent.

**Error recovery** (`debugging-and-error-recovery`): capture context → reproduce → narrow to root cause → fix cause → regression test. Stuck after 2 rounds → escalate with ruled-out items.

---

##  Playwright Skill Integration

- **Auto-Invocation Trigger:** Agents MUST NOT claim frontend tasks are complete without running `playwright-skill`.
- **Workflow:** Code Generation → Dev Server Launch/Check → Playwright Browser Execution → Assert UI/Console State → Self-Review.

---

## Git & Infra Safety

- No commit/push/amend/PR without explicit instruction
- Inspect `git status` / `git diff` before staging; never commit secrets/.env
- Infra changes: show `terraform plan` / `kubectl diff` / migration preview; confirm env + rollback; never auto-apply
- Destructive actions (`rm -rf`, DB drops, bulk resets, cloud deletion) → explicit approval

---

## Project-Specific: agent-master-skills

### Agent Registry

| Agent | Tier / Strategy | Domain | Key Skills |
|-------|-----------------|--------|------------|
| `triage` | Fast / Routing | routing | prompt-optimizer (pre-routing), agent-router |
| `planner` | Reasoning | planning | product-thinking, planning-and-task-breakdown, grilling, graphify, codegraph |
| `implementer` | Coding / General | implementation | dev-craft, testing-strategies, codegraph |
| `debugger` | Fast / Reasoning | debugging | prompt-optimizer (per-agent), debugging-and-error-recovery, codegraph, graphify |
| `code-reviewer` | High-Quality | review | prompt-optimizer (per-agent), code-review-and-quality, graphify, codegraph |
| `verifier` | Fast / Standard | verification | prompt-optimizer (per-agent), verification-before-completion |
| `frontend-engineer` | Coding / Visual | frontend | prompt-optimizer (per-agent), ui-craft, dev-craft |
| `api-designer` | Standard | api-design | prompt-optimizer (per-agent), api-design, graphify, codegraph |
| `database-engineer` | Standard | data | prompt-optimizer (per-agent), dev-craft, database-migrations |
| `devops-engineer` | Standard | infrastructure | prompt-optimizer (per-agent), devops-automation |
| `security-auditor` | Standard | security | prompt-optimizer (per-agent), bug-hunting, graphify, codegraph |
| `test-engineer` | Coding | testing | prompt-optimizer (per-agent), testing-strategies |
| `docs-engineer` | Coding | documentation | prompt-optimizer (per-agent), documentation-engineering |
| `retro-analyst` | Standard | analysis | prompt-optimizer (per-agent), retro, learn |

### Skill Chains

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

### Cost Optimization

- **prompt-optimizer** runs at triage (pre-routing, 20-40% savings) and per-agent for specialized agents (15-30% savings)
- **cost-optimizer** tracks savings via `.dev-craft/prompt-optimizer-metrics.jsonl`
- Model routing adjusts complexity thresholds based on optimization savings
- **Agents using prompt-optimizer:** triage, debugger, code-reviewer, verifier, api-designer, frontend-engineer, database-engineer, devops-engineer, security-auditor, test-engineer, docs-engineer, retro-analyst
- **Agents NOT using prompt-optimizer:** planner, implementer

### Context Management

- Memory hierarchy: Working (4k) → Project (.dev-craft/) → Skill (on-demand) → Reference (external) → Handoff (archival)
- Rotation at 70%: generate handoff, save state.json, resume from latest
- Cross-agent: sliced context per role, shared = API contract + compressed domain

---

## Maintenance

Add one line here for new gotchas/conventions/mistakes. Keep terse and specific.

# Graphify Integration
- **graphify** (`~/.claude/skills/graphify/SKILL.md`) - Convert any input/codebase to Knowledge Graph.
- **Auto-Invocation Mechanism:** Do not rely on manual `/graphify` triggers. Agents automatically invoke `graphify` whenever building/querying knowledge graphs, analyzing change impact, finding cross-module dependencies, or mapping system architecture.

## Global Graphify Routing Rules

When the user types `/graphify` or asks codebase questions, use the global graphify tool protocols before running raw terminal searches or grep.

### Execution Protocols
- For codebase questions, first run `graphify query "<question>"` when `graphify-out/graph.json` exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If `graphify-out/wiki/index.md` exists, use it for broad navigation instead of raw source browsing.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

<!-- CODEGRAPH_START -->
## CodeGraph Integration

In repositories indexed by CodeGraph (a `.codegraph/` directory exists at the repo root), reach for it BEFORE grep/find or reading files when you need to understand or locate code:

- **MCP tool** (when available): `codegraph_explore` answers most code questions in one call — the relevant symbols' verbatim source plus the call paths between them, including dynamic-dispatch hops grep can't follow. Name a file or symbol in the query to read its current line-numbered source. If it's listed but deferred, load it by name via tool search.
- **Shell** (always works): `codegraph explore "<symbol names or question>"` prints the same output.

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing is the user's decision.
<!-- CODEGRAPH_END -->
