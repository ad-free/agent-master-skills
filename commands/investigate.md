---
name: investigate
description: Systematic debugging — reproduce → isolate → hypothesize → verify → fix → regress
triggers:
  - "debug this"
  - "why is this broken"
  - "fix this bug"
  - "investigate error"
  - "test failing"
---

# /investigate — Debugging Workflow

## When to Use
- Tests failing
- Unexpected behavior
- Bug reports
- Build errors
- Performance regressions

## Workflow

### 1. Capture Context
```
skill("debugging-and-error-recovery")  # Full context: trace, input, state
```

### 2. Reproduce
- Create minimal reproduction
- Document exact steps
- Confirm deterministic failure

### 3. Isolate Root Cause
- Binary search / git bisect
- Narrow to specific function/module
- Evidence-based hypotheses

### 4. Fix Cause (Not Symptom)
- Apply minimal fix at root cause
- Verify fix resolves original issue
- Check sibling callers (Iron Law #3)

### 5. Regression Test
```
skill("qa-and-edge-case-tester")  # Add test for the bug
```

### 6. Verify
```
skill("verification-before-completion")  # All gates green
```

## Output
- Root cause analysis
- Fix with minimal diff
- Regression test added
- Verification evidence

## Completion
**DONE** — Root cause fixed, regression test passes, all gates green
**DONE_WITH_CONCERNS** — Fixed but [known limitation/follow-up needed]
**BLOCKED** — Cannot reproduce, need [access/env/data], or root cause unclear after 2 rounds
**NEEDS_CONTEXT** — Need [specific error logs/env access/reproduction steps]