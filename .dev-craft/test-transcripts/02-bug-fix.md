# Test Transcript: Bug Fix (02-bug-fix.md)

## Input
User: "The login endpoint returns 500 when user doesn't exist. Should return 401 with 'invalid credentials'."

## Expected Flow

### 1. agent-router → triage
```
Classification: Bug (500 on missing user)
Priority: G1 (auth broken)
Route: debugger → implementer
```

### 2. debugger (4-phase investigation)

#### Phase 1: REPRODUCE
```bash
Command: curl -X POST /api/auth/login -d '{"email":"nonexistent@test.com","password":"test"}'
Error: 500 Internal Server Error
Stack: TypeError: Cannot read property 'password_hash' of null at auth.ts:42
Frequency: 100% (10/10 runs)
```

#### Phase 2: ISOLATE
```
Minimal case: getUser(null) throws
Bisect: Commit abc123 added null return without check
Location: auth.ts:42 — user.password_hash without null check
```

#### Phase 3: HYPOTHESIZE
1. getUser returns null on not found (80%)
2. Race condition in cache (15%)
3. DB returns null for deleted user (5%)

#### Phase 4: VERIFY
```
Hypothesis 1 confirmed: getUser returns null on cache miss + DB miss
Fix: add null check + throw NotFoundError
Tests: original + 3 edge cases pass
Full suite: green
```

### 3. implementer (TDD)
```
RED: Write failing test for 401 on missing user
GREEN: Add null check in auth.ts:42
REFACTOR: Extract error handling to helper
TEST: All pass
```

### 4. verifier (fresh evidence)
```
Tests: npm test → 47 passed, 0 failed
Lint: npm run lint → 0 errors
Typecheck: npm run typecheck → 0 errors
Build: npm run build → success
```

### 5. code-reviewer (8-axis)
```
Findings: 0 Critical, 0 High, 1 Medium (error message could be more generic), 0 Low
Verdict: APPROVE
```

### 5. mr-pr-review (explicit invoke)
```
PR: #456
Verdict: APPROVE
Security: PASS
```

### 5. ship (automated)
```
Version bump: PATCH (v1.2.1)
CHANGELOG updated
PR created: #457
```

---

## Checkpoints to Verify
- [ ] Debugger 4-phase used (not guessing)
- [ ] TDD followed (test first)
- [ ] Fresh evidence in verifier
- [ ] Code review with 8-axis
- [ ] mr-pr-review NOT auto-run
- [ ] State.json updated