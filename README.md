# agent-master-skills

Skills and subagents for AI coding agents: composable, disciplined, evidence-based.

Built for [Claude Code](https://claude.com/claude-code); the skills are plain `SKILL.md` folders, so Cursor and Codex can
load them too. Each skill is loaded on demand when its description matches the task.

## Skills

18 skills. Two (`ship`, `retro`) are user-invoked only (`/name`); the model never auto-loads them.

### Entry points

| Skill | Use for |
|-------|---------|
| `dev-craft` | Every non-trivial code change: feature, bug, refactor/cleanup, migration, schema/API change, architecture choice, review. Picks a tier (Trivial/Standard/Large) and mode |
| `ui-craft` | Full frontend pipeline: UI features, design systems, redesigns, motion |
| `product-thinking` | Vague idea → `PRODUCT.md` |
| `project-discovery` | Spec files (xlsx/csv/md/pdf) → `DOMAIN.md` |

### Called from the entry points when a step needs depth

| Skill | Use for |
|-------|---------|
| `fe-visual-loop` | Reference-first UI: user picks a real reference site, structure extracted into `DESIGN.md`, real content, mock, pick, build, `ui-verifier` proof |
| `image-to-design-spec` | Screenshot → tokens, layout, components |
| `accessibility` | WCAG 2.2 AA design and audit |
| `debugging-and-error-recovery` | Bugs whose cause is not yet known: hypotheses, root cause, regression proof |
| `code-review-and-quality` | Eight-axis review with false-positive filtering |
| `verification-before-completion` | Fresh-evidence gates; FRESH/STALE/MISSING grading; hash-chained evidence ledger |
| `dispatching-parallel-agents` | Running independent tasks in parallel subagents |
| `context-engineering` | Long sessions, handoff documents, resume, context pruning |
| `devops-automation` | CI/CD shape, IaC, rollback strategy |
| `documentation-engineering` | Docs-as-code, runbooks, API references |

API design, test strategy, test seams, edge cases, bug and security checklists live inside `dev-craft`
(`references/fullstack.md`, `build-protocol.md`, `checklists/`).

### Utilities and user-invoked

| Skill | Use for |
|-------|---------|
| `skill-creator` | Creating or editing skills in this library |
| `eval-harness` | Golden-case regression tests for skills |
| `/ship` | Tests, diff review, version bump, changelog, commit, push, PR (only when you ask to ship) |
| `/retro` | Weekly engineering retrospective from git history |

### Archived (in `skills/_archive/`)

Unused or merged skills are moved, not deleted; move a folder back to `skills/` to restore one. Merged content:

| Former skill | Now lives in |
|---|---|
| `api-design`, `api-contract-designer` | `dev-craft/references/fullstack.md` (§New or reshaped API) |
| `tdd-seam`, `testing-strategies`, `qa-and-edge-case-tester` | `dev-craft/references/build-protocol.md`, `checklists/testing.md`, `checklists/edge-cases.md` |
| `bug-hunting` | `dev-craft/references/checklists/bugs.md`, `security.md` |
| `refactor-and-cleanup` | `dev-craft/references/refactor.md` |
| `database-migrations` | `dev-craft/plugins/database-migrations/` |
| `backend-patterns`, `architecture-decision-records` | `dev-craft/references/architecture.md` |
| `handoff`, `context-compressor-and-pruner` | `context-engineering` |
| `evidence-ledger` | `verification-before-completion/ledger/` |
| `redesign`, `animation-and-interactions` | `ui-craft/references/` |
| `playwright-skill` | Playwright MCP + the `ui-verifier` agent |

### Plugins

| Pipeline | Plugin | Purpose |
|----------|--------|---------|
| `dev-craft` | `language-rules` | Language-specific conventions for TS and Python |
| `dev-craft` | `tdd-enforcer` | Strict red-green-refactor |
| `dev-craft` | `security-audit` | Security scanning during review |
| `dev-craft` | `dependency-audit` | Dependency vulnerability scanning |
| `dev-craft` | `database-migrations` | Risk classification, reversible migrations, backfills |
| `dev-craft` | `api-versioning` | Versioning and deprecation of public APIs |
| `ui-craft` | `anti-slop` | Anti-generic UI rules, dials and presets (app, dashboard, storefront, marketing) |
| `ui-craft` | `design-intelligence` | Design system generation (palettes, typography, styles) |
| `ui-craft` | `visual-regression` | Screenshot comparison against baselines |
| `ui-craft` | `design-system-validate` | Code checked against design tokens and component specs |
| `ui-craft` | `figma-sync` | Tokens and components from Figma |
| `ui-craft` | `accessibility-deep` | Deep WCAG audit |

## How it flows

```
Request
  ├── vague idea → product-thinking → PRODUCT.md ─┐
  ├── spec files → project-discovery → DOMAIN.md ─┤
  ├── code change (feature, bug, refactor, migration, API, schema, review) ──→ dev-craft
  │     Frame → Challenge → Brief → (Design) → (Contract) → Plan → Implement → Review → Verify → Finalize
  │       Tier: Trivial (edit + check) | Standard (brief, test, evidence) | Large (phases-large.md, one approval)
  │       Design, new screen or redesign: fe-visual-loop (real reference picked by the user)
  │       Bug, cause unknown: debugging-and-error-recovery
  │       Verify (Large, or risk flag): verifier / ui-verifier agents; review: code-reviewer agent
  │       Parallel work: dispatching-parallel-agents (+ dev-craft build-extras.md for worktrees)
  ├── full UI pipeline, design system, motion → ui-craft (+ fe-visual-loop, anti-slop, accessibility)
  ├── long session / handoff / resume → context-engineering
  └── user-invoked: /ship, /retro
```

Hard gates in every tier: no commit/push/merge without an explicit instruction, never edit on `main`/`master`,
no code without a shown brief, evidence from this session after the last edit before "done". See
`skills/dev-craft/SKILL.md` and `skills/SHARED.md`.

## Agents (3)

| Agent | Tools | Purpose |
|-------|-------|---------|
| `code-reviewer` | Read, Grep, Glob | Read-only review of a diff file against the brief; cannot edit or run commands |
| `verifier` | Read, Grep, Glob, Bash, Edit, Write | Independent fresh run, mutation spot-check, REQ-to-test check; does not edit production code |
| `ui-verifier` | Read, Grep, Glob, Bash, Playwright MCP | Runs the app, screenshots at 1440 and 390, compares against the picked reference and `DESIGN.md`, ranks visual defects |

Frontmatter follows Claude Code's subagent schema (`name`, `description`, `tools`, `model`, `maxTurns`);
`tools/validate_agents.py` rejects fields Claude Code ignores. Retired agents are in `agents/_archive/`.

## Getting started

### 1. Install

**Option A: live worktree + symlinks (what this repo's author uses)**

```bash
# Live skills follow origin/master through a separate worktree, so edits on a feature branch here never leak
# into other projects' sessions. A SessionStart hook can run:
#   git fetch && git -C ~/.local/share/agent-master-skills-live checkout --detach origin/master
git worktree add --detach ~/.local/share/agent-master-skills-live master
ln -sfn ~/.local/share/agent-master-skills-live/skills ~/.claude/skills
mkdir -p ~/.claude/agents
for a in code-reviewer verifier ui-verifier; do
  ln -sfn ~/.local/share/agent-master-skills-live/agents/$a.md ~/.claude/agents/$a.md
done
```

Claude Code reads `~/.claude/skills/<name>/SKILL.md`; folders without a `SKILL.md` at that level (`_archive/`,
`references/`) are ignored.

**Option B: installer CLI (per project, or Cursor/Codex)**

```bash
cd installer && npm ci && cd ..
node installer/bin/agent-skills.js init --target claude --template fullstack   # scaffold .claude/ + AGENTS.md
node installer/bin/agent-skills.js add ./skills/dev-craft --target claude    # a local path or a GitHub repo
node installer/bin/agent-skills.js list --target claude
node installer/bin/agent-skills.js doctor --target claude
```

Targets: `claude` (`~/.claude/skills/`), `cursor` (`~/.cursor/skills/`), `codex` (`~/.codex/skills/`), or `all`.
Templates: `minimal`, `fullstack`, `frontend`, `backend`.

### 2. Use it

Just describe the task; `dev-craft` loads for any non-trivial code change. Examples:

- "Fix the off-by-one in split_bill": Standard bug path (reproduce, failing test, fix, evidence).
- "Here's requirements.xlsx": `project-discovery` → `DOMAIN.md` → `dev-craft` Large path.
- "Design a storefront home page": `fe-visual-loop` finds 3-5 real reference sites and waits for your pick.
- "Build an HRM system with 13 modules": `dev-craft` Large path with `dispatching-parallel-agents`.

## Evaluation

| Layer | Purpose | Tooling |
|-------|---------|---------|
| Structural | Every case parses and matches the schema; CI | `tools/validate_eval_cases.py`, `tools/eval_harness.py ci` |
| Behaviour | Headless agent runs on fixtures, graded against a rubric, before/after a skill change | `skills/<skill>/eval/cases/*.yaml` (`kind: behavior`) |

`skills/dev-craft/eval/measure-load.sh` reports how many reference lines each scenario loads
(`eval/load-budget.md` has the history).

## Examples

- `examples/dev-craft-session.md`: end-to-end dev-craft demo (API server scaffold).
- `examples/ui-craft-session.md`: UI component library sketch + Storybook.

## Runbook

```bash
python tools/validate_skills.py
python tools/validate_agents.py
python tools/validate_eval_cases.py
python tools/eval_harness.py ci
python -m pytest -q
```

Use `${PROJECT_ROOT}` in docs and examples to avoid absolute path leakage.
