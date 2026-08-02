# AGENTS.md — Global Agent Instructions

Cross-project rules for every OpenCode session. Project-level `AGENTS.md`
extends/overrides these.

**Skills:** library at `~/.config/opencode/skills/`. Load via explicit
`skill()` — never improvise a workflow the library already covers.

**Ponytail plugin:** runs automatically in the background on every edit/write
— it checks for reusable code before new code is written. It is a plugin
hook, not a skill; don't invoke it, don't narrate its checks, just respect
its output. Your responsibility is the *policy* (Iron Law #10, "reuse before
create"), not re-implementing what the plugin already does.

---

## 1. Skill Router — decide before acting

Route by task type, not by tech stack. Skills chain — follow the arrow.

| Task signal | Route |
|---|---|
| Vague idea, "how should we…" | product-thinking → planning-and-task-breakdown → dev-craft \| ui-craft |
| Spec files (xlsx/csv/md/pdf) | project-discovery → planning-and-task-breakdown → dev-craft |
| New feature / new project | planning-and-task-breakdown → dev-craft \| ui-craft |
| Bug / failing test / weird behavior | debugging-and-error-recovery → verification-before-completion |
| Frontend / UI work | ui-craft (+ frontend-design for visual polish) → verification-before-completion |
| Screenshot / image reference | image-to-design-spec → ui-craft |
| Infra / IaC / deploy change | dev-craft → Infra Safety (§ 7) → quality-gates |
| Large multi-module project | dev-craft + agent-orchestration |
| Multiple independent tasks | dispatching-parallel-agents |
| Review code | code-review-and-quality |
| Security audit / vuln discovery | bug-hunting → verification-before-completion |
| About to claim "done" | verification-before-completion (mandatory — § 4) |

**Unsure which skill?** Start with `planning-and-task-breakdown` — it produces
a plan every other skill can execute against.

---

## 2. Iron Laws — non-negotiable

1. No implementation without a written, approved plan.
2. No "done" claim without fresh verification evidence — show lint/type/test
   output, never assume it from memory.
3. No fix without root-cause investigation first. Patch causes, not symptoms.
4. No merge without quality gates green (lint, typecheck, tests).
5. No code shipped without self-review evidence.
6. No parallel work without verified independence + a written contract.
7. No security assessment without active probing — assumption isn't
   verification.
8. No weakening or deleting a test to force a pass. Flag a suspect test and
   wait for a decision instead.
9. No calling unfamiliar or uncommon APIs without confirming they exist
   first (docs, CLI, or a live version check).
10. **Reuse before creating.** Check for an existing type, helper, component,
    or util before writing a new one. The ponytail plugin surfaces
    candidates automatically — act on what it finds.
11. Python only via `uv run` (`uv run pytest`, `uv run python script.py`).
    Bare `python` / `python3` / `py` / `pip` / `virtualenv` are forbidden.
12. Filesystem inspection stays inside the project (`.`), depth ≤ 3, via
    `Glob` / `Grep` / CodeGraph — never unrestricted or system-wide scans.
13. No hardcoded or outdated package versions. Always resolve to latest
    stable; never a deprecated major version unless explicitly instructed.
14. No destructive or state-changing action (`git commit`/`push`,
    `terraform apply`, `kubectl apply`, `rm -rf`, DB migrations) without
    showing the diff/plan and getting explicit approval first.

---

## 3. Operating Principles

- **Plan before code; evidence before "done."** Lint → typecheck → test, in
  that order, and read the actual output.
- **Read before edit.** Match existing naming, structure, and conventions.
- **Minimal footprint.** Diff-only edits — never reprint unchanged code. One
  concern per change.
- **Lean context.** `Glob`/`Grep`/CodeGraph over full-tree reads; delegate
  broad discovery to the explore agent so the main context stays small.
- **Ambiguity:** small gap → state the assumption inline and proceed. Large
  gap → ask exactly one question (§ 5 decides which case you're in).
- **Resume, don't restart.** Check `.dev-craft/`, `.ui-craft/`, `PLAN.md`,
  and `git log` for prior state before starting fresh.
- **Readable code, always.** Self-documenting names (no cryptic single
  letters except `i/j/k` in short loops, `x/y` in short math), comments
  explain *why* not *what*, no dense one-liners that hide logic.

---

## 4. Definition of Done

A task is done only when every box below is true — and you say so explicitly
rather than reporting success by default:

- [ ] Lint, type-check, and tests all pass — output shown, not claimed.
- [ ] No test was weakened, skipped, or deleted to force a pass.
- [ ] The change addresses the actual request; no unrelated regressions.
- [ ] Edge cases (null / empty / boundary) are handled.
- [ ] Style is clean: no cryptic names, consistent imports, one concern per
      change.
- [ ] Self-review complete (`code-review-and-quality` or equivalent) — no
      open issues.
- [ ] No stray `TODO`/`FIXME` left uncaptured in an issue.

---

## 5. Escalation — Ask vs. Proceed

**Ask before proceeding when:**
- Direction is genuinely ambiguous and guessing would waste real time.
- A trade-off exists that the user should own (perf vs. readability, speed
  vs. correctness).
- The action is large or irreversible (deletions, schema migrations, public
  API changes, merges, deploys).
- Root cause is still unclear after two investigation rounds — escalate with
  what's been ruled out.

**Proceed on your own judgment when:**
- The ambiguity has an obvious, low-risk default — state it and move on.
- The codebase already has an established pattern to follow.
- Asking would cost more time than trying the direct path and verifying.

**Rule of thumb:** if a wrong guess costs more than five minutes to unwind,
ask first. Otherwise, proceed.

---

## 6. Multi-Agent Work & Error Recovery

**Parallel tasks** (`dispatching-parallel-agents`): write a shared contract
(data shapes, file ownership) before dispatch; no overlapping edits; join and
verify consistency at the end.

**Multi-module work** (`agent-orchestration`): order by dependency (DAG),
execute in stages, each agent hands off a written summary — never a silent
handoff.

**When something breaks** (`debugging-and-error-recovery`): capture full
error context (trace, input, state) → reproduce deterministically → narrow
to root cause with evidence → fix the cause → add a regression test. Stuck
after two rounds? Escalate with what's ruled out — don't keep guessing.

---

## 7. Infra & Git Safety

- Never `commit`, `push`, `amend`, or open a PR without explicit
  instruction.
- Always inspect `git status` / `git diff` before staging. Never commit
  secrets or `.env` files.
- For infra changes: show `terraform plan` / `kubectl diff` / migration
  preview first; confirm target environment and rollback path; never
  auto-apply (Iron Law #14).
- Destructive actions (`rm -rf`, DB drops/truncates, bulk resets, cloud
  resource deletion) always require explicit approval.

---

## 8. Maintaining This File

When a new gotcha, dead convention, or repeated mistake surfaces, add one
short line here instead of letting it live only in chat history. This is a
checklist, not documentation — keep entries terse and specific.

<!-- CODEGRAPH_START -->
## CodeGraph

In repositories indexed by CodeGraph (`.codegraph/` exists at repo root),
reach for it BEFORE grep/find or reading files when you need to understand
or locate code:
- **MCP tool:** `codegraph_explore`
- **Shell:** `codegraph explore "<symbol names or question>"`

If there is no `.codegraph/` directory, skip CodeGraph entirely — indexing
is the user's decision.
<!-- CODEGRAPH_END -->
