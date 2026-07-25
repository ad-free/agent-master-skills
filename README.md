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
      ├── [6]   TEST       — full suite + debugging
       ├── [7]   REVIEW     — code-review-and-quality (8 axes)
       │         └── Plugins: language-rules (style checks), security-audit
      ├── [8]   HARDEN     — cross-cutting security (7 checks)
      └── [9]   SHIP       — commit + rollback plan

    For large projects (>3 modules):
      agent-orchestration splits agents via git worktree:
        ├── Backend agent   (API + database)
        ├── Frontend agent  (UI components)
        └── Mobile agent    (mobile app)

    Pre-merge validation:
      quality-gates ──→ Gate 1 (Structure) → Gate 2 (Deterministic)
                      → Gate 3 (Security)  → Gate 4 (Convention)
                      → Gate 5 (LLM-Judge)

    Throughout:
      context-engineering manages memory, rotation, and handoffs
      debugging-and-error-recovery handles any failures
```

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
      "context-engineering": "allow"
    }
  }
}
```

### 3. Use the Pipeline

**From a vague idea:**
> "I want to build a task management app"
> → Agent loads `product-thinking` → refines into spec
> → `planning-and-task-breakdown` → PLAN.md
> → `dev-craft` → builds it

**From existing spec files:**
> "Here's my requirements.xlsx with the feature list"
> → Agent loads `project-discovery` → DOMAIN.md
> → `planning-and-task-breakdown` → PLAN.md
> → `dev-craft` → builds it

**For large multi-module projects:**
> "Build an HRM system with 13 modules"
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
product-thinking ──────→ PRODUCT.md
    │
project-discovery ─────→ DOMAIN.md
    │
    └──→ planning-and-task-breakdown ──→ PLAN.md
              │
              ▼
         dev-craft ───────────────────────→ Shipped code
           │  │  │
           │  │  └──→ quality-gates (pre-merge)
           │  │
           │  └──→ agent-orchestration (multi-agent)
           │
           └──→ debugging-and-error-recovery (failures)
           └──→ code-review-and-quality (review)
           └──→ context-engineering (memory)
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
