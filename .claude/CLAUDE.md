# CLAUDE.md — Claude Code Agent Instructions

Cross-project rules for every Claude Code session. Project-level `CLAUDE.md` extends/overrides these.

## Quick Reference

| Task Type | Primary Agent | Skill Chain |
|-----------|---------------|-------------|
| Vague idea / brainstorming | `planner` | product-thinking → planning-and-task-breakdown → dev-craft |
| Spec files (xlsx/csv/md/pdf) | `planner` | project-discovery → planning-and-task-breakdown → dev-craft |
| New feature / project | `implementer` | planning-and-task-breakdown → dev-craft / ui-craft |
| Bug / failing test | `debugger` | prompt-optimizer (pre-routing) → debugging-and-error-recovery → verification-before-completion → prompt-optimizer (per-agent) |
| Frontend / UI work | `frontend-engineer` | prompt-optimizer (pre-routing) → ui-craft → verification-before-completion → prompt-optimizer (per-agent) |
| Screenshot / image reference | `frontend-engineer` | prompt-optimizer (pre-routing) → image-to-design-spec → ui-craft |
| Infra / IaC / deploy | `devops-engineer` | prompt-optimizer (pre-routing) → dev-craft → devops-automation → verification-before-completion → prompt-optimizer (per-agent) |
| Large multi-module | `orchestrator` | dev-craft + agent-orchestration |
| Multiple independent tasks | `orchestrator` | dispatching-parallel-agents |
| Code review | `code-reviewer` | prompt-optimizer (pre-routing) → code-review-and-quality → verification-before-completion → prompt-optimizer (per-agent) |
| Security audit | `security-auditor` | prompt-optimizer (pre-routing) → bug-hunting → verification-before-completion → prompt-optimizer (per-agent) |
| Claim "done" | `verifier` | prompt-optimizer (pre-routing) → verification-before-completion (mandatory) → prompt-optimizer (per-agent) |

---

## Core Principles (Iron Laws)

1. **Plan before code** — No implementation without written, approved plan
2. **Evidence before done** — Fresh lint/type/test output required, never assume from memory
3. **Root cause fixes** — Patch causes, not symptoms
4. **Quality gates** — No merge without green lint, typecheck, tests
5. **Self-review required** — No code shipped without review evidence
6. **Contract for parallel work** — Verified independence + written contract
7. **Active security probing** — Assumption ≠ verification
8. **Never weaken tests** — Flag suspect tests, wait for decision
9. **Confirm APIs exist** — Check docs/CLI/live version before calling
10. **Reuse before create** — Check existing types/helpers/components first (Ponytail plugin)
11. **Python via uv only** — `uv run pytest`, `uv run python script.py`; bare python/pip forbidden
12. **Project-scoped inspection** — Depth ≤ 3, Glob/Grep/CodeGraph only
13. **Latest stable versions** — No hardcoded/deprecated major versions
14. **Explicit approval for destructive actions** — Show diff/plan first

---

## Operating Principles

- **Plan → Code → Verify** — Lint → typecheck → test in order, read actual output
- **Read before edit** — Match existing naming, structure, conventions
- **Minimal footprint** — Diff-only edits, one concern per change
- **Lean context** — Glob/Grep/CodeGraph over full reads; delegate to explore agent
- **Ambiguity handling** — Small gap: assume inline. Large gap: ask one question
- **Resume sessions** — Check `.dev-craft/`, `.ui-craft/`, `PLAN.md`, `git log`
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

## Git & Infra Safety

- No commit/push/amend/PR without explicit instruction
- Inspect `git status` / `git diff` before staging; never commit secrets/.env
- Infra changes: show `terraform plan` / `kubectl diff` / migration preview; confirm env + rollback; never auto-apply
- Destructive actions (`rm -rf`, DB drops, bulk resets, cloud deletion) → explicit approval

---

## Project-Specific: agent-master-skills

### Agent Registry

| Agent | Model | Domain | Key Skills |
|-------|-------|--------|------------|
| `triage` | deepseek-v4-flash-free | routing | prompt-optimizer (pre-routing), agent-router |
| `planner` | deepseek-v4-flash-free | planning | product-thinking, planning-and-task-breakdown, grilling |
| `implementer` | big-pickle | implementation | dev-craft, testing-strategies |
| `debugger` | deepseek-v4-flash-free | debugging | prompt-optimizer (per-agent), debugging-and-error-recovery |
| `code-reviewer` | big-pickle | review | prompt-optimizer (per-agent), code-review-and-quality |
| `verifier` | deepseek-v4-flash-free | verification | prompt-optimizer (per-agent), verification-before-completion |
| `frontend-engineer` | big-pickle | frontend | prompt-optimizer (per-agent), ui-craft, dev-craft |
| `api-designer` | deepseek-v4-flash-free | api-design | prompt-optimizer (per-agent), api-design |
| `database-engineer` | deepseek-v4-flash-free | data | prompt-optimizer (per-agent), dev-craft, database-migrations |
| `devops-engineer` | deepseek-v4-flash-free | infrastructure | prompt-optimizer (per-agent), devops-automation |
| `security-auditor` | deepseek-v4-flash-free | security | prompt-optimizer (per-agent), bug-hunting |
| `test-engineer` | big-pickle | testing | prompt-optimizer (per-agent), testing-strategies |
| `docs-engineer` | big-pickle | documentation | prompt-optimizer (per-agent), documentation-engineering |
| `retro-analyst` | deepseek-v4-flash-free | analysis | prompt-optimizer (per-agent), retro, learn |

### Skill Chains

**Pre-routing (runs on ALL requests):**
```
prompt-optimizer (pipeline mode) → triage/agent-router → routes to agent
```

**Per-agent (runs in agent's skill chain for specialized agents):**

```
Feature (vague):    product-thinking → planning-and-task-breakdown → grilling → dev-craft
                    → (per slice) code-review-and-quality → verification-before-completion
                    → verification-before-completion → ship → learn
                    → (per-agent: code-reviewer, verifier use prompt-optimizer)

Feature (specs):    project-discovery → planning-and-task-breakdown → grilling → dev-craft
                    → (per slice) ...
                    → (per-agent: code-reviewer, verifier use prompt-optimizer)

Bug fix:            debugging-and-error-recovery → implementer → verification-before-completion
                    → (per-agent: debugger uses prompt-optimizer)

Code review:        code-review-and-quality → verification-before-completion → verification-before-completion
                    → (per-agent: code-reviewer uses prompt-optimizer)

Security audit:     bug-hunting → code-review-and-quality → verification-before-completion → verification-before-completion
                    → (per-agent: security-auditor uses prompt-optimizer)

Deployment:         ship → verification-before-completion → verification-before-completion → learn
                    → (per-agent: shipper uses prompt-optimizer)

Retrospective:      retro → learn
                    → (per-agent: retro-analyst uses prompt-optimizer)
```

**Agents NOT using prompt-optimizer:** `planner`, `implementer` — their skills (`product-thinking`, `planning-and-task-breakdown`, `dev-craft`) handle requirement gathering directly.

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