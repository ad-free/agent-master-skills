---
name: agent-orchestration
description: Orchestrate multiple agents working in parallel on the same project. Uses git worktree for isolated workspaces, API contract handoffs, and conflict management.
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
├── ../project-api/        # worktree on api-slice branch
├── ../project-web/        # worktree on web-slice branch
└── ../project-mobile/     # worktree on mobile-slice branch
```

Each worktree shares **git objects** (history, commits) but has **independent** working trees, indexes, and HEAD refs.

### API Contract as Shared Interface

The contract (OpenAPI, Protobuf, or similar) defines:
- Endpoints, methods, and paths
- Request/response schemas
- Error codes and statuses
- Authentication requirements

It lives in the **master agent's worktree** and is consumed (not modified) by worker agents.

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

### Branch Strategy

```
main ──────┬────────────── api-slice ──────────┐
            │                                        │
            ├────────────── web-slice ─────────────┤───► integration
            │                                        │
            ├────────────── mobile-slice ───────────┘
            │
            └─ contract (owned by master agent)
```

- `contract` branch — the API contract definition file(s), owned by master agent
- `api-slice` — backend implementation
- `web-slice` — frontend implementation
- `mobile-slice` — mobile implementation
- `integration` — merge target for all worktrees

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

## Agent Split Pattern

### Master Agent

The master agent is loaded first. It:

1. Analyses the feature requirements
2. Defines the **API contract** (OpenAPI 3.x preferred)
3. Creates worktrees for each worker agent
4. Commits the contract to the `contract` branch
5. Dispatches worker agents with context
6. Runs **integration tests** after all workers complete
7. Performs the integration merge

**Context passed to each worker:**
- The API contract file (path or content)
- The worktree path and branch name
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

1. **Define** — Master writes the contract in `openapi.yaml` (or equivalent)
2. **Review** — Master validates the contract (schema correctness, completeness)
3. **Commit** — Master commits to `contract` branch
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

**Entry criteria:** Master has committed the API contract to the `contract` branch

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

**Mitigation:** The `.git/` directory is shared (not duplicated). Only working tree files are duplicated. Remove worktrees as soon as they are merged.

### Stale Worktrees

**Issue:** Worktrees left behind after branches are deleted. The worktree directory still exists on disk with no corresponding branch.

**Mitigation:** Always run `git worktree remove <path>` before deleting branches. Periodically run `git worktree prune`.

### Contract Drift

**Issue:** Workers accidentally modify the contract file in their worktree, creating subtle incompatibilities.

**Mitigation:** Set the contract file as read-only in worker worktrees. Use CI to validate that the contract in each worktree matches the `contract` branch. Enforce contract change protocol.

### Git Ref Management

**Issue:** Each worktree has its own `HEAD`, `ORIG_HEAD`, `FETCH_HEAD`, etc. Running `git gc` can fail if worktrees reference objects that another worktree needs.

**Mitigation:** Run `git gc` from the main repository only. Use `git worktree list` to verify no stale worktree references exist before garbage collection.

### Worktree Nesting

**Issue:** Creating a worktree inside another worktree is not supported by git. Worktrees must be siblings.

**Mitigation:** Always create worktrees as siblings of the main repository, not nested within another worktree.

### Cross-Platform Path Issues

**Issue:** Git worktree paths are absolute and stored in `.git/worktrees/`. Moving the repository on disk can break worktree references.

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
.project-api/.dev-craft/       # backend agent memory
.project-web/.ui-craft/        # frontend agent memory
.project-mobile/.dev-craft/    # mobile agent memory
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
- [ ] `.agent-orchestration/` state archived or removed
- [ ] CI passes on `main` after merge
