---
name: tdd-enforcer
description: Use when you need to enforce strict Test-Driven Development (RED-GREEN-REFACTOR) in the dev-craft BUILD phase. No production code without a failing test first.
model: big-pickle
version: 1.0.0
preamble-tier: 1
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "tdd"
  - "test driven development"
  - "red green refactor"
  - "test first"
  - "enforce tdd"
metadata:
  origin: agent-master-skills
  plugin-for: dev-craft
  phase: BUILD
  preferred-model: big-pickle
---

<!-- TOKEN CEILING: ~5K -->

# TDD Enforcer Plugin

## Overview

This plugin wraps the dev-craft BUILD phase to make TDD non-optional. Every slice follows:
**RED → VERIFY RED → GREEN → VERIFY GREEN → REFACTOR → VERIFY GREEN**

If you skip any step, you are not doing TDD. Delete code and start over.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

## RED - Write Failing Test

Write one minimal test showing what should happen.

<Good>
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
Clear name, tests real behavior, one thing
</Good>

<Bad>
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```
Vague name, tests mock not code
</Bad>

**Requirements:**
- One behavior per test
- Clear name describing behavior (not "test1", "works")
- Real code (no mocks unless genuinely unavoidable)

## VERIFY RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
# Run the specific test
npm test path/to/test.test.ts
```

Confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature is missing (not typos, not setup issues)

**Test passes?** You're testing existing behavior. Fix the test.

**Test errors?** Fix error, re-run until it fails correctly.

## GREEN - Minimal Code

Write simplest code to pass the test.

Don't add features, refactor other code, or "improve" beyond the test. See the RED step above for an example of minimal test-first code.

## VERIFY GREEN - Watch It Pass

**MANDATORY.**

```bash
npm test path/to/test.test.ts
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

**Test fails?** Fix code, not test.

**Other tests fail?** Fix now.

## REFACTOR - Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately (didn't watch it fail)
- Can't explain why test failed
- Tests added "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Integration with dev-craft BUILD Phase

In dev-craft, for EACH slice:

```yaml
BUILD:
  - For each slice in SLICES:
    - RED: Write failing test for slice acceptance criteria
    - VERIFY RED: Run test, confirm expected failure
    - GREEN: Write minimal implementation
    - VERIFY GREEN: Run test, confirm pass + full suite green
    - REFACTOR: Clean up (only if tests stay green)
    - COMMIT: Atomic commit with message linking to slice
```

No slice is "done" until VERIFY GREEN passes.

## Verification Checklist

Before marking any slice complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if genuinely unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Debugging Integration

Bug found? Write failing test reproducing it. Follow TDD cycle. Test proves fix and prevents regression.

Never fix bugs without a test.

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without your human partner's permission.
