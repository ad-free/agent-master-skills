# AGENTS.md — OpenCode Agent Instructions (Project: agent-master-skills)

Project-level OpenCode config. Extends global `~/.config/opencode/AGENTS.md`.

---

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

## Agent Registry

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

---

## Skill Chains

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

## Project-Specific Notes

- **prompt-optimizer** uses **Pipeline Mode** (not chat mode) — outputs structured XML task specs, no "ask user" prompts
- **Pipeline Mode** is default for pre-routing and per-agent; chat mode is opt-in for human-facing prompts
- **Agent profiles** declared in frontmatter `prompt-optimizer-profile` (role, structure, examples, grounding, self-check)