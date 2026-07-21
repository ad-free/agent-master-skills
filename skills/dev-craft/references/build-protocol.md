# BUILD — Deep Protocol (TDD Loop, SECURE, MATCH, Worktree)

Deep reference for dev-craft `[5] BUILD`. The main `SKILL.md` states the goal,
branch-isolation rules, and the 9-step per-slice loop skeleton; load this file
only when executing BUILD's per-slice detail so the trees below don't sit in
context during earlier phases.

---

**Step 3 — SECURE: Agent traces what the slice touches, then runs matching checks.**

The agent already knows every file in the slice. Start by reading the slice files to determine which security categories apply, then follow the matching branch:

```
Read the slice's files to determine what it touches:
│
├── AUTH (passwords, sessions, tokens, login, reset)?
│   Read auth code → verify:
│   ├── Passwords hashed with bcrypt/argon2? (cost ≥ 10)
│   ├── Session/JWT in httpOnly cookies, not URL params?
│   ├── JWT signature verified? `alg` restricted to RS256/HS256?
│   ├── Login rate-limited? Account lockout after N failures?
│   └── Password reset token random, single-use, time-limited?
│
├── DATA ACCESS (DB queries, API responses)?
│   Read each query → verify:
│   ├── All queries parameterized (`?`, `$1`, named params)? No string concat?
│   ├── ORM queries accept structured params, not raw SQL?
│   ├── Queries scoped to authenticated user? (`WHERE user_id = ?`)
│   └── List endpoints paginated?
│
├── USER INPUT (forms, params, uploads, headers)?
│   Read input handling → verify:
│   ├── Input validated at boundary (Zod, Pydantic, Joi)?
│   ├── File uploads: type whitelisted? Size limited? Outside web root?
│   ├── User content rendered in HTML? → escaped or safe APIs?
│   └── Any exec/spawn/subprocess with user data? → args array, not shell string
│
├── REGEX (validation, matching, routing)?
│   Read each regex → verify:
│   ├── ReDoS risk: nested quantifiers `(a+)+b`, overlapping `(a|aa)+b`,
│   │   unbounded `(.*a)*`? → rewrite without nesting, use atomic groups
│   ├── Injection: user input embedded in pattern `new RegExp(input)`?
│   │   → escape with re.escape(), never construct from input
│   ├── Anchors: missing `^...$` allows partial match? `/\d+/` matches "abc123def"
│   │   → use fullmatch or anchors for validation
│   ├── Unicode: JS without `u` flag? Python default behavior intended?
│   │   → add `u` flag in JS, use re.A if ASCII-only needed
│   └── Bounds: user-controlled `{m,n}` with large values?
│       → cap bounds, never accept user-controlled counts
│
├── BUSINESS LOGIC (payments, roles, permissions, state machines)?
│   Read authorization → verify:
│   ├── Ownership checked? (User A cannot access User B's data)
│   ├── Role/permission checks before admin operations?
│   ├── Critical actions (delete, role change, payment) logged?
│   └── Rate limiting on sensitive operations?
│
└── EXTERNAL INTEGRATIONS (webhooks, third-party APIs, MCP)?
    Read outbound code → verify:
    ├── URLs from user input? → validate scheme and host
    ├── Secrets read from env vars, not hardcoded?
    └── Webhook payloads signature-verified?
```

**SECURE output per slice:**
```
SECURE CHECK: [slice name]
- Auth: [PASS / FLAG — issue]
- Data Access: [PASS / FLAG — issue]
- User Input: [PASS / FLAG — issue]
- Regex: [PASS / FLAG — issue]
- Business Logic: [PASS / FLAG — issue]
- Integrations: [PASS / FLAG — issue]
→ All PASS or fix FLAGs before MATCH
```

---

**Step4 — MATCH: Agent verifies the slice matches existing project conventions.**

The agent reads existing code outside the current slice to detect conventions, then verifies the new code follows them.

**Conventions to detect from existing code:**
```
Read 3-5 existing files in the same area (same directory or feature) to detect:
├── File organization
│   - Where do similar files live? (features/ vs modules/ vs pages/)
│   - One component per file or grouped?
│   - Test files: colocated or in __tests__/ directory?
│
├── Naming conventions
│   - Files: camelCase, kebab-case, PascalCase, snake_case?
│   - Functions: fetchUser() vs get_user() vs UserFetcher?
│   - Variables: const or let? (most code uses const?)
│   - Types/Interfaces: IUser vs User vs UserType interface?
│
├── Import patterns
│   - Absolute imports (src/components/...) or relative (../../)?
│   - Index files for re-exports?
│   - Default export or named export?
│
├── Error handling
│   - try/catch blocks or .catch() chains or Result types?
│   - Custom error classes or generic Error?
│   - Error responses: consistent envelope format?
│
├── Code structure
│   - Single file per feature or split across files?
│   - Hooks in separate files or in components?
│   - State management approach?
│
└── Testing patterns
    - describe/it blocks or test()?
    - Assertion style: expect().toBe() or assert.equal()?
    - Mock patterns: jest.mock() or dependency injection?
```

**Verification:**
- For each convention detected, the agent reads the new slice code and flags violations
- Example: `"Existing code uses named exports, but this new file uses default export — fix to match project convention"`
- Example: `"Existing tests use describe/it blocks, new test uses test() — fix to match"`
- Example: `"Existing code imports from src/lib/* (absolute), new file uses relative ../../ — fix"`
- Convention violations are treated as Required severity (must fix before commit)

**MATCH output:**
```
MATCH CHECK: [slice name]
Conventions detected: [fileOrg, naming, imports, errorHandling, testing, structure]
- [count] violations found:
  - [file:line] — [convention violated] → [expected fix]
→ All violations fixed before LINT
```

---

**Rules:**
- **Simplicity first** — Three similar lines > premature abstraction
- **Scope discipline** — Don't touch code outside slice
- **One slice at a time** — Pipeline loops over slices
- **TDD seams** — Test at public interfaces only
- **Mock at boundaries only** — Real > fakes > stubs > mocks
- **Feature flags** — For risky production changes
- **Form generation** — React Hook Form + Zod (React projects)
- **Design system** — Use tokens, no ad-hoc values
- **SECURE before MATCH, MATCH before LINT** — Security, then consistency, then quality

---

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
REPOS=(".")
# for multi: REPOS=("$beRepo" "$feRepo")

for R in "${REPOS[@]}"; do
  BRANCH="$(jq -r --arg r "$R" '.linkedBranches[$r] // .activeBranch // empty' .dev-craft/state.json)"
  if [ -z "$BRANCH" ]; then
    BRANCH="<type>/<scope>-<short-description>"
    jq --arg r "$R" --arg b "$BRANCH" '.linkedBranches[$r] = $b' .dev-craft/state.json > .dev-craft/state.tmp \
      && mv .dev-craft/state.tmp .dev-craft/state.json
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
