---
name: eval-harness
description: Use when running golden test cases against each skill to verify behavior and catch regressions. CI gate for skill changes.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 2
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
triggers:
  - "evaluate skill"
  - "test skill"
  - "run eval"
  - "benchmark skill"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Eval Harness

## Overview

Automated evaluation framework that tests each skill against curated golden test cases. Runs in CI to prevent skill regressions. Each skill defines its own test cases; the harness executes them and compares outputs.

**Core principle:** Skills must prove they work — not just claim they do.

---

## Test Case Structure

Each skill can have an `eval/` directory with test cases:

```
skills/
  dev-craft/
    eval/
      cases/
        01-scope-mono-build.yaml
        02-scope-multi-fullstack.yaml
        03-phase-build-tdd.yaml
        04-phase-hardening.yaml
      fixtures/
        mono-repo/
        multi-repo-be/
        multi-repo-fe/
      expected/
        01-scope-mono-build.json
        02-scope-multi-fullstack.json
```

---

## Test Case Format

```yaml
name: "example-test"
skill: "some-skill"
version: "1.0"

setup:
  repo:
    topology: mono
    structure:
      - backend/
      - frontend/

input:
  prompt: "User request description"
  context:
    currentPhase: "SCOPE"

execution:
  phases: ["SCOPE", "BUILD"]
  mocks:
    npm_registry: true

verification:
  state:
    currentPhase: "BUILD"
  files:
    - path: ".dev-craft/state.json"
      mustExist: true
  assertions:
    - type: "equals"
      path: "$.state.topology"
      expected: "mono"

teardown:
  removeTempDirs: true
```

---

## Golden Test Categories

### 1. Regression Tests
Verify behavior hasn't changed:
- Same input → same output (deterministic phases)
- Phase transitions work correctly
- State persistence across sessions

### 2. Contract Tests
Verify skill interfaces:
- Input schema validation
- Output schema compliance
- Error handling format

### 3. Integration Tests
Verify cross-skill workflows:
- dev-craft → ui-craft handoff
- planning → dev-craft execution
- agent-orchestration → dispatching-parallel-agents

### 4. Edge Case Tests
- Invalid inputs handled gracefully
- Missing files/dependencies
- Network failures (mocked)
- Token budget exhaustion

### 5. Performance Tests
- Phase completes within token budget
- Context compaction triggers correctly
- Parallel execution works

---

## Harness CLI

```bash
# Run all skill evaluations
eval-harness run --all

# Run specific skill
eval-harness run --skill dev-craft

# Run specific test case
eval-harness run --skill dev-craft --case 01-scope-mono-build

# Update golden outputs (after intentional changes)
eval-harness update --skill dev-craft --case 01-scope-mono-build

# CI mode (fail on any regression)
eval-harness ci

# Generate report
eval-harness report --format html --output eval-report.html
```

---

## CI Integration

See `references/ci-eval-workflow.yml` for the CI workflow.

---

## Test Case Schema

The full JSON Schema is at `references/test-case-schema.json`.

---

## Writing Test Cases

### Principles

1. **One behavior per test** — Each case tests one specific skill behavior
2. **Deterministic** — Same input always produces same output
3. **Fast** — Mock external dependencies; use fixtures
4. **Readable** — Name describes what's being tested
5. **Maintainable** — Update golden outputs when behavior intentionally changes

### Example: TDD Enforcer Test

```yaml
name: "tdd-enforcer rejects code before test"
skill: "dev-craft"
phase: "BUILD"

setup:
  repo:
    structure:
      - src/
      - tests/

input:
  prompt: |
    Implement user login function in src/auth.ts

execution:
  phases: ["BUILD"]
  mocks:
    test_runner: true

verification:
  assertions:
    - type: "equals"
      path: "$.state.currentPhase"
      expected: "BUILD"
    - type: "contains"
      path: "$.agentOutput"
      expected: "RED"
    - type: "not_contains"
      path: "$.filesCreated"
      expected: "src/auth.ts"  # Code created before test = violation
  
  # Should fail if agent writes code without test first
  expectedFailure: true
```

---

## Metrics Tracked

| Metric | Target |
|--------|
