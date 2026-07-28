---
name: ship
description: |
  Automated ship workflow: detect base branch, run tests, review diff, bump VERSION, update CHANGELOG,
  commit, push, create PR. Use when asked to "ship", "deploy", "push to main", "create a PR", "merge and push",
  or "get it deployed". Proactively invoke when user says code is ready, asks about deploying, wants to push
  code up, or asks to create a PR. (gstack)
model: deepseek-v4-flash-free
tools: Read, Write, Edit, Bash, Grep, Glob, Agent, AskUserQuestion
preamble-tier: 4
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
triggers:
  - "ship it"
  - "create a pr"
  - "push to main"
  - "deploy this"
  - "merge and push"
  - "get it deployed"
metadata:
  origin: agent-master-skills
  source: gstack ship skill
  sensitive: true
  preferred-model: big-pickle
---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Ship: Fully Automated Ship Workflow

You are running the `/ship` workflow. This is a **non-interactive, fully automated** workflow. Do NOT ask for confirmation at any step. The user said `/ship` which means DO IT. Run straight through and output the PR URL at the end.

**Only stop for:**
- On the base branch (abort)
- Merge conflicts that can't be auto-resolved (stop, show conflicts)
- In-branch test failures (pre-existing failures are triaged, not auto-blocking)
- Pre-landing review finds ASK items that need user judgment
- MINOR or MAJOR version bump needed (ask — see Step 12)
- Greptile review comments that need user decision (complex fixes, false positives)
- AI-assessed coverage below minimum threshold (hard gate with user override — see Step 7)
- Plan items NOT DONE with no user override (see Step 8)
- Plan verification failures (see Step 8.1)
- TODOS.md missing and user wants to create one (ask — see Step 14)
- TODOS.md disorganized and user wants to reorganize (ask — see Step 14)

---

## Step 1: Base Branch Guard

```bash
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" =~ ^(main|master|develop)$ ]]; then
  echo "ERROR: On protected branch $CURRENT_BRANCH. Create feature branch first."
  exit 1
fi
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
```

---

## Step 2: Sync with Base

```bash
git fetch origin
git merge "origin/$BASE_BRANCH" --no-edit || {
  echo "Merge conflicts detected. Auto-resolving..."
  # Try auto-resolve for simple cases
  git merge --abort
  # If can't auto-resolve, STOP and show conflicts
}
```

---

## Step 3: Run Test Suite

```bash
# Detect test command
if [[ -f package.json ]]; then
  npm test
elif [[ -f pytest.ini ]] || [[ -f pyproject.toml ]]; then
  pytest
elif [[ -f go.mod ]]; then
  go test ./...
elif [[ -f Cargo.toml ]]; then
  cargo test
else
  echo "No test config found. Skipping tests."
fi
```

**Gate:** All tests must pass. If pre-existing failures (known flaky), document and continue. New failures = STOP.

---

## Step 4: Lint & Typecheck

```bash
# Lint
if [[ -f package.json ]] && grep -q '"lint"' package.json; then
  npm run lint
elif [[ -f .ruff.toml ]] || [[ -f pyproject.toml ]]; then
  ruff check .
elif [[ -f go.mod ]]; then
  golangci-lint run
fi

# Typecheck
if [[ -f package.json ]] && grep -q '"typecheck"\|"tsc"' package.json; then
  npm run typecheck
elif [[ -f pyproject.toml ]] && grep -q "pyright\|mypy" pyproject.toml; then
  pyright || mypy .
fi
```

**Gate:** 0 errors. Warnings allowed but reported.

---

## Step 5: Pre-Landing Code Review (Agent)

Invoke `code-reviewer` agent on the diff:

```bash
git diff origin/$BASE_BRANCH...HEAD > /tmp/ship-diff.patch
# Feed to code-reviewer agent
```

**Review checks:**
- Security (CRITICAL): secrets, SQLi, XSS, path traversal, CSRF, auth bypass, vulnerable deps, log leakage
- Code Quality (HIGH): large functions/files, deep nesting, error handling, mutation, console.log, missing tests, dead code
- React/Next.js (HIGH): deps arrays, render state updates, keys, prop drilling, re-renders, server/client boundary, loading/error, stale closures
- Backend (HIGH): unvalidated input, rate limiting, unbounded queries, N+1, missing timeouts, error leakage, CORS
- Performance (MEDIUM): algorithms, re-renders, bundle size, caching, images, sync I/O
- Best Practices (LOW): TODOs, JSDoc, naming, magic numbers, formatting

**Output:** Review summary with verdict (APPROVE / WARNING / BLOCK)

**Gate:** CRITICAL = BLOCK. HIGH = WARNING (user override allowed). If BLOCK → STOP.

---

## Step 6: Security Scan (Automated)

```bash
# Secrets
gitleaks detect --source . --verbose || true
trufflehog filesystem . --no-verification || true

# Dependencies
npm audit --audit-level=high || pip-audit || govulncheck ./...
```

**Gate:** 0 CRITICAL findings. HIGH = WARNING.

---

## Step 7: Coverage Check

```bash
# Run with coverage
npm test -- --coverage || pytest --cov || go test -coverprofile=coverage.out ./...

# Check thresholds
# Minimum: 80% unit, 60% overall (configurable via .ship-coverage.json)
```

**Gate:** Below threshold = HARD STOP with user override prompt:
> "Coverage at 72% (target 80%). Override? (y/n)"

---

## Step 8: Plan Verification

Read `.dev-craft/runs/<slug>/state.json` and `PLAN.md`:

- All G1 slices for this feature: DONE?
- Any deferred requirements acknowledged?
- Coverage gaps resolved?

**Gate:** Incomplete G1 work = STOP (unless user explicitly overrides).

---

## Step 9: Version Bump

```bash
# Read current version
CURRENT_VERSION=$(cat VERSION 2>/dev/null || cat package.json | jq -r .version 2>/dev/null || echo "0.0.0")

# Determine bump type from conventional commits since last tag
# feat → MINOR, fix → PATCH, BREAKING CHANGE → MAJOR
# If MAJOR/MINOR → ASK USER
```

**Prompt for MAJOR/MINOR:**
> "Commits include breaking changes/features. Bump to v{X.Y.0} (MAJOR) or v{X.(Y+1).0} (MINOR)? Current: v{CURRENT_VERSION}. Reply: major/minor/patch/skip"

---

## Step 10: Update CHANGELOG

```bash
# Generate changelog entry from conventional commits since last tag
# Format: Keep a Changelog / SemVer
# Prepend to CHANGELOG.md
```

---

## Step 11: Commit & Push

```bash
git add -A
git commit -m "chore(release): v$NEW_VERSION

$(git log --oneline --pretty=format:'- %s' HEAD~20..HEAD | grep -E '^(feat|fix|perf|refactor|docs|chore)')
" || true

git push origin HEAD
```

---

## Step 12: Create PR

```bash
# Use GitHub CLI
gh pr create \
  --base "$BASE_BRANCH" \
  --head "$CURRENT_BRANCH" \
  --title "Release v$NEW_VERSION" \
  --body "$(cat CHANGELOG.md | head -100)" \
  --label "release"
```

---

## Step 13: Output Result

```markdown
## 🚢 Ship Complete

**Version:** v$NEW_VERSION
**Branch:** $CURRENT_BRANCH → $BASE_BRANCH
**PR:** $PR_URL

**Gates Passed:**
- [x] Tests
- [x] Lint + Typecheck
- [x] Code Review (VERDICT)
- [x] Security Scan
- [x] Coverage (X%)
- [x] Plan Verification

**Commits in this release:**
- feat: ...
- fix: ...
- chore: ...
```

---

## Error Handling

| Failure Point | Action |
|---------------|--------|
| Base branch merge conflict | STOP, show `git status`, user resolves |
| Test failure (new) | STOP, show output, user fixes |
| Lint/type error | STOP, show output, user fixes |
| Review BLOCK | STOP, show findings, user fixes |
| Security CRITICAL | STOP, rotate secrets, user fixes |
| Coverage below threshold | ASK override |
| Plan items incomplete | ASK override |
| Version bump MAJOR/MINOR | ASK user |
| PR creation fails | Show error, user creates manually |

---

## Integration

- Called by `shipper` agent
- Uses `verification-before-completion` for gates
- Uses `code-review-and-quality` for review
- Uses `quality-gates` for layered validation
- Feeds `learn` with release learnings
- Feeds `retro` with deployment metrics