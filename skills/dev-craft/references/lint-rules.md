# Lint Rules — Universal Readability & Modern-Code Gate

This is the **deterministic enforcement** companion to `modern-patterns.md`.
That file explains *what* modern code looks like per language. This file makes
violations **fail a gate** so the agent cannot quietly emit single-char names,
cryptic abbreviations, or legacy/deprecated syntax. Run these before claiming
REVIEW is done — for **backend and frontend, every supported language**.

The two universal rules this file exists to enforce (agents keep violating them):

1. **No single-character / cryptic identifiers.** `x`, `d`, `tmp`, `res`, `val`,
   `cfg` are banned outside a tight loop scope. Names must be self-documenting.
2. **No legacy / deprecated idioms.** Each ecosystem has a "modern" baseline
   (e.g. Python `X | None` over `Optional[X]`, TS `unknown` over `any`). Using
   the legacy form is an automatic fail.

These rules are **language-agnostic in principle** but **language-specific in
enforcement** — you cannot lint what you have not configured. Below is a
copy-paste gate for every ecosystem the skills support. Use the one that matches
the detected stack; if a stack is missing, add it here rather than improvising.

---

## Universal Forbidden Patterns (automatic fail)

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

## Rust

```toml
# rustfmt.toml + clippy in CI
# clippy lints catch most legacy/deprecated idioms
[tool.clippy]  # via cargo clippy -- -D warnings
```

Naming is already enforced by `rustc` (snake_case vars, CamelCase types). Add:

```bash
cargo clippy --all-targets -- -D warnings
```

## Go

```bash
# go vet + golangci-lint; gofmt enforces naming (camelCase, no underscores)
gofmt -l .          # fails if any file is unformatted
go vet ./...
golangci-lint run   # enable: revive (var-naming), gocyclo, errcheck
```

Go convention bans single-char names except `i`, `j`, `k`, `err`, `ok`, `v`.

## Ruby

```yaml
# .rubocop.yml
Style/VariableName:
  Enabled: true      # snake_case, no single-char except i/j/k
Lint/UnusedVariable:
  Enabled: true
Style/IdenticalConditionalBranches: Enabled
```

## PHP

```jsonc
// .php-cs-fixer.php or phpstan.neon
// phpstan level 8 + eslint-equivalent: squizlabs/php_codesniffer PSR-12
```
PSR-12 naming: camelCase methods, no single-char variables outside loops.

---

## Enforcement Protocol (every language)

1. Detect the stack (dev-craft ALIGN / ui-craft detect phase).
2. Apply the matching config above to the project's lint config.
3. During REVIEW, **run the linter and read the output** — do not infer pass/fail.
4. Any cryptic-name hit or legacy-idiom violation = automatic fail; rename /
   modernize before proceeding. Do not "fix the message."
5. For stacks without a semantic lint rule for cryptic names, add the grep gate.

## Why

Code is written for the next human reader, not the compiler. A teammate reading
this in 6 months must understand intent without guessing. Single-char names and
legacy idioms are fully machine-detectable, so they must be blocked
**deterministically** — in both backend and frontend — not by hope.
