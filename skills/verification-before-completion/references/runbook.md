# Verification Runbook (Gate 2)

Concrete commands, evidence format, and verdict template for Gate 2
(Deterministic) of `verification-before-completion`. Ported from the
deprecated `verify-gate` skill — the policy lives in `SKILL.md`, the
how-to lives here.

## 1. Gate Checklist

Before declaring any task done, run ALL of these checks and capture output:

### 1.1 Lint

```bash
npm run lint            # JavaScript/TypeScript
uv run ruff check .     # Python
golangci-lint run       # Go
cargo clippy            # Rust
```

### 1.2 Typecheck

```bash
npm run typecheck       # JavaScript/TypeScript
uv run mypy .           # Python
go vet ./...            # Go
cargo check             # Rust
```

### 1.3 Tests

```bash
npm test                # JavaScript/TypeScript
uv run pytest           # Python
go test ./...           # Go
cargo test              # Rust
```

### 1.4 Build

```bash
npm run build           # JavaScript/TypeScript
uv run build            # Python
go build ./...          # Go
cargo build --release   # Rust
```

## 2. Evidence Capture

For each check, capture: command run, exit code, full output
(stdout + stderr), timestamp. Store under `.dev-craft/evidence/`
(or the project's equivalent), e.g. `lint-<timestamp>.txt`.

## 3. Verdict Template

All pass → `VERIFY GATE PASSED` with per-check ✅ + evidence path.
Any fail → `VERIFY GATE FAILED` with per-check status, first error
per failed check, and "fix before declaring done."

## 4. Rules

1. **No "done" without a gate pass.** Any failure = not done.
2. **Fresh evidence only.** Never reuse a previous run's output.
3. **Full output captured**, not just exit codes. **Timestamped.**
4. **No skipping** — every check runs, even if "it should pass."

## 5. Quick Gate (fast iterations)

```bash
npm run lint && npm run typecheck && npm test -- --passWithNoTests && npm run build
```

(Translate per stack using §1.)

## 6. Bypass

Only when: the user explicitly says "skip verification"; the task is
read-only (no code changes); or documentation-only. Always note the
bypass in the session log.

## 7. Retention

Keep evidence 7 days; archive completed-task evidence; clean up
anything older than 30 days.
