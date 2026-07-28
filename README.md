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

### Quality & Safety

| Skill | Purpose | Iron Law |
|-------|---------|----------|
| `quality-gates` | Layered validation: structure → deterministic → security → convention → LLM-judge | NO MERGE WITHOUT QUALITY GATES |
| `code-review-and-quality` | 8-axis code review protocol | NO CODE WITHOUT REVIEW EVIDENCE |
| `verification-before-completion` | Evidence gates before claiming done | NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE |
| `debugging-and-error-recovery` | Systematic root-cause investigation | NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST |
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
| `agent-router` | Single entry point: maps request → agent → skill chain | New (bootstrap) | First skill to load; routes all work |

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
      ├── [7]   REVIEW     — code-review-and-quality (8 axes)
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
      quality-gates ──→ Gate 0 (Schema) → Gate 1 (Structure) → Gate 2 (Deterministic)
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
      "quality-gates": "allow",
      "context-engineering": "allow",
      "agent-router": "allow",
      "token-budget": "allow",
      "learn": "allow",
      "retro": "allow",
      "ship": "allow",
      "cost-optimizer": "allow",
      "grilling": "allow",
      "handoff": "allow"
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
> → `quality-gates` before merge

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
    │       │   └── Uses: quality-gates (6 gates), bug-hunting (security)
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
    verification-before-completion → quality-gates → ship
```

See `skills/SHARED.md` for the complete skill inventory and decision tree.

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

  - Run tests:

```bash
python -m pytest -q
```

Use `${PROJECT_ROOT}` in docs and examples to avoid absolute path leakage.