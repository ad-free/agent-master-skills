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

**NEVER invoke LLM judge (Gate 5) if Gates 1-4 fail.**
