---
name: agent-orchestration
description: Use when orchestrating multiple agents to work in parallel on the same
  project, enforcing isolation, contracts, and conflict management.
metadata:
  origin: agent-master-skills

---

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
- `mono` — one repo containing BE + FE (e.g. `backend${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` + `frontend${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`). Use `git worktree` isolation below.
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
├── ..${PROJECT_ROOT}/        # worktree on api-slice branch
├── ..${PROJECT_ROOT}/        # worktree on web-slice branch
└── ..${PROJECT_ROOT}/     # worktree on mobile-slice branch
```

Each worktree shares **git objects** (history, commits) but has **independent** working trees, indexes, and HEAD refs.

### API Contract as Shared Interface

The contract (canonical file: `api-contract.md`; OpenAPI YAML content allowed when tooling supports it) defines:
- Endpoints, methods, and paths
- Request${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/response schemas
- Error codes and statuses
- Authentication requirements

It lives in the **master agent's workspace** and is consumed (not modified) by worker agents. For `mono`, the master keeps it on a `contract`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/feature branch; for `multi`, it lives in `contractRepo` (the BE repo) on the paired feature branch — matching dev-craft's SCOPE convention. Do NOT maintain a separate long-lived `contract` branch; the contract travels on the feature branch(es).

### Master${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Worker Agent Pattern

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
git worktree add ..${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/project-api api-slice
git worktree add ..${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/project-web web-slice
git worktree add ..${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/project-mobile mobile-slice
```

Each worktree:
- Lives in a **sibling directory** (e.g., `..${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/project-api` relative to the repo root)
- Is on its own **branch** (`api-slice`, `web-slice`, `mobile-slice`)
- Shares the **same `.git${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` object store** — no duplication of history
- Can `push`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`pull` independently

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
git worktree remove ..${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/project-api
git branch -D api-slice      # remove branch if no longer needed

# Prune stale worktree references
git worktree prune
```

### Multi-Repo Variant (`multi` topology)

When BE and FE are **separate repos**, `git worktree` cannot isolate across them — a worktree shares one `.git${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`. Instead, use **separate clones with paired branches**:

```bash
# Two independent repos; each gets its own feature branch, linked by issue id
cd "$beRepo" && git checkout -b "feat${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fs-user-auth"
cd "$feRepo" && git checkout -b "feat${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fs-user-auth"   # same name = trivial pairing

# OR scope-prefixed names per dev-craft SCOPE §0.2 step 5:
cd "$beRepo" && git checkout -b "feat${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/be-user-auth"
cd "$feRepo" && git checkout -b "feat${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fe-user-auth"
```

Rules for `multi`:
- **Contract:** write `api-contract.md` in `contractRepo` (BE repo by default). The FE repo reads it from there (or a synced mirror copy). Never keep two drifting copies.
- **State:** each repo keeps its own `.dev-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` / `.ui-craft${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` state; the SCOPE record's `linkedBranches` ties them (`{ be: "feat${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/be-user-auth", fe: "feat${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fe-user-auth" }`).
- **Integration:** run per-repo suites, then contract conformance (every FE-called route exists in BE, shapes match, status codes handled). Merge${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/PR each repo's branch; ship both sides together for a fullstack unit.
- The master agent still owns the contract and integration merge — isolation is by clone, not worktree.

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

1. Checks out its worktree (e.g., `..${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/project-api` on `api-slice`)
2. Reads the API contract from master
3. Implements endpoints, models, middleware, data access
4. Runs backend tests against the contract
5. Signals completion to master

### Frontend Agent

1. Checks out its worktree (e.g., `..${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/project-web` on `web-slice`)
2. Generates API client from the contract (e.g., `openapi-generator`, `orval`, `tRPC`)
3. Builds UI components against the generated client
4. Mocks API responses until backend is stable
5. Runs integration tests against the running backend when available

### Mobile Agent

1. Checks out its worktree (e.g., `..${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/project-mobile` on `mobile-slice`)
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

### Worktree Disk Usage

**Issue:** Each worktree is a full checkout of the repository. For large repos with many worktrees, disk usage can grow significantly.

**Mitigation:** The `.git${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` directory is shared (not duplicated). Only working tree files are duplicated. Remove worktrees as soon as they are merged.

### Stale Worktrees

**Issue:** Worktrees left behind after branches are deleted. The worktree directory still exists on disk with no corresponding branch.

**Mitigation:** Always run `git worktree remove <path>` before deleting branches. Periodically run `git worktree prune`.

### Contract Drift

**Issue:** Workers accidentally modify the contract file in their worktree, creating subtle incompatibilities.

**Mitigation:** Set the contract file as read-only in worker workspaces. Use CI to validate that the contract matches the committed `api-contract.md` on the feature branch. Enforce contract change protocol.

### Git Ref Management

**Issue:** Each worktree has its own `HEAD`, `ORIG_HEAD`, `FETCH_HEAD`, etc. Running `git gc` can fail if worktrees reference objects that another worktree needs.

**Mitigation:** Run `git gc` from the main repository only. Use `git worktree list` to verify no stale worktree references exist before garbage collection.

### Worktree Nesting

**Issue:** Creating a worktree inside another worktree is not supported by git. Worktrees must be siblings.

**Mitigation:** Always create worktrees as siblings of the main repository, not nested within another worktree.

### Cross-Platform Path Issues

**Issue:** Git worktree paths are absolute and stored in `.git${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`. Moving the repository on disk can break worktree references.

**Mitigation:** Avoid moving the repository while worktrees exist. If you must move it, run `git worktree repair` afterward.

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

All agents in an orchestration share a common prefix for their memory directories:

```
.project-api${PROJECT_ROOT}/       # backend agent memory
.project-web${PROJECT_ROOT}/        # frontend agent memory
.project-mobile${PROJECT_ROOT}/    # mobile agent memory
```

The master agent maintains a top-level orchestration state:

```
.agent-orchestration/
├── state.json           # overall status of all agents
├── contract.yaml        # canonical API contract
├── decisions/           # ADRs for contract changes
└── sessions/            # handoff docs per agent
```

### Exit Criteria

Before claiming completion, load `verification-before-completion` and verify:

- [ ] All worktrees merged into integration branch
- [ ] Integration tests pass
- [ ] API contract finalised and committed to `main`
- [ ] No stale worktrees remain
- [ ] `.agent-orchestration${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/` state archived or removed
- [ ] CI passes on `main` after merge