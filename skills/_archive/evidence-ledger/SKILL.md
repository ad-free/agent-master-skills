---
name: evidence-ledger
description: |
  Tamper-evident verification evidence ledger. Records test runs, lint checks,
  type checks, and build results with working-tree fingerprints. Provides
  FRESH/STALE/MISSING grading for verification gates. Use to prove completion
  with fresh evidence instead of assuming from memory.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - "record evidence"
  - "check evidence"
  - "verify gate"
  - "fresh evidence"
  - "evidence ledger"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 1.0.0
  domain: verification
  integrates-with: [verification-before-completion, dev-craft, ui-craft, ship, continuous-learning-v2]
---
TOKEN CEILING: ~3K tokens. If skill exceeds, extract sections to references/.

# Evidence Ledger — Tamper-Evident Verification Records

The evidence ledger creates an immutable, hash-chained record of all verification
activities (tests, lint, typecheck, build). Each entry is bound to the exact
working-tree content at the time of execution, preventing stale or fabricated
evidence.

## Core Concepts

### Working-Tree Fingerprint
A content hash of what's actually on disk (not git commit SHA):
- Includes untracked source files
- Excludes gitignored scratch files
- Identical content = identical fingerprint across commits/rebases/squashes
- Computed via temp index seeded from stat cache (~40x cheaper than full re-hash)

### Evidence Entry
```json
{
  "id": "evt-a1b2c3d4",
  "label": "test-unit",
  "timestamp": "2026-08-27T14:30:00Z",
  "command": "pytest tests/unit -v",
  "exit_code": 0,
  "duration_ms": 12345,
  "fingerprint": "sha256:abc123...",
  "output_hash": "sha256:def456...",
  "passed": true,
  "summary": "42 passed, 0 failed"
}
```

### Hash Chain
Each entry includes `prev_hash` linking to previous entry.
Tampering (edit, reorder, delete mid-chain) detected by `verify` command.
Truncating/deleting the entire ledger is detectable but not preventable.

## Storage

```
.dev-craft/evidence/
├── ledger.jsonl          # Hash-chained evidence entries (append-only)
├── fingerprints/         # Working-tree fingerprints cache
│   └── <fingerprint>.json
├── runs/                 # Per-run detailed output (capped 2MB, 0600)
│   └── evt-<id>.log
└── index.json            # Label → latest entry mapping
```

## Commands

### evidence run --label <label> -- <command>
Wrap any verification command, record result with fingerprint.

```bash
evidence run --label test-unit -- pytest tests/unit
evidence run --label lint -- ruff check .
evidence run --label typecheck -- mypy --strict
evidence run --label build -- npm run build
```

### evidence check --label <label> [--expect-cmd <cmd>] [--max-age <duration>] [--allow-paths <globs>]
Grade evidence for a label:
- **FRESH**: Entry exists, matches expect-cmd, within max-age, fingerprint matches current tree
- **STALE**: Entry exists but too old or fingerprint differs (tree changed since run)
- **MISSING**: No entry for label

```bash
evidence check --label test-unit --expect-cmd "pytest tests/unit" --max-age 1h
evidence check --label lint --expect-cmd "ruff check ." --allow-paths "src/**"
```

### evidence verify
Recompute hash chain, exit 3 on tamper detected.

### evidence list [--label <label>] [--since <time>]
List evidence entries.

## Verification Gates Integration

In `verification-before-completion` and `dev-craft`/`ui-craft` SHIP phase:

```yaml
# Required evidence labels (configured per project)
required_evidence:
  - label: test-unit
    expect_cmd: "pytest tests/"
    max_age: "1h"
  - label: test-integration
    expect_cmd: "pytest tests/integration"
    max_age: "4h"
  - label: lint
    expect_cmd: "ruff check ."
    max_age: "30m"
  - label: typecheck
    expect_cmd: "mypy --strict"
    max_age: "30m"
  - label: build
    expect_cmd: "npm run build"
    max_age: "1h"
```

**Gate passes only if ALL required labels are FRESH.**

## Hooks Integration

Add to `.opencode-plugin/hooks.json`:

```json
{
  "PostToolUse": [
    "hooks/evidence-capture.js"
  ]
}
```

PostToolUse hook captures test/lint/typecheck commands automatically.

## Ship Integration

`/ship` and `/land-and-deploy` cite fresh evidence instead of re-running suites:
- Checks required evidence labels
- If all FRESH → proceeds with commit/PR
- If any STALE/MISSING → blocks with specific missing evidence

## Per-Run Logs

- Stored in `.dev-craft/evidence/runs/`
- Permissions: 0600 (readable only by owner)
- Capped at 2MB per run (truncated with notice)
- Pruned after 30 days
- Machine-local by design (not committed to git)

## Ledger Format (JSONL)

```jsonl
{"id":"evt-a1b2c3d4","label":"test-unit","timestamp":"2026-08-27T14:30:00Z","command":"pytest tests/unit","exit_code":0,"duration_ms":12345,"fingerprint":"sha256:abc123...","output_hash":"sha256:def456...","passed":true,"summary":"42 passed","prev_hash":"sha256:prev..."}
{"id":"evt-e5f6g7h8","label":"lint","timestamp":"2026-08-27T14:31:00Z","command":"ruff check .","exit_code":0,"duration_ms":2345,"fingerprint":"sha256:abc123...","output_hash":"sha256:ghi789...","passed":true,"summary":"0 errors","prev_hash":"sha256:evt-a1b2c3d4..."}
```

## Fingerprint Algorithm

```python
def compute_fingerprint(repo_path):
    # 1. Get git tracked files + untracked source files
    # 2. Exclude gitignored, binary, large files
    # 3. Create temp git index from stat cache
    # 4. Hash: SHA256(sorted(file_path + file_content_hash))
    # 5. Cache by (mtime, size) for speed
    pass
```

## Grading Rules

| Grade | Condition |
|-------|-----------|
| FRESH | Entry exists AND command matches expect_cmd AND within max_age AND fingerprint matches current tree |
| STALE | Entry exists BUT (fingerprint mismatch OR exceeds max_age) |
| MISSING | No entry for label |

## Security

- Ledger is append-only (JSONL)
- Hash chain prevents mid-chain tampering
- Per-run logs 0600 permissions
- No network transmission (machine-local)
- Truncating ledger detectable via missing chain start

## References

- `references/evidence-schema.json` — Evidence entry schema
- `references/fingerprint-algorithm.md` — Fingerprint computation
- `references/grading-rules.md` — FRESH/STALE/MISSING logic
- `references/integration.md` — dev-craft/ui-craft/ship integration

## Related

- `verification-before-completion` — Mandatory verification gates (consumes evidence)
- `dev-craft` / `ui-craft` — Pipeline phases (produce evidence)
- `ship` — Release workflow (requires fresh evidence)
- `continuous-learning-v2` — Patterns extracted from evidence trends