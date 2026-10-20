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

0. **Risk flag check (one line, before the brief):** does the task touch money, authorization, personal data, a
   migration, a contract, or concurrency? If yes, say `Risk flag: <which>`, write an `Invariants:` line (for
   money: parts sum to the whole), and follow `test-agent.md`. A policy choice the code makes (who gets the
   extra cent) is a `Business rule`, not an assumption.
1. **Challenge**, then **Task Brief** (5-10 lines, in chat): goal; scope line; numbered `REQ-1..n` that are the
   acceptance criteria, each with one concrete example (given X expect Y) and a `Source:` tag; `Invariants:`
   (rules that always hold; format in `challenge.md`); out of scope; affected layers
   (FE / BE / DB / infra / tests); assumptions; open questions only the user can answer (policy ones are
   `Business rule`). Proceed if no
   assumption is risky and no question blocks (`challenge.md` says what blocks); otherwise wait. Headless or
   unanswerable: write the questions with defaults, proceed on the safe default, and flag it.
2. **Context** (read only what the layers need): the nearest similar feature; for UI the design source; for
   data the schema and latest migrations; for API the existing contract; for infra compose/CI/config.
3. **Changing existing behavior that has callers:** before editing, save current outputs for representative
   inputs and for each caller; after, show before/after and mark each difference intended or not.
   **Slices** (one complete path each): failing test, minimal code, match conventions, lint (read-only check),
   type check, relevant tests. Detail: `build-protocol.md`. Test-first can be relaxed only for pure config or
   generated code; then say how you proved it instead.
4. **UI slices:** `frontend-design.md`; look at the result before moving on.
5. **Review, Verify, Finish:** `review.md`, `verify.md`. Every `REQ` marked done / partial / not done with
   evidence; handoff in the format `AGENTS.md` defines.

Standard with a risk flag (money, authorization, personal data, migration, contract change, concurrency) also
follows `test-agent.md`. Standard creates no state files, ADRs, or codebase map.

## Modes (narrow the Standard path)

| Mode | Rules | Stop when |
|---|---|---|
| **Feature (lean)** | Derive acceptance and non-goals from the request. One end-to-end path through the layers that own the invariants. Reuse the fitting seam. Add no modes, config, dependency, or service unless acceptance needs it; state any material tradeoff. | Acceptance passes. Report only material omissions. |
| **Bug (surgical)** | Reproduce first when economical, else capture the strongest evidence. Failing test before the fix. Trace symptom to mechanism. Change the narrowest layer that owns the wrong behavior. Check for the same bug elsewhere. No cleanup outside the fix. Regression test stays. | Failure fixed and regression proof passes. |
| **Refactor (safe)** | Define the behavior boundary and establish verification before structural edits. No feature changes. One ownership boundary at a time; every intermediate state builds. Preserve public interfaces, failure behavior, ordering. Use this mode's own proof, not the full Large path, unless the refactor crosses modules or contracts. | Same proof passes before and after; requested structure achieved. |
| **Investigate** | Gather evidence before editing. Separate observed symptom from inferred cause. Rank hypotheses by evidence and cheap falsification. No edit until one mechanism explains the evidence. | Cause (or exact blocker) named with proof. No fix unless authorized. |
| **Review / PR comments** | `review.md`. Read-only unless the user asks for fixes. | Findings delivered; each comment answered. |

## Large path, state, resume

Large path overview, the `.dev-craft/` state files, the decision/assumption lists and resume rules live in
`phases-large.md` (sections Large overview and State). Standard creates none of them.

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
