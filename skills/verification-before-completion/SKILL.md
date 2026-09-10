---
name: verification-before-completion
description: |
  Use when you must prove completion with fresh evidence before any "done" claim. 5 gates: structure → deterministic → security → convention → LLM judge. Invoked by verifier, implementer, gatekeeper.
model: big-pickle
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

**Gate 2 — Deterministic:** Run the relevant test suite, build, or type check. All must pass cleanly.

**Gate 3 — Security:** Run security-relevant checks. For agent systems, this includes:
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
