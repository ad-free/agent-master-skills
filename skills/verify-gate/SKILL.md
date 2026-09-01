---
name: verify-gate
description: "Use when you need a mandatory verification gate that runs before any \"done\" claim. Captures fresh evidence of completion: lint output, test results, build status, typecheck results. Prevents premature \"done\" claims by requiring proof, not assumptions."
model: big-pickle
version: 2.1.0
preamble-tier: 3
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
triggers:
  - "verify"
  - "done"
  - "complete"
  - "finish"
  - "gate"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
---

# Verify Gate

Mandatory verification gate that runs before any "done" claim. Captures fresh evidence of completion.

---

## 1. GATE CHECKLIST

Before declaring any task done, run ALL of these checks and capture output:

### 1.1 Lint
```bash
# JavaScript/TypeScript
npm run lint

# Python
uv run ruff check .

# Go
golangci-lint run

# Rust
cargo clippy
```

### 1.2 Typecheck
```bash
# JavaScript/TypeScript
npm run typecheck

# Python
uv run mypy .

# Go
go vet ./...

# Rust
cargo check
```

### 1.3 Tests
```bash
# JavaScript/TypeScript
npm test

# Python
uv run pytest

# Go
go test ./...

# Rust
cargo test
```

### 1.4 Build
```bash
# JavaScript/TypeScript
npm run build

# Python
uv run build

# Go
go build ./...

# Rust
cargo build --release
```

---

## 2. EVIDENCE CAPTURE

For each check, capture:
- Command run
- Exit code
- Full output (stdout + stderr)
- Timestamp

Store in `.dev-craft/evidence/`:
```
.dev-craft/evidence/
  ├── lint-2024-01-15T10:30:00Z.txt
  ├── typecheck-2024-01-15T10:30:05Z.txt
  ├── test-2024-01-15T10:30:10Z.txt
  └── build-2024-01-15T10:30:15Z.txt
```

---

## 3. GATE VERDICT

### All Pass
```
✅ VERIFY GATE PASSED

Lint:        ✅ (exit 0)
Typecheck:   ✅ (exit 0)
Tests:       ✅ (exit 0)
Build:       ✅ (exit 0)

Evidence: .dev-craft/evidence/
```

### Any Fail
```
❌ VERIFY GATE FAILED

Lint:        ❌ (exit 1)
Typecheck:   ✅ (exit 0)
Tests:       ❌ (exit 1)
Build:       ✅ (exit 0)

Failed checks:
- Lint: [first error]
- Tests: [first failure]

Fix before declaring done.
```

---

## 4. GATE RULES

1. **No "done" without gate pass.** If any check fails, the task is not done.
2. **Fresh evidence only.** Never reuse output from a previous run.
3. **Full output captured.** Not just exit codes — the actual output.
4. **Timestamped.** Evidence files include the run timestamp.
5. **No skipping.** Every check must run, even if "it should pass."

---

## 5. INTEGRATION WITH HOOKS

### PreToolUse Hook
When the agent tries to call a completion-related tool (e.g., `task_complete`, `claim_done`), check if verify-gate has passed for the current session.

### PostToolUse Hook
After running verification commands, capture output to evidence directory.

---

## 6. QUICK GATE (5-second check)

For fast iterations, run a quick gate:
```bash
# Quick lint + typecheck
npm run lint && npm run typecheck

# Quick test
npm test -- --passWithNoTests

# Quick build
npm run build
```

---

## 7. GATE BYPASS

The gate can only be bypassed when:
- The user explicitly says "skip verification"
- The task is read-only (no code changes)
- The task is documentation-only

Even then, note the bypass in the session log.

---

## 8. EVIDENCE RETENTION

- Keep evidence for 7 days
- Archive completed task evidence to `.dev-craft/evidence/archive/`
- Clean up evidence older than 30 days
