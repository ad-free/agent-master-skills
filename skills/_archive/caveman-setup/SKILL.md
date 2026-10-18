---
name: caveman-setup
description: Use when you need compact environment setup with minimal configuration. Quick dev environment bootstrap without verbose documentation.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
triggers:
  - "caveman setup"
  - "compact setup"
  - "quick bootstrap"
  - "lazy setup"
  - "env setup"
metadata:
  origin: agent-master-skills
  domain: setup
  integrates-with: [caveman, devops-automation, documentation-engineering]
---

# Caveman Setup

Compact environment setup. Bootstrap with minimal tokens.

## When to Use

- Quick dev env setup: "get me started"
- Minimal configuration for new project
- Pre-commit environment check

## Workflow

1. **Check existing config** — what's already there
2. **Apply minimal setup** — essentials only
3. **Verify** — does it work?
4. **Report** — what was set up, any issues

## Output

Setup commands. Any issues found.

## When NOT to Use

- Full CI/CD → use `devops-automation`
- Project scaffolding → use `dev-craft`
- Documentation → use `documentation-engineering`