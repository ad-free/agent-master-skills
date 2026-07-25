---
name: quality-gates
description: Use when you need a layered quality validation pipeline (lint${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/test,
  security scan, and LLM judgment) before merging.
metadata:
  origin: agent-master-skills

---

# Quality Gates

## Overview

A layered validation pipeline inspired by advanced evaluation methodologies. Code quality is ensured through five sequential gates before any merge. Each gate is harder to pass than the last, and earlier gates must be green before later gates run. This prevents expensive LLM evaluations on code that fails basic checks.

**Core principle:** Deterministic checks first. LLM judgment second. Never waste a judge on code that can't lint.

```
Gate 1 (STRUCTURE)  ──►  Gate 2 (DETERMINISTIC)  ──►  Gate 3 (SECURITY)
      │                          │                           │
      ▼                          ▼                           ▼
  Gate 4 (CONVENTION)  ──►  Gate 5 (LLM-JUDGE)  ──►  [MERGE]
```

---

## When to Activate

| Scenario | Action |
|----------|--------|
| Before merging a PR | Run full pipeline |
| After BUILD phase completes | Run Gates 1-2 minimum |
| When quality assurance is explicitly requested | Run full pipeline |
| During CI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/CD pipeline | Run Gates 1-3 (deterministic), optional Gates 4-5 |
| Before a release | Run full pipeline |
| Code review finds systemic issues | Re-run from Gate 1 after fixes |

**When NOT to activate:** Trivial single-line changes (typos, comments, formatting-only) — Gate 1 only.

**Load via:** `skill(name="quality-gates")`

---

## The Deterministic-First Principle

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   NEVER invoke LLM judge (Gate 5) if Gates 1-4 fail.    │
│                                                         │
│   Gates 1-3 MUST be fully automated in CI.              │
│                                                         │
│   LLM judge is the MOST EXPENSIVE gate.                 │
│   Do not waste it on code that fails structure,         │
│   lint, tests, or security scans.                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Why deterministic-first:**
- **Cost:** LLM evaluation is 100-1000× more expensive than running `tsc --noEmit`
- **Speed:** Deterministic gates complete in seconds; LLM-as-judge takes 10-60s
- **Reliability:** Linters and type checkers are definitive — no hallucination risk
- **Signal-to-noise:** A failing test gives you a specific line. A failing judge gives you a paragraph.

**Short-circuit rules:**
- Gate 1 fail → HALT. No point running anything else.
- Gate 2 fail → HALT. Fix lint${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/build before anything else.
- Gate 3 fail → HALT. Security issues block merge by policy.
- Gate 4 fail → WARN. Convention violations flag but may not block (configurable).
- Gate 5 fail → REVIEW. Judge findings need human verification (judges can be wrong).

---

## The Layered Pipeline

### Gate 1: Structure

**Goal:** Verify the codebase is complete enough to evaluate. No point linting files that don't exist.

**Checks:**

```
1. FILE EXISTENCE
   ├── All expected files exist per spec${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/design
   ├── No missing imports (every import target exists)
   ├── No dangling symlinks
   └── Directory structure matches design plan

2. NO PLACEHOLDER CODE
   ├── No "TODO" or "FIXME" comments (configurable — allow specific tracked TODOs)
   ├── No "console.log", "print()", "debugger", "die()", "dd()"
   ├── No commented-out code blocks (> 3 consecutive commented lines)
   ├── No "as any" / "@ts-ignore" / "${PROJECT_ROOT}/ eslint-disable-next-line" without justification comment
   └── No stub functions: `function foo() { throw new Error('Not implemented') }`

3. SCHEMA VALIDATION
   ├── Configuration files valid (JSON, YAML, TOML parse correctly)
   ├── Database migrations runnable (no syntax errors in SQL${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/migration files)
   ├── API contracts match implementation (api-contract.md vs actual routes)
   ├── TypeScript: tsconfig.json compiles without "paths" resolution errors
   └── Environment variable files have `.env.example` (not real secrets)
```

**Pass criteria:** All checks pass OR explicitly waived (waivers must be documented with reason and expiry).

**Output:**
```
╔══════════════════════════════════════════════════════╗
║  GATE 1: STRUCTURE                                   ║
╠══════════════════════════════════════════════════════╣
║  File Existence:  ──── PASS (14${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/14 expected found)   ║
║  Placeholder Scan: ──── PASS (0 violations)           ║
║  Schema Valid:    ──── PASS (all configs valid)       ║
║  Result:          ──── ✅ PASS                        ║
╚══════════════════════════════════════════════════════╝
```

---

### Gate 2: Deterministic

**Goal:** All machine-verifiable quality checks pass. These are binary — pass or fail — with no subjectivity.

**Checks:**

 ```
 1. LINT
     ├── Linter passes with zero errors (configurable: warnings may be allowed)
     ├── Formatter passes (code is idempotent under formatter)
     └── No lint rule disable comments without team-approved exception list
     └── Use the per-stack config from dev-craft `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/lint-rules.md`
        (ruff UP rules for Python; ESLint id-length + no-explicit-any for TS${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/JS;
         clippy${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/PSR-12 for other stacks). These enforce no
         single-char${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/cryptic names and no legacy${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/deprecated idioms.

 2. TYPE CHECK
     ├── Type checker passes (tsc, mypy, pyright, flow, etc.)
     ├── Strict mode where enabled — no implicit any
     └── No type assertion casts without justification

 3. TEST
     ├── Full test suite passes (unit + integration + e2e where configured)
     ├── No flaky tests identified (test passes 3${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/3 consecutive runs)
     ├── Coverage does not decrease from baseline (if coverage configured)
     └── New code has ≥ 80% coverage (configurable per project)
     **Gate 2 runs the test plan `testing-strategies` produced — it does not
     decide test type or shape; that decision happens upstream, before BUILD.**

 4. BUILD
     ├── Production build succeeds (webpack, vite, tsc, cargo build, etc.)
     ├── Bundle size within threshold (configurable — alert if > 10% increase)
     └── No new warnings introduced
 ```

**Pass criteria:** All four check categories must pass. No exceptions. If lint fails, the pipeline stops — do not run tests.

**Output:**
```
╔══════════════════════════════════════════════════════╗
║  GATE 2: DETERMINISTIC                               ║
╠══════════════════════════════════════════════════════╣
║  Lint:           ──── PASS (0 errors, 2 warnings)    ║
║  Type Check:     ──── PASS (strict mode)              ║
║  Tests:          ──── PASS (142${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/142, +2.1% cov)       ║
║  Build:          ──── PASS (2.1s, +3.2% bundle)       ║
║  Result:         ──── ✅ PASS                          ║
╚══════════════════════════════════════════════════════╝
```

---

### Gate 3: Security

**Goal:** Identify security vulnerabilities that deterministic tools miss. Scans for secrets, auth gaps, and injection vectors.

**Checks:**

```
1. SECRETS SCAN
   ├── No API keys, tokens, passwords in source files
   ├── No private keys (RSA, EC, SSH, PGP) in tracked files
   ├── No `.env` file committed (must be in .gitignore)
   ├── No hardcoded JWT secrets, signing keys, or encryption keys
   ├── No cloud provider credentials (AWS_ACCESS_KEY, GCP service account, etc.)
   ├── No OAuth tokens, webhook secrets, or session secrets
   └── No connection strings with inline credentials

2. AUTH VERIFICATION
   ├── Every route${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/endpoint has auth middleware or is intentionally public
   ├── Public endpoints are explicitly documented as such
   ├── Admin routes have role${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/permission checks
   ├── User-scoped data is scoped to the authenticated user (no IDOR)
   ├── Auth bypass routes (login, register, password reset) have rate limiting
   └── Session${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/JWT tokens in httpOnly cookies (not accessible via JS)

3. INJECTION SCAN
   ├── All SQL queries use parameterized statements or ORM (no string concat)
   ├── No user input passed to exec${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/shell commands
   ├── File paths from user input are validated and restricted
   ├── HTML output is escaped or uses safe rendering APIs
   ├── API responses include no secrets or stack traces in error bodies
   └── User-uploaded files: type-whitelisted, size-limited, outside web root
```

**Pass criteria:** Zero secrets found. All routes verified. No injection vectors. Any finding blocks merge.

**Output:**
```
╔══════════════════════════════════════════════════════╗
║  GATE 3: SECURITY                                    ║
╠══════════════════════════════════════════════════════╣
║  Secrets Scan:   ──── PASS (0 secrets found)         ║
║  Auth Verify:    ──── PASS (34${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/34 routes verified)   ║
║  Injection Scan: ──── PASS (0 injection vectors)     ║
║  Result:         ──── ✅ PASS                        ║
╚══════════════════════════════════════════════════════╝
```

---

### Gate 4: Convention

Delegated to `code-review-and-quality` Axis 8:

- Load `skill(name="code-review-and-quality")`
- Run Axis 8 (Conventions) check
- Apply findings as Gate 4 results

Gate 4 passes when `code-review-and-quality` Axis 8 passes with no Required or Critical findings.

---

### Gate 5: LLM-Judge

**Goal:** Apply LLM judgment to code quality aspects that cannot be deterministically verified. This is the most expensive gate and should only run after Gates 1-4 pass.

**Core rules:**
1. **Evidence-first:** Require specific line numbers and code citations before any score
2. **No "vibe" scoring:** Every score must be justified with concrete observations
3. **Bias mitigation:** Use position swaps for pairwise reviews
4. **Confidence calibration:** Judge reports confidence level for each score

Load `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/llm-judge-protocol.md` for full protocol: direct scoring, pairwise scoring, bias mitigation table, position swap protocol, and evidence-first rules.

---

## Gate Configuration

Per-project configuration for which gates are required, optional, or skipped.

### Configuration Format

Store as `.quality-gates.json` at project root:

```json
{
  "version": 1,
  "gates": {
    "structure": {
      "required": true,
      "checks": {
        "placeholder": { "allowList": ["TODO: tracked in JIRA-123"] },
        "schema": { "strict": true }
      }
    },
    "deterministic": {
      "required": true,
      "checks": {
        "lint": { "maxWarnings": 5 },
        "type": { "strict": true },
        "test": { "coverageThreshold": 80, "minPass": "100%" },
        "build": { "bundleIncreaseLimit": 10 }
      }
    },
    "security": {
      "required": true,
      "checks": {
        "secrets": { "excludePatterns": ["*.test.ts"] },
        "injection": { "scanLevel": "strict" }
      }
    },
    "convention": {
      "required": false,
      "checks": {
        "naming": { "severity": "warn" },
        "errorHandling": { "severity": "error" }
      }
    },
    "llmJudge": {
      "required": false,
      "checks": {
        "direct": { "enabled": true },
        "pairwise": { "enabled": true },
        "confidenceThreshold": "high"
      }
    }
  },
  "shortCircuit": true,
  "autoFix": {
    "enabled": true,
    "maxIterations": 3
  }
}
```

### Configuration Scenarios

| Scenario | structure | deterministic | security | convention | llmJudge |
|----------|-----------|---------------|----------|------------|----------|
| CI fast-lane | required | required | required | skipped | skipped |
| Full pre-merge | required | required | required | required | required |
| Release gate | required | required | required | required | required |
| Prototype | required | optional | optional | skipped | skipped |
| Hotfix | required | required | required | skipped | skipped |
| Code review only | required | required | required | required | optional |

---

## Output Format

### Quality Report

After all gates run (or at point of failure), produce a consolidated report:

```markdown
# Quality Report: [Feature${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Branch Name]

**Commit:** `abc1234`
**Date:** 2026-07-14
**Duration:** 2m 34s
**Configuration:** `.quality-gates.json` v1

---

## Results

| Gate | Status | Duration | Details |
|------|--------|----------|---------|
| 1. Structure | ✅ PASS | 0.8s | 3${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/3 checks passed |
| 2. Deterministic | ✅ PASS | 12.4s | lint${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/build all green |
| 3. Security | ✅ PASS | 2.1s | 0 secrets, 0 injection vectors |
| 4. Convention | ⚠ PASS | 1.5s | 1 advisory (see details) |
| 5. LLM-Judge | ✅ PASS | 18.2s | direct: 8.5${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/10, pairwise: clean |

**Overall: ✅ PASS** — All gates passed. Ready for merge.

---

## Gate Details

### Gate 1: Structure
| Check | Status | Detail |
|-------|--------|--------|
| File Existence | ✅ | 14${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/14 expected files found, 0 missing |
| Placeholder Scan | ✅ | 0 violations |
| Schema Valid | ✅ | All configs valid, migration parses |

### Gate 2: Deterministic
| Check | Status | Detail |
|-------|--------|--------|
| Lint | ✅ | 0 errors, 2 warnings (config max: 5) |
| Type Check | ✅ | strict mode, 0 errors |
| Tests | ✅ | 142${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/142 pass, coverage +2.1% |
| Build | ✅ | 2.1s, bundle +3.2% (limit: 10%) |

### Gate 3: Security
| Check | Status | Detail |
|-------|--------|--------|
| Secrets Scan | ✅ | 0 secrets in tracked files |
| Auth Verify | ✅ | 34${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/34 routes have auth or are intentional public |
| Injection Scan | ✅ | 0 injection vectors |

### Gate 4: Convention
| Check | Status | Detail |
|-------|--------|--------|
| File Organization | ✅ | Follows existing pattern |
| Naming | ⚠ | `user-service.ts:42` — PascalCase utility function, project uses camelCase |
| Imports${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Exports | ✅ | Matches project |
| Error Handling | ✅ | Matches project pattern |
| Code Structure | ✅ | Follows existing patterns |

### Gate 5: LLM-Judge

#### Direct Scoring
| Criterion | Score | Confidence | Summary |
|-----------|-------|------------|---------|
| Schema Compliance | 9${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/10 | High | All types match OpenAPI spec. Minor: missing `description` on 2 fields. |
| Test Coverage | 8${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/10 | High | 85% coverage on new code. Missing edge case test for empty state. |
| Compilation | 10${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/10 | High | Build produces zero warnings. |

#### Pairwise Scoring
| Criterion | Winner | Confidence | Summary |
|-----------|--------|------------|---------|
| Readability | Variant A | High | Cleaner separation of concerns |
| Architecture | Variant A | Medium | Both valid; A is more idiomatic for the codebase |

---

## Recommendations

1. **Advisory:** Fix naming on `src${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/user-service.ts:42` to match camelCase convention (low priority, non-blocking).
2. **Suggestion:** Add empty-state test for order list component (improves coverage to 92%).
3. **Follow-up:** Token blacklist on logout out of scope for this change — create tracked issue.

---

## Gate Configuration Used

- shortCircuit: true (stopped on first failure? No — all passed)
- autoFix: enabled, 0 iterations needed
```

---

## Common Gotchas

Load `references${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/quality-gate-gotchas.md` for the full list, including: judge sensitivity to prompt wording, rubric drift, confidence calibration, FP${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/FN rates, position bias, context window limits, and latency impact.

---

## Integration with dev-craft

quality-gates runs AFTER dev-craft completes its phases:

- dev-craft BUILD → MATCH step covers conventions (Gate 4 territory)
- dev-craft REVIEW → invokes code-review-and-quality (Gate 4-5 territory)
- dev-craft HARDEN → covers security deeply (Gate 3 territory)
- dev-craft SHIP → final verification before merge

**When to run quality-gates:**

- As a pre-merge CI gate (runs all 5 gates independently)
- As a final quality check after dev-craft SHIP
- When you want LLM-Judge evaluation (Gate 5) that dev-craft doesn't provide

**quality-gates does NOT replace dev-craft's phases. It adds:**

- Deterministic pre-checks (Gates 1-2) before human review
- LLM-Judge evaluation (Gate 5) for subjective quality assessment
- A configurable pass${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fail framework for CI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/CD

---

## Integration with code-review-and-quality

The `code-review-and-quality` skill and this `quality-gates` skill are complementary:

| Aspect | code-review-and-quality | quality-gates |
|--------|------------------------|---------------|
| **Focus** | Eight-axis qualitative review | Layered quantitative pipeline |
| **When** | During dev-craft REVIEW | Pre-merge / CI / full quality assurance |
| **Approach** | Human-structured review | Automated gates + LLM judge |
| **Output** | Findings with severity | Pass${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/fail per gate with evidence |
| **Relationship** | Feeds into quality-gates | Validates review was thorough |

**Combined workflow:**

```
code-review-and-quality ──► quality-gates Gate 4 (Convention)
        │                           │
        ▼                           ▼
  Findings scored                Conventions checked
        │                           │
        └──────────┬────────────────┘
                   ▼
         Consolidated quality report
                   │
                   ▼
              Gate 5 (LLM-Judge)
                   │
                   ▼
              MERGE decision
```

---

## Verification Checklist

After running quality-gates:

- [ ] Gate 1: All expected files exist, no placeholders, all schemas valid
- [ ] Gate 2: Lint passes, type check passes, tests pass, build succeeds
- [ ] Gate 3: No secrets, auth verified on all routes, no injection vectors
- [ ] Gate 4: Code matches project conventions (naming, imports, structure, error handling)
- [ ] Gate 5: All judge evidence includes line numbers, confidence levels reported, bias mitigations applied
- [ ] Quality report generated and saved
- [ ] All Critical findings addressed (none dismissed without documented reason)
- [ ] Configuration file `.quality-gates.json` exists (or default config used)
- [ ] Judge calibration data tracked (if Gate 5 ran)

---

## See Also

- `code-review-and-quality` — Eight-axis code review (complementary)
- `dev-craft` — Full-stack engineering pipeline with REVIEW and HARDEN phases
- `debugging-and-error-recovery` — Fix issues found by quality gates
- `bug-hunting` — Deep security inspection (feeds Gate 3)
- `performance-profiling` — Performance gate extension for Gate 2