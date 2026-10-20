# BUILD extras (load only when the condition applies)

Load when: 3+ modules or parallel backend/frontend agents (worktree mode), or Large work across repos that needs the
per-repo branch check (BUILD step 0b, SHIP pre-commit). Not needed for a Standard single-repo task.

**Git Worktree Mode (for large/multi-module projects):**

When a project has 3+ modules or needs parallel backend + frontend development, use git worktree isolation:

```bash
git worktree add ../project-api api-slice     # Backend agent
git worktree add ../project-web web-slice      # Frontend agent
git worktree add ../project-mobile mobile-slice # Mobile agent
```

**Workflow:**
1. Define API contract first (OpenAPI spec)
2. Each agent works in its own worktree on its own branch
3. Backend implements API from contract
4. Frontend consumes API contract, builds UI
5. Mobile builds against same contract
6. Master agent merges worktrees via integration branch

**When to use worktree mode:**
- Project has separate backend + frontend
- Multiple developers/agents working simultaneously
- Module count > 5
- Estimated total effort > 2 weeks

**When NOT to use:** Single-module project, solo development, prototype/exploration.

**Cleanup:**
```bash
git worktree list
git worktree remove ../project-api
```

## Branch Verification Script (per-repo, used by BUILD step 0b and SHIP pre-commit)

```bash
STATE="${DEV_CRAFT_STATE:-.dev-craft/state.json}"   # or .dev-craft/runs/<slug>/state.json
REPOS=(".")
# for multi: REPOS=("$beRepo" "$feRepo")

for R in "${REPOS[@]}"; do
  BRANCH="$(jq -r --arg r "$R" '.linkedBranches[$r] // .activeBranch // empty' "$STATE")"
  if [ -z "$BRANCH" ]; then
    BRANCH="<type>/<scope>-<short-description>"
    jq --arg r "$R" --arg b "$BRANCH" '.linkedBranches[$r] = $b' "$STATE" > "$STATE.tmp" \
      && mv "$STATE.tmp" "$STATE"
  fi
  ( cd "$R" && {
    if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
      git checkout "$BRANCH"
    elif [ "$(git branch --show-current)" = "$BRANCH" ]; then
      :
    else
      git checkout -b "$BRANCH"
    fi
    CURRENT="$(git branch --show-current)"
    case "$CURRENT" in
      main|master|develop) echo "ERROR[$R]: still on base branch"; exit 1 ;;
      "")                  echo "ERROR[$R]: detached HEAD"; exit 1 ;;
      "$BRANCH")           echo "OK[$R]: on $BRANCH" ;;
      *)                   echo "ERROR[$R]: on $CURRENT, expected $BRANCH"; exit 1 ;;
    esac
  } )
done
```

Record `activeBranch` / `linkedBranches` in state.json **only after** each branch is confirmed to exist and we are on it.

