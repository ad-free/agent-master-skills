---
name: caveman-evidence-review
description: Use when you need compact, evidence-based code review. Quick diff scan with minimal commentary — finds real issues without verbose prose.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
triggers:
  - "caveman review"
  - "compact review"
  - "quick diff check"
  - "lazy review"
  - "evidence review"
metadata:
  origin: agent-master-skills
  domain: review
  integrates-with: [caveman, code-review-and-quality, verification-before-completion]
---

# Caveman Evidence Review

Compact, evidence-based code review. Find real issues with minimal tokens.

## When to Use

- Quick diff scan: "what changed?"
- Pre-commit check for obvious issues
- Fast evidence gathering before formal review

## Workflow

1. **`git diff`** — see what changed
2. **Grep for anti-patterns** — security, error handling, hardcoded values
3. **Read 2-5 files** — only the changed ones
4. **Report** — findings with `path:line` evidence, max 10 lines

## Output

Bullet points with file:line references. No essays.

## When NOT to Use

- Full code review → use `code-review-and-quality`
- Security audit → use `bug-hunting`
- Architecture review → use `grilling`