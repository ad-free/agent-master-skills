# No project AGENTS.md / CLAUDE.md

Read when the repo root (and the folder you will edit) has neither file. The global rules still apply; what is
missing are the project facts. Derive them, prove them, use them, then offer to save them. Never guess a
command, and never block the user's task on writing this file.

1. **Substitutes first:** `AGENTS.md`/`CLAUDE.md` in subfolders (`backend/`, `frontend/`), `.cursorrules`,
   `.github/copilot-instructions.md`, `CONTRIBUTING.md`, README, `docs/`, the project's memory.
2. **Derive, most reliable source first:** CI workflows (`.github/workflows/*`: what CI runs is the de facto
   gate) > `Makefile` / `package.json` scripts / `pyproject.toml` / `justfile` > lint configs >
   `docker-compose*` and `.env.example` (never read `.env`) > `git log --oneline -20` for commit style.
3. **Baseline:** run the derived gate once before editing. It proves the commands work and records failures
   that already exist, so they are not blamed on the change.
4. **Ask only what cannot be derived** (<=3, one message, each with a safe default): which database is safe for
   tests (default: none; treat every DB as the user's dev DB), commands that touch production, write scope.
5. **Say it in the brief:** `No AGENTS.md; gate derived from <source>: <cmd>`.
6. **Finalize:** show the filled-in draft below in the handoff (each line's source in a comment) and ask whether
   to save it. It is a new file in the user's repo: create it only on a yes, never commit it. Trivial tasks skip
   the draft and only find the one check command.

## Draft (keep it under ~40 lines; facts, not essays)

```markdown
# AGENTS.md — <project>

Gate: `<one command that runs lint, types and tests; e.g. make check>`

## Commands
- Run: `<cmd>` (from `<dir>`)
- Test: backend `<cmd>`; frontend `<cmd>`; e2e `<cmd or none>`
- Lint/types: `<cmd>`
- Migrations: `<tool/cmd>`; safe test database: `<url pattern or "none: ask">`

## Rules
- Never: <commands that touch production or shared data>
- Write scope defaults: <e.g. backend and frontend; infra read-only>
- Conventions the linters do not enforce: <naming, layering, i18n keys, error format>
- Done means: gate passes; UI changes checked at 1440 and 390 in every locale and role they touch
```

The `Gate:` line is read by the Stop hook (`tools/hooks/stop-gate.sh`): keep it one line, backticked, and fast
enough to run at every stop (put slow e2e suites in the Commands list instead). The hook runs it only after the
user approves it once (`stop-gate.sh --trust`); tell them, never run that yourself. Add a one-line `CLAUDE.md`
containing `@AGENTS.md` so Claude Code and Codex read the same file.
