---
name: dev-craft
description: Right-sized engineering workflow for building features, multi-file changes, refactors, schema/API/UI work, and resuming earlier work. Use it whenever the user asks to build, implement, add, or extend a feature, start a module, resume a task, or "run dev-craft", even if they never name a pipeline. Scales from a short Task Brief for small changes to a full phased pipeline with persistent state for large ones. Enforces requirements traceability, evidence before claims, and project conventions. Skip it for typos, one-line fixes, and trivial config edits.
version: 3.0.0
---

# dev-craft

Build the right thing, to project conventions, with proof. Scale the ceremony to the task: do not run the
full pipeline for small work.

Precedence: the user's request, then the project `AGENTS.md`, then this skill, then `references/` defaults.
Where this skill conflicts with `AGENTS.md` hard rules (commits, destructive ops, secrets), `AGENTS.md` wins.

## 1. Pick the tier first

State the tier in one line and let the user override it.

| Tier | When | Path |
|---|---|---|
| **Trivial** | typo, rename, one-line fix, trivial config | No pipeline. The Minimum Bar (no cryptic names, no legacy idioms) and the project lint gate still apply. |
| **Standard** | a feature or fix touching a few files, a UI change, one endpoint, a small schema change | §3 |
| **Large** | new module, schema + API + UI together, public interface or migration with risk, auth/security, ambiguous scope, multi-session work | §4 |

## 2. Input quality gate

| Input | Action |
|---|---|
| Short or vague ("Build HRM", "Make me a CRM") | Do not start building. Draft a Task Brief from what is known, list the open questions, and ask the user to confirm. Offer `product-thinking` if the idea itself is unformed. |
| "Just build it, I'll know it when I see it" | Same: draft the brief and get a yes. Building without written requirements usually produces rework. |
| Spec files attached (md, pdf, xlsx, csv) | Load `project-discovery` to extract the domain model, then continue. |
| `PRODUCT.md`, `DOMAIN.md`, or `PLAN.md` exists | Load it as the requirements source. |
| Clear request or spec | Proceed. |

## 3. Standard path

1. **Task Brief** (5-10 lines, in chat): goal; numbered requirements `REQ-1..n` (these are the acceptance
   criteria); out of scope; affected layers (FE / BE / DB / infra / tests); assumptions; open questions the
   user owns. Proceed if no assumption is risky and no open question blocks. Otherwise wait for the user.
2. **Context** (read only what the layers need): project `AGENTS.md`; the nearest similar feature; for UI the
   design source; for data the schema and latest migrations; for API the existing contract; for infra the
   compose/CI/config files. Reuse detected conventions from `.dev-craft/state.json` if present and current.
3. **Build in slices** (one complete path per slice): write a failing test → minimal code → match conventions
   → lint (read-only check) → type check → run the relevant tests. Detail: `references/build-protocol.md`.
4. **UI slices:** apply §6 and look at the result before moving on.
5. **Finish:** requirements check (every `REQ` marked done / partial / not done, with evidence), self-review
   of the diff, handoff in the format `AGENTS.md` defines.

Standard tasks create no state files, ADRs, or codebase map.

## 4. Large path

Full detail per phase: `references/phases-large.md`. Load it phase by phase, not all at once.

```
LOAD → SCOPE → REQUIRE → SCAN → ALIGN → DESIGN → TRACE ──[ONE APPROVAL CHECKPOINT]──→
BUILD → TEST → REVIEW → HARDEN → SHIP-PREP
(SOURCE and CONTRACT run only when needed; STATUS is available any time)
```

| Phase | Output |
|---|---|
| LOAD | `state.json` initialized or resumed |
| SCOPE | layer (be / fe / fullstack) and mode (build / ticket) |
| REQUIRE | `domain.md` from specs, or confirmed "no specs" |
| SCAN | conventions and codebase map (once; cached by git commit) |
| ALIGN | scope confirmed, assumptions, out of scope, glossary |
| DESIGN | spec + plan + build order + ADRs (includes data model and infra changes) |
| TRACE | requirements matrix `REQ-ID → task → acceptance criterion` (coverage gate) |
| BUILD | vertical slices (§3 step 3 loop) |
| TEST | full relevant suites; contract conformance for fullstack |
| REVIEW | seven-axis review, lint gate, requirements reality-check |
| HARDEN | cross-cutting security and risk register |
| SHIP-PREP | rollback plan, ADR updates, final verification, proposed commit message |

**One approval checkpoint:** after TRACE, present the brief, plan, build order, and matrix together and get one
explicit approval before BUILD. Do not ask for sign-off at each phase.

**Ticket mode** (small change inside an already-understood codebase): LOAD → SCOPE → scoped BUILD → TEST →
REVIEW → SHIP-PREP. Skip REQUIRE and TRACE unless the change alters spec coverage.

## 5. Hard gates

<HARD-GATE>
1. **No commit, push, or merge.** Stage the intended files and propose a conventional commit message. Commit
   only when the user explicitly asks. Creating a feature branch is allowed (`git switch -c <type>/<slug>`).
2. **Branch guard.** Never edit while on `main`, `master`, or `develop`. Create a feature branch first, in
   every repo the scope touches.
3. **No code without an approved brief.** Standard: the brief was shown and nothing risky is open. Large: the
   explicit checkpoint approval.
4. **Coverage (Large).** Every P1 requirement traces to a task with an acceptance criterion before BUILD.
   Lower-priority gaps may be deferred only with the user's explicit acknowledgement.
5. **Evidence before done.** A claim counts only with output from this session, produced after the last
   relevant edit: a command and its result, a test, a screenshot, or `path:line`. Never write "should work"
   or "zero issues" without evidence. Unverified requirements are not complete.
6. **State integrity (Large).** `state.json` and `session.md` are current at every phase boundary.
</HARD-GATE>

## 6. Layer rules

- **Conventions:** project conventions always win. `references/clean-code-defaults.md` applies only where the
  project has no convention. Match the nearest existing example.
- **UI:** read the design source (project `DESIGN.md`/theme/tokens first, then `~/.config/agents/DESIGN.md`).
  Reuse existing components, use tokens only, handle loading / empty / error / disabled / long-content states.
  Before moving on, run the app and capture screenshots at mobile and desktop widths of every changed route;
  compare with the nearest existing screen. If the app cannot run, say so and report the remaining risk.
  Larger UI pipelines go to `ui-craft`.
- **Data:** read the current schema and the latest migrations first. Every change is a migration with a
  rollback, plus NOT NULL, defaults, foreign keys, and indexes on FK and filtered columns. State the effect on
  existing data. For migrations, prove upgrade and rollback in a disposable database.
- **API:** extract the existing contract from source, never guess. New endpoints are tagged `[NEW]` in
  `api-contract.md`. Validate input at the boundary, return errors in the project's error format, check
  authorization on every new endpoint.
- **Infra and config:** read existing compose/CI/IaC first, name the target environment, list new env vars in
  the handoff, and never hardcode secrets or environment-specific values.
- **Stack versions:** read exact versions from dependency files. Fetch official docs only for new libraries,
  new APIs, or version-sensitive code (SOURCE phase), not for every dependency.

## 7. Per-slice quality gates

Every slice passes before it is staged: lint (read-only check), type check, relevant tests, convention match,
security basics (no hardcoded secrets, no `eval`, no unsafe HTML injection), and the clean-code minimum bar.
Run `references/lint-rules.md` as the deterministic lint gate where the project uses it.

**Review stance:** assume the first pass needs work, but cap revision cycles at two. After that, summarize
what was tried and ask. Automatic fail: claiming "zero issues" or a perfect score without running the tools.

## 8. State (Large only)

```
.dev-craft/
├── state.json    # phase, tier, stack, conventions + git hash, requirements status, sessionFile
├── spec.md       # brief, plan, build order, requirements matrix, ADR summaries
└── session.md    # handoff for context rotation: goal, decisions, changed files, verification, open items
```

Add `.dev-craft/` to `.git/info/exclude` so it does not pollute `git status`. Update state at phase boundaries,
not after every step.

| Resume scenario | Behavior |
|---|---|
| No `.dev-craft/` | Start at LOAD |
| State exists and `sessionFile` is current | Load state, skip completed phases |
| `sessionFile` missing or stale | Flag it to the user before proceeding |
| All phases complete | Ask whether this is a new task before creating a session |
| Context near limit | Write `session.md`, resume from it |

## 9. Status reporting

- Standard: just the handoff. No status block.
- Large: after each phase and when resuming, print one block, and fold ad-hoc user fixes into the current
  phase instead of silently editing.

```
STATUS: Phase <n> [done/pending] | NEXT: <single next action> | STATE: sessionFile=<file>
```

## 10. Failure handling

| Failure | Response |
|---|---|
| State missing or stale | Repair state and session file first |
| Tests fail | Invoke `debugging-and-error-recovery`; rerun after each fix |
| Lint or type check fails | Fix and rerun, never skip |
| Two failed fix attempts | Stop, summarize, change approach or ask |
| Critical or High security finding | Block, remediate before proceeding |
| Contract conformance fails | Fix the implementation to match the contract |

## 11. Related skills and references

Skills (invoke only for the phase that needs them): `planning-and-task-breakdown` (task slicing),
`testing-strategies` (before writing tests), `api-design`, `architecture-patterns`, `code-review-and-quality`
and `bug-hunting` (REVIEW, security-sensitive code), `observability-engineering` (HARDEN),
`verification-before-completion` (phase exits), `debugging-and-error-recovery`, `product-thinking`,
`project-discovery`, `ui-craft`.

References (load on demand):
- `references/phases-large.md`: detailed workflow per Large-path phase
- `references/phase-template.md`: template for each phase
- `references/clean-code-defaults.md`: naming, structure, error handling, typing defaults
- `references/build-protocol.md`: per-slice SECURE and MATCH detail, worktree mode
- `references/harden-checks.md`: eight cross-cutting security checks
- `references/lint-rules.md`: deterministic lint gate
- `references/modern-patterns.md`: clean patterns and defensive programming
- `references/codebase-map-template.md`: template for the SCAN phase
- `references/cross-skill.md`: cross-skill conventions and best practices
