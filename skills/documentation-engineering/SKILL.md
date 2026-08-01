---
name: documentation-engineering
description: |
  Technical documentation specialist for ADRs, API references, runbooks, onboarding guides, and docs-as-code pipelines.
  Use when documentation needs creating, updating, or automating.
  Includes interactive type selection and local markdown generation.
  
model: nemotron-3-ultra-free
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "create documentation"
  - "write docs"
  - "generate docs"
  - "update docs"
  - "adr"
  - "runbook"
  - "api docs"
  - "onboarding guide"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.0.0
  domain: specialized-engineering
  integrates-with: [dev-craft, ui-craft, planning-and-task-breakdown]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Documentation Engineering

Treats documentation as code — versioned, reviewed, tested, deployed.

## When to Use

- Creating any technical documentation (ADRs, API refs, runbooks, guides)
- Setting up docs-as-code pipeline (lint, test, build, deploy)
- Post-review documentation updates (after `mr-pr-review`)
- Onboarding new team members

**When NOT to use:** Quick comments in code, trivial README tweaks.

## Invocation Protocol

**Load when:** Documentation work needed, or post-review at Gate 7
**Invoke via:** `skill(name="documentation-engineering")`
**Resume to:** `skill("learn")` for learnings

---

## Documentation Type Selection (MANDATORY Before Generation)

**ASK the human before generating any documentation:**

```
DOCUMENTATION TYPE SELECTION
═══════════════════════════
What documentation to generate locally?

1. ADR — Architecture Decision Record (irreversible decisions)
2. Runbook — Operational procedure (deploy, rollback, debug)
3. User Guide — Feature walkthrough for end users
4. Changelog Entry — This release (prepend to CHANGELOG.md)
5. Onboarding Guide — New developer setup
6. API Reference — From OpenAPI spec (if spec exists)
7. Custom — Describe what you need

Reply: 1, 2, 4-5, or 'custom: <description>'
```

**Only generate selected type(s).** No auto-generation without explicit selection.

---

## Document Templates

All templates in `references/` directory:

| Template | Output Path | Purpose |
|----------|-------------|---------|
| `adr-template.md` | `docs/adr/NNN-title.md` | Architecture decisions |
| `runbook-template.md` | `docs/runbooks/<svc>-<action>.md` | Ops procedures |
| `user-guide-template.md` | `docs/guides/<feature>.md` | Feature walkthroughs |
| `changelog-template.md` | `CHANGELOG.md` (prepend) | Release notes |
| `onboarding-template.md` | `docs/onboarding/<topic>.md` | New dev setup |
| `api-doc-template.md` | `docs/api/<service>.md` | API reference |

---

## ADR Template (from `adr-template.md`)

```markdown
# ADR-NNN: <Title>

## Status
Proposed | Accepted | Superseded | Deprecated

## Context
What is the issue? What forces are at play?

## Decision
What are we doing? Be specific.

## Alternatives Considered
| Alternative | Why Rejected |
|-------------|--------------|
| Option A | Reason |
| Option B | Reason |

## Consequences

### Positive
- 

### Negative
- 

### Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|

## Related
- ADR-XXX
- Issue #YYY

## Implementation Notes
- 
```

---

## Runbook Template (from `runbook-template.md`)

```markdown
# Runbook: <Service> — <Action>

## Overview
- **Service:** <name>
- **Action:** <deploy | rollback | debug | scale | backup | restore>
- **Owner:** <team/person>
- **Last Updated:** <date>
- **Last Tested:** <date>

## Prerequisites
- Access: <required roles, VPN, keys>
- Tools: <CLI, dashboards, scripts>
- Dependencies: <other services must be healthy>

## Procedure

### Step 1: <Name>
```bash
# Command
```
**Verify:** <expected output>
**Rollback if:** <condition>

### Step 2: <Name>
...

## Verification
- [ ] Health check: <command/URL>
- [ ] Metrics: <dashboard link>
- [ ] Logs: <query>

## Rollback
```bash
# Rollback commands
```
**RTO:** <time> | **RPO:** <time>

## Troubleshooting
| Symptom | Likely Cause | Action |
|---------|--------------|--------|

## Links
- Dashboard: <URL>
- Logs: <URL>
- ADR: <link>
- Repo: <link>
```

---

## User Guide Template (from `user-guide-template.md`)

```markdown
# <Feature> User Guide

## Audience
<Who uses this — role, permissions, context>

## Overview
<What this feature does, why it exists>

## Quick Start
<5-minute path to value>

## Detailed Walkthrough

### <Section 1>
<Steps, screenshots, expected outcomes>

### <Section 2>
...

## Common Tasks
| Task | Steps |
|------|-------|

## Troubleshooting
| Problem | Cause | Solution |
|---------|-------|----------|

## Related
- ADR: <link>
- API: <link>
- Video: <link>
```

---

## Changelog Template (from `changelog-template.md`)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [vX.Y.Z] - YYYY-MM-DD

### Added
- <feature> — <context>

### Changed
- <improvement> — <context>

### Fixed
- <bug> — <context>

### Removed
- <deprecated> — <context>

### Security
- <fix> — <CVE/context>
```

---

## Onboarding Template (from `onboarding-template.md`)

```markdown
# Onboarding: <Topic>

## Audience
New <role> joining <team/project>

## Prerequisites
- [ ] Access granted (GitHub, cloud, tools)
- [ ] Local environment (OS, runtime, tools)
- [ ] Repo cloned and building

## Steps

### 1. Environment Setup
```bash
# Commands
```

### 2. First Build & Test
```bash
# Commands
```

### 3. First Task Walkthrough
<Link to a good first issue>

### 4. Key Resources
| Resource | Link |
|----------|------|

### 5. Team Contacts
| Role | Person | Slack/Email |
|------|--------|-------------|

## Time to First Commit
Target: <30 minutes
```

---

## API Reference Template (from `api-doc-template.md`)

```markdown
# API Reference: <Service>

## Base URL
`https://api.example.com/v1`

## Authentication
<Method: Bearer, API Key, etc.>

## Endpoints

### GET /resource
<Description>

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|

**Query Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|

**Response 200:**
```json
{
  "field": "type"
}
```

**Response 4xx/5xx:**
```json
{
  "error": "code",
  "message": "description"
}
```

**Example:**
```bash
curl -X GET "https://api.example.com/v1/resource" \
  -H "Authorization: Bearer <token>"
```
```

---

## Generation Workflow

### For ADR
1. Load `references/adr-template.md`
2. Fill from context (PR review, design discussion)
3. Number sequentially (next NNN)
4. Write to `docs/adr/NNN-title.md`
5. Update `docs/adr/README.md` index

### For Runbook
1. Load `references/runbook-template.md`
2. Fill from incident/post-mortem or deployment SOP
3. Write to `docs/runbooks/<svc>-<action>.md`
4. Link from ADR and service README

### For User Guide
1. Load `references/user-guide-template.md`
2. Fill from feature spec + UI walkthrough
3. Write to `docs/guides/<feature>.md`
4. Link from feature README

### For Changelog
1. Load `references/changelog-template.md`
2. Extract from PR titles (conventional commits)
3. Prepend to `CHANGELOG.md`
4. Group by Added/Changed/Fixed/Removed/Security

### For Onboarding
1. Load `references/onboarding-template.md`
2. Fill from team knowledge + repo state
3. Write to `docs/onboarding/<topic>.md`
4. Link from main README

### For API Reference
1. If OpenAPI spec exists → auto-generate
2. Else load `references/api-doc-template.md`
3. Fill from code + contract
4. Write to `docs/api/<service>.md`

---

## Docs-as-Code Pipeline

**Minimum viable pipeline (add to CI):**

```yaml
# .github/workflows/docs.yml
name: Docs
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check links
        run: npx markdown-link-check docs/**/*.md
      - name: Lint markdown
        run: npx markdownlint-cli2 docs/
      - name: Check examples
        run: |
          # Extract code blocks, validate syntax
      - name: Build site
        run: npx vitepress build docs  # or docusaurus, mkdocs
      - name: Deploy preview
        uses: peaceiris/actions-gh-pages@v3
        if: github.event_name == 'pull_request'
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: .vitepress/dist
```

**Quality Gates (run in CI):**
- [ ] No broken links (`markdown-link-check`)
- [ ] Style pass (`markdownlint`, `vale`)
- [ ] Code examples compile/run
- [ ] API examples match OpenAPI spec
- [ ] ADR index updated
- [ ] Runbook tested < 90 days ago

---

## Integration Points

### Post-Review (Gate 7)
After `mr-pr-review` completes, human asked:
> "Generate documentation? [y/n/m/s]"
If yes → invoke this skill with type selection.

### Post-Ship
`ship` skill invokes for:
- Changelog entry (always)
- ADR if architectural decision made
- Runbook if new deployment pattern

### Handoff
Outputs to `state.json.documentation`:
```json
{
  "generated": ["ADR-017", "runbook-deploy-auth"],
  "pending": ["user-guide-payments"],
  "prUrl": "https://github.com/org/repo/pull/123"
}
```

---

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "We'll document later" | Later never comes; document when context is fresh |
| "Code is self-documenting" | Code shows *what*, not *why* or *how to operate* |
| "Only devs read docs" | On-call, support, future-you need runbooks |
| "Auto-gen is enough" | Auto-gen gives reference; guides need human context |

---

## Verification Checklist

Before completing:

- [ ] Type selected by human (no auto-gen)
- [ ] Template loaded from `references/`
- [ ] All placeholders filled with real values
- [ ] Links valid (relative for repo, absolute for external)
- [ ] Code examples tested (compile/run)
- [ ] Cross-links to ADRs, issues, PRs added
- [ ] Index updated (ADR index, runbook index, guide index)
- [ ] CI pipeline passes (links, lint, build)
- [ ] State updated with generated/pending docs