---
name: code-review-and-quality
description: Use when reviewing code or receiving review feedback. Eight-axis quality
  assessment before merging any change.
metadata:
  origin: agent-master-skills

---

# Code Review & Quality

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

## Eight-Axis Review

Review code across ALL eight axes. Missing one axis means incomplete review.

### Axis 1: Correctness

- Does code match the spec${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/requirements?
- Are edge cases handled (null, empty, boundary, error)?
- Are error paths handled (not just happy path)?
- Are return types correct?
- Are async operations properly awaited?

### Axis 2: Readability

- Are names clear and consistent?
- **No single-character or cryptic identifiers** (`x`, `d`, `tmp`, `res`) outside a tight loop scope — see dev-craft `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/lint-rules.md` gate.
- Is control flow straightforward (no deep nesting, no clever tricks)?
- Does each function have a clear single responsibility?
- Would a new developer understand this code?

### Axis 3: Architecture

- Does the change follow existing patterns?
- Are module boundaries clean?
- Is feature-specific logic in shared modules?
- Does it introduce new dependencies unnecessarily?

### Axis 4: Performance

- Any N+1 query patterns?
- Any unbounded loops or unconstrained data?
- Any synchronous I${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/O that should be async?
- Any missing pagination on lists?
- Any large objects on hot paths?

### Axis 5: Security

- Input validated at boundaries?
- Secrets out of code${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/logs?
- Parameterized queries (no string concatenation)?
- External data treated as untrusted?
- Any auth${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/authorization bypass?
- Any unsafe deserialization?

**Regex security — review every regex in the diff:**
- ReDoS risk: nested quantifiers `(a+)+b`, overlapping alternatives `(a|aa)+b`, unbounded `(.*a)*` patterns?
- User-controlled regex: `new RegExp(userInput)` without `re.escape()`?
- Missing anchors: `${PROJECT_ROOT}/ without `^...$` allows partial match bypass?
- Unicode safety: missing `u` flag in JS? Wrong dot-all behavior? `\w` Unicode scope matches intent?
- Bounded repetition: user-controlled `{m,n}` with large ranges causing ReDoS?

### Axis 6: Testing

- Tests exist for new code?
- Tests cover edge cases?
- Tests are maintainable (not brittle)?
- Mocks are at boundaries only?

**Judgment criterion:** Judge tests against the failure mode stated when they were written (see `testing-strategies`) — a test with no stated failure mode is itself a review finding, not just a coverage gap.

### Axis 7: Modern Patterns

- No deprecated APIs for the detected version?
- Code follows current-version docs?
- Source citations for correct version?
- Lint${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/tests pass?
- **No legacy typing / deprecated idioms** — varies by stack (Python `Optional[X]`→`X | None`; TS `any`→`unknown`, `var`→`const`; etc.). Blocked by the stack's native linter per dev-craft `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/lint-rules.md`.


### Axis 8: Conventions

- New code follows project conventions detected in ALIGN phase?

**File organization:**
- Does the new file go where existing similar files live?
- Test colocated or in a test directory? (match existing pattern)

**Naming:**
- Files: match existing case convention (kebab, camel, Pascal, snake)?
- Functions${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/variables: match existing naming style?
- Types${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/interfaces: match existing prefix${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/suffix convention?

**Imports & exports:**
- Import style matches existing code (absolute vs relative, grouped vs inline)?
- Export style matches (named vs default)?
- Existing code uses barrel${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/index exports — does new code follow?

**Error handling:**
- Does the new code use the same error handling pattern as existing code?
- (try${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/catch vs Result types vs error boundaries)?

**Code structure:**
- Does the new code follow the same file-per-component or grouped approach?
- Does it match the existing state management and data fetching patterns?

**Testing:**
- Do new tests follow the same framework and assertion style?
- Same describe${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/it structure or test() calls?

| Severity | Meaning | Action |
|----------|---------|--------|
| Critical | Blocks merge | Must fix before merge |
| Required | Must address | Should fix, but not a blocker |
| Nit | Minor, optional | Author may ignore |
| Optional | Suggestion | Worth considering |

## Review Output Format

```markdown
## Review: [Feature${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Fix Name]

**Verdict:** [APPROVED / CHANGES REQUESTED]

### Axis 1: Correctness
- [Finding with location and explanation]

### Axis 2: Readability
- [Finding with location and explanation]

### Axis 3: Architecture
- [Finding with location and explanation]

### Axis 4: Performance
- [Finding with location and explanation]

### Axis 5: Security
- [Finding with location and explanation]

### Axis 6: Testing
- [Finding with location and explanation]

### Axis 7: Modern Patterns
- [Finding with location and explanation]

### Axis 8: Conventions
- [Finding with location and explanation]

### Summary
- Critical: [count]
- Required: [count]
- Nit: [count]
- Optional: [count]
```

## Forbidden Review Responses

When receiving review feedback, NEVER:

- "You're absolutely right!" (without verification)
- "I'll fix that later" (without creating a tracked item)
- "That's intentional" (without explaining why)
- "It's just a style thing" (without checking if it violates conventions)
- "The tests pass, so it's fine" (tests don't catch everything)

## Correct Review Responses

When receiving review feedback, ALWAYS:

1. **Read the feedback completely**
2. **Verify the finding** — is it actually a problem?
3. **Respond with evidence** — show you checked
4. **Fix or explain** — either fix it or explain why not
5. **Re-verify** — run tests after changes

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

## Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "It's just a style thing" | Style conventions exist for consistency. Follow them. |
| "The tests pass" | Tests don't catch architecture, security, or readability. |
| "It's a small change" | Small changes break things. Review thoroughly. |
| "I wrote it, I know it's correct" | Review your own code as if you didn't write it. |
| "Review takes too long" | Bugs in production take longer. Review properly. |
| "It's just a prototype" | Prototypes become production. Review them. |
| "My human partner approved it" | Approval without review is not review. Still review. |
| "I'll review it properly next time" | No. Review it properly now. |

## Red Flags — STOP and Review Thoroughly

- Large diff (> 500 lines)
- New dependencies added
- Security-sensitive code (auth, payments, data)
- Database schema changes
- API changes
- Error handling patterns changed
- Performance-critical code

**All of these mean: Extra scrutiny required.**

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

## Self-Review Protocol

When reviewing your own code:

1. **Wait** — at least 10 minutes between writing and reviewing
2. **Pretend** — you're a new developer seeing this for the first time
3. **Check each axis** — don't skip any
4. **Be honest** — find real issues, not just nits
5. **Fix what you find** — don't just note it

## Integration

**Use with:**
- `verification-before-completion` — Verification evidence required for review
- `debugging-and-error-recovery` — Fix issues found in review
- `bug-hunting` — Deep security review feeds into bug hunting methodology
- `dev-craft` Phase 5 BUILD (TDD loop) — Tests provide review evidence