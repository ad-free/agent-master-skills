---
name: eval-harness
description: |
  Use when running golden test cases against each skill to verify behavior and catch regressions.
  CI gate for skill changes. Implements Eval-Driven Development (EDD) with pass@k metrics,
  capability/regression evals, and code/model/human grader types.
model: gpt-5-nano
version: 2.1.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - "evaluate skill"
  - "test skill"
  - "run eval"
  - "benchmark skill"
  - "eval-driven development"
  - "pass@k"
  - "capability eval"
  - "regression eval"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 2.1.0
  domain: quality-safety
  integrates-with: [verification-before-completion, code-review-and-quality, agent-eval]
  source-enhancements: v2.1.0 EDD + pass@k from ECC eval-harness
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Eval Harness

## Overview

Automated evaluation framework that tests each skill against curated golden test cases. Runs in CI to prevent skill regressions. Each skill defines its own test cases; the harness executes them and compares outputs. Implements Eval-Driven Development (EDD) principles.

**Core principle:** Skills must prove they work — not just claim they do.

---

## Eval-Driven Development (EDD)

Treat evals as the "unit tests of AI development":

- **Define expected behavior BEFORE implementation** — success criteria first
- **Run evals continuously during development** — catch regressions early
- **Track regressions with each change** — every skill change runs the eval suite
- **Use pass@k metrics for reliability** — measure what actually works

### Eval Types

#### Capability Evals
Test if a skill can do something new:
```markdown
[CAPABILITY EVAL: feature-name]
Task: Description of what the skill should accomplish
Success Criteria:
  - [ ] Criterion 1
  - [ ] Criterion 2
Expected Output: Description of expected result
```

#### Regression Evals
Ensure changes don't break existing functionality:
```markdown
[REGRESSION EVAL: feature-name]
Baseline: SHA or checkpoint name
Tests:
  - existing-test-1: PASS/FAIL
  - existing-test-2: PASS/FAIL
Result: X/Y passed (previously Y/Y)
```

---

## Grader Types

### 1. Code-Based Grader (deterministic — prefer first)
```bash
# Check if file contains expected pattern
grep -q "export function handleAuth" src/auth.ts && echo "PASS" || echo "FAIL"

# Check if tests pass
npm test -- --testPathPattern="auth" && echo "PASS" || echo "FAIL"

# Check if build succeeds
npm run build && echo "PASS" || echo "FAIL"
```

### 2. Rule-Based Grader
Regex/schema constraints:
```yaml
assertions:
  - type: "equals"
    path: "$.state.topology"
    expected: "mono"
  - type: "matches"
    path: "$.version"
    expected: "^2\\.\\d+\\.\\d+$"
```

### 3. Model-Based Grader (LLM-as-judge)
```markdown
[MODEL GRADER PROMPT]
Evaluate the following output:
1. Does it solve the stated problem?
2. Is it well-structured?
3. Are edge cases handled?
4. Is error handling appropriate?

Score: 1-5 (1=poor, 5=excellent)
Reasoning: [explanation]
```

### 4. Human Grader
Flag for manual review:
```markdown
[HUMAN REVIEW REQUIRED]
Change: Description of what changed
Reason: Why human review is needed
Risk Level: LOW/MEDIUM/HIGH
```

---

## pass@k Metrics

### pass@k — "At least one success in k attempts"
- `pass@1`: First attempt success rate (direct reliability)
- `pass@3`: Success within 3 attempts (practical reliability)
- Typical target: pass@3 ≥ 90% for capability evals

### pass^k — "All k trials succeed"
- Higher bar for reliability (stability test)
- `pass^3`: 3 consecutive successes
- Target: pass^3 = 100% for release-critical regression paths

### Recommended Thresholds
| Eval Type | Metric | Threshold |
|-----------|--------|-----------|
| Capability | pass@3 | ≥ 0.90 |
| Regression (release-critical) | pass^3 | = 1.00 |
| Regression (general) | pass@1 | ≥ 0.95 |

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

| Metric | Target | When |
|--------|--------|------|
| pass@1 | ≥ 90% | Every eval run |
| pass@3 | ≥ 90% | Capability evals |
| pass^3 | = 100% | Release-critical regression |
| Coverage | Per-skill cases exercised | Every skill change |
| Token budget | Phase completes within budget | Performance evals |
| Time | Each case < timeout (default 60s) | CI gate |
| Cost per task | $, tracked when model-API available | Benchmark mode |

---

## Eval Workflow

### 1. Define (Before Coding)
```markdown
## EVAL DEFINITION: feature-xyz

### Capability Evals
1. Can create new user account
2. Can validate email format
3. Can hash password securely

### Regression Evals
1. Existing login still works
2. Session management unchanged

### Success Metrics
- pass@3 > 90% for capability evals
- pass^3 = 100% for regression evals
```

### 2. Implement
Write code to pass the defined evals.

### 3. Evaluate
```bash
eval-harness run --skill dev-craft
```

### 4. Report
```markdown
EVAL REPORT: feature-xyz
========================

Capability Evals:
  create-user:     PASS (pass@1)
  validate-email:  PASS (pass@2)
  hash-password:   PASS (pass@1)
  Overall:         3/3 passed

Regression Evals:
  login-flow:      PASS
  session-mgmt:    PASS
  Overall:         2/2 passed

Metrics:
  pass@1: 100% (5/5)
  pass@3: 100% (5/5)

Status: READY FOR REVIEW
```

---

## Eval Storage

Store evals in project:
```
skills/
  <skill-name>/
    eval/
      cases/          # YAML test case definitions
      fixtures/       # Input fixture repos/files
      expected/       # Golden output files
      results/        # Latest run results (gitignored)
      logs/           # Run history
```

Per-project evals (when evaluating against a real codebase):
```
.dev-craft/
  evals/
    <feature>.md      # Eval definition
    <feature>.log     # Eval run history
    baseline.json     # Regression baselines
```

---

## Best Practices

1. **Define evals BEFORE coding** — Forces clear thinking about success criteria
2. **Run evals frequently** — Catch regressions early
3. **Track pass@k over time** — Monitor reliability trends
4. **Use code graders when possible** — Deterministic > probabilistic
5. **Human review for security** — Never fully automate security checks
6. **Keep evals fast** — Slow evals don't get run (target < 60s each)
7. **Version evals with code** — Evals are first-class artifacts
8. **Pin golden outputs** — Update only on intentional changes
9. **Run at least 3 trials** for pass@k — agents are non-deterministic
10. **Include one deterministic judge per task** — LLM judges add noise
11. **Cost awareness** — Only run pass@k trials for cases with `pass_at_k: true`; use `gpt-5-nano` for simple evals; cache results to avoid re-runs on unchanged code

---

## Eval Anti-Patterns

- Overfitting prompts to known eval examples
- Measuring only happy-path outputs
- Ignoring cost and latency drift while chasing pass rates
- Allowing flaky graders in release gates
- Weakening a test to force a pass (Iron Law #8)
- Updating golden outputs without reviewing the diff

---

## Integration Patterns

### Pre-Implementation
```
eval-harness define <feature>
```
Creates eval definition file at `.dev-craft/evals/<feature>.md`

### During Implementation
```
eval-harness check <feature>
```
Runs current evals and reports status

### Post-Implementation
```
eval-harness report <feature>
```
Generates full eval report

### CI Gate (release)
```
eval-harness ci
```
Fails on any regression; run on skill changes

---

## References

- `references/test-case-schema.json` — YAML test case schema
- `references/ci-eval-workflow.yml` — GitHub Actions CI workflow
- `skills/agent-eval/` — Head-to-head agent comparison (sister skill)
