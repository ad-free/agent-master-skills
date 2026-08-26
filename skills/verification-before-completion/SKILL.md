---
name: verification-before-completion
description: |
  Enforce fresh verification evidence before any completion claim. 5 gates: structure → deterministic → security → convention → LLM judge.
  Use MANDATORILY before claiming any task, phase, or feature complete.
  Invoked by: verifier, implementer, gatekeeper.
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
triggers:
  - "verify this is done"
  - "run verification gates"
  - "check completion"
  - "run tests and lint"
metadata:
  origin: agent-master-skills
  gates: 5
  fresh-evidence-rule: true
  preferred-model: nemotron-3-ultra-free
  integrates-with: [code-review-and-quality, dev-craft, ship, bug-hunting]
  source-enhancements: ECC verification gates (deterministic-before-LLM-judge); merged quality-gates v2.0.0
---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Verification Before Completion

## Overview

Claiming work is complete without proof is dishonesty, not efficiency.

**Core principle:** Fresh evidence or it didn't happen.

## When to Use

- Before marking a task complete
- Before committing code
- Before reporting status to your human partner
- Before moving to the next phase
- Before saying "it works"

**When NOT to use:** Never. Verification is always required.

## Invocation Protocol

**Load when:** About to claim any task, phase, or feature is complete
**Invoke via:** `skill(name="verification-before-completion")`
**Resume to:** Continue to next phase or mark task complete

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

"Tests pass" is not evidence unless you just ran them.
"It should work" is not evidence.
"I think it's done" is not evidence.

## Verification Requirements

### What Counts as Evidence

| Evidence Type | Valid | Invalid |
|---------------|-------|---------|
| Test output from this session | Fresh run, captured output | "Tests were passing earlier" |
| Lint output from this session | Fresh run, zero errors | "I didn't change those files" |
| Build output from this session | Fresh build, success | "It built before" |
| Manual test with screenshots | You tested it yourself | "It should work" |
| Type checker output | Fresh run, no errors | "Types look right" |

### What Does NOT Count

- "I'm pretty sure it works"
- "It worked in my head"
- "The code looks correct"
- "I didn't change anything that could break it"
- "It was working before"
- "I tested it mentally"

## Verification Checklist

Before any completion claim, you MUST check all boxes with **fresh** output from this session:

```
VERIFICATION EVIDENCE:
- [ ] Tests: [command] → [X passed, Y failed]
- [ ] Lint: [command] → [0 errors]
- [ ] Type check: [command] → [0 errors]
- [ ] Build: [command] → [success]
- [ ] Manual test: [what you tested and result]
```

## The Fresh Evidence Rule

```
Evidence older than your last code change is INVALID.
```

**Timeline:**
1. You write/modify code
2. You run tests → they pass (evidence captured)
3. You modify MORE code
4. Step 2 evidence is now INVALID
5. You must re-run tests to get FRESH evidence

**Exception:** Evidence from after the LAST code change is fresh.

## Completion Claim Format

When claiming work is complete, you MUST provide:

```
COMPLETION CLAIM:
Feature: [what was built/fixed]
Evidence:
- Tests: [command] → [output summary]
- Lint: [command] → [0 errors]
- Type check: [command] → [0 errors]
- Build: [command] → [success]
- Manual: [what you verified]
Status: COMPLETE
```

**No evidence = no completion claim.**

## Common Rationalizations

| Rationalization | Reality |
|----------------|---------|
| "I just ran them 5 minutes ago" | Code changes invalidate old evidence. Re-run. |
| "The tests would catch it" | Only if you run them. Run them. |
| "I didn't change anything that could break it" | How do you know? Run the tests. |
| "It's obvious it works" | Obvious to you ≠ verified. Prove it. |
| "Running tests takes too long" | Debugging later takes longer. Run them. |
| "I'll verify at the end" | You won't. Or you'll find 10 bugs. Verify now. |
| "My human partner trusts me" | Trust is built on evidence, not claims. Show proof. |
| "It's just a small change" | Small changes break things. Verify. |

## Red Flags — STOP and Verify

- About to say "done" without running tests
- About to commit without lint/type check
- About to move to next phase without evidence
- About to report status without proof
- "I'm confident it works"
- "It should be fine"
- "I'll verify later"

**All of these mean: Run the verification now.**

## Verification Gates (from ECC - Deterministic Before LLM Judge)

Apply the Verification Checklist at three points: before changes (baseline tests pass), after each slice (new + existing tests, lint, type, build), and before claiming done (full suite + manual verification + no debug artifacts). Before committing, also run a secrets scanner and ensure no dead code remains.

### Gate 0: Schema & Token Ceiling (Pre-Gate)

Catch structural/schema issues and token budget problems BEFORE any other gate runs. This gate runs instantly and catches failures that would make downstream gates meaningless.

```
1. SCHEMA VALIDATION
   - JSON/YAML/TOML configs parse without errors
   - TypeScript: tsconfig.json valid, no "paths" resolution errors
   - Database migrations: SQL syntax valid, no dangling references
   - API contracts: OpenAPI/GraphQL schema valid
   - Package manifests: package.json, Cargo.toml, pyproject.toml valid
   - State files: .dev-craft/state.json valid JSON

2. TOKEN CEILING GUARDRAIL (from gstack)
   - Estimate skill/agent context load
   - Warning at 40K tokens (~160KB) — "Watch for feature bloat"
   - Hard stop at 80% context window — "Context rotation required"
   - Philosophy: "Modern models have 200K-1M windows, but 40K skill content is the limit for focus"
```

**Pass criteria:** All schemas valid. Token usage within budget. If token budget exceeded → trigger `context-engineering` rotation protocol.

### Gate Ordering (CRITICAL - Deterministic First)

**NEVER invoke LLM judge (Gate 5) if Gates 1-4 fail.**

```
Gate 1: STRUCTURE      → Gate 2: DETERMINISTIC  → Gate 3: SECURITY
    │                        │                        │
    ▼                        ▼                        ▼
Gate 4: CONVENTION   → Gate 5: LLM-JUDGE     → [COMPLETE]
```

| Gate | Name | Checks | Must Pass Before |
|------|------|--------|------------------|
| 0 | Schema & Token | Configs parse, token budget within ceiling | Gate 1 |
| 1 | Structure | Files exist, git clean, configs valid | Gate 2 |
| 2 | Deterministic | Tests, Lint, Typecheck, Build | Gate 3 |
| 3 | Security | Secrets scan, dependency audit | Gate 4 |
| 4 | Convention | Format, commit msg, branch name | Gate 5 |
| 5 | LLM Judge | Code review quality, architecture alignment | — |

This prevents expensive LLM evaluations on code that fails basic checks.

**Why deterministic-first:**
- **Cost:** LLM evaluation is 100-1000x more expensive than running `tsc --noEmit`
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

### Gate 1: Structure

**Goal:** Verify the codebase is complete enough to evaluate. No point linting files that don't exist.

```
1. FILE EXISTENCE
   - All expected files exist per spec/design
   - No missing imports (every import target exists)
   - No dangling symlinks
   - Directory structure matches design plan

2. NO PLACEHOLDER CODE
   - No "TODO" or "FIXME" comments (configurable — allow specific tracked TODOs)
   - No "console.log", "print()", "debugger", "die()", "dd()"
   - No commented-out code blocks (> 3 consecutive commented lines)
   - No "as any" / "@ts-ignore" / "eslint-disable-next-line" without justification comment
   - No stub functions: `function foo() { throw new Error('Not implemented') }`

3. SCHEMA VALIDATION
   - Configuration files valid (JSON, YAML, TOML parse correctly)
   - Database migrations runnable (no syntax errors in SQL/migration files)
   - API contracts match implementation (api-contract.md vs actual routes)
   - TypeScript: tsconfig.json compiles without "paths" resolution errors
   - Environment variable files have `.env.example` (not real secrets)
```

**Pass criteria:** All checks pass OR explicitly waived (waivers must be documented with reason and expiry).

### Gate 2: Deterministic

**Goal:** All machine-verifiable quality checks pass. These are binary — pass or fail — with no subjectivity.

```
1. LINT
   - Linter passes with zero errors (configurable: warnings may be allowed)
   - Formatter passes (code is idempotent under formatter)
   - No lint rule disable comments without team-approved exception list
   - Use per-stack config from dev-craft `references/lint-rules.md`
     (ruff UP rules for Python; ESLint id-length + no-explicit-any for TS/JS;
      clippy/PSR-12 for other stacks)

2. TYPE CHECK
   - Type checker passes (tsc, mypy, pyright, flow, etc.)
   - Strict mode where enabled — no implicit any
   - No type assertion casts without justification

3. TEST
   - Full test suite passes (unit + integration + e2e where configured)
   - No flaky tests identified (test passes 3/3 consecutive runs)
   - Coverage does not decrease from baseline (if coverage configured)

4. BUILD
   - Production build succeeds
   - Bundle size within budget (if configured)
   - No new build warnings (or all warnings are tracked exceptions)
```

**Pass criteria:** All four check categories must pass. No exceptions. If lint fails, the pipeline stops — do not run tests.

### Gate 3: Security

**Goal:** Identify security vulnerabilities that deterministic tools miss. Scans for secrets, auth gaps, and injection vectors.

**Review Subagent Integration:** Consumes findings from `review-orchestrator`'s `security-reviewer` subagent (at `.dev-craft/review-findings/security-reviewer.json`). Also leverages `bug-hunting` for deep security audit.

```
1. SECRETS SCAN
   - No API keys, tokens, passwords in source files
   - No private keys (RSA, EC, SSH, PGP) in tracked files
   - No `.env` file committed (must be in .gitignore)
   - No hardcoded JWT secrets, signing keys, or encryption keys
   - No cloud provider credentials (AWS_ACCESS_KEY, GCP service account, etc.)
   - No OAuth tokens, webhook secrets, or session secrets
   - No connection strings with inline credentials

2. AUTH VERIFICATION
   - Every route/endpoint has auth middleware or is intentionally public
   - Public endpoints are explicitly documented as such
   - Admin routes have role/permission checks
   - User-scoped data is scoped to the authenticated user (no IDOR)
   - Auth bypass routes (login, register, password reset) have rate limiting
   - Session/JWT tokens in httpOnly cookies (not accessible via JS)

3. INJECTION SCAN
   - All SQL queries use parameterized statements or ORM (no string concat)
   - No user input passed to exec/shell commands
   - File paths from user input are validated and restricted
   - HTML output is escaped or uses safe rendering APIs
   - API responses include no secrets or stack traces in error bodies
   - User-uploaded files: type-whitelisted, size-limited, outside web root
```

**Pass criteria:** Zero secrets found. All routes verified. No injection vectors. Any finding blocks merge.

### Gate 4: Convention

Delegated to `code-review-and-quality` Axis 8:

- Load `skill(name="code-review-and-quality")`
- Run Axis 8 (Conventions) check
- Apply findings as Gate 4 results

Gate 4 passes when `code-review-and-quality` Axis 8 passes with no Required or Critical findings.

**Review Subagent Integration:** Consumes findings from `review-orchestrator`'s `style-reviewer` subagent (at `.dev-craft/review-findings/style-reviewer.json`). Style findings feed into convention checking. Also delegates to `language-rules` plugin for language-specific conventions.

### Gate 5: LLM-Judge

**Goal:** Apply LLM judgment to code quality aspects that cannot be deterministically verified. This is the most expensive gate and should only run after Gates 1-4 pass.

**Core rules:**
1. **Evidence-first:** Require specific line numbers and code citations before any score
2. **No "vibe" scoring:** Every score must be justified with concrete observations
3. **Bias mitigation:** Use position swaps for pairwise reviews
4. **Confidence calibration:** Judge reports confidence level for each score

Load `references/llm-judge-protocol.md` for full protocol: direct scoring, pairwise scoring, bias mitigation table, position swap protocol, and evidence-first rules.

**Review Subagent Integration:** Consumes all aggregated review findings from `review-orchestrator` at `.dev-craft/review-findings/aggregated.json`. The LLM judge evaluates whether all findings have been adequately addressed or documented as accepted risks.

## Gate Configuration

Per-project configuration for which gates are required, optional, or skipped. Store as `.verification-before-completion.json` at project root:

```json
{
  "version": 1,
  "gates": {
    "structure": { "required": true, "checks": { "placeholder": { "allowList": ["TODO: tracked in JIRA-123"] } } },
    "deterministic": { "required": true, "checks": { "lint": { "maxWarnings": 5 }, "test": { "coverageThreshold": 80 } } },
    "security": { "required": true, "checks": { "secrets": { "excludePatterns": ["*.test.ts"] } } },
    "convention": { "required": false, "checks": { "naming": { "severity": "warn" } } },
    "llmJudge": { "required": false, "checks": { "direct": { "enabled": true }, "confidenceThreshold": "high" } }
  },
  "shortCircuit": true,
  "autoFix": { "enabled": true, "maxIterations": 3 }
}
```

| Scenario | structure | deterministic | security | convention | llmJudge |
|----------|-----------|---------------|----------|------------|----------|
| CI fast-lane | required | required | required | skipped | skipped |
| Full pre-merge | required | required | required | required | required |
| Release gate | required | required | required | required | required |
| Prototype | required | optional | optional | skipped | skipped |
| Hotfix | required | required | required | skipped | skipped |
| Code review only | required | required | required | required | optional |

**Common gotchas:** See `references/quality-gate-gotchas.md`.

## The Verification Script

For any completion claim, run:

```bash
# Replace with your project's actual commands
npm test && npm run lint && npm run typecheck && npm run build
```

**Capture the output. Include it in your completion claim.**

## When Failing Verification

If verification fails:

1. **Stop** — do not claim completion
2. **Diagnose** — use debugging-and-error-recovery skill
3. **Fix** — address the failure
4. **Re-verify** — run the full verification again
5. **Repeat** — until all gates pass

**Never claim completion with failing verification.**

## Integration

**Use with:**
- `dev-craft` Phase 5 BUILD (TDD loop) — Tests provide verification evidence; REVIEW phase invokes these gates
- `debugging-and-error-recovery` — Fix failures before verifying
- `code-review-and-quality` — Review includes verification evidence; feeds findings into Gate 4
- `review-orchestrator` + `review-subagents` — Parallel subagents provide findings for Gate 3 (security) and Gate 4 (convention); Gate 5 (LLM-Judge) consumes all aggregated findings
- `bug-hunting` — Security verification gates before completion claim; deep security inspection feeds Gate 3
- `ship` — pre-merge CI gate

**Output:** Produce a consolidated quality report: gate-by-gate pass/fail with check details and recommendations.