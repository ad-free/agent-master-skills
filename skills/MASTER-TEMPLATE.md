---
name: <skill-name>
description: |
  <One-line description of when to use this skill. Include what it does,
  when it is invoked, and what it explicitly does NOT do.>
model: <model-name>
version: 1.0.0
preamble-tier: <1-4>
allowed-tools:
  - <Tool1>
  - <Tool2>
  - <Tool3>
triggers:
  - "<trigger phrase 1>"
  - "<trigger phrase 2>"
  - "<trigger phrase 3>"
metadata:
  origin: agent-master-skills
  preferred-model: <model-name>
  version: 1.0.0
  domain: <domain-tag>
  integrates-with: [<skill1>, <skill2>]
---

TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# <skill-name>

## Relationship to existing skills

- <Skill A>: <how this skill relates>
- <Skill B>: <how this skill relates>

## When to Use

- <Use case 1>
- <Use case 2>
- <Use case 3>

## When NOT to Use

- <Anti-pattern 1>
- <Anti-pattern 2>

## Workflow

### Phase 1: <Phase Name>

<Detailed instructions for this phase>

### Phase 2: <Phase Name>

<Detailed instructions for this phase>

### Phase 3: <Phase Name>

<Detailed instructions for this phase>

## Context Management

- <How to manage conversation context>
- <What to persist between sessions>
- <State file location if applicable>

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| <Tool> | <What it does> | <Limitations> |
| <Tool> | <What it does> | <Limitations> |

## Output Contract

<What the skill must produce on completion>

## Completion Status Protocol

**Every skill must report completion status using one of:**

- **DONE** — Completed with evidence (lint output, test results, typecheck, files created)
- **DONE_WITH_CONCERNS** — Completed, but list concerns (known limitations, follow-ups needed, tech debt)
- **BLOCKED** — Cannot proceed; state blocker and what was tried (missing info, env issue, root cause unclear after 2 rounds)
- **NEEDS_CONTEXT** — Missing info; state exactly what is needed (requirements, access, clarification, data)

**Escalation Format:** `STATUS`, `REASON`, `ATTEMPTED`, `RECOMMENDATION`

**Mandatory Evidence for DONE:**
- Lint/typecheck/test output (not claimed, shown)
- No tests weakened/skipped/deleted to pass
- Edge cases handled (null/empty/boundary)
- Self-review complete (code-review-and-quality or equivalent)

## Quality Gates

- <Check 1>
- <Check 2>
- <Check 3>

## Error Handling

<How to handle common failure modes>

## References

- <Link to reference file if applicable>