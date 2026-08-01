---
name: qa-and-edge-case-tester
description: |
  Automated E2E/unit test generation, edge-case analysis, boundary testing,
  and false-positive bug suppression. Use when generating tests for a
  feature, analyzing edge cases, or validating test quality. Do NOT use
  for deciding what kind of test to write (see testing-strategies) or
  for reviewing test quality after the fact (see code-review-and-quality).
  
model: big-pickle
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "generate tests"
  - "edge case testing"
  - "boundary testing"
  - "QA automation"
  - "E2E test"
  - "unit test generation"
  - "test edge cases"
  - "false positive bug"
  - "test coverage"
  - "boundary analysis"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: specialized-engineering
  integrates-with: [testing-strategies, dev-craft]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# qa-and-edge-case-tester

## Relationship to existing skills

- testing-strategies: Decides WHAT kind of test to write (unit vs integration vs e2e vs contract vs property-based); qa-and-edge-case-tester generates the actual test code and performs edge-case analysis.
- code-review-and-quality: Reviews test quality after the fact; qa-and-edge-case-tester produces tests that code-review-and-quality then reviews.
- dev-craft: Provides the engineering pipeline; qa-and-edge-case-tester is invoked during the TEST phase.
- debugging-and-error-recovery: Uses test results to identify bugs; qa-and-edge-case-tester generates the tests that debugging-and-error-recovery then uses.

## When to Use

- Generating unit tests for a new module or function
- Generating E2E tests for a new feature or user flow
- Analyzing edge cases and boundary conditions for a feature
- Writing boundary tests for input validation and error handling
- Suppressing false-positive bugs in test suites
- Improving test coverage for existing code
- Validating that test cases cover all specified failure modes
- Creating test data and mock scenarios for integration testing

## When NOT to Use

- Deciding what kind of test to write — see testing-strategies
- Reviewing test quality after the fact — see code-review-and-quality
- Debugging a failing test to find the root cause — see debugging-and-error-recovery
- Adding new features or functionality — see dev-craft
- Fixing bugs in production code — see debugging-and-error-recovery

## Workflow

### Phase 1: Test Strategy Alignment

1. **Read the testing strategy**: check if testing-strategies has been applied to this feature
2. **Identify the failure modes**: what can go wrong? (network errors, invalid input, empty state, timeout, race condition, etc.)
3. **Determine test types needed**: unit, integration, E2E, contract, property-based
4. **Identify the test framework**: Jest, Vitest, Playwright, Cypress, React Testing Library, etc.
5. **Define coverage targets**: what percentage of code paths must be covered?
6. **Get user confirmation** on the test strategy before generating tests

### Phase 2: Edge Case Analysis

1. **Identify input boundaries**: what are the min, max, and edge values for each input?
2. **Identify type boundaries**: null, undefined, empty string, zero, negative numbers, very large numbers
3. **Identify state boundaries**: initial state, loading state, error state, empty state, full state
4. **Identify timing boundaries**: fast clicks, slow network, timeout, race conditions
5. **Identify concurrency boundaries**: simultaneous actions, conflicting updates, optimistic vs pessimistic updates
6. **Identify security boundaries**: XSS, CSRF, injection, unauthorized access, privilege escalation
7. **Document all edge cases** with expected behavior for each

### Phase 3: Test Generation

1. **Generate unit tests** for each function/module:
   - Happy path tests for each function
   - Edge case tests for each identified boundary
   - Error case tests for each failure mode
   - Mock tests for external dependencies
2. **Generate integration tests** for each module interaction:
   - Happy path integration flows
   - Error propagation tests
   - Timeout and retry tests
3. **Generate E2E tests** for each user flow:
   - Happy path user journeys
   - Edge case user journeys (slow network, invalid input, etc.)
   - Error recovery user journeys
4. **Generate property-based tests** where applicable:
   - Invariant properties that should always hold
   - Fuzzing tests for input validation
5. **Generate mock data** for each test scenario

### Phase 4: False Positive Suppression

1. **Run the test suite**: identify flaky or inconsistent tests
2. **Analyze flaky tests**: determine if the flakiness is caused by:
   - Timing issues (use explicit waits instead of `sleep`)
   - Non-deterministic data (use seeded random or fixed fixtures)
   - Shared state (isolate test setup and teardown)
   - External dependencies (mock or stub external services)
3. **Fix flaky tests**: apply the appropriate fix for each flakiness cause
4. **Add stability assertions**: add checks that verify test stability before committing
5. **Document known limitations**: note any tests that are inherently flaky and why

### Phase 5: Boundary Testing

1. **Execute boundary tests**: test each identified boundary condition
2. **Verify off-by-one errors**: check array bounds, string lengths, numeric ranges
3. **Verify type coercion**: check how the system handles type mismatches
4. **Verify overflow/underflow**: check numeric boundaries and string length limits
5. **Verify empty and null inputs**: check how the system handles missing or empty data
6. **Document boundary test results**: pass/fail for each boundary condition

### Phase 6: Validation and Coverage

1. **Run the full test suite**: all tests must pass
2. **Check coverage**: verify that coverage targets are met
3. **Review test quality**: ensure tests are meaningful, not just coverage padding
4. **Check for test duplication**: remove redundant tests that test the same thing
5. **Update test documentation**: document what each test covers and why
6. **Run lint and typecheck on tests**: ensure test code follows the same quality standards as production code

## Context Management

- Track QA state in `.dev-craft/qa/<project>/state.json` with fields: `session_id`, `feature`, `test_types`, `edge_cases_identified`, `tests_generated`, `flaky_tests_fixed`, `coverage_percentage`, `status`
- On session resume, check state.json for any in-progress QA session and continue from the last completed phase

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read source code, existing tests, and test configuration | Only read project source and test files |
| Write | Create new test files and mock data | Follow the project's test conventions and naming |
| Edit | Refactor existing tests for quality or coverage | Preserve existing test behavior; never weaken tests |
| Bash | Run test suite, coverage reports, lint on tests | Must run the full test suite after generating tests |
| Grep | Find test patterns, coverage gaps, or flaky test indicators | Search within the test scope |
| Glob | Find test files and configuration | Pattern: `**/*.test.{ts,tsx,js,jsx}` |
| Task | Spawn subagent for deep edge-case analysis or flaky test investigation | Subagent must report findings, not make edits |

## Output Contract

On completion, the skill must produce:

1. Generated test files for each identified test type (unit, integration, E2E)
2. Edge case analysis document with all identified boundaries and expected behaviors
3. False positive suppression report with flaky tests fixed and stability assertions added
4. Boundary testing results document
5. Coverage report showing coverage percentage and any remaining gaps
6. Updated state.json with the QA session results
7. Test documentation describing what each test covers and why

## Quality Gates

- [ ] All identified failure modes have corresponding tests
- [ ] All edge cases have tests with expected behavior documented
- [ ] No flaky tests remain in the suite
- [ ] Coverage targets are met or exceeded
- [ ] No tests are weakened or disabled to make the suite pass
- [ ] Test code passes lint and typecheck
- [ ] Full test suite passes with all new tests
- [ ] No test duplication exists (each test covers a unique scenario)
- [ ] Boundary tests verify off-by-one, type coercion, overflow, and empty/null inputs
- [ ] Mock data conforms to the API contract

## Error Handling

- **Test generation fails for a complex module**: break the module into smaller units and generate tests for each unit separately
- **Flaky test cannot be fixed**: document the flakiness cause, add a retry mechanism or skip marker, and escalate to the user
- **Coverage target not met**: identify the uncovered code paths, generate additional tests for those paths, and re-run coverage
- **Edge case analysis misses a boundary**: re-run the analysis with a broader scope, check external references for common edge cases
- **Test suite fails after generating tests**: identify the failing test, determine if it's a test bug or a production bug, and fix accordingly