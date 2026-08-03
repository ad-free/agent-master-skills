---
name: ship
description: Ship workflow — verify → bump version → changelog → commit → push → PR
triggers:
  - "ship this"
  - "deploy"
  - "push to main"
  - "create PR"
  - "merge and push"
---

# /ship — Ship Workflow

## When to Use
- Feature complete and ready to deploy
- Creating a PR for review
- Pushing to main branch
- Releasing a version

## Prerequisites
- All quality gates pass (`/review`)
- Tests pass
- No uncommitted secrets or .env files

## Workflow

### 1. Final Verification
```
skill("verification-before-completion")  # Fresh evidence
```

### 2. Ship Execution
```
skill("ship")  # Detect base branch, run tests, review diff, bump VERSION, update CHANGELOG, commit, push, create PR
```

### 3. Post-Ship
- Verify CI/CD passes
- Monitor deployment (if applicable)
- Update documentation (`/document-release`)

## Output
- PR/merge created
- Version bumped
- CHANGELOG updated
- Deployment triggered (if configured)

## Completion
**DONE** — Shipped, PR created/merged, deployment verified
**DONE_WITH_CONCERNS** — Shipped but [monitoring/deployment issue]
**BLOCKED** — CI failed, tests broken, or merge conflict
**NEEDS_CONTEXT** — Need [target environment/approval/credentials]