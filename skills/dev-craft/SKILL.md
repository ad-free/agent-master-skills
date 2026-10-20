---
name: dev-craft
description: Use for non-trivial coding work - building or changing features, fixing bugs, refactors, schema/API/UI changes, reviewing a diff or PR comments, resuming earlier work. Skip typos, one-line edits, trivial config, quick questions, and throwaway scripts.
version: 4.0.0
---

# dev-craft

Build the right thing, to project conventions, with proof. Scale the ceremony to the task; a full pipeline for
a small change is a failure.

Precedence: the user's request, then project `AGENTS.md` and repo rules (lint, formatter, design system), then
this skill, then `references/` defaults. `AGENTS.md` hard rules (commits, destructive ops, secrets) always win.

## 1. Pick the tier (say it in one line; the user can override; unsure = one tier up)

| Tier | When | Path |
|---|---|---|
| **Trivial** | typo, rename, one-line fix, trivial config | Edit, run the relevant check. Project lint and clean-code minimum still apply. |
| **Standard** | feature or fix in a few files, one endpoint, a UI change, a small schema change, a review | Section 3 |
| **Large** | new module or service, schema + API + UI together, risky migration, auth/security, ambiguous scope, multi-session | Section 3 + `references/phases-large.md` |

Vague input ("Build HRM", "make me a CRM") or attached spec files: read `references/workflow.md` §Input gate
before anything else. Do not start building from a one-liner.

## 2. Scope: what you may write, what you must read

Set it in Frame, state it in one line, keep it visible in the Task Brief:
`Scope: frontend; write: frontend; read-only: backend, database`.

- The other side is read-only, not out of sight. A UI is only right if it matches the real API; a backend change
  is only safe if you know who consumes it. Read the real endpoints, shapes, errors, and consumers.
- Something outside write scope seems wrong or missing: report it as a finding with options. Never edit it
  quietly and never invent the field or endpoint. Editing it needs the user's approval and makes the task
  full-stack (`references/fullstack.md`).

## 3. Flow

```
Frame -> Challenge -> Brief/Spec -> (Design) -> (Contract) -> Plan -> Implement -> Review -> Verify -> Finalize
```
Parenthesised steps run only for UI work (Design) or 2+ components (Contract). Moving backward is normal: if
Implement or Review shows the spec is wrong, stop, record it, return to Challenge/Brief. Never adapt silently.

| Step | Do | Read now | Gate to leave |
|---|---|---|---|
| Frame | Restate task; read AGENTS.md, nearest similar feature, tests, stack versions; set scope + tier | `references/workflow.md` | Scope, tier, stack known |
| Challenge | Test the request against the repo and itself; findings tagged by basis; <=3 questions with defaults; <=3 proposals | `references/challenge.md` | Blocking questions answered; assumptions listed |
| Brief | Task Brief: numbered `REQ-n`, each with a concrete example and `Source:` tag; `Invariants:` list | `references/workflow.md`, `references/challenge.md` | User confirmed (Standard: shown, nothing risky open) |
| Design (UI) | Choose screens, components, design system, states, charts; write `design.md` | `references/frontend-design.md` (+ `ui-patterns/<domain>.md`) | User confirmed direction |
| Data (schema touched) | Review the model; findings as options; check queries | `references/data-modeling.md` (new service: `architecture.md`) | Findings decided |
| Contract (2+ sides) | Define request/response/errors/auth once, consumers listed | `references/fullstack.md` | Consumers agree |
| Plan | Thin vertical slices; every REQ maps to a test | `references/workflow.md`, Large: `phases-large.md` | Every REQ has a test and a done-condition |
| Implement | Failing test, minimal code, match conventions, lint, types, tests; stay in write scope | `references/build-protocol.md`, `idioms/README.md` | Slice proof passes |
| Review | Review your own diff as a stranger would; try to break it | `references/review.md` | No open high-severity finding |
| Verify | Run everything after the last edit; fill the Evidence table; screenshots for UI | `references/verify.md` | Evidence table complete or gaps stated |
| Finalize | Walk REQs, handoff per `AGENTS.md`, propose commit message (do not commit) | `references/verify.md` | Report matches what was done |

Other entry points: **bug** (reproduce, failing test, root cause, fix, regression proof), **refactor**,
**investigate**, **review a diff**, **incoming PR comments**: see `references/workflow.md` §Modes and
`references/review.md`. Large work runs the phased path in `references/phases-large.md` with one approval
checkpoint after TRACE.

## 4. Hard gates

<HARD-GATE>
1. **No commit, push, or merge.** The history is the user's; stage intended files and propose a conventional
   message. Creating a feature branch (`git switch -c <type>/<slug>`) is allowed.
2. **Branch guard.** Never edit on `main`, `master`, or `develop`: protected-branch mistakes are hard to undo.
   Branch first, in every repo the scope touches.
3. **No code without a shown brief** (Large: explicit approval). Unwritten requirements are the main source of rework.
4. **Coverage (Large).** Every P1 requirement traces to a task with an acceptance criterion before BUILD.
5. **Evidence before done.** A claim counts only with output from this session produced after the last
   relevant edit. "Should work" is a guess. Anything not run goes under "Not verified".
6. **Write scope.** No edits outside it without approval; the boundary is the user's call, not yours.
7. **State integrity (Large).** `state.json` and `session.md` are current at every phase boundary, or a
   resumed session starts from lies.
</HARD-GATE>

## 5. Read-now table

| Condition | File |
|---|---|
| Any Standard/Large task | `references/workflow.md` |
| Weighing the request, ambiguity, assumptions | `references/challenge.md` |
| UI built or changed | `references/frontend-design.md`, `references/checklists/ui.md`, one `ui-patterns/` file |
| Tables/schema/queries touched; new service | `references/data-modeling.md`; `references/architecture.md` |
| 2+ components, or FE-only/BE-only against the other side | `references/fullstack.md` |
| Writing code | `references/build-protocol.md`, `references/clean-code-defaults.md`, `references/idioms/README.md` |
| Lint gate | `references/lint-rules.md` |
| Parallel agents / 3+ modules / multi-repo branch check | `references/build-extras.md` |
| Review a diff, PR comments, REVIEW phase | `references/review.md`, `references/checklists/bugs.md`, `references/checklists/security.md` |
| Writing or judging tests | `references/checklists/testing.md` |
| Large task, or Standard with a risk flag (money, authorization, personal data, migration, contract, concurrency) | `references/test-agent.md` |
| Before saying done | `references/verify.md`, `references/red-flags.md` |
| Large phases, state, ADR/spec templates | `references/phases-large.md`, `references/phase-templates.md`, `references/codebase-map-template.md` |
| HARDEN | `references/harden-checks.md` |
| Written plan with DAG | `references/folded-planning-and-task-breakdown.md` |

Related skills (invoke only when that step needs them): `testing-strategies`, `tdd-seam`, `api-design`,
`code-review-and-quality`, `bug-hunting`, `debugging-and-error-recovery`, `observability-engineering`,
`verification-before-completion`, `qa-and-edge-case-tester`, `fe-visual-loop`, `playwright-skill`,
`dispatching-parallel-agents`, `product-thinking`, `project-discovery`, `ui-craft` (full UI pipeline).
If a related skill or plugin is not available, use the matching file in `references/checklists/`
(`bug-hunting` -> `bugs.md`/`security.md`, `testing-strategies` -> `testing.md`); if it is available, use it and
skip the inline file. Plugins under `plugins/`: `tdd-enforcer`, `database-migrations`, `security-audit`, `api-versioning`,
`dependency-audit`, `language-rules`.
