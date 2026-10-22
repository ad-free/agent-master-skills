# Shared Documentation for agent-master-skills

## Routing and inventory

One source each, so they cannot drift:
- Which skill to load: `AGENTS-TOOLS.md` → "Skill routing". `dev-craft` is the entry point for every
  non-trivial code change; `ui-craft` for the UI pipeline.
- What exists: `README.md` → "Skills" and "Agents".

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

## Agent Registry

See `README.md` → "Agents" (verifier, code-reviewer, debugger, test-engineer, security-auditor).

### Removed Skills (use the replacement)

| Removed Skill | Now Use |
|---------------|---------|
| `refactor-and-cleanup` | `dev-craft` (Refactor mode, `references/refactor.md`) |
| `database-migrations` | `dev-craft` (`plugins/database-migrations/`) |
| `backend-patterns`, `architecture-decision-records` | `dev-craft` (`references/architecture.md`) |
| `api-contract-designer` | `api-design` (`references/contract-first.md`) |
| `qa-and-edge-case-tester` | `testing-strategies` (`references/edge-cases.md`) |
| `handoff`, `context-compressor-and-pruner` | `context-engineering` |
| `evidence-ledger`, `verify-gate` | `verification-before-completion` |
| `redesign`, `animation-and-interactions`, `animation-craft` | `ui-craft` (`redesign-audit.md`, `motion.md`) |
| `two-axis-review` | `code-review-and-quality` |
| `secops-and-vulnerability-scanner`, `agent-payment-x402` | `bug-hunting` |
| `agent-sort`, `agent-orchestration`, `conductor` | `dispatching-parallel-agents` |
| `design-system-auditor` | `ui-craft` plugin `design-system-validate` |
| `diataxis-docs` | `documentation-engineering` |
| `performance-profiling` (was plugin) | `performance-profiler-and-tuner` |
| `image-to-code`, `imagegen`, `agent-shield`, `pair-agent`, `cost-optimizer`, `token-budget`, `learn`, `continuous-learning-v2`, `agent-eval`, `agent-self-evaluation` | Retired; restore from `skills/_archive/` if needed |

### Removed Agents (use the replacement)

| Removed Agent | Now Use |
|--------------|---------|
| `planner`, `implementer`, `orchestrator`, `fullstack-developer`, `senior-developer` | `dev-craft` skill in the main agent |
| `backend-architect`, `api-designer`, `database-engineer` | `dev-craft` + `api-design` |
| `frontend-engineer`, `frontend-developer` | `ui-craft` |
| `devops-engineer` | `devops-automation` skill |
| `docs-engineer`, `technical-writer` | `documentation-engineering` skill |
| `error-detective` | `debugger` agent |
| `application-security-engineer` | `security-auditor` agent |
| `quality-engineer`, `api-tester`, `performance-benchmarker` | `test-engineer` + `verifier` agents |
| Archived files | `agents/_archive/` |
