---
name: debugging-and-error-recovery
description: Use when tests fail, builds break, or behavior doesn't match expectations.
  Systematic root-cause investigation, not guessing.
metadata:
  origin: agent-master-skills

---

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

### Phase 1: REPRODUCE

Make the failure happen reliably.

**Steps:**
1. Run the failing test${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/command exactly as specified
2. Capture the full error output
3. Identify the exact conditions that trigger the failure
4. Confirm it fails every time (not flaky)

**Exit criterion:** You can make the failure happen on demand.

### Phase 2: LOCALIZE

Find where the failure originates.

**Steps:**
1. Read the error message carefully — it tells you exactly what failed
2. Check the stack trace — find the first frame in YOUR code (not library code)
3. Add debug output around the failure point
4. Check if it's a regression: when did it last work?
5. Compare working vs. failing states

**Exit criterion:** You know the exact file, line, and condition that causes the failure.

### Phase 3: REDUCE

Shrink to the minimal failing case.

**Steps:**
1. Remove everything that's not necessary for the failure
2. Simplify inputs until you find the minimal trigger
3. Comment out code until the failure disappears
4. The last thing you removed is the cause

**Exit criterion:** You have the smallest possible reproduction that demonstrates the bug.

### Phase 4: FIX

Fix the root cause, not the symptom.

**Steps:**
1. Fix the actual root cause identified in Phase 2-3
2. Write a test that reproduces the bug (RED)
3. Implement the fix (GREEN)
4. Refactor if needed (REFACTOR)
5. Run the full test suite to confirm no regressions

**Exit criterion:** Bug is fixed, test passes, full suite passes.

## The 3+ Rule

```
If you've made 3+ fix attempts that didn't work, STOP.
You're guessing. You have a deeper architectural problem.
```

**When this happens:**
1. Revert all recent changes
2. Return to Phase 1 (REPRODUCE)
3. Gather more evidence before trying again
4. Consider: is this actually a different problem?

## Evidence Collection

Before fixing, gather:

```
EVIDENCE:
- Error message: [exact text]
- Stack trace: [relevant frames]
- Last working state: [commit${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/timestamp]
- Changes since then: [git log${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/diff]
- Environment: [OS, versions, config]
- Reproduction steps: [exact sequence]
```

**Never fix without evidence.** "It seems like..." is not evidence.

## Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "I know what the fix is" | If you knew, it would work. It didn't. Investigate. |
| "It's probably just X" | "Probably" means you're guessing. Verify. |
| "I'll just try this quick fix" | Quick fixes create quick new bugs. Investigate first. |
| "The test is wrong, not the code" | Maybe. But prove it with evidence, not assumption. |
| "It worked before, must be environment" | Maybe. But check what changed in the code first. |
| "This is too complex to debug" | No. Break it down. Follow the four phases. |
| "I don't have time to investigate" | You don't have time NOT to. Quick fixes waste more time. |

## Red Flags — STOP and Investigate

- Making multiple fix attempts without understanding why
- Changing code without knowing what it does
- Fixing "nearby" code hoping it helps
- Skipping the reproduction step
- Ignoring error messages because they're "confusing"
- Adding code to suppress errors
- "It works on my machine" without investigation

**All of these mean: Stop guessing. Start investigating.**

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

Before investigating the code, check if the issue is caused by agent context degradation. These patterns mimic real bugs but have different root causes:

| Degradation Pattern | Symptoms | Fix |
|---------------------|----------|-----|
| **Lost-in-the-Middle** | Agent writes code that compiles but references definitions from earlier context that don't exist. Imports or functions used but never defined in current scope. | Rotate context. Load only the relevant files. Resume with fresh short context. |
| **Context Poisoning** | Agent writes code that contradicts itself (e.g., two different validation strategies in the same file). Style drifts mid-file. | Clear session. Re-establish conventions. Feed only consistent examples. |
| **Distraction** | Agent adds unrelated code (dashboard components in an API endpoint). Fixes a different bug than the one reported. | Re-read the error message. Re-anchor to the specific failure. Remove unrelated code. |
| **Clash** | Agent's training data contradicts something established earlier (e.g., writes React class component after agreeing to use hooks). | Re-verify conventions. Re-establish project rules. Check AGREED.md. |
| **Confusion** | Agent produces syntactically valid but semantically wrong code. Uses wrong library version's API. References deprecated patterns. | Fetch current-version docs. Verify API signatures. Check migration guides. |

**Diagnostic question:** Ask yourself: "Is this a bug in the code, or a bug in the agent's understanding?"

**If context degradation is suspected:**
1. Save current state to handoff document
2. Rotate context (new session)
3. Load only: the error message, relevant file(s), plan document
4. Resume debugging from Phase 1 (REPRODUCE)

### Git Bisect — Regression Tracking

When a bug is a regression (it used to work):

**Setup:**
```bash
git bisect start
git bisect bad              # Current broken state
git bisect good <commit>    # Last known working state
```

**During bisect:**
```bash
# At each checkout, test:
git bisect good  # If bug not present
git bisect bad   # If bug present
```

**Exit:**
```bash
git bisect reset
```

**Pro tip:** Write a single command that reproduces the bug:
```bash
git bisect run npm test -- --grep "failing-test-name"
```

This finds the exact commit that introduced the regression without manual testing.

## Integration

**Use with:**
- `dev-craft` Phase 5 BUILD (TDD loop) — Bug fixes follow TDD: test first, then fix
- `verification-before-completion` — Verify the fix before claiming done
- `bug-hunting` — Security vulnerabilities found through bug hunting are debugged using this methodology
- `systematic-debugging` — Full four-phase investigation for complex issues
- `quality-gates` — Deterministic checks catch bugs before LLM judge. Debugging feeds findings back into gate configuration.