---
name: quality-gates
description: "Layered quality validation pipeline: deterministic checks first, LLM judgment second. Schema validation, lint/type/test, security scan, code review, LLM-as-judge with bias mitigation."
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
| During CI/CD pipeline | Run Gates 1-3 (deterministic), optional Gates 4-5 |
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
- Gate 2 fail → HALT. Fix lint/type/test/build before anything else.
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
   ├── All expected files exist per spec/design
   ├── No missing imports (every import target exists)
   ├── No dangling symlinks
   └── Directory structure matches design plan

2. NO PLACEHOLDER CODE
   ├── No "TODO" or "FIXME" comments (configurable — allow specific tracked TODOs)
   ├── No "console.log", "print()", "debugger", "die()", "dd()"
   ├── No commented-out code blocks (> 3 consecutive commented lines)
   ├── No "as any" / "@ts-ignore" / "// eslint-disable-next-line" without justification comment
   └── No stub functions: `function foo() { throw new Error('Not implemented') }`

3. SCHEMA VALIDATION
   ├── Configuration files valid (JSON, YAML, TOML parse correctly)
   ├── Database migrations runnable (no syntax errors in SQL/migration files)
   ├── API contracts match implementation (OpenAPI spec vs actual routes)
   ├── TypeScript: tsconfig.json compiles without "paths" resolution errors
   └── Environment variable files have `.env.example` (not real secrets)
```

**Pass criteria:** All checks pass OR explicitly waived (waivers must be documented with reason and expiry).

**Output:**
```
╔══════════════════════════════════════════════════════╗
║  GATE 1: STRUCTURE                                   ║
╠══════════════════════════════════════════════════════╣
║  File Existence:  ──── PASS (14/14 expected found)   ║
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
    └── Use the per-stack config from dev-craft `references/lint-rules.md`
       (ruff UP rules for Python; ESLint id-length + no-explicit-any for TS/JS;
        clippy/gofmt/RuboCop/PSR-12 for other stacks). These enforce no
        single-char/cryptic names and no legacy/deprecated idioms.

2. TYPE CHECK
   ├── Type checker passes (tsc, mypy, pyright, flow, etc.)
   ├── Strict mode where enabled — no implicit any
   └── No type assertion casts without justification

3. TEST
   ├── Full test suite passes (unit + integration + e2e where configured)
   ├── No flaky tests identified (test passes 3/3 consecutive runs)
   ├── Coverage does not decrease from baseline (if coverage configured)
   └── New code has ≥ 80% coverage (configurable per project)

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
║  Tests:          ──── PASS (142/142, +2.1% cov)       ║
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
   ├── Every route/endpoint has auth middleware or is intentionally public
   ├── Public endpoints are explicitly documented as such
   ├── Admin routes have role/permission checks
   ├── User-scoped data is scoped to the authenticated user (no IDOR)
   ├── Auth bypass routes (login, register, password reset) have rate limiting
   └── Session/JWT tokens in httpOnly cookies (not accessible via JS)

3. INJECTION SCAN
   ├── All SQL queries use parameterized statements or ORM (no string concat)
   ├── No user input passed to exec/eval/shell commands
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
║  Auth Verify:    ──── PASS (34/34 routes verified)   ║
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

**Goal:** Apply LLM judgment to aspects of code quality that cannot be deterministically verified. This is the most expensive gate and should only run after Gates 1-4 pass.

**Core rules:**
1. **Evidence-first:** Require specific line numbers and code citations before any score
2. **No "vibe" scoring:** Every score must be justified with concrete observations
3. **Bias mitigation:** Use position swaps for pairwise reviews; length normalization for long files
4. **Confidence calibration:** Judge reports confidence level for each score (high/medium/low)

---

#### Direct Scoring (Objective Criteria)

Use when there is a clear factual basis for evaluation. Each criterion is scored independently.

**When to use direct scoring:**
- Does the code compile? (post-build verification)
- Is test coverage above threshold? (quantitative measurement)
- Does the code match the schema? (compliance verification)
- Does the code follow a specific algorithm correctly? (correctness verification)
- Is there documentation for every public API? (completeness check)

**Format:**
```
┌─────────────────────────────────────────────────────┐
│  DIRECT SCORE: [CRITERION NAME]                      │
├─────────────────────────────────────────────────────┤
│  Evidence:                                           │
│  ├── src/auth/login.ts:45-52 — JWT token expires     │
│  │   in 15 min as required by spec §3.2              │
│  └── src/auth/login.ts:88 — Refresh token rotation   │
│      implemented per security policy                 │
│                                                      │
│  Score: 9/10                                         │
│  Confidence: High                                    │
│                                                      │
│  Note: Token blacklist on logout not implemented     │
│  but not in scope for this change. Flag for follow-up│
└─────────────────────────────────────────────────────┘
```

**Scoring scale:**
| Score | Meaning |
|-------|---------|
| 10/10 | Perfect — no improvements possible |
| 8-9/10 | Excellent — minor nits only |
| 6-7/10 | Good — has some issues but acceptable |
| 4-5/10 | Marginal — significant issues need addressing |
| 1-3/10 | Poor — fundamental problems |
| 0/10 | Fails basic requirements |

---

#### Pairwise Scoring (Subjective Criteria)

Use when evaluation requires comparison or taste. Two implementations are compared side-by-side.

**When to use pairwise scoring:**
- Code style and readability (which is cleaner?)
- Architecture decisions (which approach is more maintainable?)
- API design (which interface is more intuitive?)
- Component composition (which is more reusable?)
- Naming conventions (which names are clearer?)

**Format:**
```
┌─────────────────────────────────────────────────────┐
│  PAIRWISE: Code Readability                          │
├─────────────────────────────────────────────────────┤
│  Variant A: src/feature/v1/service.ts               │
│  Variant B: src/feature/v2/service.ts               │
│                                                      │
│  Evidence A:                                         │
│  ├── service.ts:15 — Single responsibility:          │
│  │   `processOrder()` only handles order flow        │
│  └── service.ts:30 — Clear error paths with          │
│      early returns                                   │
│                                                      │
│  Evidence B:                                         │
│  ├── service.ts:12 — `handle()` does both order      │
│  │   and payment logic in one function               │
│  └── service.ts:45 — Deeply nested if/else           │
│      (4 levels)                                      │
│                                                      │
│  Winner: Variant A                                   │
│  Confidence: High                                    │
│  Reasoning: A has clearer separation of concerns,    │
│  fewer nesting levels, and more descriptive names.   │
│  B's combined handler makes testing harder.          │
└─────────────────────────────────────────────────────┘
```

---

#### Bias Mitigation

LLM-as-judge is powerful but has known biases. These mitigations are mandatory.

| Bias | Mitigation | Implementation |
|------|-----------|----------------|
| **Position bias** | Swap order for pairwise reviews | Run pairwise twice: A→B and B→A. If results differ, flag for human review. |
| **Length bias** | Normalize for longer responses | Require evidence-per-line-count ratio. A 200-line file should have proportionally more evidence than a 20-line file. |
| **Verbosity bias** | Penalize unnecessarily verbose code | In pairwise scoring, add "succinctness" as a criterion. Fluff counts against score. |
| **First-impression bias** | Require full file read | Judge must read the entire file before scoring. Partial reads invalidate the evaluation. |
| **Anchor bias** | Independent scoring | For direct scoring, score each criterion independently. Do not let one criterion's score influence another. |
| **Self-consistency bias** | 3-shot sampling | For critical evaluations, run the judge 3 times with the same prompt. If scores vary by > 2 points, flag for human review. |
| **Recency bias** | Random file order | When evaluating multiple files, randomize the order to prevent recency effects. |

**Position swap protocol:**
```
1. Present Variant A first, Variant B second → score
2. Present Variant B first, Variant A second → score
3. Compare results
   ├── Same winner? → Accept with higher confidence
   ├── Different winner? → Flag for human review (evidence likely too close)
   └── Score diff > 2? → Flag — bias detected, escalate
```

---

#### Evidence-First Protocol

**Purpose:** Prevent "vibe-based" scoring where the judge gives a score without being able to point to specific code.

**Rules:**
1. **Cite first, score second.** The entire evidence section must be written before any score.
2. **Line numbers are mandatory.** Every evidence point must include a file and line number.
3. **Code snippets required** for any claim about correctness or convention violations.
4. **No "it feels like" or "it seems like"** — every claim must reference observable code.
5. **Missing evidence = invalid score.** If evidence cannot be produced, score is N/A.

**Example (invalid):**
```
Score: 7/10
Reasoning: The code is fairly well-structured but could be cleaner.
```
→ REJECTED. No evidence, no line numbers, no specific claims.

**Example (valid):**
```
Evidence:
- src/orders.ts:22-30 — `calculateTotal()` uses a single
  reduce() call. Clear, functional, tested.
- src/orders.ts:55-60 — `applyDiscount()` modifies the
  original array instead of returning a new one. This
  caused a bug in the invoice module (see issue #142).

Score: 6/10
Confidence: Medium
Reasoning: One clear function, one bug-introducing
mutation. Score reflects the mutation issue.
```
→ ACCEPTED. Specific, observable, actionable.

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
# Quality Report: [Feature/Branch Name]

**Commit:** `abc1234`
**Date:** 2026-07-14
**Duration:** 2m 34s
**Configuration:** `.quality-gates.json` v1

---

## Results

| Gate | Status | Duration | Details |
|------|--------|----------|---------|
| 1. Structure | ✅ PASS | 0.8s | 3/3 checks passed |
| 2. Deterministic | ✅ PASS | 12.4s | lint/type/test/build all green |
| 3. Security | ✅ PASS | 2.1s | 0 secrets, 0 injection vectors |
| 4. Convention | ⚠ PASS | 1.5s | 1 advisory (see details) |
| 5. LLM-Judge | ✅ PASS | 18.2s | direct: 8.5/10, pairwise: clean |

**Overall: ✅ PASS** — All gates passed. Ready for merge.

---

## Gate Details

### Gate 1: Structure
| Check | Status | Detail |
|-------|--------|--------|
| File Existence | ✅ | 14/14 expected files found, 0 missing |
| Placeholder Scan | ✅ | 0 violations |
| Schema Valid | ✅ | All configs valid, migration parses |

### Gate 2: Deterministic
| Check | Status | Detail |
|-------|--------|--------|
| Lint | ✅ | 0 errors, 2 warnings (config max: 5) |
| Type Check | ✅ | strict mode, 0 errors |
| Tests | ✅ | 142/142 pass, coverage +2.1% |
| Build | ✅ | 2.1s, bundle +3.2% (limit: 10%) |

### Gate 3: Security
| Check | Status | Detail |
|-------|--------|--------|
| Secrets Scan | ✅ | 0 secrets in tracked files |
| Auth Verify | ✅ | 34/34 routes have auth or are intentional public |
| Injection Scan | ✅ | 0 injection vectors |

### Gate 4: Convention
| Check | Status | Detail |
|-------|--------|--------|
| File Organization | ✅ | Follows existing pattern |
| Naming | ⚠ | `user-service.ts:42` — PascalCase utility function, project uses camelCase |
| Imports/Exports | ✅ | Matches project |
| Error Handling | ✅ | Matches project pattern |
| Code Structure | ✅ | Follows existing patterns |

### Gate 5: LLM-Judge

#### Direct Scoring
| Criterion | Score | Confidence | Summary |
|-----------|-------|------------|---------|
| Schema Compliance | 9/10 | High | All types match OpenAPI spec. Minor: missing `description` on 2 fields. |
| Test Coverage | 8/10 | High | 85% coverage on new code. Missing edge case test for empty state. |
| Compilation | 10/10 | High | Build produces zero warnings. |

#### Pairwise Scoring
| Criterion | Winner | Confidence | Summary |
|-----------|--------|------------|---------|
| Readability | Variant A | High | Cleaner separation of concerns |
| Architecture | Variant A | Medium | Both valid; A is more idiomatic for the codebase |

---

## Recommendations

1. **Advisory:** Fix naming on `src/feature/user-service.ts:42` to match camelCase convention (low priority, non-blocking).
2. **Suggestion:** Add empty-state test for order list component (improves coverage to 92%).
3. **Follow-up:** Token blacklist on logout out of scope for this change — create tracked issue.

---

## Gate Configuration Used

- shortCircuit: true (stopped on first failure? No — all passed)
- autoFix: enabled, 0 iterations needed
```

---

## Common Gotchas

### 1. Judge Sensitivity to Prompt Wording

**Problem:** LLM judges are highly sensitive to how scoring criteria are phrased. Changing "rate code quality" to "rate code maintainability" can change scores by 2+ points.

**Solution:**
- Use fixed, versioned prompt templates stored in `.quality-gates/prompts/`
- Never ad-lib the judge prompt
- Template: `evaluate-code-v3.md` with frozen wording
- Prompt changes require team review + version bump

### 2. Rubric Drift

**Problem:** Over time, the judge's scoring standards drift. What was a 7/10 last month is now a 5/10 because the judge got stricter (or lazier).

**Solution:**
- Calibrate weekly against a held-out set of 10 reference code samples
- Track score distribution over time — if mean shifts > 1 point, investigate
- Re-run rubric calibration against human-annotated gold standard every month
- Store calibration results in `.quality-gates/calibration.json`

### 3. Confidence Calibration

**Problem:** Judges may be overconfident (saying "High" confidence when evidence is thin) or underconfident (saying "Low" when correct).

**Solution:**
- Track judge accuracy per confidence level:

```
Confidence Level | Accuracy | Frequency
-----------------|----------|----------
High             | 94%      | 45% of scores
Medium           | 82%      | 35% of scores
Low              | 65%      | 20% of scores
```

- If "High" confidence accuracy falls below 90%, flag for investigation
- If "Low" confidence is used more than 30% of the time, the judge may need retuning

### 4. False Positives / False Negatives

**Problem:** Judges may flag things that aren't problems (false positive) or miss real issues (false negative).

**Solution:**
- Track false positive rate per gate
- If false positive rate > 20%, relax that gate's criteria
- If false negative rate > 10%, tighten that gate's criteria
- NEVER auto-block on judge findings — always require human verification for rejections

### 5. Position Bias in Practice

**Problem:** Even with position swaps, bias can persist if the two variants differ significantly in length.

**Solution:**
- Add `lengthRatio` to pairwise output: if Variant A is 3× longer than Variant B, flag for review
- Judge must explicitly account for length differences: "Variant A is longer because it handles 3 additional edge cases"
- If both position-swap runs agree, confidence increases. If they disagree, hard-block for human review.

### 6. Context Window Limits

**Problem:** Large files or large diffs may exceed the judge's context window, causing incomplete evaluation.

**Solution:**
- Break large diffs into chunks of ≤ 500 lines each
- Evaluate each chunk independently
- Aggregate scores using min (conservative) or mean (balanced) — configurable
- Flag in report: "File was evaluated in 3 chunks"

### 7. Latency Impact

**Problem:** LLM judge calls can take 10-60 seconds per evaluation, slowing down CI.

**Solution:**
- Run Gates 1-4 in CI (fast path)
- Run Gate 5 on-demand or asynchronously
- Cache identical judge evaluations (same code, same prompt → same result)
- Use cheaper models for low-confidence evaluations, expensive models for high-stakes

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
- A configurable pass/fail framework for CI/CD

---

## Integration with code-review-and-quality

The `code-review-and-quality` skill and this `quality-gates` skill are complementary:

| Aspect | code-review-and-quality | quality-gates |
|--------|------------------------|---------------|
| **Focus** | Eight-axis qualitative review | Layered quantitative pipeline |
| **When** | During dev-craft REVIEW | Pre-merge / CI / full quality assurance |
| **Approach** | Human-structured review | Automated gates + LLM judge |
| **Output** | Findings with severity | Pass/fail per gate with evidence |
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
- `performance-optimization` — Performance gate extension for Gate 2
- `ai/agents/dev.md` — Developer agent instructions
