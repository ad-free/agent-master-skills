---
name: debugging-and-error-recovery
description: |
  Systematic root-cause investigation with hypothesis testing, regression
  prevention, and automated self-correction loops. Use when tests fail, builds
  break, or behavior is unexpected — no guessing. Invoked by: debugger,
  implementer, test-engineer.
model: nemotron-3-ultra-free
version: 2.0.0
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
  - "hypothesis test"
  - "regression check"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.0.0
  domain: debugging
  integrates-with: [verification-before-completion, dev-craft, test-engineer, systematic-debugging]
---

TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# Debugging & Error Recovery

## Relationship to existing skills

- `systematic-debugging` — hypothesis-testing framework this skill builds on; load `systematic-debugging` for the full scientific-method debugging loop
- `dev-craft` — invokes this skill during TEST phase when suites fail
- `verification-before-completion` — runs after fixes to confirm evidence
- `bug-hunting` — security-focused debugging; this skill covers general debugging

## When to Use

- Tests fail unexpectedly
- Build errors occur
- Behavior doesn't match expectations
- Runtime errors or crashes
- Performance degradation
- Integration failures
- Regression after a change

**When NOT to use:** Trivial typos, obvious syntax errors, missing imports — fix these directly.

## When NOT to Use

- The error message is clear and the fix is obvious
- You haven't reproduced the failure yet
- You're fixing a symptom instead of the root cause

## Workflow

### Phase 1: REPRODUCE — make the failure happen reliably

Run the failing command, capture full output, confirm it's not flaky.

**Exit criterion:** You can make the failure happen on demand.

### Phase 2: HYPOTHESIZE — form a falsifiable hypothesis

Before investigating code, state your hypothesis explicitly:

```
HYPOTHESIS: <what you think causes the failure>
FALSIFIABLE: <how you would prove this wrong>
EVIDENCE NEEDED: <what output or state would confirm/deny>
```

If you cannot state a falsifiable hypothesis, you're guessing — go back to Phase 1.

**Hypothesis-testing loop:**

1. State hypothesis
2. Design experiment to test it
3. Run experiment
4. Accept or reject hypothesis
5. If rejected, refine or form new hypothesis
6. If accepted, proceed to REDUCE

**Never proceed to FIX without a confirmed hypothesis.**

### Phase 3: LOCALIZE — find where the failure originates

Read the error, check the stack trace (first frame in YOUR code), check if regression.

**Exit criterion:** You know the exact file, line, and condition that causes the failure.

### Phase 4: REDUCE — shrink to the minimal failing case

Remove non-essentials until the failure disappears; the last thing removed is the cause.

**Exit criterion:** Smallest possible reproduction that demonstrates the bug.

### Phase 5: FIX — fix root cause, not symptom

Write test (RED), implement fix (GREEN), refactor if needed. Run full suite.

**Exit criterion:** Bug is fixed, test passes, full suite passes.

### Phase 6: REGRESSION PREVENTION — ensure the fix doesn't break anything else

Run the regression prevention checklist (see below). If any check fails, return to Phase 1.

**Exit criterion:** All regression checks pass, hypothesis confirmed, fix is permanent.

### Phase 7: SELF-CORRECTION LOOP — automated verification

After fixing, run an automated self-correction loop:

1. Re-run the original failing command — must pass now
2. Run the full test suite — must pass
3. Run `git diff` — verify only the intended files changed
4. Run the regression checklist — all items must pass
5. If any step fails, the self-correction loop restarts from the failing step

**Exit criterion:** All self-correction steps pass consecutively (no regressions).

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Guessing at fixes creates new bugs. Investigate first, fix second.

## The 3+ Rule

```
If you've made 3+ fix attempts that didn't work, STOP.
You're guessing. You have a deeper architectural problem.
```

**When this happens:** revert all recent changes, return to REPRODUCE, gather more evidence.

## Evidence Collection

Before fixing, gather: error message, stack trace, last working state, changes since then, environment, and reproduction steps. **Never fix without evidence.**

## Regression Prevention Checklist

Before claiming the bug is fixed, run through every item:

- [ ] Can you reproduce the failure reliably?
- [ ] Do you know exactly where it fails?
- [ ] Do you know exactly why it fails?
- [ ] Did you write a test that reproduces the bug?
- [ ] Does the test fail without the fix?
- [ ] Does the test pass with the fix?
- [ ] Does the full test suite pass?
- [ ] Did you check for regressions in adjacent modules?
- [ ] Did you check for regressions in dependent services?
- [ ] Is the hypothesis documented and confirmed?
- [ ] Is the fix minimal (no extra changes)?
- [ ] Is there a test that would catch this regression if it recurs?

Can't check all boxes? You didn't fix the bug. You fixed a symptom.

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "I know what the fix is" | If you knew, it would work. Investigate. |
| "It's probably just X" | "Probably" = guessing. Verify. |
| "I'll just try this quick fix" | Quick fixes create new bugs. Investigate first. |
| "The test is wrong, not the code" | Maybe. Prove it with evidence. |
| "It works on my machine" | Prove it with reproducible steps and environment info. |

## Red Flags — STOP and Investigate

Multiple fix attempts without understanding why, fixing "nearby" code hoping it helps, skipping reproduction, ignoring error messages, adding code to suppress errors, "It works on my machine" without investigation, or fixing a symptom instead of the root cause.

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
| Hypothesis rejected 3+ times | Return to REPRODUCE. Gather more evidence. Consider architectural problem. |

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

## Self-Correction Loop (from systematic-debugging)

After any fix, run this automated loop before declaring done:

1. **Re-run the original failure** — must pass now
2. **Run the full test suite** — must pass
3. **Check the diff** — only intended files should have changed
4. **Run the regression checklist** — all items must pass
5. **If any step fails → restart the loop from the failing step**

This loop prevents the most common debugging failure mode: declaring a fix done when it's actually incomplete or introduces a new bug.

## Integration

**Use with:** `dev-craft` (BUILD TDD loop), `verification-before-completion` (verify fixes), `bug-hunting` (security vuln debugging), `quality-gates` (deterministic checks), `systematic-debugging` (hypothesis-testing framework).

## Quality Gates

- [ ] Hypothesis stated and falsifiable before investigation
- [ ] Failure reproduced reliably
- [ ] Root cause identified (not just a symptom)
- [ ] Fix is minimal and targeted
- [ ] Test added that reproduces the bug
- [ ] Test passes with the fix
- [ ] Full test suite passes
- [ ] Regression checklist fully checked
- [ ] Self-correction loop passes consecutively
- [ ] Hypothesis confirmed by evidence

## Error Handling

| Failure Mode | Response |
|--------------|----------|
| Cannot reproduce | Check environment, timing, state. Try fresh clone. |
| Hypothesis repeatedly rejected | Return to REPRODUCE, gather more evidence |
| Fix introduces new failures | Revert fix, re-investigate root cause |
| Self-correction loop fails | Restart from the failing step, do not skip |
| Context degradation suspected | Rotate context, reload relevant files only |
| 3+ failed fix attempts | Stop, suspect architectural problem, revert and re-investigate |

## References

- `references/debugging-hypothesis.md` — Hypothesis-testing template and falsification checklist
- `references/regression-checklist.md` — Expanded regression prevention checklist
- `references/self-correction-loop.md` — Automated self-correction loop protocol