# agent-master-skills

Skills for AI coding agents — composable, disciplined, evidence-based.

Designed for [OpenCode](https://opencode.ai). Each skill is a `SKILL.md` that agents load on demand via the `skill()` tool.

## Skills

### Core Pipelines

| Skill | Purpose | Phases |
|-------|---------|--------|
| `dev-craft` | Full-stack engineering pipeline | 15 (LOAD → SCOPE → REQUIRE → ARCH-SCAN → ALIGN → DESIGN → BUILD-ORDER → REQUIREMENTS-EXTRACTION → SOURCE → CONTRACT → BUILD → TEST → REVIEW → HARDEN → SHIP) |
| `ui-craft` | Frontend development pipeline | 10 (LOAD → AUDIT → ALIGN → DESIGN → REQUIREMENTS-EXTRACTION → SOURCE → BUILD → REVIEW → HARDEN → SHIP) |

### Product Discovery

| Skill | Purpose | Output |
|-------|---------|--------|
| `product-thinking` | Structured idea refinement: vague concept → clear spec | `PRODUCT.md` |
| `project-discovery` | Ingest existing specifications (xlsx/csv/md/pdf) → domain model | `DOMAIN.md` |

### Planning & Execution

| Skill | Purpose | Iron Law |
|-------|---------|----------|
| `planning-and-task-breakdown` | Breaks work into ordered, verifiable tasks | NO IMPLEMENTATION WITHOUT A WRITTEN PLAN |
| `agent-orchestration` | Multi-agent parallel builds with git worktree isolation | NO PARALLEL AGENTS WITHOUT A SHARED CONTRACT |
| `dispatching-parallel-agents` | Parallel execution of independent tasks | NO PARALLEL DISPATCH WITHOUT INDEPENDENCE VERIFICATION |

### Specialized Engineering Skills

| Skill | Purpose | Iron Law / Key Principle |
|-------|---------|--------------------------|
| `api-design` | Design robust APIs (REST, GraphQL, gRPC) with versioning, docs, security | Design for consumers first; make it evolvable; explicit over implicit |
| `testing-strategies` | Comprehensive testing: unit, integration, e2e, contract, property-based | Test behavior, not implementation; pyramid over ice cream cone |
| `documentation-engineering` | ADRs, API docs, docs-as-code pipelines, technical writing | Documentation is code: versioned, reviewed, tested, deployed |
| `devops-automation` | CI/CD, IaC (Terraform), Kubernetes, progressive delivery, secrets | Everything as code; pipeline as product; progressive delivery |
| `observability-engineering` | Structured logging, metrics (RED/USE), distributed tracing, SLOs, alerting | Observability > monitoring; SLOs over alerts; three pillars unified |
| `architecture-patterns` | Hexagonal/Clean, DDD, Event-driven, CQRS, Microservices patterns | Architecture serves the problem; start simple; extract when pain proven |
| `database-migrations` | Safe schema changes with rollback, backfill, and zero-downtime deployment | NO MIGRATION WITHOUT A BACKUP AND ROLLBACK PLAN | Planning and executing database migrations | 2.0.0 |
| `backend-patterns` | Hexagonal, layered, CQRS, repository, saga, event sourcing patterns | NO DEPENDENCY VIOLATION IN THE DOMAIN LAYER | Structuring backend services with clean architecture | 2.0.0 |
| `refactor-and-cleanup` | Dead code removal, duplication elimination, naming, complexity reduction | NO REFACTORING WITHOUT A TEST SAFETY NET | Cleaning up technical debt and code quality | 2.0.0 |

### Frontend & UI Skills

| Skill | Purpose | Iron Law / Key Principle |
|-------|---------|--------------------------|
| `ui-component-builder` | Build accessible, modular React/Vue/Tailwind components with design tokens | NO COMPONENT WITHOUT DESIGN TOKEN CONSISTENCY | Building modern, responsive, accessible UI components | 2.0.0 |
| `design-system-auditor` | Audit UI code for design consistency, responsiveness, performance, and WCAG | NO UI WITHOUT DESIGN TOKEN COMPLIANCE | Validating UI against design tokens and accessibility standards | 2.0.0 |
| `animation-and-interactions` | CSS/Framer Motion animations, micro-interactions, and visual polish | NO ANIMATION WITHOUT PERFORMANCE BUDGET | Crafting smooth animations without performance degradation | 2.0.0 |

### Quality & Safety

| Skill | Purpose | Iron Law |
|-------|---------|----------|
| `verification-before-completion` | Layered validation: structure → deterministic → security → convention → LLM-judge | NO MERGE WITHOUT QUALITY GATES |
| `code-review-and-quality` | 8-axis code review protocol | NO CODE WITHOUT REVIEW EVIDENCE |
| `review-orchestrator` | Parallel specialized review subagents (security, style, debug, performance) | NO REVIEW WITHOUT PARALLEL PERSPECTIVES |
| `review-subagents` | Individual specialized subagents invoked by review-orchestrator | NO SUBAGENT WITHOUT COMPRESSED FINDINGS |
| `debugging-and-error-recovery` | Systematic root-cause investigation | NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST |
| `bug-hunting` | Deep security vulnerability discovery | NO ATTACK SURFACE WITHOUT INTENTIONAL PROBING |
| `api-contract-designer` | OpenAPI/Swagger specs, GraphQL schemas, type definitions, and mock data | NO INTEGRATION WITHOUT A SIGNED CONTRACT | Designing FE-BE integration contracts and generating types | 2.0.0 |
| `qa-and-edge-case-tester` | Automated test generation, edge-case analysis, boundary testing | NO TEST WITHOUT A STATED FAILURE MODE | Generating tests, analyzing edge cases, suppressing false positives | 2.0.0 |
| `bug-hunting` | Deep security vulnerability discovery | NO ATTACK SURFACE WITHOUT INTENTIONAL PROBING |

### Context & Memory

| Skill | Purpose |
|-------|---------|
| `context-engineering` | Agent context setup, memory hierarchy, session continuity, context rotation |
| `image-to-design-spec` | Screenshot → design tokens, layout detection, design system generation |

### New High-Value Skills (v2.0+)

| Skill | Purpose | Source | When to Use |
|-------|---------|--------|-------------|
| `token-budget` | Token estimation, user-chosen response depth, context compression | ECC | Response length control, context window management |
| `learn` | Persistent project learnings DB (search, prune, export, stats) | gstack | Cross-session knowledge capture |
| `retro` | Weekly engineering retrospective with git analysis | gstack | Sprint/weekly reflection, trend tracking |
| `ship` | One-command automated release (test → review → version → changelog → PR) | gstack | Ready to deploy, want full automation |
| `cost-optimizer` | Model routing (Haiku/Sonnet), budget tracking, prompt caching | ECC | LLM API cost control |
| `grilling` | Adversarial stress-test of plans/designs | mattpocock | Plan validation, risk identification |
| `handoff` | Agent-to-agent and session-to-session context transfer | mattpocock | Context rotation, multi-agent coordination |

### Batch 1 — New Skills (v2.1)

| Skill | Domain | Purpose |
|-------|--------|---------|
| `database-migrations` | Coding & Engineering | Safe schema changes with rollback, backfill, and zero-downtime deployment |
| `backend-patterns` | Coding & Engineering | Hexagonal, layered, CQRS, repository, saga, event sourcing implementation patterns |
| `refactor-and-cleanup` | Coding & Engineering | Dead code removal, duplication elimination, naming, complexity reduction |
| `agent-router` | Single entry point: maps request → agent → skill chain | New (bootstrap) | First skill to load; routes all work |

### Batch 2 — New Skills (v2.1)

| Skill | Domain | Purpose |
|-------|--------|---------|
| `ui-component-builder` | Frontend & UI | Build accessible, modular React/Vue/Tailwind components with design tokens |
| `design-system-auditor` | Frontend & UI | Audit UI code for design consistency, responsiveness, performance, and WCAG |
| `animation-and-interactions` | Frontend & UI | CSS/Framer Motion animations, micro-interactions, and visual polish |
| `api-contract-designer` | Specialized Integration | OpenAPI/Swagger specs, GraphQL schemas, type definitions, and mock data |
| `qa-and-edge-case-tester` | Specialized Integration | Automated test generation, edge-case analysis, boundary testing |

### Batch 3 — New Skills (v2.1)

| Skill | Domain | Purpose |
|-------|--------|---------|
| `architecture-decision-records` | Architecture & Specialized | Draft, evaluate, and maintain ADRs and trade-off matrices |
| `secops-and-vulnerability-scanner` | Security & Specialized | Static analysis, OWASP Top 10, dependency audit, secrets detection |
| `performance-profiler-and-tuner` | Performance & Specialized | Bottleneck analysis, memory leak detection, query optimization, profiling |
| `context-compressor-and-pruner` | Orchestration & Specialized | Context window management, summarization, stale context pruning |
| `agent-eval` | Orchestration & Specialized | Head-to-head agent comparison: pass rate, cost, time, consistency on custom tasks |
| `agent-eval` | Orchestration & Specialized | Self-correcting evaluation loops, agent output benchmarking, failure diagnosis |
| `review-subagents` | Quality & Safety | Parallel specialized review subagents (security, style, debug, performance) |
| `review-orchestrator` | Quality & Safety | Orchestrates review-subagents, aggregates findings, feeds into gates |

### Plugins

Beyond the core skills, two pipelines have plugin systems for extending functionality:

| Pipeline | Plugin | Phase | Purpose |
|----------|--------|-------|---------|
| `dev-craft` | `language-rules` | BUILD / REVIEW | Language-specific conventions for TS, Python, Go, Rust |
| `ui-craft` | `design-intelligence` | DESIGN | Structured design system generation (palettes, typography, styles) |
| `ui-craft` | `anti-slop` | BUILD | Anti-generic UI rules — no emoji icons, proper spacing, intentional gradients |

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
    planning-and-task-breakdown ────────→ PLAN.md
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
      ├── [7]   REVIEW     — review-orchestrator (parallel subagents) → code-review-and-quality (8 axes)
      │         └── Plugins: language-rules (style checks), security-audit
      ├── [8]   HARDEN     — cross-cutting security (7 checks)
      ├── [9]   SHIP       — automated via `ship` skill
      └── [H]   HANDOFF    — context rotation via `handoff` skill

    For large projects (>3 modules):
      agent-orchestration splits agents via git worktree:
        ├── Backend agent   (API + database)
        ├── Frontend agent  (UI components)
        └── Mobile agent    (mobile app)

    Pre-merge validation:
      verification-before-completion ──→ Gate 0 (Schema) → Gate 1 (Structure) → Gate 2 (Deterministic)
                      → Gate 3 (Security)  → Gate 4 (Convention) → Gate 5 (LLM-Judge)

    Throughout:
      context-engineering manages memory, rotation, and handoffs
      debugging-and-error-recovery handles any failures
      token-budget controls response depth
      cost-optimizer routes models for cost efficiency
      learn captures cross-session learnings
      retro runs weekly retrospectives
```

## Agent Registry (27 Agents)

### Core Pipeline Agents
| Agent | Model | Purpose |
|-------|-------|---------|
| `planner` | nemotron-3-ultra-free | Creates PLAN.md from spec |
| `implementer` | big-pickle | TDD implementation |
| `verifier` | deepseek-v4-flash-free | Fresh evidence gates |
| `gatekeeper` | gpt-5-nano | Always-active guardrails |
| `triage` | gpt-5-nano | Classify + route requests |

### Domain Specialists
| Agent | Model | Purpose |
|-------|-------|---------|
| `api-designer` | big-pickle | API contracts, OpenAPI |
| `database-engineer` | deepseek-v4-flash-free | Schema, migrations, queries |
| `frontend-engineer` | big-pickle | React, TS, CSS, a11y |
| `devops-engineer` | deepseek-v4-flash-free | CI/CD, Terraform, K8s |
| `security-auditor` | big-pickle | Threat model, code review |
| `debugger` | nemotron-3-ultra-free | Root-cause investigation |
| `test-engineer` | big-pickle | Test strategy, flaky fixes |
| `docs-engineer` | gpt-5-nano | ADRs, API docs, runbooks |
| `react-ts-reviewer` | big-pickle | React/TS deep review (hooks, re-renders, types) |
| `python-reviewer` | big-pickle | Python deep review (async, typing, idioms) |
| `go-reviewer` | big-pickle | Go deep review (concurrency, error handling) |

### Meta / Orchestration
| Agent | Model | Purpose |
|-------|-------|---------|
| `orchestrator` | nemotron-3-ultra-free | Multi-agent coordination |
| `context-guard` | gpt-5-nano | Context rotation, handoffs |
| `retro-analyst` | deepseek-v4-flash-free | Weekly retrospectives |

All agents use **free OpenCode Zen models** (Nemotron 3 Ultra, Big Pickle, DeepSeek V4 Flash, GPT-5 Nano, etc.)

## Getting Started

### 1. Install Skills in OpenCode

Skills must be placed in a directory OpenCode scans:

```bash
# Global install (available in every project)
ln -sfn "$(pwd)/skills/" ~/.config/opencode/skills

# Or per-project install
mkdir -p .opencode/skills/
ln -sfn "$(pwd)/skills/dev-craft" .opencode/skills/dev-craft
ln -sfn "$(pwd)/skills/product-thinking" .opencode/skills/product-thinking
# ... link only the skills you need
```

OpenCode auto-discovers skills from:
- `~/.config/opencode/skills/<name>/SKILL.md` (global)
- `.opencode/skills/<name>/SKILL.md` (per-project)

### 2. Configure Permissions (optional)

In `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "product-thinking": "allow",
      "project-discovery": "allow",
      "dev-craft": "allow",
      "agent-orchestration": "allow",
      "verification-before-completion": "allow",
      "context-engineering": "allow",
      "agent-router": "allow",
      "token-budget": "allow",
      "learn": "allow",
      "retro": "allow",
      "ship": "allow",
      "cost-optimizer": "allow",
      "grilling": "allow",
      "handoff": "allow",
      "review-orchestrator": "allow",
      "review-subagents": "allow",
      "eval-harness": "allow",
      "agent-eval": "allow"
    }
  }
}
```

### 3. Use the Pipeline

**From a vague idea:**
> "I want to build a task management app"
> → Agent loads `agent-router` → routes to `planner`
> → `product-thinking` → refines into spec
> → `planning-and-task-breakdown` → PLAN.md
> → `grilling` → risk-register.md
> → `dev-craft` → builds it

**From existing spec files:**
> "Here's my requirements.xlsx with the feature list"
> → Agent loads `agent-router` → routes to `planner`
> → `project-discovery` → DOMAIN.md
> → `planning-and-task-breakdown` → PLAN.md
> → `grilling` → risk-register.md
> → `dev-craft` → builds it

**For large multi-module projects:**
> "Build an HRM system with 13 modules"
> → `agent-router` → `planner` + `orchestrator`
> → `product-thinking` → `planning-and-task-breakdown`
> → `dev-craft` (master) + `agent-orchestration` (backend/frontend/mobile)
> → `verification-before-completion` before merge

## Philosophy

1. **Plan before code** — write the plan, then implement
2. **Evidence over assumption** — prove it works, don't assume
3. **Root cause over symptoms** — investigate before fixing
4. **Review over trust** — systematic quality checks
5. **Deterministic before judgment** — run lint/type/test before LLM evaluation

## Integration Map

```
Entry: agent-router (bootstrap)
    │
    ├── product-thinking / project-discovery (if vague/specs)
    │       │
    │       ▼
    ├── planning-and-task-breakdown ──→ PLAN.md
    │       │
    │       ▼
    │   grilling (adversarial review) ──→ risk-register.md
    │       │
    │       ▼
    ├── dev-craft / ui-craft (main pipelines)
    │       │
    │       ├── Phase 0-2: SCOPE, ALIGN, DESIGN
    │       │   └── Plugins: architecture-patterns, api-design, design-intelligence
    │       │
    │       ├── Phase 3-5: SOURCE, BUILD, TEST
    │       │   └── Uses: debugging-and-error-recovery, testing-strategies
    │       │   └── Parallel: dispatching-parallel-agents
    │       │   └── Multi-agent: agent-orchestration (git worktrees)
    │       │
    │       ├── Phase 6: REVIEW
    │       │   └── Uses: code-review-and-quality (8-axis + gates)
    │       │
    │       ├── Phase 7: HARDEN
    │       │   └── Uses: verification-before-completion (6 gates), bug-hunting (security)
    │       │
    │       ├── Phase 8: SHIP
    │       │   └── Uses: ship (automated), verification-before-completion
    │       │
    │       └── Phase H: HANDOFF
    │           └── Uses: handoff protocol, learn (capture)
    │
    ├── cost-optimizer (background, routes models)
    ├── token-budget (user-facing depth control)
    ├── context-engineering (manages context window)
    │
    └── Weekly: retro → learn

Verification Gates (every slice):
    verification-before-completion → verification-before-completion → ship
```

See `skills/SHARED.md` for the complete skill inventory and decision tree.

## Commands & Contexts

Quick-invokable workflows live in `commands/`, mode-specific configs in `contexts/`.

### Commands (`commands/`)

| Command | Workflow |
|---------|----------|
| `/plan` | Scope → plan → review → approve (`product-thinking` → `planning-and-task-breakdown` → `grilling`) |
| `/spec` | Requirements → spec → plan (`project-discovery` → `product-thinking` → `planning-and-task-breakdown`) |
| `/review` | Parallel subagent review (`review-orchestrator` → `review-subagents`) → `code-review-and-quality` → `verification-before-completion` → `bug-hunting` |
| `/investigate` | Debugging (`debugging-and-error-recovery` → `verification-before-completion`) |
| `/qa` | Test generation + validation (`qa-and-edge-case-tester` → `testing-strategies` → `visual-regression`) |
| `/ship` | Ship/deploy (`ship` → `verification-before-completion`) |
| `/context-save` | Checkpoint (`context-compressor-and-pruner` → `learn` → `handoff`) |
| `/context-restore` | Resume (`context-engineering` → `handoff` → `learn`) |
| `/retro` | Weekly retrospective (`retro` → `learn`) |

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
| `agent-eval` | Head-to-head agent comparison (pass rate, cost, time, consistency) | Task YAMLs in `.eval-agents/tasks/` |

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