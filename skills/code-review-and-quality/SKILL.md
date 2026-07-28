---
name: code-review-and-quality
description: |
  Eight-axis code review with confidence-based filtering, pre-report gate, and false positive suppression.
  Use before merging PRs, after implementing features, or when receiving review feedback.
  Invoked by: code-reviewer, implementer, verifier.
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
triggers:
  - "review this PR"
  - "code review"
  - "review my changes"
  - "check this code"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  axes: 8
  integrates-with: [verification-before-completion, quality-gates, bug-hunting]
  source-enhancements: ECC code-reviewer (Pre-Report Gate, False Positives, Confidence Filtering)
---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Code Review & Quality v2.0

## Overview

Review is not about finding faults. It's about ensuring quality.

**Core principle:** Review what matters. Ignore what doesn't.

## When to Use

- Before merging a pull request
- After completing a feature or fix
- When receiving review feedback
- When reviewing your own code
- When another agent asks for review

**When NOT to use:** Trivial changes (typos, comments, formatting only)

## Invocation Protocol

**Load when:** Reviewing code, receiving review feedback, before merging
**Invoke via:** `skill(name="code-review-and-quality")`
**Resume to:** Continue to HARDEN or SHIP phase

## The Iron Law

```
NO CODE WITHOUT REVIEW EVIDENCE
```

"Looks good to me" without systematic review is not approval. It's negligence.

---

## Review Process (MANDATORY)

### Step 1: Gather Context
```bash
git diff --staged
git diff
# If no diff, check recent commits
git log --oneline -5
```

### Step 2: Understand Scope
- Identify which files changed
- What feature/fix they relate to
- How they connect to existing code

### Step 3: Read Surrounding Code
**Don't review changes in isolation.** Read the full file and understand:
- Imports, dependencies, call sites
- Related tests
- Existing patterns in the codebase

### Step 4: Apply Confidence-Based Filtering

**IMPORTANT:** Do not flood the review with noise. Apply these filters:

| Confidence | Action |
|------------|--------|
| **>80%** | Report — it's a real issue |
| **50-80%** | State assumption, ask for confirmation |
| **<50%** | Skip — not confident enough |

**Additional Filters:**
- Skip stylistic preferences unless they violate project conventions
- Skip issues in unchanged code unless CRITICAL security
- Consolidate similar issues (e.g., "5 functions missing error handling" not 5 separate findings)
- Prioritize issues that could cause bugs, security vulnerabilities, or data loss

### Step 5: Pre-Report Gate (Answer ALL before filing)

**Before writing any finding, answer all four questions. If any answer is "no" or "unsure", downgrade severity or drop the finding.**

1. **Can I cite the exact line?** Name the file and line. Vague findings like "somewhere in the auth layer" are not actionable and must be dropped.
2. **Can I describe the concrete failure mode?** Name the input, state, and bad outcome. If you cannot name the trigger, you are pattern-matching, not reviewing.
3. **Have I read the surrounding context?** Check callers, imports, and tests. Many apparent issues are already handled one frame up or guarded by a type.
4. **Is the severity defensible?** A missing JSDoc is never HIGH. A single `any` in a test fixture is never CRITICAL. Severity inflation erodes trust faster than missed findings.

### Step 6: HIGH/CRITICAL Require Proof

For any finding tagged HIGH or CRITICAL, include:
- The exact snippet and line number
- The specific failure scenario: input, state, and outcome
- Why existing guards (types, validation, framework defaults) do not catch it

If you cannot produce all three, demote to MEDIUM or drop.

### Step 7: Accept Zero Findings

**A clean review is a valid review.** Do not manufacture findings to justify the invocation. If the diff is small, well-typed, tested, and follows the project's patterns, the correct output is a summary with zero rows and verdict `APPROVE`.

Manufactured findings, filler nits, speculative "consider using X", and hypothetical edge cases without a trigger are the primary failure mode of LLM reviewers and directly undermine this agent's usefulness.

---

## Common False Positives — SKIP These

Patterns that LLM reviewers commonly mis-flag. Skip unless you have evidence specific to this codebase:

### Error Handling
- **"Consider adding error handling"** on a call whose error path is handled by the caller or framework:
  - Express error middleware
  - React error boundaries
  - Top-level `try/catch`
  - Promise chains with `.catch` upstream

### Input Validation
- **"Missing input validation"** when the function is internal and its callers already validate. Trace at least one caller before flagging.

### Magic Numbers
- **"Magic number"** for well-known constants: `200`, `404`, `1000` ms, `60`, `24`, `1024`, array index `0` or `-1`, HTTP status codes, and single-use local constants whose meaning is obvious from the variable name.

### Function Length
- **"Function too long"** for exhaustive `switch` statements, configuration objects, test tables, or generated code. Length is not complexity.

### Documentation
- **"Missing JSDoc"** on single-purpose internal helpers whose name and signature are self-describing.

### Variable Declaration
- **"Prefer `const` over `let`"** when the variable IS reassigned. Read the whole function before flagging.

### Null Safety
- **"Possible null dereference"** when the preceding line narrows the type or an `if` guard is in scope. Trace type flow instead of pattern-matching on `?.`.

### Database
- **"N+1 query"** on fixed-cardinality loops (enum iteration, 4-element array) or on paths already using `DataLoader`/batching.

### Async
- **"Missing await"** on fire-and-forget calls (logging, metrics, background queue pushes). Check for `void` prefix or comment before flagging.

### Language
- **"Should use TypeScript"** or **"Should have types"** in a JavaScript-only file. Match the project's existing language; do not suggest a stack change.

### Tests
- **"Hardcoded value"** for values in test fixtures, example code, or documentation snippets. Tests SHOULD have hardcoded expectations.

### Security Theater
- Flagging `Math.random()` in non-cryptographic context (animation, jitter, sampling)
- Flagging `eval`/`Function` in a plugin system that is explicitly a code-loading surface

**When tempted to flag one of the above, ask:** "Would a senior engineer on THIS team actually change this in review?" If no, skip.

---

## Eight-Axis Review

Review code across ALL eight axes. Missing one axis means incomplete review.

### Axis 1: Correctness
Does the code match the spec? Are edge cases, error paths, and async operations handled correctly?

### Axis 2: Readability
Clear names (no cryptic identifiers), straightforward control flow, single responsibility per function. Would a new developer understand it?

### Axis 3: Architecture
Follows existing patterns? Clean module boundaries? No unnecessary dependencies? Feature logic not leaking into shared modules?

### Axis 4: Performance
Any N+1 queries, unbounded loops, sync I/O that should be async, missing pagination, or large objects on hot paths?

### Axis 5: Security
Input validated, secrets not in code/logs, parameterized queries, external data untrusted, auth checks in place, no unsafe deserialization. Review every regex for ReDoS, user-controlled input, missing anchors, and Unicode safety.

### Axis 6: Testing
Tests exist for new code, cover edge cases, are maintainable, and mock at boundaries only. Judge tests against their stated failure mode (see `testing-strategies`).

### Axis 7: Modern Patterns
No deprecated APIs, code follows current-version docs, no legacy typing/deprecated idioms (blocked by linter per `dev-craft/references/lint-rules.md`).

### Axis 8: Conventions
New code matches project conventions for file organization, naming, imports/exports, error handling, code structure, and testing framework.

| Severity | Meaning | Action |
|----------|---------|--------|
| **Critical** | Blocks merge | Must fix before merge |
| **Required** | Must address | Should fix, but not a blocker |
| **Nit** | Minor, optional | Author may ignore |
| **Optional** | Suggestion | Worth considering |

---

## Language-Specific Checklists

### React/Next.js Patterns (HIGH)
- Missing dependency arrays in `useEffect`/`useMemo`/`useCallback`
- State updates in render → infinite loops
- Array index as key with reorderable items
- Prop drilling (3+ levels) → use context or composition
- Unnecessary re-renders → missing memoization
- Client/server boundary violations (`useState`/`useEffect` in Server Components)
- Missing loading/error states in data fetching
- Stale closures in event handlers

### Node.js/Backend Patterns (HIGH)
- Unvalidated input (request body/params without schema validation)
- Missing rate limiting on public endpoints
- Unbounded queries (`SELECT *`, no LIMIT on user-facing)
- N+1 queries → use JOIN or batch
- Missing timeouts on external HTTP calls
- Error message leakage (internal details to clients)
- Missing CORS configuration

### Security (CRITICAL)
- **Hardcoded credentials** — API keys, passwords, tokens, connection strings in source
- **SQL injection** — String concatenation in queries instead of parameterized
- **XSS** — Unescaped user input rendered in HTML/JSX
- **Path traversal** — User-controlled file paths without sanitization
- **CSRF** — State-changing endpoints without CSRF protection
- **Auth bypass** — Missing auth checks on protected routes
- **Insecure dependencies** — Known vulnerable packages
- **Exposed secrets in logs** — Logging sensitive data (tokens, passwords, PII)

---

## Review Output Format

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

Verdict: **WARNING** — 2 HIGH issues should be resolved before merge.
```

### Approval Criteria
- **Approve**: No CRITICAL or HIGH issues (including clean reviews with zero findings)
- **Warning**: HIGH issues only (can merge with caution)
- **Block**: CRITICAL issues found — must fix before merge

**Never withhold approval to appear rigorous.** If the diff is clean, approve it.

---

## Forbidden Review Responses

When receiving review feedback, NEVER:
- "You're absolutely right!" (without verification)
- "I'll fix that later" (without creating a tracked item)
- "That's intentional" (without explaining why)
- "It's just a style thing" (without checking conventions)
- "The tests pass, so it's fine" (tests don't catch everything)

## Correct Review Responses

When receiving review feedback, ALWAYS:
1. **Read the feedback completely**
2. **Verify the finding** — is it actually a problem?
3. **Respond with evidence** — show you checked
4. **Fix or explain** — either fix it or explain why not
5. **Re-verify** — run tests after changes

---

## YAGNI Check

Before approving any "professional" or "enterprise" feature:

```
YAGNI CHECK:
- Was this requested in the spec?
- Is this actually needed NOW?
- Will this be used in the next 2 weeks?
- If not, REMOVE IT.
```

**YAGNI = You Aren't Gonna Need It.** If it's not in the spec, it's scope creep.

---

## Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "The tests pass" | Tests don't catch architecture, security, or readability. |
| "It's a small change" | Small changes break things. Review thoroughly. |
| "It's just a prototype" | Prototypes become production. Review them. |
| "Review takes too long" | Bugs in production take longer. |

---

## Red Flags — STOP and Review Thoroughly

Large diff (>500 lines), new dependencies, security-sensitive code, DB/API changes, or performance-critical paths. **Extra scrutiny required.**

---

## Review Checklist

Before approving any code:

- [ ] All eight axes reviewed
- [ ] Every finding has severity assigned
- [ ] Critical findings addressed
- [ ] YAGNI check passed
- [ ] Tests exist and pass
- [ ] Lint passes
- [ ] Type check passes
- [ ] No security concerns (including regex)
- [ ] Code matches project conventions (naming, imports, structure, error handling)

---

## Self-Review Protocol

Wait 10+ minutes, then review as if you're seeing the code for the first time. Check every axis, find real issues, and fix them.

---

## Integration

**Use with:** `verification-before-completion`, `debugging-and-error-recovery`, `bug-hunting`, `dev-craft` BUILD phase.

**References:**
- `references/false-positives.md` — Complete false positive catalog
- `references/prompt-defense.md` — Security baseline for reviewers
- `references/review-output-format.md` — Output template