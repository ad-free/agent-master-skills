# AGENTS-TOOLS.md — Skills, Pipelines, and Delegation

Read this only when a task needs skill routing, a planning pipeline, or subagent dispatch.
Skills come from `github.com/ad-free/agent-master-skills`. Use only skills that are actually installed in the
current host. If one is absent, follow the equivalent workflow directly. Honor skills marked
user-invoked-only. Tool-managed behavior (RTK, CodeGraph, Graphify, Ponytail) is described in `AGENTS.md` §5.

## Skill routing

Pick one entry skill, then add others only for the active phase. A role is not an instruction to spawn a
subagent.

| Task | Entry skill | Add only when needed |
|---|---|---|
| Vague product idea | `product-thinking` (→ `PRODUCT.md`) | `planning-and-task-breakdown` |
| Existing spec files (xlsx/csv/md/pdf) | `project-discovery` (→ `DOMAIN.md`) | `planning-and-task-breakdown` |
| Break work into tasks | `planning-and-task-breakdown` (→ `PLAN.md`) | — |
| Multi-file feature | `dev-craft` | `quality-gates` before merge |
| Frontend / UI work | `ui-craft` | `image-to-design-spec` for screenshot-led work |
| Bug / failing test | `debugging-and-error-recovery` | `bug-hunting` if security-relevant |
| Code review | `code-review-and-quality` | `bug-hunting` |
| Security audit | `bug-hunting` | `code-review-and-quality` |
| Pre-merge validation | `quality-gates` | — |
| Completion check | `verification-before-completion` | — |
| Large multi-module build | `agent-orchestration` | `dispatching-parallel-agents` |
| Long sessions, handoffs | `context-engineering` | — |

Anything not in this table (small fixes, refactors, docs, config) does not need a skill. Do the work on the
short path from `AGENTS.md` §4.

## Planning pipeline: one source of truth

Never run two requirement-to-task pipelines for the same feature.

- If the repo has a `.specify/` directory (Spec Kit) and the feature is substantial, use Spec Kit.
  Inspect the active feature state first (`.specify/feature.json` if present) and resume rather than
  duplicate. Reuse the existing constitution and resolve critical findings before coding. Do not create
  `PRODUCT.md`, `DOMAIN.md`, or `PLAN.md` alongside it.
- Otherwise use the skills chain: `product-thinking` or `project-discovery` →
  `planning-and-task-breakdown` → `dev-craft`.
- Never initialize Spec Kit, install a workflow, or overwrite managed or uncommitted files without approval.
- Checklist or phase completion does not replace tests or review.

## When to use `dev-craft`

Use it for multi-file features, new modules, or work that needs design and review phases. Do not use it for
bug fixes, small edits, refactors, or docs. For those, follow `AGENTS.md` §4.

## Subagents

Delegate only when the host permits it and the work is independent, a specialist review, or an isolated
workstream. For independent tasks use `dispatching-parallel-agents`; for multi-module builds use
`agent-orchestration` (shared contract and git worktree isolation).

- **Before dispatch**, define: one goal, minimal context, expected deliverable, file/interface ownership,
  acceptance criteria, read-only vs. may-edit. Use isolated worktrees for parallel writers.
- **Pass:** relevant contract or data shape, symbols/files, acceptance criteria, open questions.
- **Never pass:** the whole conversation, full memory history, full graph reports, unrelated docs.
- **Return format:** Findings/Changes · Evidence (`path:line`) · Risks/Unknowns · Verification.

**Context rotation:** when context grows too large, write a compact handoff (goal, decisions, changed
files, verification, open issues) using `context-engineering`, keep only durable conclusions in memory, and
resume from the handoff plus current repo state. Never carry raw logs, full transcripts, or full graph
reports across rotations.

## Maintenance notes for the agent

- Do not edit marker-fenced sections that CodeGraph, Graphify, or RTK add to instruction files.
- Do not add per-tool usage essays here. Each installed tool already injects its own guidance.
- If a skill named here does not exist in the current host, say so once and continue without it.
