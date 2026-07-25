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
| Critical | Blocks merge | Must fix before merge |
| Required | Must address | Should fix, but not a blocker |
| Nit | Minor, optional | Author may ignore |
| Optional | Suggestion | Worth considering |

## Review Output Format

Output follows the eight-axis structure with severity ratings. See `references/review-output-format.md` for the template.

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
| "The tests pass" | Tests don't catch architecture, security, or readability. |
| "It's a small change" | Small changes break things. Review thoroughly. |
| "It's just a prototype" | Prototypes become production. Review them. |
| "Review takes too long" | Bugs in production take longer. |

## Red Flags — STOP and Review Thoroughly

Large diff (>500 lines), new dependencies, security-sensitive code, DB/API changes, or performance-critical paths. **Extra scrutiny required.**

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

Wait 10+ minutes, then review as if you're seeing the code for the first time. Check every axis, find real issues, and fix them.

## Integration

**Use with:** `verification-before-completion`, `debugging-and-error-recovery`, `bug-hunting`, `dev-craft` BUILD phase.