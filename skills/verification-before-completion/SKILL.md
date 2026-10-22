---
name: verification-before-completion
description: |
  Use before saying "done", "fixed" or "complete" on work done outside dev-craft, or when proof must outlive
  the session (CI handoff, release, audit) via the hash-chained evidence ledger. Grades evidence
  FRESH/STALE/MISSING; 5 gates: structure, deterministic, security, convention, LLM judge. Inside dev-craft,
  its Verify step covers this.
version: 2.1.0
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
  - "about to claim done"
  - "verify before completion"
  - "verification gates"
  - "quality gates"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.1.0
  domain: quality-safety
  integrates-with: [dev-craft, debugging-and-error-recovery, code-review-and-quality, bug-hunting, ship]
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Verification Before Completion

Enforce fresh verification evidence before any completion claim. 5 gates: structure → deterministic → security → convention → LLM judge.

**Gate 1 — Structure:** Ensure the change has a plan, the code follows project patterns, and no unrelated files are modified.

**Gate 2 — Deterministic:** Run the relevant test suite, build, or type check. All must pass cleanly. Runbook with per-language commands, evidence format, and verdict template: `references/runbook.md`.

**Gate 3 — Security:** Run security-relevant checks. For ordinary code: no secrets in the diff, authorization on
every new endpoint, input validated at the boundary, dependency audit if dependencies changed. For agent/LLM
systems, also:
- Tool discipline: Are all required tools code-gated (not just prompt-text)?
- Memory contamination: No stale context from prior sessions leaking into current work?
- Wrapper regression: Does the base model still work correctly without the wrapper?
- Hidden repair loops: No silent LLM passes running after the main agent loop?
- Rendering integrity: Does the output look correct in the target platform?

**Gate 4 — Convention:** Ensure code follows project conventions (no single-char vars, modern idioms, etc.). For agent systems, verify the agent-architecture-audit findings are addressed.

**Gate 5 — LLM Judge:** Use an LLM to evaluate if the change is genuinely complete and correct. For agent systems, the judge should specifically verify:
- No wrapper regression vs. base model
- Tool calls match the required set
- Memory state is clean and session-local
- Output format is consistent and correct

**NEVER invoke LLM judge (Gate 5) if Gates 1-4 fail.**

## Freshness: is the evidence still true?

Grade every claim before reporting it:

| Grade | Meaning | Allowed to claim done? |
|---|---|---|
| FRESH | Ran in this session, after the last relevant edit, command matches the claim | Yes |
| STALE | Ran, but files changed since or it was a different command | No: re-run |
| MISSING | Not run | No: run it, or list under "Not verified" |

When proof must survive the session (CI handoff, `ship`, audits), record it with the hash-chained evidence
ledger: `ledger/cli/evidence.js run --label test -- <cmd>`, then `check --label test --max-age 1h`. Details:
`references/evidence-ledger.md`.
