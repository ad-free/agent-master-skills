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
├── Is this frontend/UI work?
│   ├── Yes → ui-craft
│   └── No → dev-craft
│
├── Is this a security concern?
│   ├── Yes → bug-hunting (deep) or security-audit plugin (automated)
│   └── No → continue above
│
└── Are you about to claim completion?
    └── Yes → verification-before-completion
```

### Quick Reference

| Situation | Load This Skill |
|-----------|-----------------|
| Starting new feature | `planning-and-task-breakdown` |
| Building backend/API | `dev-craft` |
| Building UI/frontend | `ui-craft` |
| Tests failing | `debugging-and-error-recovery` |
| About to say "done" | `verification-before-completion` |
| Reviewing code | `code-review-and-quality` |
| Security audit / bug bounty | `bug-hunting` |
| Multiple independent tasks | `dispatching-parallel-agents` |
| product-thinking | Structured idea refinement: vague concept → clear spec | Prompt is vague, idea-stage, missing requirements |
| Screenshot/image as reference | `image-to-design-spec` |

### Skill Chaining Pattern

```
1. planning → creates plan
2. dev-craft or ui-craft → executes plan
3. debugging → fixes failures during build
4. code-review → quality gate before merge
5. bug-hunting → security audit before deployment
6. HARDEN (dev-craft) → security scan + hardening
7. verification → proves completion
```

---

## Skill Inventory

### Core Pipelines

| Skill | Purpose | Lines |
|-------|---------|-------|
| `dev-craft` | Backend development pipeline (10 phases) | 540+ |
| `ui-craft` | Frontend development pipeline (9 phases) | 700+ |

### Security & Quality Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `bug-hunting` | Systematic vulnerability discovery (5-phase: Recon → Scan → Test → Exploit → Disclosure) | Security audit, bug bounty, pre-release review |
| `code-review-and-quality` | Code review protocols (8-axis review) | Reviewing code, receiving review feedback |

### Essential Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `planning-and-task-breakdown` | Breaks work into ordered, verifiable tasks | Have a spec, need implementable units |
| `debugging-and-error-recovery` | Root-cause investigation (4-phase methodology) | Tests fail, bugs reported, unexpected behavior |
| `verification-before-completion` | Evidence gates preventing false completion | Before claiming any task/phase is complete |
| `dispatching-parallel-agents` | Parallel subagent execution | Multiple independent tasks exist |
| `image-to-design-spec` | Analyzes screenshots → design tokens | User provides visual reference material |

### Skill Integration Map

```
dev-craft Pipeline Phases → Essential Skills
├── Phase 1: ARCH-SCAN → (standalone)
├── Phase 2: ALIGN → (standalone) + image-to-design-spec (if screenshot)
├── Phase 3: DESIGN → (standalone)
├── Phase 4: SOURCE → (standalone)
├── Phase 5: BUILD → uses debugging-and-error-recovery
├── Phase 6: TEST → uses debugging-and-error-recovery
├── Phase 7: REVIEW → uses code-review-and-quality
├── Phase 8: HARDEN → uses security-audit plugin + bug-hunting (if registered)
├── Phase 9: SHIP → uses verification-before-completion
└── Phase H: HANDOFF → (standalone)

ui-craft Pipeline Phases → Essential Skills
├── Phase 0: LOAD → (standalone)
├── Phase 1: AUDIT → (standalone)
├── Phase 2: ALIGN → (standalone) + image-to-design-spec (if screenshot)
├── Phase 3: DESIGN → (standalone)
├── Phase 4: SOURCE → (standalone)
├── Phase 5: BUILD → uses debugging-and-error-recovery
├── Phase 6: REVIEW → uses code-review-and-quality + UI Security Axis 8
├── Phase 7: HARDEN → uses verification-before-completion
├── Phase 8: SHIP → uses verification-before-completion
└── Phase H: HANDOFF → (standalone)

planning-and-task-breakdown → image-to-design-spec (if screenshot in Step 0)

Cross-Cutting → dispatching-parallel-agents
└── Any phase with independent tasks → parallel execution

├── Phase 0.5: REQUIRE → domain discovery from specs
├── Phase 3.5: BUILD-ORDER → module dependency sequencing
├── Throughout: Complex multi-agent → uses agent-orchestration
├── Pre-merge: → uses quality-gates (layered validation)
```

## Plugin System

See [`PLUGIN-SYSTEM.md`](./PLUGIN-SYSTEM.md) for plugin architecture, format, registration, and available plugins.

## Workflow Bundles

See [`WORKFLOW-BUNDLES.md`](./WORKFLOW-BUNDLES.md) for pre-configured workflows (SaaS MVP, Admin Dashboard, E-commerce, Landing Page).

---

## Cross-Skill Communication Protocol

### State File Schema

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
