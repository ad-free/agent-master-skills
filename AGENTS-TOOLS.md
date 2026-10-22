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
| Vague product idea | `product-thinking` (→ `PRODUCT.md`) | then `dev-craft` |
| Existing spec files (xlsx/csv/md/pdf) | `project-discovery` (→ `DOMAIN.md`) | then `dev-craft` |
| Feature, bug, refactor, migration, schema/API change | `dev-craft` (picks tier and mode) | `debugging-and-error-recovery` when the bug's cause is unknown; `tdd-seam` for test placement; `api-design` for a new or changed API surface |
| Frontend / UI pipeline, redesign, motion | `ui-craft` | `fe-visual-loop` for show-before-build; `image-to-design-spec` for screenshot-led work; `accessibility` |
| Code review | `code-review-and-quality` | `bug-hunting` |
| Security audit | `bug-hunting` | `code-review-and-quality` |
| Completion check outside dev-craft, stored proof | `verification-before-completion` (includes the evidence ledger) | — |
| Ship / PR text | `ship` (user-invoked; prepare only unless the user names commit/push/PR) | `retro` (user-invoked) |
| Long session, handoff, resume | `context-engineering` | — |
| Independent tasks in parallel | `dispatching-parallel-agents` | — |

Anything not in this table (typos, one-line fixes, docs, config) does not need a skill. Do the work on the
short path from `AGENTS.md` §4.

## Planning pipeline: one source of truth

Never run two requirement-to-task pipelines for the same feature.

- If the repo has a `.specify/` directory (Spec Kit) and the feature is substantial, use Spec Kit.
  Inspect the active feature state first (`.specify/feature.json` if present) and resume rather than
  duplicate. Reuse the existing constitution and resolve critical findings before coding. Do not create
  `PRODUCT.md`, `DOMAIN.md`, or `PLAN.md` alongside it.
- Otherwise (the usual case: most projects have no `.specify/`) use the skills chain: `product-thinking` or `project-discovery` →
  `dev-craft` (its plan step covers task breakdown).
- Never initialize Spec Kit, install a workflow, or overwrite managed or uncommitted files without approval.
- Checklist or phase completion does not replace tests or review.

## When to use `dev-craft`

Use it for every non-trivial code change: features, bugs, refactors and cleanup, migrations, architecture
choices, reviews. Its modes (`references/workflow.md` §Modes) scale the process to the task. It absorbed the
former refactor-and-cleanup, database-migrations, backend-patterns and architecture-decision-records skills.
Skip it for typos, one-line fixes, and docs.

## Subagents

Delegate only when the host permits it and the work is independent, a specialist review, or an isolated
workstream. For independent tasks use `dispatching-parallel-agents`; for multi-module builds with a shared
contract and git worktree isolation, follow dev-craft `references/build-extras.md`.

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
