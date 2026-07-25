---
name: documentation-engineering
description: "Use when deciding doc format, ADR process, API reference generation,\
  \ or docs-as-code pipeline \u2014 not for writing the content of a specific ADR\
  \ or guide (that's plain writing work once the format is decided)."
metadata:
  origin: adapted from ECC and addyosmani/agent-skills
  version: 1

---

# documentation-engineering

## Relationship to existing skills

dev-craft's DESIGN phase should invoke this skill to pick the doc format and process for the ADRs and API references it will produce. This skill owns the *how* (format, tooling, lifecycle); the content is still written in dev-craft or by the team using the chosen format.

## Iron Law

**NO UNDOCUMENTED IRREVERSIBLE DECISION.**

If a decision can't be reversed without reading code and guessing intent, it must have an ADR in the project's chosen format. If the project has no ADR format yet, that's the first doc to create.

## Decision tree

1. **What needs documenting?**
   - Architecture decisions → **ADRs** (MADR format in `docs/` with index table). → `reference/adr-format.md`
   - API contracts → **OpenAPI/GraphQL schema → generated reference** (Redoc/Scalar), not hand-written. → `reference/api-doc-generation.md`
   - Runbooks/operational procedures → **Markdown in `docs/`**, linked from alerts. → `reference/runbook-format.md`
   - Developer onboarding/guides → **MkDocs/Docusaurus** (choose one, standardize). → `reference/docs-site-generator.md`

2. **How is it built and deployed?**
   - **Docs-as-code**: Markdown in repo, CI builds site, deploys on merge (GitHub Pages/Cloudflare Pages). → `reference/docs-as-code-pipeline.md`
   - API reference generated from source annotations (not separate spec files) — single source of truth. → `reference/api-spec-from-code.md`

3. **How does it stay current?**
   - ADR index check in CI (no gaps in numbering). → `reference/adr-lint.md`
   - API doc freshness check: fail build if OpenAPI spec older than code change touching routes. → `reference/api-doc-freshness.md`
   - Broken link check in CI. → `reference/link-check.md`

## Output

A doc process decision: format chosen, tooling selected, CI checks defined, folder structure created — handed to dev-craft DESIGN as the "how we document" input for this project.