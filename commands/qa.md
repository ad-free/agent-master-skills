---
name: qa
description: Quality assurance — test generation → edge cases → E2E → validation
triggers:
  - "test this"
  - "qa check"
  - "generate tests"
  - "edge cases"
  - "does this work"
---

# /qa — Quality Assurance Workflow

## When to Use
- After implementation, before review
- Generating test coverage
- Validating edge cases
- E2E testing
- Pre-deployment validation

## Workflow

### 1. Test Strategy
```
skill("testing-strategies")  # Decide: unit vs integration vs E2E vs contract vs property-based
```

### 2. Test Generation
```
skill("qa-and-edge-case-tester")  # Automated E2E/unit generation, edge-case analysis, boundary testing
```

### 3. Run Tests
- Execute test suite
- Verify coverage targets met
- Check for flaky tests

### 4. Edge Case Validation
- Boundary conditions
- Null/empty inputs
- Error paths
- Concurrency/race conditions

### 5. Visual/Integration (if applicable)
```
skill("visual-regression")  # Playwright/Cypress screenshot comparison
```

### 6. Verification
```
skill("verification-before-completion")  # Fresh test evidence
```

## Output
- Test files created/updated
- Coverage report
- Edge case matrix
- Pass/fail evidence

## Completion
**DONE** — All tests pass, coverage targets met, edge cases covered
**DONE_WITH_CONCERNS** — Tests pass but [coverage gap/flaky test/known gap]
**BLOCKED** — Tests failing, infrastructure issues, or uncovered critical paths
**NEEDS_CONTEXT** — Need [test environment/test data/clarification on expected behavior]