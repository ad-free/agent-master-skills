# Workflow

Detail for the flow in `SKILL.md`. Read the section you need.

## Input gate

| Input | Action |
|---|---|
| Short or vague ("Build HRM", "Make me a CRM") | Do not build. Draft a Task Brief from what is known, list open questions, ask the user to confirm. Offer `product-thinking` if the idea itself is unformed. |
| "Just build it, I'll know it when I see it" | Same: draft the brief and get a yes. Building without written requirements produces rework. |
| Spec files attached (md, pdf, xlsx, csv) | Load `project-discovery` to extract the domain model, then continue. |
| `PRODUCT.md`, `DOMAIN.md`, or `PLAN.md` exists | Load it as the requirements source. |
| Thin description | Offer the task template in `challenge.md`. |
| Clear request or spec | Proceed. |

## Frame (all Standard/Large tasks)

1. Read project `AGENTS.md`, the nearest similar feature, the test setup, and exact stack versions from
   dependency files. Reuse `.dev-craft/` state if present and current.
2. Set **scope** (write vs read-only, `SKILL.md` §2) and **tier**.
3. Record the stack block once and reuse it (run commands from the right directory in monorepos):
```
Scope: <surfaces>; write: <...>; read-only: <...>
Backend: <lang/version>, <framework>, tests: <cmd>, lint: <cmd>
Frontend: <lang/version>, <framework>, tests: <cmd>, lint: <cmd>
Database: <engine/version>, migrations: <tool/cmd>
Integration/e2e: <cmd or "none">
```

## Standard path

1. **Challenge**, then **Task Brief** (5-10 lines, in chat): goal; scope line; numbered `REQ-1..n` that are the
   acceptance criteria, each with one concrete example (given X expect Y); out of scope; affected layers
   (FE / BE / DB / infra / tests); assumptions; open questions only the user can answer. Proceed if no
   assumption is risky and no question blocks (`challenge.md` says what blocks); otherwise wait. Headless or
   unanswerable: write the questions with defaults, proceed on the safe default, and flag it.
2. **Context** (read only what the layers need): the nearest similar feature; for UI the design source; for
   data the schema and latest migrations; for API the existing contract; for infra compose/CI/config.
3. **Slices** (one complete path each): failing test, minimal code, match conventions, lint (read-only check),
   type check, relevant tests. Detail: `build-protocol.md`. Test-first can be relaxed only for pure config or
   generated code; then say how you proved it instead.
4. **UI slices:** `frontend-design.md`; look at the result before moving on.
5. **Review, Verify, Finish:** `review.md`, `verify.md`. Every `REQ` marked done / partial / not done with
   evidence; handoff in the format `AGENTS.md` defines.

Standard creates no state files, ADRs, or codebase map.

## Modes (narrow the Standard path)

| Mode | Rules | Stop when |
|---|---|---|
| **Feature (lean)** | Derive acceptance and non-goals from the request. One end-to-end path through the layers that own the invariants. Reuse the fitting seam. Add no modes, config, dependency, or service unless acceptance needs it; state any material tradeoff. | Acceptance passes. Report only material omissions. |
| **Bug (surgical)** | Reproduce first when economical, else capture the strongest evidence. Failing test before the fix. Trace symptom to mechanism. Change the narrowest layer that owns the wrong behavior. Check for the same bug elsewhere. No cleanup outside the fix. Regression test stays. | Failure fixed and regression proof passes. |
| **Refactor (safe)** | Define the behavior boundary and establish verification before structural edits. No feature changes. One ownership boundary at a time; every intermediate state builds. Preserve public interfaces, failure behavior, ordering. Use this mode's own proof, not the full Large path, unless the refactor crosses modules or contracts. | Same proof passes before and after; requested structure achieved. |
| **Investigate** | Gather evidence before editing. Separate observed symptom from inferred cause. Rank hypotheses by evidence and cheap falsification. No edit until one mechanism explains the evidence. | Cause (or exact blocker) named with proof. No fix unless authorized. |
| **Review / PR comments** | `review.md`. Read-only unless the user asks for fixes. | Findings delivered; each comment answered. |

## Large path

Load `phases-large.md` one phase at a time.

```
LOAD -> SCOPE -> REQUIRE -> SCAN -> ALIGN (incl. Challenge) -> DESIGN -> TRACE --[ONE APPROVAL]--> BUILD -> TEST -> REVIEW -> HARDEN -> SHIP-PREP
(SOURCE and CONTRACT run only when needed; STATUS any time)
```

| Phase | Output |
|---|---|
| LOAD | state initialized or resumed |
| SCOPE | layer (be / fe / fullstack), mode (build / ticket), scope line |
| REQUIRE | `domain.md` from specs, or confirmed "no specs" |
| SCAN | conventions and codebase map (once; cached by git commit) |
| ALIGN | findings, assumptions, out of scope, glossary |
| DESIGN | spec + plan + build order + ADRs; `design.md` for UI; data model and infra changes |
| TRACE | matrix `REQ-ID -> task -> acceptance criterion -> test` |
| BUILD | vertical slices |
| TEST | full relevant suites; contract conformance for fullstack |
| REVIEW | `review.md` axes, lint gate, requirements reality-check |
| HARDEN | `harden-checks.md`, risk register |
| SHIP-PREP | rollback plan, ADR updates, final verification, proposed commit message |

**One approval checkpoint** after TRACE: present brief, plan, build order, and matrix together. Do not ask for
sign-off per phase.
**Ticket mode** (bounded change in an understood codebase): LOAD, SCOPE, scoped BUILD, TEST, REVIEW, SHIP-PREP.

## Layer rules

- **Conventions:** project conventions win; `clean-code-defaults.md` only where the project has none. Match
  the nearest existing example.
- **UI:** `frontend-design.md`, `checklists/ui.md`. Larger UI pipelines go to `ui-craft`.
- **Data:** `data-modeling.md`. Every change is a migration with rollback; state the effect on existing data.
- **API:** extract the existing contract from source, never guess; tag new endpoints `[NEW]`; validate input at
  the boundary; errors in the project's format; authorization on every new endpoint. See `fullstack.md`.
- **Infra/config:** read existing compose/CI/IaC first, name the target environment, list new env vars in the
  handoff, never hardcode secrets or environment-specific values.
- **Stack versions:** read exact versions from dependency files; fetch official docs only for new libraries,
  new APIs, or version-sensitive code.

## Per-slice quality gates

Before staging: lint (read-only), type check, relevant tests, convention match, security basics (no hardcoded
secrets, no `eval`, no unsafe HTML), clean-code minimum. `lint-rules.md` is the deterministic lint gate. Cap
revision cycles at two, then summarize what was tried and ask. Claiming "zero issues" without running the tools fails the gate.

## State (Large only)

```
.dev-craft/runs/<slug>/
  state.json   # phase, tier, scope, stack, conventions + git hash, requirement status, sessionFile
  spec.md      # brief, plan, build order, requirements matrix, ADR summaries, design/contract if any
  session.md   # handoff: goal, done, next, blockers, changed files, verification, DECISIONS, ASSUMPTIONS
```
(Matches `skills/SHARED.md`. A legacy `.dev-craft/state.json` is read as-is if it exists.) Add `.dev-craft/` to
`.git/info/exclude`. Update state at phase boundaries only.

`session.md` keeps two lists so nothing is decided silently and the final report can quote them:
`Decision: <what>; why; basis Code|Docs|Run|Logic; reversible yes|no` and `ASSUMPTION: <what>; basis`.

| Resume scenario | Behavior |
|---|---|
| No `.dev-craft/` | Start at LOAD |
| State exists, `sessionFile` current | Load state, skip completed phases |
| `sessionFile` missing or stale | Flag it to the user before proceeding |
| All phases complete | Ask whether this is a new task before creating a session |
| Context near limit | Write `session.md`, resume from it |

Large status line after each phase and on resume (fold ad-hoc user fixes into the current phase):
`STATUS: Phase <n> [done/pending] | NEXT: <single next action> | STATE: sessionFile=<file>`. Standard: handoff only.

## Failure handling

| Failure | Response |
|---|---|
| State missing or stale | Repair state and session file first |
| Tests fail | `debugging-and-error-recovery`; rerun after each fix; never loosen the test |
| Lint or type check fails | Fix and rerun, never skip |
| Two failed fix attempts | Stop, summarize, change approach or ask |
| Critical or High security finding | Block, remediate before proceeding |
| Contract conformance fails | Fix the implementation to match the contract |
| Spec found wrong during Implement/Review | Stop, record in `session.md`, return to Challenge/Brief |
