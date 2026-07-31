---
name: quality-gates
description: |
  Layered validation pipeline: Structure → Deterministic → Security → Convention → LLM Judge.
  Use before merging PRs, after BUILD phase, before releases, or in CI/CD.
  Invoked by: verifier, gatekeeper, shipper.
  
model: gpt-5-nano
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
triggers:
  - "run quality gates"
  - "validate before merge"
  - "pre-merge checks"
  - "run all checks"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 2.0.0
  domain: security-quality
  integrates-with: [verification-before-completion, code-review-and-quality, dev-craft]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~10K tokens. If skill exceeds, extract sections to references/.

# Quality Gates

## Overview

A layered validation pipeline inspired by advanced evaluation methodologies. Code quality is ensured through **six** sequential gates before any merge. Each gate is harder to pass than the last, and earlier gates must be green before later gates run. This prevents expensive LLM evaluations on code that fails basic checks.

**Core principle:** Deterministic checks first. LLM judgment second. Never waste a judge on code that can't lint.

```
Gate 0 (SCHEMA)     ──►  Gate 1 (STRUCTURE)  ──►  Gate 2 (DETERMINISTIC)  ──►  Gate 3 (SECURITY)
      │                          │                          │                           │
      ▼                          ▼                          ▼                           ▼
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
- Gate 0 fail → HALT. Invalid schema = cannot proceed.
- Gate 1 fail → HALT. No point running anything else.
- Gate 2 fail → HALT. Fix lint/build before anything else.
- Gate 3 fail → HALT. Security issues block merge by policy.
- Gate 4 fail → WARN. Convention violations flag but may not block (configurable).
- Gate 5 fail → REVIEW. Judge findings need human verification (judges can be wrong).

---

## Gate 0: Schema & Token Ceiling (Pre-Gate)

**Goal:** Catch structural/schema issues and token budget problems BEFORE any other gate runs. This gate runs instantly and catches failures that would make downstream gates meaningless.

**Checks:**

```
1. SCHEMA VALIDATION
   ├── JSON/YAML/TOML configs parse without errors
   ├── TypeScript: tsconfig.json valid, no "paths" resolution errors
   ├── Database migrations: SQL syntax valid, no dangling references
   ├── API contracts: OpenAPI/GraphQL schema valid
   ├── Package manifests: package.json, Cargo.toml, pyproject.toml valid
   └── State files: .dev-craft/state.json valid JSON

2. TOKEN CEILING GUARDRAIL (from gstack)
   ├── Estimate skill/agent context load
   ├── Warning at 40K tokens (~160KB) — "Watch for feature bloat"
   ├── Hard stop at 80% context window — "Context rotation required"
   └── Philosophy: "Modern models have 200K-1M windows, but 40K skill content is the limit for focus"

**Pass criteria:** All schemas valid. Token usage within budget. If token budget exceeded → trigger `context-engineering` rotation protocol.

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
   ├── No "as any" / "@ts-ignore" / "/ eslint-disable-next-line" without justification comment
   └── No stub functions: `function foo() { throw new Error('Not implemented') }`

3. SCHEMA VALIDATION
   ├── Configuration files valid (JSON, YAML, TOML parse correctly)
   ├── Database migrations runnable (no syntax errors in SQL/migration files)
   ├── API contracts match implementation (api-contract.md vs actual routes)
   ├── TypeScript: tsconfig.json compiles without "paths" resolution errors
   └── Environment variable files have `.env.example` (not real secrets)
```

**Pass criteria:** All checks pass OR explicitly waived (waivers must be documented with reason and expiry).

---

### Gate 3: Deterministic

**Goal:** All machine-verifiable quality checks pass. These are binary — pass or fail — with no subjectivity.

**Checks:**

 ```
 1. LINT
     ├── Linter passes with zero errors (configurable: warnings may be allowed)
     ├── Formatter passes (code is idempotent under formatter)
     └── No lint rule disable comments without team-approved exception list
     └── Use the per-stack config from dev-craft `references/lint-rules.md`
        (ruff UP rules for Python; ESLint id-length + no-explicit-any for TS/JS;
         clippy/PSR-12 for other stacks). These enforce no
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
     **Gate 2 runs the test plan `testing-strategies` produced — it does not
     decide test type or shape; that decision happens upstream, before BUILD.**

 4. BUILD
     ├── Production build succeeds (webpack, vite, tsc, cargo build, etc.)
     ├── Bundle size within threshold (configurable — alert if > 10% increase)
     └── No new warnings introduced
 ```

**Pass criteria:** All four check categories must pass. No exceptions. If lint fails, the pipeline stops — do not run tests.

---

### Gate 4: Security

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
   ├── No user input passed to exec/shell commands
   ├── File paths from user input are validated and restricted
   ├── HTML output is escaped or uses safe rendering APIs
   ├── API responses include no secrets or stack traces in error bodies
   └── User-uploaded files: type-whitelisted, size-limited, outside web root
```

**Pass criteria:** Zero secrets found. All routes verified. No injection vectors. Any finding blocks merge.

---

### Gate 5: Convention

Delegated to `code-review-and-quality` Axis 8:

- Load `skill(name="code-review-and-quality")`
- Run Axis 8 (Conventions) check
- Apply findings as Gate 4 results

Gate 4 passes when `code-review-and-quality` Axis 8 passes with no Required or Critical findings.

---

### Gate 6: LLM-Judge

**Goal:** Apply LLM judgment to code quality aspects that cannot be deterministically verified. This is the most expensive gate and should only run after Gates 1-4 pass.

**Core rules:**
1. **Evidence-first:** Require specific line numbers and code citations before any score
2. **No "vibe" scoring:** Every score must be justified with concrete observations
3. **Bias mitigation:** Use position swaps for pairwise reviews
4. **Confidence calibration:** Judge reports confidence level for each score

Load `references/llm-judge-protocol.md` for full protocol: direct scoring, pairwise scoring, bias mitigation table, position swap protocol, and evidence-first rules.

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

Produce a consolidated report: gate-by-gate pass/fail with check details and recommendations. See `references/quality-report-example.md` for the full format.

---

## Common Gotchas

See `references/quality-gate-gotchas.md`.

---

## Integration

**With dev-craft:** Runs after dev-craft SHIP or as a pre-merge CI gate. Adds deterministic pre-checks (Gates 1-2), LLM-Judge (Gate 5), and a configurable pass/fail framework.
- BUILD → MATCH covers Gate 4 territory
- REVIEW → code-review-and-quality covers Gates 4-5 territory
- HARDEN covers Gate 3 territory

**With code-review-and-quality:** code-review-and-quality feeds findings into Gate 4 (Convention); quality-gates provides the layered framework.

---

## See Also

- `code-review-and-quality` — Eight-axis code review (complementary)
- `dev-craft` — Full-stack engineering pipeline with REVIEW and HARDEN phases
- `debugging-and-error-recovery` — Fix issues found by quality gates
- `bug-hunting` — Deep security inspection (feeds Gate 3)
- `performance-profiling` — Performance gate extension for Gate 2