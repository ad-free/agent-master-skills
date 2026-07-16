# AGENTS.md — agent-master-skills

Persistent instructions for any AI agent working in this repository.
This repo is a **skill library for OpenCode**, not an application. Every change
here changes how agents behave in downstream projects.

---

## 0. What This Repo Is

- A collection of composable agent skills. Each skill lives in `skills/<name>/`
  and is a `SKILL.md` (plus optional `references/`, `scripts/`, `plugins/`).
- Skills are loaded on demand via the `skill()` tool. They are NOT auto-run.
- Installed into OpenCode as symlinks (see README). Edits here are live
  immediately — there is no build step.

**Consequence:** precision and clarity in every SKILL.md matters. A vague or
contradictory instruction here degrades agent behavior everywhere the skill is
used. Treat this repo as a published library.

---

## 1. Skill Router (load the right skill first)

Before doing any task, pick the skill from this decision tree. Do not improvise
a workflow when a skill exists for it.

```
User Request
 ├─ vague / idea-stage prompt?        → product-thinking → planning-and-task-breakdown → dev-craft | ui-craft
 ├─ spec files given (xlsx/csv/md/pdf)?→ project-discovery → planning-and-task-breakdown → dev-craft
 ├─ new feature / project?
 │   ├─ has clear spec?               → planning-and-task-breakdown → dev-craft | ui-craft
 │   └─ no spec?                      → planning-and-task-breakdown (collect, verify, ask, write plan)
 ├─ bug / failing test / weird behavior? → debugging-and-error-recovery
 ├─ large multi-module project?       → dev-craft + agent-orchestration (git worktree isolation)
 ├─ multiple independent tasks?       → dispatching-parallel-agents
 ├─ about to claim "done"?            → verification-before-completion
 ├─ review code?                      → code-review-and-quality
 ├─ security audit / vuln discovery?  → bug-hunting
 ├─ frontend / UI work?               → ui-craft
 ├─ screenshot / image as reference?  → image-to-design-spec
 └─ pre-merge / release validation?   → quality-gates
```

When unsure, **plan first** (`planning-and-task-breakdown`), then execute.

---

## 2. Iron Laws (non-negotiable)

These are the discipline gates the skills encode. Honor them even when a skill
is not explicitly loaded.

1. **NO implementation without a written plan.** (`planning-and-task-breakdown`)
2. **NO parallel agents without a shared contract.** (`agent-orchestration`)
3. **NO parallel dispatch without independence verification.** (`dispatching-parallel-agents`)
4. **NO merge without quality gates.** (`quality-gates`)
5. **NO code without review evidence.** (`code-review-and-quality`)
6. **NO completion claims without fresh verification evidence.** (`verification-before-completion`)
7. **NO fixes without root-cause investigation first.** (`debugging-and-error-recovery`)
8. **NO attack surface without intentional probing.** (`bug-hunting`)

---

## 3. Daily Operating Rules (performance & correctness)

These keep agent output fast, cheap, and correct.

- **Plan before code.** A 5-minute plan prevents an hour of rework. Never skip
  `planning-and-task-breakdown` on multi-file or multi-module work.
- **Evidence over assumption.** Prove it works (run lint/type/test, read the
  output) before saying so. Never claim success from memory.
- **Deterministic before judgment.** Run `lint`/`typecheck`/`test` first;
  only escalate to LLM-judgment (code-review, quality-gates LLM axis) after
  deterministic checks pass.
- **Root cause over symptoms.** When something fails, find the cause; do not
  patch the error message and hope.
- **Keep context lean.** Prefer `Glob`/`Grep` over reading whole trees. Read
  only the files you act on. Use the `Task` tool for broad exploration so the
  main context stays small.
- **Minimize token waste.** Concise responses. Batch independent tool calls in
  one message. Do not re-read files you already have in context.
- **One skill, one concern.** Skills and plugins must be single-responsibility
  and idempotent (running twice yields the same result).
- **Checkpoints, not autopilot.** Pipeline phases have human checkpoints. Stop
  and surface decisions; do not silently barrel through.
- **Resume, don't restart.** Pipeline state lives in `.dev-craft/runs/<slug>/`
  (`state.json`, registered in `.dev-craft/index.json`). Detect and resume prior
  progress instead of redoing work.

---

## 4. Repo Etiquette (contributing to the skills)

When editing skills in this repo:

- **Edit SKILL.md, not copies.** Skills are symlinked into `~/.config/opencode/skills`.
  Never edit the symlink target's resolved copy elsewhere — edit the source here.
- **Front-matter is required.** Every skill `SKILL.md` starts with:
  ```yaml
  ---
  name: <skill-name>
  description: <one-line, when-to-use, loaded on demand>
  metadata:
    origin: agent-master-skills
  ---
  ```
  The `description` is what makes the skill discoverable — make it specific
  about *when* to use it.
- **No build, no install script to run.** After editing, the change is live.
  Verify by loading the skill via `skill()` in a test session.
- **Keep README in sync.** If you add/remove/rename a skill, update the tables
  in `README.md` and `skills/SHARED.md`.
- **Respect the skill router.** Don't create overlapping skills. Extend via the
  plugin system (`skills/PLUGIN-SYSTEM.md`) when adding optional capability.
- **Don't commit secrets, state, or caches.** `.gitignore` already excludes
  `.venv/`, `__pycache__/`, `.ruff_cache/`, etc. Never force-add them.
- **Cross-skill consistency.** Shared terminology lives in `context.md`; the
  handoff/state schema is in `skills/SHARED.md`. Keep them aligned.

---

## 5. Verification Before Claiming Done

Before reporting any task complete in THIS repo (e.g. a skill edit or refactor):

1. The edited `SKILL.md` still has valid front-matter and renders.
2. `README.md` / `SHARED.md` tables reflect the change.
3. The skill loads without error via `skill(<name>)` in a session.
4. No broken symlinks remain in `~/.config/opencode/skills`.

---

## 6. Quick Reference

| Situation | Skill |
|-----------|-------|
| Vague idea | product-thinking |
| Spec files (xlsx/csv/md/pdf) | project-discovery |
| New feature / plan | planning-and-task-breakdown |
| Backend / API build | dev-craft |
| Frontend / UI build | ui-craft |
| Tests fail / bug | debugging-and-error-recovery |
| About to say "done" | verification-before-completion |
| Code review | code-review-and-quality |
| Security audit | bug-hunting |
| Parallel independent tasks | dispatching-parallel-agents |
| Multi-module orchestration | agent-orchestration |
| Pre-merge validation | quality-gates |
| Screenshot → design tokens | image-to-design-spec |
