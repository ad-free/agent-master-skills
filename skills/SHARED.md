# Shared Documentation for agent-master-skills

## Start Here — Skill Router

Determine which skill to load based on your current situation:

```
User Request Received
│
├── Is the prompt vague, short, or idea-stage?
│   └── Yes → product-thinking → planning-and-task-breakdown → dev-craft or ui-craft
│
├── Are spec files provided (xlsx, csv, md, pdf)?
│   └── Yes → project-discovery → dev-craft (REQUIRE) → planning-and-task-breakdown
│
├── Is this a large multi-module project?
│   └── Yes → product-thinking → planning-and-task-breakdown → dev-craft + agent-orchestration
│
├── SCOPE gate (run first in dev-craft / ui-craft): what is the topology & domain?
│   ├── 2 separate repos (BE + FE)? → topology = multi → paired branches, shared api-contract.md in contractRepo
│   ├── 1 repo with BE + FE?        → topology = mono, scope = fullstack → dev-craft CONTRACT phase
│   ├── BE only / FE only ticket?   → scope = be|fe, mode = ticket → scoped branch, skip heavy phases
│   └── (all of the above feed agent-orchestration when parallel agents are needed)
│
├── Pre-merge or release validation?
│   └── Yes → quality-gates (after dev-craft completes)
│
├── Is this a new feature or project?
│   ├── Yes → Do you have a clear spec?
│   │   ├── Yes → planning-and-task-breakdown
│   │   │         → dev-craft or ui-craft
│   │   └── No → planning-and-task-breakdown
│   │             (collect info, verify, ask questions, write plan)
│   └── No → Is this a bug fix or improvement?
│       ├── Yes → debugging-and-error-recovery
│       └── No → What needs to happen?
│           ├── Code review → code-review-and-quality
│           ├── Security audit → bug-hunting
│           ├── Parallel work → dispatching-parallel-agents
│           └── Other → plan first, then execute
│
├── Creating or modifying skills?
│   └── Yes → skill-creator
│
├── Is this frontend/UI work?
│   ├── Yes → ui-craft (if the user explicitly asks for dev-craft anyway, dev-craft's own Skill Alignment Check §0.2 step 3a will catch the mismatch and surface it)
│   └── No → dev-craft
│
├── Is this an infra / IaC / deploy change?
│   └── Yes → dev-craft + Infra Safety Checklist (see the user's global AGENTS.md §4.1)
│
├── Is this a security concern?
│   ├── Yes → bug-hunting (deep) or security-audit plugin (automated)
│   └── No → continue above
│
├── Token budget / context management?
│   └── Yes → token-budget, context-engineering, learn
│
├── Weekly retrospective / learning capture?
│   └── Yes → retro, learn
│
├── Automated ship/release?
│   └── Yes → ship
│
├── Cost optimization / model routing?
│   └── Yes → cost-optimizer
│
└── Are you about to claim completion?
    └── Yes → verification-before-completion
```

> **SCOPE note:** dev-craft's `[0.2] SCOPE` gate classifies every run by `topology` (mono/multi), `scope` (be/fe/fullstack), and `mode` (build/ticket). The router above points you to the right skill; SCOPE decides the branch/contract/phase shape *within* it. For multi-repo fullstack, the canonical contract is `api-contract.md` in the BE repo (`contractRepo`); agent-orchestration has a multi-repo variant that uses paired branches instead of git worktree.

### Minimum Bar (applies to every code edit)

Regardless of which skill is loaded — or whether any skill is loaded — the
following always applies to any code you write or edit in a downstream project.
This is the floor, not the pipeline; it cannot be skipped even for "trivial"
changes.

1. **No single-character / cryptic identifiers** outside the documented
   exceptions (tight loop counters, mathematical `x`/`y`). `x`, `d`, `tmp`,
   `res`, `val`, `cfg`, `ctx` as dumped values are banned.
2. **No legacy / deprecated idioms.** Use the modern baseline per language
   (e.g. Python `X | None` over `Optional[X]`, TS `unknown` over `any`).

The concrete, per-language enforcement (linters, config, the grep gate for
cryptic names) lives in **`dev-craft/references/lint-rules.md`** — read that
file for the specifics rather than re-deriving them. This section intentionally
does not copy those rules; they have one source of truth.

> **Why this exists:** dev-craft's "When NOT to use" excludes single-line
> fixes and typo corrections from the full 15-phase pipeline — correctly, so a
> one-line change doesn't trigger the whole flow. But that exemption must not
> also exempt the edit from the deterministic readability/modern-code gate. The
> gate runs for *every* code edit, trivial or not.

### Quick Reference

| Situation | Load This Skill |
|-----------|-----------------|
| Starting new feature | `planning-and-task-breakdown` |
| Building backend/API | `dev-craft` |
| Building UI/frontend | `ui-craft` |
| Designing APIs (REST/GraphQL/gRPC) | `api-design` |
| Establishing testing strategy | `testing-strategies` |
| Setting up documentation/ADRs | `documentation-engineering` |
| Setting up CI/CD/IaC/deployment | `devops-automation` |
| Implementing observability (logs/metrics/traces/SLOs) | `observability-engineering` |
| Choosing architecture pattern | `architecture-patterns` |
| Tests failing | `debugging-and-error-recovery` |
| About to say "done" | `verification-before-completion` |
| Reviewing code | `code-review-and-quality` |
| Security audit / bug bounty | `bug-hunting` |
| Multiple independent tasks | `dispatching-parallel-agents` |
| Creating or modifying skills | `skill-creator` |
| Vague idea / missing requirements | `product-thinking` |
| Screenshot/image as reference | `image-to-design-spec` |
| Token budget / context management | `token-budget` |
| Persistent learning / memory | `learn` |
| Weekly retrospective | `retro` |
| Automated release / ship | `ship` |
| Cost optimization / model routing | `cost-optimizer` |

---

### Skill Disambiguation Rules (prevent wrong-skill triggers)

| If the user says… | Load THIS | NOT this (adjacent skill) |
|-------------------|-----------|---------------------------|
| "what kind of test should I write" | `testing-strategies` | `verification-before-completion` / `code-review-and-quality` |
| "is this ready to merge" | `quality-gates` / `verification-before-completion` | `testing-strategies` |
| "design the API for the new webhook endpoint" | `api-design` | `dev-craft` (BUILD) / `bug-hunting` |
| "review this endpoint for security holes" | `bug-hunting` | `api-design` |
| "how should we roll this out" | `devops-automation` | `quality-gates` |
| "did the deploy actually succeed" | `verification-before-completion` | `devops-automation` |
| "what should we alert on for this service" | `observability-engineering` | `bug-hunting` / `dev-craft` HARDEN |
| "is this service hardened against attack" | `dev-craft` HARDEN / `bug-hunting` | `observability-engineering` |
| "should this be one service or three" | `architecture-patterns` | `dev-craft` ARCH-SCAN |
| "what's wrong with the current codebase structure" | `dev-craft` ARCH-SCAN | `architecture-patterns` |

### Skill Chaining Pattern

```
1. product-thinking / project-discovery → PRODUCT.md / DOMAIN.md
2. planning-and-task-breakdown → PLAN.md
3. grilling (adversarial review of plan)
4. dev-craft / ui-craft → executes plan
   ├── dev-craft phases use: architecture-patterns, api-design, testing-strategies, devops-automation
   ├── ui-craft phases use: design-intelligence, anti-slop, testing-strategies
   ├── Both use: debugging-and-error-recovery (failures)
5. code-review-and-quality → per-slice review
6. verification-before-completion → per-slice evidence
7. quality-gates → pre-merge layered validation
8. bug-hunting → security audit (pre-deploy)
9. ship → automated release
10. learn → capture learnings
11. retro → weekly retrospective
```

---

## Skill Inventory

### Core Pipelines

| Skill | Purpose | Lines | Version | Preamble Tier |
|-------|---------|-------|---------|---------------|
| `dev-craft` | Full-stack engineering pipeline (15 phases) | 1142 | 1.2.0 | 3 |
| `ui-craft` | Frontend development pipeline (10 phases) | 813 | 1.1.0 | 3 |

### Specialized Engineering Skills

| Skill | Purpose | Iron Law | When to Use | Version | Tier |
|-------|---------|----------|-------------|---------|------|
| `api-design` | Design robust APIs with REST, GraphQL, gRPC patterns, versioning, security | **NO ENDPOINT WITHOUT A CONSUMER-STATED CONTRACT** | Designing new APIs, evaluating existing, planning versioning | 1.0.0 | 3 |
| `testing-strategies` | Comprehensive testing: unit, integration, e2e, contract, property-based | **NO TEST WITHOUT A STATED FAILURE MODE** | Setting up test strategy, debugging flaky tests, improving coverage | 1.0.0 | 3 |
| `documentation-engineering` | ADRs, API docs, docs-as-code pipelines, technical writing | **NO UNDOCUMENTED IRREVERSIBLE DECISION** | Establishing doc standards, generating API refs, runbooks | 1.0.0 | 3 |
| `devops-automation` | CI/CD, IaC (Terraform), Kubernetes, progressive delivery, secrets | **NO DEPLOY WITHOUT A TESTED ROLLBACK PATH** | Setting up CI/CD, migrating to IaC, deployment strategies | 1.0.0 | 3 |
| `observability-engineering` | Structured logging, metrics (RED/USE), distributed tracing, SLOs, alerting | **NO ALERT WITHOUT AN OWNER AND A RUNBOOK LINK** | Setting up observability, debugging production, SLO design | 1.0.0 | 3 |
| `architecture-patterns` | Hexagonal/Clean, DDD, Event-driven, CQRS, Microservices with trade-offs | **NO PATTERN WITHOUT A STATED TRADE-OFF** | Starting new project, refactoring legacy, evaluating patterns | 1.0.0 | 2 |

### Security & Quality Skills

| Skill | Purpose | When to Use | Version | Tier |
|-------|---------|-------------|---------|------|
| `bug-hunting` | Systematic vulnerability discovery (5-phase: Recon → Scan → Test → Exploit → Disclosure) | Security audit, bug bounty, pre-release review | 1.0.0 | 4 |
| `code-review-and-quality` | Code review protocols (8-axis review with confidence gates) | Reviewing code, receiving review feedback | 1.2.0 | 3 |

### Essential Skills

| Skill | Purpose | When to Use | Version | Tier |
|-------|---------|-------------|---------|------|
| `planning-and-task-breakdown` | Breaks work into ordered, verifiable tasks | Have a spec, need implementable units | 1.1.0 | 2 |
| `agent-orchestration` | Parallel multi-agent builds with isolated workspaces + shared API contract | Large project, 3+ modules, or parallel BE/FE/mobile agents | 1.1.0 | 3 |
| `debugging-and-error-recovery` | Root-cause investigation (4-phase methodology) | Tests fail, bugs reported, unexpected behavior | 1.0.0 | 4 |
| `verification-before-completion` | Evidence gates preventing false completion | Before claiming any task/phase is complete | 1.0.0 | 3 |
| `dispatching-parallel-agents` | Parallel subagent execution | Multiple independent tasks exist | 1.1.0 | 3 |
| `image-to-design-spec` | Analyzes screenshots → design tokens | User provides visual reference material | 1.0.0 | 3 |
| `skill-creator` | Create/modify skills for agent-master-skills | Building new skills, improving existing | 1.0.0 | 2 |

### New High-Value Skills (v2.0+)

| Skill | Purpose | Source | When to Use | Version | Tier |
|-------|---------|--------|-------------|---------|------|
| `token-budget` | Token estimation, user-chosen response depth, context compression | ECC | Response length control, context window management | 1.0.0 | 4 |
| `learn` | Persistent project learnings DB (search, prune, export, stats) | gstack | Cross-session knowledge capture | 1.0.0 | 1 |
| `retro` | Weekly engineering retrospective with git analysis | gstack | Sprint/weekly reflection, trend tracking | 1.0.0 | 1 |
| `ship` | One-command automated release (test → review → version → changelog → PR) | gstack | Ready to deploy, want full automation | 1.0.0 | 3 |
| `cost-optimizer` | Model routing (Haiku/Sonnet), budget tracking, prompt caching | ECC | LLM API cost control | 1.0.0 | 4 |
| `grilling` | Adversarial stress-test of plans/designs | mattpocock | Plan validation, risk identification | 1.0.0 | 2 |
| `handoff` | Agent-to-agent and session-to-session context transfer | mattpocock | Context rotation, multi-agent coordination | 1.0.0 | 1 |
| `agent-router` | Single entry point: maps request → agent → skill chain | New (bootstrap) | First skill to load; routes all work | 1.0.0 | 1 |

---

### Skill Integration Map

```
Entry Point
    │
    ▼
agent-router (bootstrap) ──→ routes to pipeline
    │
    ├── product-thinking / project-discovery (if vague/specs)
    │       │
    │       ▼
    ├── planning-and-task-breakdown ──→ PLAN.md
    │       │
    │       ▼
    │   grilling (adversarial review)
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
    │       │   └── Uses: quality-gates (5 gates), bug-hunting (security)
    │       │
    │       ├── Phase 8: SHIP
    │       │   └── Uses: ship (automated), verification-before-completion
    │       │
    │       └── Phase H: HANDOFF
    │           └── Uses: handoff protocol, learn (capture)
    │
    ├── cost-optimizer (runs in background, routes models)
    ├── token-budget (user-facing depth control)
    ├── context-engineering (manages context window)
    │
    └── Weekly: retro → learn

Verification Gates (every slice):
    verification-before-completion → quality-gates → ship
```

---

## Plugin System

See [`PLUGIN-SYSTEM.md`](./PLUGIN-SYSTEM.md) for plugin architecture, format, registration, and available plugins.

## Workflow Bundles

See [`WORKFLOW-BUNDLES.md`](./WORKFLOW-BUNDLES.md) for pre-configured workflows (SaaS MVP, Admin Dashboard, E-commerce, Landing Page).

---

## Phase Templates (Shared)

Common phase structures used by both dev-craft and ui-craft. Reference these instead of duplicating.

### Template: Human Checkpoint
```
**Exit criterion:** Human explicitly approves [what] with yes/no.

**State write:** Save [key data] to state.json.
```

### Template: Gate with Evidence
```
**Exit criterion (HARD GATE):** [Condition]. [Failure mode] is the failure this prevents.

**Evidence required:**
- [ ] [Check 1]: [command] → [expected output]
- [ ] [Check 2]: [command] → [expected output]
```

### Template: Resume Logic
```
**Resume Logic:**

| Scenario | Behavior |
|---|---|
| No state dir | Phase X if codebase exists, Phase Y if greenfield |
| State exists + complete | Ask: "New feature? Start fresh?" |
| State exists + incomplete | Load context.md, restore slice progress |
| Context near limit | Generate handoff doc, resume next session |
```

### Template: Branch Isolation
```
**Branch isolation (mandatory):** Every run starts on a dedicated feature branch — never commit directly to `main`/`develop`. 

**Base-branch guard (enforced before every commit):** Treat `main`, `master`, `develop` as protected. If `git branch --show-current` reports a base branch at commit time, STOP and create/checkout the feature branch first.
```

### Template: Verification Checklist
```
VERIFICATION EVIDENCE:
- [ ] Tests: [command] → [X passed, Y failed]
- [ ] Lint: [command] → [0 errors]
- [ ] Type check: [command] → [0 errors]
- [ ] Build: [command] → [success]
- [ ] Manual test: [what you tested and result]

**Fresh Evidence Rule:** Evidence older than last code change is INVALID. Re-run.
```

---

## Cross-Skill Communication Protocol

### State File Schema (Extended v2.0)

Both dev-craft and ui-craft use compatible `state.json` formats, stored per run under
`.dev-craft/runs/<slug>/state.json` (registry in `.dev-craft/index.json`):

```json
{
  "currentPhase": 3,
  "completed": [0, 1, 2],
  "stack": {
    "react": "19.0.0",
    "tailwind": "4.0.0"
  },
  "slices": ["auth", "dashboard", "settings"],
  "currentSlice": 1,
  "plugins": ["security-audit"],
  "requirementsExtracted": 47,
  "coverageGaps": ["REQ-011", "REQ-027"],
  "deferredRequirements": ["REQ-030"],
  "crossSkill": {
    "backendSliceNeeded": ["auth-api"],
    "apiContract": ".dev-craft/runs/<slug>/api-contract.md"
  },
  "learningsCaptured": [
    {"id": "learn-001", "text": "Stripe webhook idempotency requires sorting by created timestamp", "source": "verification", "timestamp": "2026-01-15T10:30:00Z"}
  ],
  "retroHistory": [
    {"date": "2026-01-10", "file": ".dev-craft/retros/2026-01-10.md", "actionItems": 3}
  ],
  "tokenUsage": {
    "total": 125000,
    "byAgent": {"planner": 15000, "implementer": 85000, "verifier": 5000},
    "lastRotation": "2026-01-15T09:00:00Z"
  },
  "costTracking": {
    "totalUSD": 0.00,
    "byModel": {"nemotron-3-ultra-free": 0.00, "big-pickle": 0.00, "deepseek-v4-flash-free": 0.00},
    "budgetUSD": 10.00
  }
}
```

> **Coverage gate keys** (`requirementsExtracted`, `coverageGaps`, `deferredRequirements`)
> back the `[3.7] REQUIREMENTS-EXTRACTION` COVERAGE GATE in both dev-craft and ui-craft.
> A run may not advance to BUILD/SOURCE until every P1/G1 requirement is traced to a task
> (no unresolved `coverageGaps` of priority P1/G1 unless recorded in `deferredRequirements`
> with explicit human acknowledgement).

### Handoff Document Format

When switching between pipelines, generate a handoff document:

```markdown
# Handoff: [Pipeline] → [Pipeline]

## Context
- Feature: User authentication
- Current state: Backend API complete
- Next: Frontend login UI

## API Contract
- POST /api/auth/login
- POST /api/auth/signup
- POST /api/auth/reset

## Design System
- Colors: .ui-craft/tokens/tokens.css
- Components: src/components/ui/

## Requirements
- Form validation with React Hook Form + Zod
- Error handling with toast notifications
- Loading states with skeleton UI
```

### Shared Glossary

Both pipelines share `context.md` for consistent terminology:

```markdown
# Glossary

- **User**: Authenticated person using the application
- **Session**: JWT token stored in httpOnly cookie
- **Dashboard**: Main landing page after login
- **Settings**: User profile and preferences page
```

---

## Cross-Skill Coordination

1. **Design system first** — ui-craft creates tokens, dev-craft uses them
2. **API contract early** — dev-craft defines API, ui-craft consumes it
3. **Shared state** — Keep both pipelines' state files in sync
4. **Regular handoffs** — Switch pipelines at natural boundaries
5. **Unified testing** — Both pipelines contribute to E2E tests

---

## Agent Registry (v2.0)

All 27 agents with model assignments and tool restrictions:

### Core Pipeline Agents
| Agent | Model | Tools | Max Steps | Purpose |
|-------|-------|-------|-----------|---------|
| `planner` | nemotron-3-ultra-free | Read, Grep, Glob, Bash | 15 | Creates PLAN.md from spec |
| `implementer` | big-pickle | Read, Write, Edit, Bash, Grep, Glob | 12 | TDD implementation |
| `verifier` | deepseek-v4-flash-free | Read, Bash, Grep, Glob | 8 | Fresh evidence gates |
| `gatekeeper` | gpt-5-nano | Read, Bash, Grep, Glob | 5 | Always-active guardrails |
| `triage` | gpt-5-nano | Read, Grep, Glob | 5 | Classify + route requests |

### Domain Specialists
| Agent | Model | Tools | Max Steps | Purpose |
|-------|-------|-------|-----------|---------|
| `api-designer` | big-pickle | Read, Write, Edit | 10 | API contracts, OpenAPI |
| `database-engineer` | deepseek-v4-flash-free | Read, Write, Edit, Bash, Grep, Glob | 10 | Schema, migrations, queries |
| `frontend-engineer` | big-pickle | Read, Write, Edit, Bash, Grep, Glob | 12 | React, TS, CSS, a11y |
| `devops-engineer` | deepseek-v4-flash-free | Read, Write, Edit, Bash, Grep, Glob | 12 | CI/CD, Terraform, K8s |
| `security-auditor` | big-pickle | Read, Grep, Glob, Bash | 12 | Threat model, code review |
| `debugger` | nemotron-3-ultra-free | Read, Grep, Glob, Bash | 15 | Root-cause investigation |
| `test-engineer` | big-pickle | Read, Write, Edit, Bash, Grep, Glob | 12 | Test strategy, flaky fixes |
| `docs-engineer` | gpt-5-nano | Read, Write, Edit | 8 | ADRs, API docs, runbooks |

### Meta / Orchestration
| Agent | Model | Tools | Max Steps | Purpose |
|-------|-------|-------|-----------|---------|
| `orchestrator` | nemotron-3-ultra-free | Agent, Read, Bash, Grep, Glob | 20 | Multi-agent coordination |
| `context-guard` | gpt-5-nano | Read, Bash | 3 | Context rotation, handoffs |
| `retro-analyst` | deepseek-v4-flash-free | Read, Bash, Grep, Glob | 10 | Weekly retrospectives |

### Legacy Agents (Aliased to Specialists)
| Legacy Agent | Now Use |
|--------------|---------|
| `senior-developer` | `planner` + `implementer` |
| `backend-architect` | `api-designer` + `database-engineer` |
| `frontend-developer` | `frontend-engineer` |
| `code-reviewer` | `verifier` (auto) + `security-auditor` (security) |
| `application-security-engineer` | `security-auditor` |
| `database-optimizer` | `database-engineer` |
| `performance-benchmarker` | `test-engineer` + `debugger` |
| `devops-engineer` | `devops-engineer` (upgraded) |
| `ai-engineer` | `implementer` (ML tasks) |
| `api-tester` | `test-engineer` |
| `quality-engineer` | `test-engineer` + `verifier` |
| `mobile-developer` | `frontend-engineer` (mobile) |
| `product-manager` | `planner` + `product-thinking` skill |
| `technical-writer` | `docs-engineer` |