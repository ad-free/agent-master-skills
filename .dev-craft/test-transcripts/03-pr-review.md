# Test Transcript: PR Review (03-pr-review.md)

## Input
User: "Review PR #123 for the auth JWT feature"

## Expected Flow

### 1. mr-pr-review invoked explicitly
```
User: "Review PR #123"
Agent: loads mr-pr-review skill
```

### 2. Source Detection
```
git remote -v → github.com
gh CLI available → Yes
```

### 3. Fetch PR Data
```bash
gh pr view 123 --json files,commits,additions,deletions,body,title,author,baseRefName,headRefName
```

### 4. Full Review Execution

#### 8-Axis Review
| Axis | Findings |
|------|----------|
| Correctness | ✅ Spec match, edge cases handled |
| Readability | ⚠️ 2 functions >50 lines |
| Architecture | ✅ Follows patterns |
| Performance | ⚠️ N+1 query in dashboard list |
| Security | ❌ SQL injection in user lookup |
| Testing | ⚠️ Missing integration test for reset flow |
| Modern Patterns | ✅ No deprecated APIs |
| Conventions | ✅ Follows project style |

#### Security Deep-Dive
- Secrets: None found
- Auth: All routes protected, public endpoints documented
- Injection: SQL injection in `src/auth/login.ts:42` (string concat)

#### Vulnerability Patterns
- No IDOR, proper authZ
- No crypto failures
- No XSS (proper escaping)

#### Test Coverage
- Missing: Integration test for password reset flow
- Contract test: PASS

#### Documentation
- API reference: Updated
- Changelog: Missing entry

### 5. Output Report

```
[HIGH] SQL Injection in user lookup
File: src/auth/login.ts:42
Issue: String concatenation in SQL query allows injection
Fix: Use parameterized query

```ts
// BAD
const query = `SELECT * FROM users WHERE email = '${email}'`;

// GOOD
const query = `SELECT * FROM users WHERE email = $1`;
await db.query(query, [email]);
```

[HIGH] N+1 Query in Dashboard List
File: src/dashboard/list.ts:67
Issue: Loop executes query per item
Fix: Use JOIN or batch load

[MEDIUM] Function too long (85 lines)
File: src/auth/refresh.ts:15
```

### Summary
```
## Review Summary

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 0     | pass   |
| HIGH     | 2     | warn   |
| MEDIUM   | 3     | info   |
| LOW      | 1     | note   |

Verdict: REQUEST_CHANGES — 2 HIGH issues should be resolved before merge.
```

### Handoff
- State updated: `state.json.prReview`
- Next: `documentation-engineering` if docs needed