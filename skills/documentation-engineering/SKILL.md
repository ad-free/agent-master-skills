---
name: documentation-engineering
description: |
  Use when you need to create, maintain, or automate technical documentation including ADRs,
  API references, runbooks, onboarding guides, and docs-as-code pipelines.
model: gpt-5-nano
version: 2.1.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - "write documentation"
  - "create ADR"
  - "API docs"
  - "runbook"
  - "onboarding guide"
  - "docs-as-code"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 2.1.0
  domain: documentation
  integrates-with: [dev-craft, architecture-decision-records]
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Documentation Engineering

Technical documentation specialist for ADRs, API references, runbooks, onboarding guides, and docs-as-code pipelines.
Use when documentation needs creating, updating, or automating.
Includes interactive type selection and local markdown generation.

## Documentation Types

| Type | Purpose | Output |
|------|---------|--------|
| ADR | Architecture decisions | `docs/adr/NNNN-title.md` |
| API Reference | REST/GraphQL endpoints | `docs/api/reference.md` |
| Runbook | Operational procedures | `docs/runbooks/*.md` |
| Onboarding | New team member guide | `docs/onboarding/*.md` |
| Docs-as-Code | Pipeline + templates | `.github/workflows/docs.yml` |

## Workflow

1. **Discover** — What docs exist? What's missing? What's stale?
2. **Select Type** — Match need to documentation type above
3. **Generate** — Use templates + project context
4. **Validate** — Links work, examples run, styling consistent
5. **Deploy** — CI pipeline publishes to docs site
