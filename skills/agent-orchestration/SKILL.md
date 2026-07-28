---
name: agent-orchestration
description: |
  Coordinate multiple agents (backend, frontend, mobile) in parallel using git worktrees.
  Use for large features requiring parallel BE/FE/Mobile execution with shared contracts.
  Invoked by: orchestrator agent.
version: 1.1.0
preamble-tier: 3
allowed-tools:
  - Agent
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "orchestrate parallel agents"
  - "run backend and frontend in parallel"
  - "coordinate multiple agents"
  - "split work across agents"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  topology-support: [mono, multi]
  contract-required: true
  integrates-with: [dev-craft, dispatching-parallel-agents]
---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Agent Orchestration

## Overview

Split large features across multiple agents (backend, frontend, mobile) working simultaneously on the same repository. Each agent gets an isolated `git worktree` — an independent working directory with its own branch — eliminating file-level conflicts without sacrificing shared history.

**Core principle:** Parallel development on the same codebase is safe when isolation is enforced by the tool, not by discipline.

## When to Activate

- **Project is large enough for parallel agents** — a single agent would be a bottleneck
- **Backend + Frontend + Mobile split** — three independent slices with a shared API contract
- **Multiple independent features** — features that touch different layers of the stack
- **Team-of-one context switching** — you are the only developer but want to parallelise your own agents
- **Integration risk is high** — long-running branches will conflict; worktrees keep them in sync continuously

**When NOT to use:**
- Task fits in a single PR by one agent
- Agents need to modify the same files (worktrees won't help here)
- No clear shared contract (API, schema, etc.) exists yet

**Topology (mono vs multi):** This skill coordinates agents on a **shared codebase**. Two layouts apply:
- `mono` — one repo containing BE + FE (e.g. `backend/` + `frontend/`). Use `git worktree` isolation below.
- `multi` — separate BE repo and FE repo (two checkouts). `git worktree` cannot span repos, so use **separate clones + paired branches** instead (see Multi-Repo Variant). The shared contract still applies, but lives in the BE repo (`contractRepo`) as `api-contract.md`, aligned with dev-craft's SCOPE gate (§0.2).

This skill's state must align with dev-craft's SCOPE record: read `topology`, `scope`, `mode`, `repos`, `contractRepo`, and `linkedBranches` from the active dev-craft run so agents branch and read the contract consistently.

## The Iron Law

```
NO PARALLEL AGENTS WITHOUT A SHARED CONTRACT
```

Without a defined API contract, agents will build incompatible interfaces. The contract is the synchronization boundary — it must be stable before parallel work begins.

## Core Concepts

### Git Worktree Isolation

A `git worktree` is a separate working directory linked to the same repository. Each worktree can be on a different branch, have its own staged changes, and operate independently.

```
main repository/
├── .git/                  # shared object store
├── src/                   # main checkout (usually main branch)
├── ../        # worktree on api-slice branch
├── ../        # worktree on web-slice branch
└── ../     # worktree on mobile-slice branch
```

Each worktree shares **git objects** (history, commits) but has **independent** working trees, indexes, and HEAD refs.

### API Contract as Shared Interface

The contract (canonical file: `api-contract.md`; OpenAPI YAML content allowed when tooling supports it) defines:
- Endpoints, methods, and paths
- Request/response schemas
- Error codes and statuses
- Authentication requirements

It lives in the **master agent's workspace** and is consumed (not modified) by worker agents. For `mono`, the master keeps it on a `contract`/feature branch; for `multi`, it lives in `contractRepo` (the BE repo) on the paired feature branch — matching dev-craft's SCOPE convention. Do NOT maintain a separate long-lived `contract` branch; the contract travels on the feature branch(es).

### Master/Worker Agent Pattern

| Role | Responsibility |
|------|---------------|
| **Master agent** | Owns API contract, domain model, integration tests. Defines the "what" |
| **Backend agent** | Implements API endpoints, business logic, data layer in its worktree |
| **Frontend agent** | Consumes API contract, builds UI components, generates API client |
| **Mobile agent** | Builds mobile app against the same contract in its worktree |

### Synchronization Points

Synchronization happens at defined **handoff gates**, not continuously:

```
CONTRACT DEFINED ──► ALL AGENTS START
       │
       ▼
BACKEND STABLE ──► FRONTEND INTEGRATION TEST
       │
       ▼
ALL COMPLETE ──► INTEGRATION MERGE
```

## Worktree Setup

### Creating Worktrees

Run from the main repository root:

```bash
# Create worktrees for each agent
git worktree add ../project-api api-slice
git worktree add ../project-web web-slice
git worktree add ../project-mobile mobile-slice
```

Each worktree:
- Lives in a **sibling directory** (e.g., `../project-api` relative to the repo root)
- Is on its own **branch** (`api-slice`, `web-slice`, `mobile-slice`)
- Shares the **same `.git/` object store** — no duplication of history
- Can `push`/`pull` independently

### Branch Strategy (mono)

```
main ──────┬────────────── api-slice ──────────┐
           │                                        │
           ├────────────── web-slice ─────────────┤───► integration
           │                                        │
           ├────────────── mobile-slice ───────────┘
           │
           └─ contract (owned by master agent)
```

- `api-slice` — backend implementation
- `web-slice` — frontend implementation
- `mobile-slice` — mobile implementation
- `integration` — merge target for all worktrees
- The contract (`api-contract.md`) is committed on the feature branch(es), not a separate `contract` branch.

### Listing & Cleaning Worktrees

```bash
# List all worktrees
git worktree list

# Remove a worktree when done
git worktree remove ../project-api
git branch -D api-slice      # remove branch if no longer needed

# Prune stale worktree references
git worktree prune
```

### Multi-Repo Variant (`multi` topology)

When BE and FE are **separate repos**, use **separate clones with paired branches** instead of worktrees:

- **Contract:** `api-contract.md` lives in `contractRepo` (BE repo); FE reads from there. Never two drifting copies.
- **State:** each repo keeps its own `.dev-craft/` / `.ui-craft/`; `linkedBranches` in SCOPE ties them.
- **Integration:** run per-repo suites then contract conformance. Merge/PR each repo's branch; ship together.
- Master agent still owns the contract and integration merge.

The master agent is loaded first. It:

1. Analyses the feature requirements
2. Defines the **API contract** (`api-contract.md`; OpenAPI 3.x content preferred)
3. Creates workspaces for each worker agent (worktrees for `mono`, separate clones for `multi`)
4. Commits the contract on the feature branch(es) — for `multi`, in `contractRepo` (the BE repo)
5. Dispatches worker agents with context
6. Runs **integration tests** after all workers complete
7. Performs the integration merge

**Context passed to each worker:**
- The API contract file (path or content) — for `multi`, the path in `contractRepo` (or mirror)
- The workspace path and branch name (worktree path for `mono`; clone path + branch for `multi`)
- Feature requirements relevant to their layer
- Shared domain glossary

### Backend Agent

1. Checks out its worktree (e.g., `../project-api` on `api-slice`)
2. Reads the API contract from master
3. Implements endpoints, models, middleware, data access
4. Runs backend tests against the contract
5. Signals completion to master

### Frontend Agent

1. Checks out its worktree (e.g., `../project-web` on `web-slice`)
2. Generates API client from the contract (e.g., `openapi-generator`, `orval`, `tRPC`)
3. Builds UI components against the generated client
4. Mocks API responses until backend is stable
5. Runs integration tests against the running backend when available

### Mobile Agent

1. Checks out its worktree (e.g., `../project-mobile` on `mobile-slice`)
2. Generates mobile API client from the contract
3. Builds mobile screens against the contract
4. Uses mock data until backend stabilises

## API Contract Handoff

### Contract as Source of Truth

```
Master defines OpenAPI contract
        │
        ▼
Backend: implements FROM contract
Frontend: generates client FROM contract
Mobile: generates client FROM contract
```

### Contract Lifecycle

1. **Define** — Master writes the contract in `api-contract.md` (OpenAPI YAML content allowed; canonical filename stays `api-contract.md`)
2. **Review** — Master validates the contract (schema correctness, completeness)
3. **Commit** — Master commits the contract on the feature branch(es) (`contractRepo` for `multi`)
4. **Distribute** — Workers fetch and reference the contract
5. **Freeze** — Contract is frozen during implementation; changes require master approval
6. **Iterate** — If contract must change, master updates and all agents sync

### Contract Change Protocol

When a worker discovers the contract needs modification:

```
Worker identifies gap ──► Reports to master
                                │
                    Master evaluates impact
                                │
                    ┌───────────┴───────────┐
                    │                       │
                Accept                  Reject
                    │                       │
            Master updates            Worker works
            contract, alerts          around it or
            all workers               negotiates
```

## Conflict Prevention

### How Worktrees Prevent Conflicts

- **File-level isolation** — worktrees on different branches never compete for the same file
- **Independent indexes** — staging in one worktree doesn't affect another
- **Shared objects** — commits are visible across all worktrees immediately
- **No merge conflicts during development** — conflicts only appear during integration

### Contract Change Discipline

| Rule | Rationale |
|------|-----------|
| Contract is read-only for workers | Prevents accidental contract drift |
| Contract changes require master approval | Maintains single source of truth |
| Workers pull contract updates explicitly | Avoids surprise breaking changes |
| Contract changes are atomic (single commit) | Workers know exactly what changed |

### Integration Merge

When all workers signal completion:

```bash
# From the main repository
git checkout integration

# Merge each worktree branch
git merge api-slice
git merge web-slice
git merge mobile-slice

# Resolve any integration conflicts
# Run full test suite
# If green — merge to main
```

Conflicts during integration are **true conflicts** (not structural noise) and require human review.

## Synchronization Points

### Gate 1: Contract Defined

**Entry criteria:** Master has committed `api-contract.md` on the feature branch(es) (`contractRepo` for `multi`)

**Actions:**
- Master creates all worktrees
- Master pushes the contract branch
- Master dispatches worker agents
- Each worker fetches and checks out their worktree

**Exit criteria:** All workers confirm they have the contract and understand their task

### Gate 2: Backend Stable

**Entry criteria:** Backend agent has running endpoints that pass contract tests

**Actions:**
- Backend deploys to a staging environment or exposes endpoints
- Frontend agent switches from mocks to real backend calls
- Frontend runs integration tests against live backend
- Mobile agent tests against staging endpoints

**Exit criteria:** Frontend integration tests pass against real backend

### Gate 3: All Agents Complete

**Entry criteria:** Each agent signals completion with passing tests

**Actions:**
- Master runs the full integration test suite
- Master performs the integration merge
- Master resolves any merge conflicts
- Master runs final test suite on integration branch

**Exit criteria:** Integration branch passes all tests, ready for `main`

## Gotchas

| Gotcha | Mitigation |
|--------|------------|
| Contract Drift — workers modify the contract file | Set contract read-only in worker workspaces; CI validates against committed version |
| Stale Worktrees — dirs left after branches deleted | `git worktree remove <path>` before deleting branches; periodic `git worktree prune` |
| Worktree Nesting — unsupported inside other worktrees | Always create worktrees as siblings of main repo |
| Disk Usage — full checkout per worktree | `.git/` is shared; remove worktrees as soon as merged |
| Cross-Platform Paths — absolute paths break on repo move | Run `git worktree repair` after moving repo |

## Integration with Other Skills

### Skill Chaining

```
planning-and-task-breakdown
        │
        ▼
agent-orchestration (master agent)
        │
    ┌───┼───────────┐
    │   │           │
    ▼   ▼           ▼
dev-craft     dev-craft    dev-craft or
(backend)    (frontend)   mobile-native
                        (custom skill)
        │
        ▼
verification-before-completion
```

| Agent Role | Loaded Skill |
|------------|-------------|
| Master agent | `agent-orchestration` — orchestrates the entire split |
| Backend agent | `dev-craft` — API, business logic, data layer |
| Frontend agent | `ui-craft` (or `dev-craft` with UI framework) — components, pages, client generation |
| Mobile agent | `dev-craft` or mobile-native skill for (React Native, Flutter, Swift, Kotlin) |

### Shared Memory Convention

Agents share a project-prefix pattern (`.project-api/`, `.project-web/`). Master maintains `.agent-orchestration/` with `state.json`, `contract.yaml`, `decisions/`, and `sessions/`.

### Exit Criteria

Before claiming completion, load `verification-before-completion` and verify:

- [ ] All worktrees merged into integration branch
- [ ] Integration tests pass
- [ ] API contract finalised and committed to `main`
- [ ] No stale worktrees remain
- [ ] `.agent-orchestration/` state archived or removed
- [ ] CI passes on `main` after merge