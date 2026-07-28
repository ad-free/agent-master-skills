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
  integrates-with: [quality-gates, code-review-and-quality, dev-craft, ship, shipper]
  source-enhancements: ECC verification gates (deterministic-before-LLM-judge)
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
| 1 | Structure | Files exist, git clean, configs valid | Gate 2 |
| 2 | Deterministic | Tests, Lint, Typecheck, Build | Gate 3 |
| 3 | Security | Secrets scan, dependency audit | Gate 4 |
| 4 | Convention | Format, commit msg, branch name | Gate 5 |
| 5 | LLM Judge | Code review quality, architecture alignment | — |

This prevents expensive LLM evaluations on code that fails basic checks.

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
- `dev-craft` Phase 5 BUILD (TDD loop) — Tests provide verification evidence
- `debugging-and-error-recovery` — Fix failures before verifying
- `code-review-and-quality` — Review includes verification evidence
- `bug-hunting` — Security verification gates before completion claim