# Lint Rules — Universal Readability & Modern-Code Gate

This is the **deterministic enforcement** companion to `idioms/` (which says *what* modern code looks like
for the detected version). This file makes violations **fail a gate** so the agent cannot quietly emit
single-char names, cryptic abbreviations, or legacy/deprecated syntax. Run it before claiming REVIEW is done,
for backend (Python) and frontend (TypeScript/JavaScript). Other languages: use the repo's own lint config.

The two universal rules this file exists to enforce (agents keep violating them):

1. **No single-character / cryptic identifiers.** `x`, `d`, `tmp`, `res`, `val`,
   `cfg` are banned outside a tight loop scope. Names must be self-documenting.
2. **No legacy / deprecated idioms.** Each ecosystem has a "modern" baseline
   (e.g. Python `X | None` over `Optional[X]`, TS `unknown` over `any`). Using
   the legacy form fails the gate, because these are machine-detectable and not worth a reviewer's time.

Enforcement is language-specific: you cannot lint what you have not configured. Use the gate for the detected
stack. Where the repo already has a lint config, extend it; do not replace it.

---

## Universal forbidden patterns (fail the gate)

| Category | Forbidden | Required |
|---|---|---|
| Single-char name | `x =`, `d =`, `i =` (outside for-loop) | descriptive name |
| Cryptic abbrev | `tmp`, `res`, `val`, `cfg`, `ctx` as dumped values | `temp`, `result`, `value`, `config`, `context` |
| Magic values | `if status == 3:` | named enum / constant |
| Comment restating code | `# increment i` | comment explaining *why* |

---

## Python (backend / scripts)

```toml
# pyproject.toml
[tool.ruff]
target-version = "py311"
lint.select = ["E", "F", "UP", "RUF", "B"]   # UP = pyupgrade (legacy typing)

[tool.ruff.lint.pyupgrade]
keep-runtime-typing = false   # UP007 Optional→|, UP035 List→list, UP045 Union→|

[tool.ruff.lint.mccabe]
max-complexity = 10
```

Cryptic-name guard (ruff cannot judge semantics, so add a grep gate in CI):

```bash
grep -rnE '^\s*[a-z]{1,3} = ' src/ && { echo "FAIL: cryptic identifiers"; exit 1; }
```

## TypeScript / JavaScript (frontend & Node backend)

```jsonc
// .eslintrc / eslint.config.js — use @typescript-eslint
{
  "rules": {
    "id-length": ["error", { "min": 3, "exceptions": ["i", "j", "k", "e", "_", "id", "ok"] }],
    "no-explicit-any": "error",                 // ban `any` → use `unknown`
    "prefer-const": "error",
    "no-var": "error",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

Legacy→modern map: `any`→`unknown`, `var`→`const/let`, `.then()`→`async/await`,
default export→named export, `interface` over `type` for object shapes.

## Enforcement Protocol (every language)

1. Detect the stack (Frame / SCAN; `idioms/README.md`).
2. Apply the matching config above to the project's lint config.
3. During REVIEW, **run the linter and read the output** — do not infer pass/fail.
4. Any cryptic-name hit or legacy-idiom violation fails the gate; rename or modernize before proceeding.
   Fix the code, not the message (suppressing the rule hides the problem).
5. For stacks without a semantic lint rule for cryptic names, add the grep gate.

## Why

Code is written for the next human reader, not the compiler. A teammate reading
this in 6 months must understand intent without guessing. Single-char names and
legacy idioms are fully machine-detectable, so they must be blocked
**deterministically** — in both backend and frontend — not by hope.
