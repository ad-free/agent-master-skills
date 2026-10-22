# Contract Lifecycle & Sync Gates (folded from `agent-orchestration`)

## Contract lifecycle

1. **Define** — Master writes `api-contract.md` (OpenAPI YAML content allowed;
   canonical filename stays `api-contract.md`).
2. **Review** — Master validates schema correctness, completeness.
3. **Commit** — On the feature branch(es); in `contractRepo` (BE repo) for `multi`.
4. **Distribute** — Workers fetch and reference it. Never two drifting copies.
5. **Freeze** — Frozen during implementation; changes require master approval.
6. **Iterate** — Master updates, all workers sync explicitly.

## Contract change protocol

```
Worker identifies gap ──► Reports to master ──► Master evaluates impact
        ┌─────────────────────┴─────────────────────┐
     Accept                                      Reject
        │                                            │
  Master updates contract,                  Worker works around
  alerts all workers                         or negotiates
```

| Rule | Rationale |
|------|-----------|
| Contract is read-only for workers | Prevents accidental contract drift |
| Changes require master approval | Single source of truth |
| Workers pull updates explicitly | No surprise breakage |
| Changes are atomic (single commit) | Workers see exactly what changed |

## Roles

| Role | Responsibility |
|------|---------------|
| **Master** | Owns contract, domain model, integration tests. Analyses requirements, creates workspaces, dispatches workers, runs integration tests, performs merge |
| **Backend** | Implements endpoints/models/middleware from contract in its worktree; runs backend contract tests |
| **Frontend** | Generates API client (`openapi-generator`, `orval`, `tRPC`); builds UI; mocks responses until backend is stable |
| **Mobile** | Generates mobile client; builds screens; uses mock data until backend stabilises |

**Context per worker:** contract path/content, workspace path + branch, layer requirements, shared glossary.
**Skill mapping:** master → `conductor`; backend → `dev-craft`; frontend → `ui-craft`; mobile → `dev-craft`/native.

## Sync gates

**Gate 1 — Contract defined.** Entry: `api-contract.md` committed (in
`contractRepo` for `multi`). Actions: master creates worktrees, pushes contract,
dispatches workers. Exit: all workers confirm contract + task understanding.

**Gate 2 — Backend stable.** Entry: backend endpoints pass contract tests.
Actions: backend exposes staging; frontend/mobile switch from mocks to live
calls. Exit: frontend integration tests pass against real backend.

**Gate 3 — All complete.** Entry: each agent signals completion with passing
tests. Actions: master runs full integration suite, merges, resolves conflicts,
re-runs suite. Exit: integration branch green, ready for `main`.

## Shared-memory convention

Master maintains `.agent-orchestration/` with `state.json`, `contract.yaml`,
`decisions/`, `sessions/` (dir name kept for continuity across existing runs).

## Exit checklist

Load `verification-before-completion` and confirm: all worktrees merged;
integration tests pass; contract finalised on `main`; no stale worktrees;
`.agent-orchestration/` archived/removed; CI green on `main`.

## Gotchas

| Gotcha | Mitigation |
|--------|------------|
| Contract drift (workers edit contract) | Read-only in worker workspaces; CI validates committed version |
| Stale worktrees | `git worktree remove <path>` before deleting branches; periodic `prune` |
| Worktree nesting (unsupported) | Siblings of main repo only |
| Disk usage (full checkout each) | `.git/` shared; remove right after merge |
| Cross-platform paths | `git worktree repair` after moving repo |
