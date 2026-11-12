# PLAN: skills, subagents and UI design workflow

Status: Phase 1 done in the working tree (2026-11-12, D1 = archive), not committed. Install step done:
`~/.claude/agents/{code-reviewer,verifier,ui-verifier}.md` link to the live worktree (old copies in
`~/.claude/agents.bak-2026-11-12`); the new agents take effect once this branch reaches `origin/master`.
Phase 1 merged (#29). Phase 2 done in the working tree on `chore/skills-prune` (D2/D3/D5/D6 defaults; D4 default
plus `project-discovery` kept; `eval-harness` kept in place because `tools/validate_eval_cases.py` reads its
schema); Phase 2 merged (#30). Load target: 607 -> 490 on `chore/dev-craft-load-budget` (evals in
`skills/dev-craft/eval/load-budget.md` §Round 3). Phases 3 and 4 not started.
Branch: `chore/skills-agents-cleanup-plan`. Written 2026-11-12.

## Goal

1. Subagents that actually enforce their limits and match how `dev-craft` uses them.
2. A skill library that matches what is used: fewer skills, no routes to skills that are switched off.
3. UI work that starts from a real reference and is judged against it, so designs stop coming out generic.

## Evidence this plan rests on

- Usage log, 2026-10-18 to 2026-11-11, 596 calls, Claude Code only: `dev-craft` 100, `debugging-and-error-recovery` 13,
  `ui-craft` 9, `fe-visual-loop` 2; `api-design`, `bug-hunting`, `testing-strategies` 0. Subagents: 46 generic,
  6 Code Reviewer, 0 for Verifier, Debugger, Test Engineer, Security Auditor. Playwright MCP 195 calls.
- Agent files use `allowed-tools` / `max-steps`; Claude Code reads `tools` / `maxTurns`. All five agents currently
  run with all tools.
- 15 skills are `off` in `~/.claude/settings.json`; `AGENTS-TOOLS.md` still routes to five of them.
- `armorify-ppe/docs/design/g-pro-shop`: direction "G" of mocks invented from words; improved only when a
  ThemeForest reference was supplied.

## Decisions needed from you (my default in bold)

| # | Decision | Options |
|---|---|---|
| D1 | Zero-use agents `debugger`, `test-engineer`, `security-auditor` | **archive** / keep and fix |
| D2 | `bug-hunting`, `testing-strategies` (duplicated by dev-craft checklists) | **archive the skills, keep the checklists** / keep skills, delete checklists |
| D3 | `api-design`, `tdd-seam` | **fold into dev-craft references** / keep as skills |
| D4 | The 15 "off" skills | **re-enable `image-to-design-spec`, `dispatching-parallel-agents`, `context-engineering`, `ship`; archive the other 11** / archive all / keep all |
| D5 | `playwright-skill`, local `skill-creator`, `code-review-and-quality` (overlap with MCP and built-ins) | **archive `playwright-skill`; keep the other two** |
| D6 | `commands/`, `contexts/` (not installed anywhere) | **delete** / keep |
| D7 | Skill-gate hook (in `~/.claude/hooks`, outside this repo) | **tighten the regexes** / set to `warn` / leave |
| D8 | Inter font: global `DESIGN.md` prescribes it, `anti-slop` bans it | **allow Inter for app/admin screens, ban it only for marketing pages** |

Phases 1 and 4 do not depend on any decision and can start on approval of the plan alone.

## Phase 1: fix the subagents

Files: `agents/*.md`, `tools/validate_agents.py`, `tests/test_validators.py`, `agents/README.md`,
`agents/AGENT_TEMPLATE.md`.

1. Frontmatter to the real schema: `name` (kebab-case), `description`, `tools`, `model`, `maxTurns`. Remove `mode`,
   `triggers`, `samplePrompts`, `preamble-tier`, `owner`, `version`, `allowed-tools`, `max-steps`.
2. `code-reviewer`: `tools: Read, Grep, Glob` (no Bash: a shell can write, so read-only would rest on
   instructions only), `model: inherit`. Input is the brief and a diff file the main agent writes.
3. `verifier`: rewrite to the Verifier role in `dev-craft/references/test-agent.md` (fresh full run, mutation
   spot-check, REQ-to-test check, return format). `model: inherit`, no haiku.
4. New `ui-verifier`: Playwright MCP tools plus Read/Bash. Runs the app, screenshots at 1440 and 390, reads console
   errors, compares against the picked reference and `DESIGN.md`, returns ranked visual defects with screenshot paths.
5. Delete the "Skill Chain" and "Handoff" sections (they point at `prompt-optimizer` and `implementer`).
6. D1: move the three unused agents to `agents/_archive/`.
7. `validate_agents.py`: require the real fields, reject the dead ones. Update its test.
8. `test-agent.md`: name the agents (`verifier`, `ui-verifier`) so dev-craft dispatches them instead of a generic agent.

Done when: `python3 tools/validate_agents.py` and `pytest -q` pass; a fresh session lists `code-reviewer` with three
tools, not "All tools"; a write attempt inside `code-reviewer` is refused.

Install step (yours, or mine with approval, since it touches `~/.claude`): replace the copied files in
`~/.claude/agents/` with symlinks to the live worktree so agents stop drifting.

## Phase 2: prune and reconcile skills (after D2 to D6)

Files: `skills/*`, `skills/_archive/`, `AGENTS-TOOLS.md`, `skills/dev-craft/SKILL.md`, `marketplace.json`,
`plugin.yaml`, `skills/SHARED.md`.

1. Move archived skills to `skills/_archive/` (git mv, nothing deleted).
2. D2: remove the "if the skill is installed, skip the checklist" branching from `dev-craft/SKILL.md` and
   `test-agent.md`.
3. D3: move the unique content of `api-design` into `dev-craft/references/fullstack.md` and of `tdd-seam` into
   `build-protocol.md`; keep each under the load budget.
4. `AGENTS-TOOLS.md` routing table: every skill named there must exist and be enabled.
5. Frontmatter sweep on the remaining skills: drop `triggers`, `preamble-tier`, `preferred-model`; move `version`
   under `metadata`; remove `allowed-tools` unless pre-approval is intended. Update `validate_skills.py` to match.
6. `marketplace.json`, `plugin.yaml`, `SHARED.md` list only live skills.
7. D4 settings change: remove the re-enabled skills from `skillOverrides` (in `~/.claude/settings.json`, needs
   your approval).

Done when: `validate_skills.py`, `validate_eval_cases.py`, `pytest -q` pass; a grep for every archived skill and
agent name returns no hit outside `_archive/`; `eval/measure-load.sh` shows Standard bug fix at or under 500 lines
(583 today).

## Phase 3: reference-first UI design

Files: `skills/fe-visual-loop/SKILL.md`, `skills/dev-craft/references/frontend-design.md`,
`skills/dev-craft/references/checklists/ui.md`, `skills/ui-craft/plugins/anti-slop/SKILL.md`,
`skills/dev-craft/references/ui-patterns/*.md`, root `DESIGN.md`.

1. `fe-visual-loop` Step 1 becomes "Reference": if you give none, the agent finds 3 to 5 real sites or template
   demos in the same category, screenshots them, and you pick. Inventing directions from adjectives is removed.
2. New Step 2 "Extract": section inventory in order, grid, type scale, spacing, colour roles, image treatment,
   written to the project's `DESIGN.md` (uses `image-to-design-spec`, D4).
3. Content gate: real content before layout (for a shop: at least 12 distinct products, real categories, trust
   content). No repeated items to fill a section.
4. Proof step: `ui-verifier` compares build and reference side by side at the same widths; done only when a second
   pass returns no high-severity visual defect.
5. Redesign rule: a redesign starts a new file from a new reference; the rejected mock is never edited.
6. `dev-craft` Design step: for a new screen or redesign it calls `fe-visual-loop` and you approve screenshots, not
   a text `design.md`. Small tweaks keep the three-line path.
7. `frontend-design.md`: add a short "visual quality" section (type hierarchy, spacing rhythm, density per screen
   type, one accent, tabular numbers, what a finished table/form/empty state looks like), about 30 lines.
8. `anti-slop`: add app, dashboard and storefront presets; apply D8.
9. Licence note in `fe-visual-loop`: a template is a reference for structure; using its code or assets needs a
   licence.

Done when: a new eval case passes (prompt "design a storefront home page" with no reference: the agent must
present references and wait for a pick before writing any mock); and one real run on `armorify-ppe` home page,
with before/after screenshots at 1440 and 390 shown to you.

## Phase 4: measurement and docs

1. `README.md`: rewrite the pipeline section, agent table, skill count and install steps to match Phases 1 to 3.
2. Usage log: also record reads under `skills/**/references/` so the next pruning has data on reference files
   (`~/.claude/hooks/log-usage.sh` and the hook matcher, outside this repo, needs approval).
3. D7: tighten `skill-routes.tsv` so words like "add" or "start" alone do not trigger the gate.
4. D6: remove `commands/` and `contexts/`.

Done when: README names no archived skill or agent; the log shows reference reads after one dev-craft session.

## Order and size

| Order | Phase | Size | Depends on |
|---|---|---|---|
| 1 | Phase 1 subagents | small, one session | nothing |
| 2 | Phase 3 UI design | medium, one or two sessions | `ui-verifier` from Phase 1, D4, D8 |
| 3 | Phase 2 pruning | medium, mostly moves | D2 to D6 |
| 4 | Phase 4 docs and measurement | small | Phases 1 to 3 |

One PR per phase. I do not commit, push or open PRs; I stage and propose the message.

## Out of scope

- Codex-side configuration and usage (the log has no Codex data).
- Rewriting `ui-craft`'s 10-phase pipeline.
- Buying or integrating a specific ThemeForest template for `armorify-ppe`.
- Adding eval cases for skills other than the new `fe-visual-loop` case.

## Risks

- Archiving a skill you use rarely but value: the log covers only 25 days. Archiving is a `git mv`, so restoring is
  one move back.
- The merge decisions in D2, D3 are based on descriptions and usage; I will read each skill body before moving
  content and report anything unique that would be lost.
- Changes under `~/.claude` (agents symlinks, settings, hooks) affect every project at once. Each is listed above
  and waits for explicit approval.
- Live skills follow `origin/master`: every merged phase reaches all your projects at the next session start.
