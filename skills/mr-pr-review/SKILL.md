---
name: mr-pr-review
description: |
  Peer review skill for GitHub Pull Requests and GitLab Merge Requests.
  Reviews code changes with full 8-axis audit, security deep-dive, performance analysis,
  and architecture alignment. Use when a PR/MR is ready for peer review.
  NOT auto-run — human must invoke explicitly.
  
model: big-pickle
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
triggers:
  - "review pr"
  - "review mr"
  - "peer review"
  - "mr-pr-review"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: quality-safety
  integrates-with: [code-review-and-quality, quality-gates]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# MR/PR Review Skill

Reviews GitHub PRs / GitLab MRs with full context, detailed findings, and actionable verdicts.

## When to Use

- PR/MR created and ready for peer review
- After `ship` skill completes (human asked to run)
- Security-sensitive changes need deep review
- Architecture review needed for cross-cutting changes

**Do NOT auto-run** — human must invoke explicitly. After `ship` completes, agent notes: "Run `mr-pr-review` for peer review?"

---

## Source Detection & CLI Check

### 1. Detect Repo Hosting
```bash
git remote -v | head -1
# github.com  → GitHub
# gitlab.com  → GitLab
# other       → Ask user
```

### 2. Check CLI Availability
```bash
command -v gh >/dev/null 2>&1 && echo "gh available" || echo "gh missing"
command -v glab >/dev/null 2>&1 && echo "glab available" || echo "glab missing"
```

### 3. Fetch Strategy
| Source | CLI Available | Method |
|--------|---------------|--------|
| GitHub | `gh` | `gh pr view <num> --json files,commits,additions,deletions,body` |
| GitLab | `glab` | `glab mr show <num> --json changes,commits,title,description` |
| Any | Neither | Ask user to paste `git diff` or provide PR/MR URL for manual fetch |

**If CLI missing:** Ask: "GitHub CLI (`gh`) not found. Install? Or provide diff manually?"

---

## Review Scope (ALL)

### 1. 8-Axis Code Review (from `code-review-and-quality`)
- Correctness — spec match, edge cases, async handling
- Readability — names, flow, single responsibility
- Architecture — patterns, boundaries, dependencies
- Performance — N+1, unbounded loops, sync I/O, pagination, large objects
- Security — input validation, secrets, parameterized queries, auth checks, regex safety
- Testing — behavior coverage, edge cases, maintainable, mock at boundaries
- Modern Patterns — no deprecated APIs, current-version docs, no legacy idioms
- Conventions — file org, naming, imports, error handling, structure, test framework

### 2. Security Deep-Dive (from `bug-hunting`)
- Secrets scan (API keys, tokens, passwords, private keys, .env, JWT secrets)
- Auth verification (every route has middleware, public endpoints documented, admin routes have RBAC, user-scoped data, rate limiting on auth bypass)
- Injection scan (SQL param queries, no shell exec with user input, path validation, HTML escaping, no secrets in errors, file upload restrictions)

### 3. Vulnerability Patterns (OWASP Top 10 + Language-Specific)
- Broken Access Control — IDOR, forced browsing, elevation
- Cryptographic Failures — weak hash, hardcoded keys, missing TLS
- Injection — SQL, NoSQL, Command, LDAP, XSS
- Insecure Design — missing threat model, biz logic flaws
- Security Misconfiguration — defaults, verbose errors, exposed admin
- Vulnerable Components — CVE scan via `npm audit` / `pip-audit` / `govulncheck`
- Auth Failures — credential stuffing, session fixation, weak password policy
- Software Integrity — unsigned deps, CI/CD tampering
- Logging Failures — unlogged auth events, missing audit trail
- SSRF — user-supplied URLs in fetch, missing allowlist

### 4. Architecture Alignment
- ADR compliance (check `docs/adr/`)
- Contract conformance (OpenAPI vs implementation)
- Cross-cutting concerns (observability, error handling, config)

### 5. Test Coverage Gaps
- New code paths without tests
- Integration test for new API endpoints
- Contract test (Pact) for consumer-driven endpoints
- E2E for critical user flows

### 6. Documentation Updates
- API reference matches implementation
- Runbooks updated for new deployment patterns
- ADR created for architectural decisions
- Changelog entry present

### 7. Breaking Change Detection
- API contract changes (removed fields, changed types, new required params)
- Database schema breaking changes
- Config/environment variable changes
- Removed/renamed exported functions

---

## Process

### Step 1: Fetch PR/MR Data
```bash
# GitHub
gh pr view 123 --json files,commits,additions,deletions,body,title,author,baseRefName,headRefName

# GitLab
glab mr show 456 --json changes,commits,title,description,author,source_branch,target_branch

# Manual diff
git diff origin/main...HEAD
```

### Step 2: Load Context
- Read `api-contract.md` if exists
- Read relevant ADRs from `docs/adr/`
- Read `requirements.md` for traceability
- Read recent ADRs for context

### Step 3: Analyze Diff
```bash
# Per-file analysis
gh pr view 123 --json files --jq '.files[] | {path: .path, additions: .additions, deletions: .deletions, patch: .patch}'
```

### Step 4: Run 8-Axis Review
For each file in diff:
1. Read full file (context)
2. Apply all 8 axes
3. Apply security deep-dive
4. Check architecture alignment

### Step 4: Categorize Findings
| Severity | Criteria | Action |
|----------|----------|--------|
| **Critical** | Blocks merge — security vuln, data loss, broken build | Must fix |
| **High** | Significant bug risk, major architecture violation | Should fix |
| **Medium** | Maintainability, performance, convention | Can fix |
| **Low** | Nit, style, minor improvement | Optional |
| **Ask** | Uncertain, needs human judgment | Discuss |

### Step 5: Confidence Filtering
- **>80% confident** → Report
- **50-80%** → State assumption, ask for confirmation
- **<50%** → Skip (not confident enough)

### Step 6: False Positive Suppression
Apply `references/false-positives.md` patterns — skip known false positives unless evidence specific to this codebase.

### Step 7: Output Report

---

## Output Format

### Per Finding
```
[SEVERITY] Brief title
File: path/to/file.ts:42
Issue: Concrete description with input/state/outcome
Fix: Specific code change

```ts
// BAD: current code
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD: parameterized
const query = `SELECT * FROM users WHERE id = $1`;
const result = await db.query(query, [userId]);
```
```

### Summary (REQUIRED at end)
```markdown
## Review Summary

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 0     | pass   |
| HIGH     | 2     | warn   |
| MEDIUM   | 3     | info   |
| LOW      | 1     | note   |

**Verdict:** REQUEST_CHANGES — 2 HIGH issues should be resolved before merge.

### Key Findings
1. **[HIGH] SQL Injection in user lookup** — `src/auth/login.ts:42`
2. **[HIGH] Missing auth on admin endpoint** — `src/api/admin.ts:15`
3. **[MEDIUM] N+1 query in dashboard** — `src/dashboard/list.ts:67`
```

### Approval Criteria
- **Approve**: No CRITICAL/HIGH (clean review with zero findings is valid)
- **Request Changes**: HIGH issues only (can merge with caution)
- **Block**: CRITICAL issues found — must fix before merge

**Never withhold approval to appear rigorous.** If diff is clean, approve it.

---

## PR/MR Interaction (Optional)

If CLI available and user confirms:
```bash
# Post review as review comment
gh pr review 123 --body "$(cat review-report.md)" --request-changes

# Or approve
gh pr review 123 --approve --body "LGTM"
```

---

## Out-of-Scope Detection

If during review you discover issues NOT in current PR scope:
1. Document in `.dev-craft/out-of-scope/YYYY-MM-DD-<slug>.md`
2. Ask: "Create follow-up ticket? [y/n]"
3. If yes → create GitHub Issue (if `gh` available) or local markdown

---

## Handoff

**State write:** Update `state.json.prReview`:
```json
{
  "prNumber": 123,
  "status": "request_changes",
  "findings": {"critical": 0, "high": 2, "medium": 3, "low": 1},
  "verdict": "request_changes",
  "reviewedAt": "2026-07-28T10:30:00Z"
}
```

**Next skill:** `skill("documentation-engineering")` if docs needed, else `skill("learn")` to capture review learnings.