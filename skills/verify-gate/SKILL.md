---
name: verify-gate
description: |
  DEPRECATED — merged into `verification-before-completion`. Load
  `verification-before-completion` instead; this shim exists only so existing
  installs and references keep resolving.
model: big-pickle
version: 1.0.0
preamble-tier: 3
allowed-tools:
  - Read
triggers:
  - "verify-gate"
  - "verify gate"
metadata:
  origin: agent-master-skills
  deprecated: true
  superseded-by: verification-before-completion
---

# `verify-gate` — Deprecated

Merged into `verification-before-completion`. The 5-gate policy lives there;
the per-language command runbook lives in its `references/runbook.md`.

Load `skill("verification-before-completion")` instead. Note the old broad
triggers (`done`, `finish`, `complete`) are intentionally NOT carried over —
the canonical skill already owns completion-gate routing. This file will be
removed in a future release.
