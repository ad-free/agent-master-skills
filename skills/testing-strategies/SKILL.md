---
name: testing-strategies
description: |
  Use when deciding WHAT kind of test to write for a change — unit vs integration vs e2e vs contract vs property-based, and what failure mode each test covers.
  Do NOT use for "did tests pass" (see verification-before-completion) or "review my test coverage" (see code-review-and-quality).
  Do NOT use for writing the test code itself (that's BUILD work once the test type/failure-mode is decided).
model: nemotron-3-ultra-free
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "test strategy"
  - "testing approach"
  - "what to test"
  - "test plan"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.0.0
  domain: specialized-engineering
  integrates-with: [dev-craft, ui-craft, debugging-and-error-recovery, verification-before-completion]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# testing-strategies

## Relationship to existing skills

dev-craft's TEST phase should invoke this skill BEFORE writing tests, to decide the test type and stated failure mode for each test. quality-gates runs the test plan this skill produces; code-review-and-quality judges tests against their stated failure modes; verification-before-completion runs the full suite. This skill owns the "what and why" of the test strategy, not the "how" of writing individual tests.

## Iron Law

**NO TEST WITHOUT A STATED FAILURE MODE.**

Every test must declare what specific failure it detects: "this test fails if X breaks." A test without a stated failure mode is not a test — it's a ceremony. If you can't state the failure mode, you don't know why the test exists.

## Decision tree

1. **What fails if this code is wrong?**
   - A pure function's output → **unit test** (fast, deterministic, no I/O). → `reference/unit-test-patterns.md`
   - A database query or external API call → **integration test** (real DB/service or Testcontainers). → `reference/integration-test-patterns.md`
   - A user-facing flow across the stack → **e2e test** (Playwright/Cypress, critical paths only). → `reference/e2e-test-patterns.md`
   - A contract between producer/consumer (API, message schema) → **contract test** (Pact for consumer-driven, schema validation for provider). → `reference/contract-test-patterns.md`
   - Complex logic with many input combinations → **property-based test** (Hypothesis/fast-check, find edge cases humans miss). → `reference/property-based-test-patterns.md`

2. **Where does this test run in CI?**
   - Unit: every PR, < 30s total
   - Integration: every PR with services (Testcontainers), < 3 min
   - Contract: consumer generates pact on PR; provider verifies on merge + can-i-deploy gate
   - E2E: nightly + on merge to main (expensive, flaky risk)
   - Property-based: every PR (fast) + nightly deep run (more iterations)

3. **What's the failure mode statement?**
   - Required for every test: `/ Failure mode: this test fails if [specific behavior] breaks`
   - Examples:
     - `/ Failure mode: this test fails if discount calculation returns wrong amount for gold tier`
     - `/ Failure mode: this test fails if /orders endpoint returns 500 when DB is down`
     - `/ Failure mode: this test fails if checkout flow doesn't send confirmation email`

4. **Flaky test protocol:**
   - If a test flakes > 1/20 runs: quarantine immediately (`@pytest.mark.flaky`), fix or delete within 48h
   - Root cause before re-enable: timing? shared state? external dependency? → `reference/flaky-test-protocol.md`

## Output

A test strategy doc for the change: list of tests to write with their type, failure mode statement, and CI stage — handed to dev-craft's TEST phase before BUILD starts.