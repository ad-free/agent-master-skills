# agent-master-skills

Skills for AI coding agents — composable, disciplined, evidence-based.

Built for [Claude Code](https://claude.com/claude-code); the skills are plain `SKILL.md` folders, so Cursor and Codex can
load them too. Each skill is loaded on demand when its description matches the task.

## Skills

32 skills. Six are user-invoked only (`/name`); the model never auto-loads them, so they cost no context.

### Entry points

| Skill | Use for |
|-------|---------|
| `dev-craft` | Every non-trivial code change: feature, bug, refactor/cleanup, migration, schema/API change, architecture choice, review. Picks a tier (Trivial/Standard/Large) and mode |
| `ui-craft` | Frontend pipeline: UI features, design systems, redesigns, motion |
| `product-thinking` | Vague idea → `PRODUCT.md` |
| `project-discovery` | Spec files (xlsx/csv/md/pdf) → `DOMAIN.md` |

### Called from the entry points when a step needs depth

| Skill | Use for |
|-------|---------|
| `api-design` | API style, versioning, trust boundary; contract-first flow (spec, generated types, mocks) |
| `testing-strategies` | Which test type per failure mode; edge-case and boundary table; flaky-test causes |
| `tdd-seam` | Where a test attaches (public seam); red-green-refactor slices |
| `debugging-and-error-recovery` | Bugs whose cause is not yet known: hypotheses, root cause, regression proof |
| `verification-before-completion` | Fresh-evidence gates; FRESH/STALE/MISSING grading; hash-chained evidence ledger |
| `code-review-and-quality` | Eight-axis review with false-positive filtering |
| `bug-hunting` | Security audit and vulnerability discovery |
| `fe-visual-loop` | Show-before-build: screenshot 2-3 directions, user picks, build, compare |
| `image-to-design-spec` | Screenshot → tokens, layout, components |
| `accessibility` | WCAG 2.2 AA design and audit |
| `playwright-skill` | Browser automation and QA |
| `dispatching-parallel-agents` | Running independent tasks in parallel subagents |
| `context-engineering` | Long sessions, handoff documents, resume, context pruning |
| `devops-automation` | CI/CD shape, IaC, rollback strategy |
| `observability-engineering` | What to log, measure, trace, alert on |
| `performance-profiler-and-tuner` | Bottlenecks, memory, queries, bundle size |
| `documentation-engineering` | Docs-as-code, runbooks, API references |

### Utilities

| Skill | Use for |
|-------|---------|
| `skill-creator` | Creating or editing skills in this library |
| `eval-harness` | Golden-case regression tests for skills |
| `prompt-optimizer` | Turning a rough prompt into a finished one |
| `caveman-compress` | Compressing memory files to save input tokens |
| `caveman-commit` | Terse Conventional Commit messages |

### User-invoked only

`ship`, `grilling`, `retro`, `tech-advisor`, `agent-architecture-audit`, `caveman`.

### Archived (in `skills/_archive/`)

Merged, with their strongest content kept:

| Former skill | Now lives in |
|---|---|
| `refactor-and-cleanup` | `dev-craft/references/refactor.md` |
| `database-migrations` | `dev-craft/plugins/database-migrations/` |
| `backend-patterns`, `architecture-decision-records` | `dev-craft/references/architecture.md`, `architecture-patterns.md` |
| `api-contract-designer` | `api-design/references/contract-first.md` |
| `qa-and-edge-case-tester` | `testing-strategies/references/edge-cases.md` |
| `handoff`, `context-compressor-and-pruner` | `context-engineering` (+ `references/handoff.md`) |
| `evidence-ledger` | `verification-before-completion/ledger/` |
| `redesign`, `animation-and-interactions` | `ui-craft/references/redesign-audit.md`, `motion.md` |

Retired (niche, rarely triggered): `image-to-code`, `imagegen`, `conductor`, `agent-shield`, `pair-agent`,
`cost-optimizer`, `continuous-learning-v2`, `agent-eval`. Move a folder back to `skills/` to restore one.

### Plugins

Beyond the core skills, two pipelines have plugin systems for extending functionality:

| Pipeline | Plugin | Phase | Purpose |
|----------|--------|-------|---------|
| `dev-craft` | `language-rules` | BUILD / REVIEW | Language-specific conventions for TS and Python |
| `ui-craft` | `design-intelligence` | DESIGN | Structured design system generation (palettes, typography, styles) |
| `ui-craft` | `anti-slop` | BUILD | Anti-generic UI rules — no emoji icons, proper spacing, intentional gradients |
| `ui-craft` | `visual-regression` | REVIEW | Playwright screenshot comparison with baseline management and diff visualization |
| `ui-craft` | `design-system-validate` | REVIEW | Validate code against design tokens and component specs |
| `ui-craft` | `figma-sync` | DESIGN | Sync design tokens and components from Figma via MCP/API |
| `dev-craft` | `tdd-enforcer` | BUILD | Strict RED-GREEN-REFACTOR enforcement |
| `dev-craft` | `security-audit` | REVIEW | Security vulnerability scanning during code review |
| `dev-craft` | `dependency-audit` | HARDEN | Dependency vulnerability scanning |
| `dev-craft` | `database-migrations` | BUILD | Risk classification, reversible migrations, backfills |
| `dev-craft` | `api-versioning` | CONTRACT | Versioning and deprecation of public APIs |
| `ui-craft` | `accessibility-deep` | REVIEW | Deep WCAG audit |

## Pipeline Flow

```
Vague idea / short prompt
    │
    ▼
product-thinking ──────────────────────→ PRODUCT.md
  (4-round refinement: domain → scope → features → priority)
    │
    ├── With spec files (xlsx/csv/md/pdf)
    │   ▼
    │   project-discovery ─────────────→ DOMAIN.md
    │     (extract entities, features, priorities, dependencies)
    │
    └── Clear prompt / PRODUCT.md / DOMAIN.md
        │
        ▼
    dev-craft ────────→ PLAN.md
      (validate → dependency map → vertical slices → tasks)
        │
        ▼
    grilling ───────────────────────────→ risk-register.md
      (adversarial stress-test of plan)
        │
        ▼
    dev-craft ──────────────────────────→ Shipped code
      ├── [0]   LOAD       — initialize or resume
      ├── [0.5] REQUIRE    — load PRODUCT.md / DOMAIN.md
      ├── [1]   ARCH-SCAN  — codebase smell detection
      ├── [2]   ALIGN      — domain-calibrated questions + stack detection
      ├── [3]   DESIGN     — spec + ADRs + task list
      ├── [3.5] BUILD-ORDER— dependency sequencing (for multi-module)
      ├── [4]   SOURCE     — official docs verification
      ├── [5]   BUILD      — TDD + SECURE + MATCH + git worktree
      │         └── Plugins: language-rules (language conventions), tdd-enforcer
      ├── [6]   TEST       — full suite + debugging
      ├── [7]   REVIEW     — code-review-and-quality (parallel subagents optional) (8 axes)
      │         └── Plugins: language-rules (style checks), security-audit
      ├── [8]   HARDEN     — cross-cutting security (7 checks)
      ├── [9]   SHIP       — automated via `ship` skill
      └── [H]   HANDOFF    — context rotation via `context-engineering` skill

    For large projects (>3 modules):
      dev-craft build-extras.md splits agents via git worktree:
        ├── Backend agent   (API + database)
        ├── Frontend agent  (UI components)
        └── Mobile agent    (mobile app)

    Pre-merge validation:
      verification-before-completion ──→ Gate 0 (Schema) → Gate 1 (Structure) → Gate 2 (Deterministic)
                      → Gate 3 (Security)  → Gate 4 (Convention) → Gate 5 (LLM-Judge)

    Throughout:
      context-engineering manages memory, rotation, and handoffs
      debugging-and-error-recovery handles any failures
      retro runs weekly retrospectives
```

## Agents (5)

| Agent | Purpose |
|-------|---------|
| `verifier` | Fresh evidence before any "done" claim |
| `code-reviewer` | Read-only review of a diff against its requirements |
| `debugger` | Root-cause investigation |
| `test-engineer` | Test strategy and flaky-test fixes |
| `security-auditor` | Threat model and security review |

Role agents that duplicated skills (planner, implementer, orchestrator, fullstack, backend, API, database,
frontend, devops, docs, error-detective) are in `agents/_archive/`; `dev-craft` covers their flow.

## Getting Started

### 1. Install Skills

**Option A: symlink the whole library (what this repo's author uses)**

```bash
ln -sfn "$(pwd)/skills" ~/.claude/skills      # every skill, always current
mkdir -p ~/.claude/agents && cp agents/*.md ~/.claude/agents/   # skip AGENT_TEMPLATE.md and README.md
rm -f ~/.claude/agents/AGENT_TEMPLATE.md ~/.claude/agents/README.md
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

### 2. Permissions

Skills need no permission entry in Claude Code. User-invoked skills (`ship`, `grilling`, `retro`, `tech-advisor`,
`agent-architecture-audit`, `caveman`) run only when you type `/name`.

### 3. Use the Pipeline

**From a vague idea:**
> "I want to build a task management app"
> → Agent loads `dev-craft` → routes to `planner`
> → `product-thinking` → refines into spec
> → `dev-craft` → PLAN.md
> → `grilling` → risk-register.md
> → `dev-craft` → builds it

**From existing spec files:**
> "Here's my requirements.xlsx with the feature list"
> → Agent loads `dev-craft` → routes to `planner`
> → `project-discovery` → DOMAIN.md
> → `dev-craft` → PLAN.md
> → `grilling` → risk-register.md
> → `dev-craft` → builds it

**For large multi-module projects:**
> "Build an HRM system with 13 modules"
> → `dev-craft` → `planner` + `orchestrator`
> → `product-thinking` → `dev-craft`
> → `dev-craft` (master) + `dispatching-parallel-agents` (backend/frontend/mobile)
> → `verification-before-completion` before merge

**For UI redesign / audit:**
> "This page looks outdated, redesign it"
> → `dev-craft` → `frontend-engineer`
> → `ui-craft` → pain points, before/after → `ui-craft` → build
> → `anti-slop` + `playwright-skill` → QA + visual polish
> → `verification-before-completion` before merge

**For image generation:**
> "Generate a hero image for the landing page"
> → `dev-craft` → `frontend-engineer`
> → `ui-craft` → generates premium image → `ui-craft` → integrates into layout

## Philosophy

1. **Plan before code** — write the plan, then implement
2. **Evidence over assumption** — prove it works, don't assume
3. **Root cause over symptoms** — investigate before fixing
4. **Review over trust** — systematic quality checks
5. **Deterministic before judgment** — run lint/type/test before LLM evaluation

## Integration Map

```
Request
  ├── vague idea / spec files → product-thinking / project-discovery → dev-craft
  ├── code change (feature, bug, refactor, migration, API, schema) → dev-craft
  │     Frame → Challenge → Brief → (Design) → (Contract) → Plan → Implement → Review → Verify → Finalize
  │       Contract: api-design (contract-first)       Implement: tdd-seam, testing-strategies
  │       Bug, cause unknown: debugging-and-error-recovery
  │       Review: code-review-and-quality, bug-hunting  Verify: verification-before-completion
  │       Parallel work: dispatching-parallel-agents (+ dev-craft build-extras.md for worktrees)
  ├── UI pipeline, redesign, motion → ui-craft (+ fe-visual-loop, image-to-design-spec, accessibility, playwright-skill)
  ├── long session / handoff / resume → context-engineering
  └── user-invoked: /ship, /grilling, /retro, /tech-advisor, /agent-architecture-audit, /caveman

```

See `skills/SHARED.md` for the complete skill inventory and decision tree.

## Commands & Contexts

Quick-invokable workflows live in `commands/`, mode-specific configs in `contexts/`.

### Commands (`commands/`)

| Command | Workflow |
|---------|----------|
| `/plan` | Scope → plan → review → approve (`product-thinking` → `dev-craft` → `grilling`) |
| `/spec` | Requirements → spec → plan (`project-discovery` → `product-thinking` → `dev-craft`) |
| `/review` | Review (`code-review-and-quality` → `verification-before-completion`) |
| `/investigate` | Debugging (`debugging-and-error-recovery` → `verification-before-completion`) |
| `/qa` | Test generation + validation (`testing-strategies` → `playwright-skill` → `visual-regression`) |
| `/ship` | Ship/deploy (`ship` → `verification-before-completion`) |
| `/context-save` | Checkpoint (`context-engineering`) |
| `/context-restore` | Resume (`context-engineering`) |
| `/retro` | Weekly retrospective (`retro`) |

### Contexts (`contexts/`)

| Context | Model | Preamble | Best For |
|---------|-------|----------|----------|
| `dev` | big-pickle | tier 3 | Implementation, coding |
| `review` | nemotron-3-ultra-free | tier 4 | Analysis, review, audit |
| `research` | nemotron-3-ultra-free | tier 2 | Exploration, discovery |
| `debug` | nemotron-3-ultra-free | tier 2 | Root-cause investigation |

## Evaluation Framework

The repo ships two evaluation layers:

| Layer | Purpose | Tooling |
|-------|---------|---------|
| `eval-harness` | Golden regression of skills (EDD: capability/regression evals, pass@k, code/model/human graders) | `tools/eval_harness.py`, `tools/validate_eval_cases.py` |

Eval cases live under `skills/<skill>/eval/cases/*.yaml`. CI runs them via `.github/workflows/eval-harness.yml`.

## Examples

Sample sessions are provided under `examples/` to help you try the pipelines locally.

- `examples/dev-craft-session.md` — end-to-end dev-craft demo (API server scaffold).
- `examples/api-design-session.md` — API design contract → OpenAPI → scaffold.
- `examples/ui-craft-session.md` — UI component library sketch + Storybook.

## Runbook

Validator and test helpers are available in `tools/`:

  - Run skill validator:

```bash
python tools/validate_skills.py
```

  - Run agent validator:

```bash
python tools/validate_agents.py
```

  - Validate eval cases:

```bash
python tools/validate_eval_cases.py
```

  - Run eval harness (CI mode):

```bash
python tools/eval_harness.py ci
```

  - Run tests:

```bash
python -m pytest -q
```

Use `${PROJECT_ROOT}` in docs and examples to avoid absolute path leakage.