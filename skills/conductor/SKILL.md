---
name: conductor
description: Orchestrates parallel workstreams using git worktrees for isolated execution. Manages shared contracts, dependency ordering, and cross-workstream verification. Use for large features requiring backend+frontend+mobile parallel execution.
version: 1.0.0
triggers:
  - "parallel sprints"
  - "conductor"
  - "worktree"
  - "parallel work"
  - "multi-agent"
metadata:
  origin: agent-master-skills
  ports: gstack/conductor, agent-orchestration
---

# Conductor — Parallel Sprint Orchestration

Orchestrates parallel workstreams using git worktrees for isolated execution.

---

## 1. WORKTREE ISOLATION

Each workstream gets its own git worktree for independent execution.

### Create Worktree
```bash
# Create worktree for backend work
git worktree add ../project-backend -b feat/backend-api

# Create worktree for frontend work
git worktree add ../project-frontend -b feat/frontend-ui

# Create worktree for mobile work
git worktree add ../project-mobile -b feat/mobile-app
```

### List Worktrees
```bash
git worktree list
```

### Remove Worktree
```bash
# After merge
git worktree remove ../project-backend
git branch -d feat/backend-api
```

---

## 2. SHARED CONTRACTS

Before parallel work begins, define shared contracts that all workstreams must follow.

### Contract Types

#### API Contract
```yaml
# contracts/api.yaml
endpoints:
  - path: /api/users
    method: GET
    response:
      - id: string
        name: string
        email: string
  
  - path: /api/users/:id
    method: POST
    body:
      - name: string
        email: string
    response:
      - id: string
        name: string
        email: string
        createdAt: string
```

#### Type Contract
```typescript
// contracts/types.ts
export interface User {
  id: string;
  name: string;
  email: string;
  createdAt: string;
}

export interface CreateUserRequest {
  name: string;
  email: string;
}
```

#### Event Contract
```yaml
# contracts/events.yaml
events:
  - name: user.created
    payload:
      - userId: string
        name: string
        email: string
  
  - name: user.updated
    payload:
      - userId: string
        changes: object
```

---

## 3. DEPENDENCY ORDERING

Order workstreams by dependency (DAG), execute in stages.

### Dependency Graph
```yaml
# contracts/dependencies.yaml
stages:
  - name: stage-1
    workstreams:
      - name: database
        tasks: [schema, migrations]
      
  - name: stage-2
    workstreams:
      - name: backend
        tasks: [api, auth]
        depends_on: [database]
      
  - name: stage-3
    workstreams:
      - name: frontend
        tasks: [ui, components]
        depends_on: [backend]
      - name: mobile
        tasks: [app, screens]
        depends_on: [backend]
```

### Execute by Stage
```bash
# Stage 1: Database
cd ../project-database
# ... implement schema and migrations

# Stage 2: Backend (after database is merged)
cd ../project-backend
# ... implement API and auth

# Stage 3: Frontend + Mobile (parallel, after backend is merged)
cd ../project-frontend  # ... implement UI
cd ../project-mobile    # ... implement app
```

---

## 4. WORKSTREAM HANDOFF

Each workstream hands off a written summary — never a silent handoff.

### Handoff Template
```markdown
# Workstream Handoff: [name]

## Completed
- [ ] Task 1
- [ ] Task 2

## Files Changed
- src/api/users.ts
- src/db/schema.ts

## Contract Implementation
- [x] API contract followed
- [x] Types contract followed
- [ ] Event contract pending

## Tests
- Unit tests: ✅
- Integration tests: ✅
- E2E tests: ⏳

## Known Issues
- None

## Next Steps
- Frontend can consume /api/users endpoint
- Mobile can consume /api/users endpoint
```

---

## 5. PARALLEL EXECUTION

### Backend + Frontend Parallel
```bash
# Backend worktree
cd ../project-backend
git checkout -b feat/backend-api
# ... implement API

# Frontend worktree (parallel)
cd ../project-frontend
git checkout -b feat/frontend-ui
# ... implement UI using API contract
```

### Shared Contract Verification
```bash
# After both workstreams complete
cd ../project

# Verify backend implements contract
grep -r "GET /api/users" src/api/

# Verify frontend consumes contract
grep -r "/api/users" src/api/
```

---

## 6. MERGE STRATEGY

### Sequential Merge (Dependency Order)
```bash
# 1. Merge database first
git checkout main
git merge feat/database

# 2. Merge backend (depends on database)
git checkout main
git merge feat/backend-api

# 3. Merge frontend + mobile (parallel, depend on backend)
git checkout main
git merge feat/frontend-ui
git merge feat/mobile-app
```

### Conflict Resolution
```bash
# If merge conflicts occur
git checkout --conflicts=merge <file>
# Resolve conflicts
git add <file>
git commit -m "merge: resolve conflicts in <file>"
```

---

## 7. VERIFICATION GATES

Each workstream must pass verification before handoff:

1. **Lint**: Code passes linter
2. **Typecheck**: Types are correct
3. **Tests**: All tests pass
4. **Build**: Build succeeds
5. **Contract**: Implements shared contract

### Gate Evidence
```bash
# Capture evidence
npm run lint > .dev-craft/evidence/lint.txt 2>&1
npm run typecheck > .dev-craft/evidence/typecheck.txt 2>&1
npm test > .dev-craft/evidence/test.txt 2>&1
npm run build > .dev-craft/evidence/build.txt 2>&1
```

---

## 8. CONDUCTOR COMMAND

The `/conductor` command orchestrates parallel sprints:

```bash
# Start parallel sprints
/conductor start --workstreams=backend,frontend,mobile

# Check status
/conductor status

# Handoff workstream
/conductor handoff backend

# Merge workstream
/conductor merge backend

# Clean up
/conductor cleanup
```

---

## 9. WORKTREE CLEANUP

After all workstreams are merged:
```bash
# List worktrees
git worktree list

# Remove merged worktrees
git worktree remove ../project-backend
git worktree remove ../project-frontend
git worktree remove ../project-mobile

# Prune stale worktrees
git worktree prune

# Delete merged branches
git branch -d feat/backend-api
git branch -d feat/frontend-ui
git branch -d feat/mobile-app
```

---

## 10. BEST PRACTICES

### Do
- Define shared contracts before parallel work
- Order workstreams by dependency
- Hand off written summaries
- Verify each workstream before handoff
- Merge in dependency order

### Don't
- Start parallel work without contracts
- Skip verification gates
- Merge out of dependency order
- Leave worktrees uncleaned
- Forget to hand off summaries

---

## 11. EXAMPLE WORKFLOW

### Feature: User Authentication

#### Stage 1: Database
```bash
git worktree add ../project-database -b feat/database
cd ../project-database
# Implement schema and migrations
git add . && git commit -m "feat: add user schema"
git push origin feat/database
# Merge to main
```

#### Stage 2: Backend
```bash
git worktree add ../project-backend -b feat/backend
cd ../project-backend
# Implement API using database schema
git add . && git commit -m "feat: add user API"
git push origin feat/backend
# Merge to main
```

#### Stage 3: Frontend + Mobile (Parallel)
```bash
# Frontend
git worktree add ../project-frontend -b feat/frontend
cd ../project-frontend
# Implement UI using API contract
git add . && git commit -m "feat: add user UI"
git push origin feat/frontend

# Mobile (parallel)
git worktree add ../project-mobile -b feat/mobile
cd ../project-mobile
# Implement app using API contract
git add . && git commit -m "feat: add user app"
git push origin feat/mobile
```

#### Stage 4: Merge All
```bash
cd ../project
git merge feat/database
git merge feat/backend
git merge feat/frontend
git merge feat/mobile
```
