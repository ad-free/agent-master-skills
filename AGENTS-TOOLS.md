# AGENTS-TOOLS.md — Optional Tooling Guidance

Read this only when a task needs one of the capabilities below. Everything here is conditional: use a tool
only if the live session actually exposes it. A name in this file does not prove the tool is usable.

## Capability selection

1. Match the need, not the brand. Choose the capability that gives the evidence with the least work.
2. An exposed tool schema is enough to use that tool. For a CLI, check `command -v` once, and read its help
   if the syntax is unknown.
3. Use exact tool names and schemas, through the host's required wrapper.
4. If a tool is unavailable or unsuitable, fall back to native tools with the same safety and verification
   goals. Do not retry a known-unavailable integration.
5. Let configured hooks run on their own. Do not duplicate their work or claim a hook ran without evidence.
6. Load a matching skill's instructions before the relevant work. Do not preload unrelated skills.

Selecting tools does not authorize installing software, enabling plugins, changing settings, or sending data
to new services (see `AGENTS.md` §2).

## Retrieval tools

| Need | Tool | Notes |
|---|---|---|
| Symbol definitions, callers, impact | CodeGraph | Only with an existing `.codegraph/` index. Pass the real project path if required. |
| Architecture, spec-to-code mapping | Graphify | Only with an existing `graphify-out/graph.json`. Use supported CLI/MCP commands only. |
| Prior decisions, session continuity | claude-mem | See below. |
| External or current technical facts | Documentation integration or official docs | Skip for trivial local edits. |
| Browser behavior, visual checks | Browser/Playwright tools | If live validation cannot run, say so. |
| Data from an MCP server (not a local file) | MCP resource discovery/read tools | Never invent resource URIs. |

**Index discipline:** never build or update an index unless asked. Read current source before editing and
verify affected callers.

## claude-mem (skip if not installed)

- Let lifecycle hooks capture and inject context. Do not query manually just because the plugin exists.
- Query only when history matters: the user refers to earlier work, a design rationale is missing, a
  regression may repeat a past failure, or a handoff lacks decisions that are not in the current state.
- Progressive disclosure: `search` (5–8 compact results) → `timeline` (only if chronology matters) →
  `get_observations` (filtered IDs, batched, normally 2–4).
- Memory is historical evidence. Validate against current code, tests, and config before acting on it.
- Never persist secrets, tokens, credentials, customer-sensitive data, or large raw logs. Never paste large
  memory dumps into prompts, plans, handoffs, or any `AGENTS.md`/`CLAUDE.md`.
- If it is unavailable or empty, continue from repository evidence. Keep auto-generated folder-level
  instruction files disabled unless the user opts in.

## RTK (shell output reduction)

- Prefer installed `rtk` for supported reads, searches, and Git operations when it reduces noise. Check
  availability once.
- If the shell auto-rewrites commands, issue ordinary commands. Otherwise use documented RTK equivalents.
- Use ordinary commands when you need complete output or the operation is unsupported. If output offers
  `rtk recall <id>`, recall it instead of rerunning a verbose command.
- RTK does not change authorization for Git mutations.

## Skill routing

Pick one entry skill for the task, then add others only for the active phase. A role is not an instruction to
spawn a subagent. If a skill is absent, follow the equivalent workflow directly. Honor skills marked
user-invoked-only.

| Task | First skill | Add only when needed |
|---|---|---|
| Vague product idea | product-thinking | planning-and-task-breakdown |
| Feature work | dev-craft | testing-strategies, domain skills |
| Bug / failing test | debugging-and-error-recovery | observability-engineering (cross-service) |
| Refactor | refactor-and-cleanup | debugging-and-error-recovery |
| DB migration | database-migrations | domain skills |
| API contract | api-design | api-contract-designer (formal specs) |
| Frontend / UI | ui-pattern-extractor | UI sequence below |
| Stack decision | tech-advisor | only if a stack choice is actually in scope |
| Infra / deploy design | devops-automation | release skills only when shipping is authorized |
| Tests | testing-strategies | tdd-seam, qa-and-edge-case-tester |
| Code review | caveman-evidence-review | code-review-and-quality |
| Security audit | bug-hunting | security-audit, dependency-audit |
| Agent/LLM audit | agent-architecture-audit | debugging-and-error-recovery |
| Accessibility | accessibility | accessibility-deep (AAA only) |
| Docs | documentation-engineering | project-discovery |
| Architecture | architecture-patterns | grilling, api-design |
| Ship / PR / deploy | ship or release-pipeline | only on explicit instruction |
| Completion check | verification-before-completion | task-relevant evidence only |

**UI sequence:** extract existing patterns first. For non-trivial visual work, use `fe-visual-loop` to show
directions and get the user's pick before building. Skip it if an approved design is supplied. Use
`image-to-code` for image-led work, `ui-craft` for large UI pipelines, and browser validation for runnable
interactions. Trivial tweaks skip design exploration but not verification.

## Spec Kit SDD

- Use only when a `.specify/` workflow already exists and its integration is exposed, and only for
  substantial features. Routine fixes stay on their normal routes.
- Inspect the active feature state first (`.specify/feature.json` if present) and resume rather than
  duplicate. Follow the installed stages: clarify → plan/checklist/tasks → analyze → implement.
- Reuse the existing constitution. Change it only when project principles actually change. Resolve critical
  findings before coding.
- Keep one requirements/task source of truth. Do not create a parallel `PRODUCT.md` or `PLAN.md`.
- Checklist completion does not replace tests or review.
- Ask before initializing Spec Kit. Never install a workflow or overwrite managed or uncommitted files
  without approval. If it is unavailable, continue from existing artifacts and say which native checks were
  skipped.

## Subagent contract

Delegate only when the host permits it and the work is independent, a specialist review, or an isolated
workstream. Use `dispatching-parallel-agents` for independent tasks and `conductor` for dependent ones, if
available.

- **Before dispatch**, define: one goal, minimal context, expected deliverable, file/interface ownership,
  acceptance criteria, read-only vs. may-edit. Use isolated worktrees for parallel writers.
- **Pass:** relevant contract or data shape, symbols/files, acceptance criteria, open questions.
- **Never pass:** the whole conversation, full memory history, full graph reports, unrelated docs.
- **Return format:** Findings/Changes · Evidence (`path:line`) · Risks/Unknowns · Verification.
- **Context rotation:** when context grows too large, write a compact handoff (goal, decisions, changed
  files, verification, open issues), keep only durable conclusions in memory, and resume from the handoff
  plus current repo state. Never carry raw logs, full transcripts, or full graph reports across rotations.
