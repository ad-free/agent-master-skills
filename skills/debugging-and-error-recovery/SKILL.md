---
name: debugging-and-error-recovery
description: |
  4-phase systematic root-cause investigation: Reproduce → Localize → Reduce → Fix.
  Use when tests fail, builds break, or behavior is unexpected — no guessing.
  Invoked by: debugger, implementer, test-engineer.
version: 1.1.0
preamble-tier: 4
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "debug this failure"
  - "test is failing"
  - "find root cause"
  - "investigate this error"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  phases: 4
  integrates-with: [verification-before-completion, dev-craft, test-engineer]
---

TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# Debugging & Error Recovery

## Overview

Stop guessing. Start investigating.

**Core principle:** Every bug has a root cause. Finding it systematically is faster than fixing symptoms.

## When to Use

- Tests fail unexpectedly
- Build errors occur
- Behavior doesn't match expectations
- Runtime errors or crashes
- Performance degradation
- Integration failures

**When NOT to use:** Trivial typos, obvious syntax errors, missing imports — fix these directly.

## Invocation Protocol

**Load when:** Test fails, build breaks, unexpected behavior occurs
**Invoke via:** `skill(name="debugging-and-error-recovery")`
**Resume to:** Return to the phase that invoked you (BUILD, TEST, or REVIEW)

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Guessing at fixes creates new bugs. Investigate first, fix second.

## Four-Phase Investigation

```
REPRODUCE → LOCALIZE → REDUCE → FIX
```

### Phase 1: REPRODUCE — make the failure happen reliably. Run the failing command, capture full output, confirm it's not flaky.

**Exit criterion:** You can make the failure happen on demand.

### Phase 2: LOCALIZE — find where the failure originates. Read the error, check the stack trace (first frame in YOUR code), check if regression.

**Exit criterion:** You know the exact file, line, and condition that causes the failure.

### Phase 3: REDUCE — shrink to the minimal failing case. Remove non-essentials until the failure disappears; the last thing removed is the cause.

**Exit criterion:** Smallest possible reproduction that demonstrates the bug.

### Phase 4: FIX — fix root cause, not symptom. Write test (RED), implement fix (GREEN), refactor if needed. Run full suite.

**Exit criterion:** Bug is fixed, test passes, full suite passes.

## The 3+ Rule

```
If you've made 3+ fix attempts that didn't work, STOP.
You're guessing. You have a deeper architectural problem.
```

**When this happens:** revert all recent changes, return to REPRODUCE, gather more evidence.

## Evidence Collection

Before fixing, gather error message, stack trace, last working state, changes since then, environment, and reproduction steps. **Never fix without evidence.**

## Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "I know what the fix is" | If you knew, it would work. Investigate. |
| "It's probably just X" | "Probably" = guessing. Verify. |
| "I'll just try this quick fix" | Quick fixes create new bugs. Investigate first. |
| "The test is wrong, not the code" | Maybe. Prove it with evidence. |

## Red Flags — STOP and Investigate

Multiple fix attempts without understanding why, fixing "nearby" code hoping it helps, skipping reproduction, ignoring error messages, adding code to suppress errors, or "It works on my machine" without investigation.

## Debugging Checklist

Before claiming the bug is fixed:

- [ ] Can you reproduce the failure reliably?
- [ ] Do you know exactly where it fails?
- [ ] Do you know exactly why it fails?
- [ ] Did you write a test that reproduces the bug?
- [ ] Does the test fail without the fix?
- [ ] Does the test pass with the fix?
- [ ] Does the full test suite pass?
- [ ] Did you check for regressions?

Can't check all boxes? You didn't fix the bug. You fixed a symptom.

## When Stuck

| Problem | Solution |
|---------|----------|
| Can't reproduce | Check environment, timing, state. Try fresh clone. |
| Don't know where it fails | Add logging. Binary search the code. Comment out code. |
| Fix doesn't work | You're fixing the symptom, not the cause. Re-investigate. |
| Multiple things broken | Fix one at a time. Start with the first failure. |
| It's in library code | Work around it. Report it. Don't fix library code. |

### Context Degradation Detection

Before investigating, check if the issue is agent context degradation:

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Lost-in-the-Middle** | References definitions not in current scope | Rotate context, load only relevant files |
| **Context Poisoning** | Contradictory code, style drift mid-file | Clear session, re-establish conventions |
| **Distraction** | Unrelated code added, wrong bug being fixed | Re-anchor to the specific failure |
| **Confusion** | Wrong API version, deprecated patterns | Fetch current-version docs, verify signatures |

Diagnostic: "Is this a bug in the code, or in the agent's understanding?" If suspected: save state, rotate context, load only error + relevant file(s), resume from REPRODUCE.

### Git Bisect — Regression Tracking

When a bug is a regression, use `git bisect` to find the exact commit:

```bash
git bisect start && git bisect bad && git bisect good <last-working>
# At each checkout: git bisect good/bad
git bisect reset
```

**Pro tip:** Use `git bisect run npm test -- --grep "failing-test-name"` to automate the search.

## Integration

**Use with:** `dev-craft` (BUILD TDD loop), `verification-before-completion` (verify fixes), `bug-hunting` (security vuln debugging), `quality-gates` (deterministic checks).