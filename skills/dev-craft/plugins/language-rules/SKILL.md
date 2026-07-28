---
name: language-rules
description: Use when you need language-specific coding conventions and style enforcement for TypeScript, Python, Go, or Rust during the BUILD or REVIEW phase.
model: big-pickle
version: 1.0.0
preamble-tier: 1
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "language conventions"
  - "code style"
  - "linting rules"
  - "language best practices"
  - "coding standards"
metadata:
  origin: agent-master-skills
  plugin-for: dev-craft
  phase: BUILD | REVIEW
  preferred-model: big-pickle
---

<!-- TOKEN CEILING: ~2K -->

# Language Rules Plugin

## When to Use

Writing/reviewing code in TypeScript, Python, Go, or Rust.

## Language Rules

### TypeScript / JavaScript

```
- Use `const` over `let`; never use `var`
- Prefer `unknown` over `any` — `any` banned unless unavoidable
- Use `PascalCase` for types/interfaces/enums, `camelCase` for variables/functions
- Use `type` for simple unions/primitives, `interface` for object shapes with extends
- Nullish coalescing (`??`) over `||` for default values
- Optional chaining (`?.`) over long `&&` chains
- Async/await over raw `.then()` — no callback pyramids
- Explicit return types on public API functions
- Use `as const` for literal types; `satisfies` for type narrowing
- No utility types in function signatures where plain types work
- Prefer `Map`/`Set` over `{}` for dynamic key collections
- Enums: prefer `const enum` or union types; avoid runtime enums
- Tests: Vitest or Jest; describe/it pattern, no test frameworks mixing
- Import ordering: external → internal, absolute → relative
```

### Python

```
- Use `uv run python` — never bare `python`/`python3`
- Type hints: modern syntax (PEP 604/585) — `int | None`, `list[str]`, not `Optional[int]`, `List[str]`
- Use `pathlib.Path` over `os.path` in new code
- f-strings over `.format()` or `%`-formatting
- Imports at top of file — never inline (except circular import or optional heavy dep)
- Single-letter variable names banned except `i`/`j`/`k` in tight loops, `x`/`y` in math code
- Use `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants
- Type annotate all public API functions; type annotate internals where non-obvious
- Use `ruff` for linting (not flake8/pylint); `mypy` or `pyright` for type checking
- Prefer `@dataclass` over manual `__init__` for data containers
- Use `enum.StrEnum` / `enum.IntEnum` over plain class constants
- Context managers (`with`) for resource acquisition/release
- Prefer `|` for unions in isinstance checks: `isinstance(x, int | str)`
- Exception types: be specific; no bare `except:` without re-raise
- Tests: pytest with plain `assert` — no unittest.TestCase
```

### Go

```
- `gofmt` standard — no tabs vs spaces debate (tabs, 1 tab = 1 indent)
- Error handling: always check errors; `if err != nil { return ... }` is idiomatic, not repetitive
- Use `errors.Is` / `errors.As` for error comparison; never `==` on errors
- Receiver naming: 1-2 letter abbreviation of type (`u User` → `u`)
- Exported = `PascalCase`, unexported = `camelCase`
- No getter/setter boilerplate — use direct field access
- Use `context.Context` as first param in public functions that do I/O
- Prefer `make()` for maps/slices with known size
- Nil slices are valid — don't initialize to empty slice unless needed
- Use `defer` for cleanup (close, unlock, etc.) immediately after acquisition
- Interface types should describe behavior (small, 1-3 methods), not data
- Avoid `init()` — explicit initialization preferred
- Tests: `_test.go` files, `go test`; use `t` parameter for Fatal/Error
- Use `golangci-lint` for linting with default config + errcheck
```

### Rust

```
- `cargo fmt` and `cargo clippy` must pass before commit
- Use `Result<T, E>` for fallible functions; `Option<T>` for optional values
- Prefer `match` over `if let` when exhaustiveness matters
- Use `impl Trait` in argument position, generics with `where` for complex bounds
- Use `thiserror` for library error types; `anyhow` for application/binary code
- Prefer `?` operator over manual `match` on Result/Option
- Use `&str` over `&String`; `&[T]` over `&Vec<T>` for function parameters
- Derive common traits: `Debug, Clone, Copy, PartialEq, Eq, Hash, Default`
- Use `struct` with named fields over tuple structs unless single-field newtype
- Field naming: `snake_case` for functions/variables, `PascalCase` for types/traits/enums
- Module hierarchy: one concern per module; `mod.rs` deprecated — use `module_name.rs` + `module_name/`
- Avoid `unsafe` unless FFI or performance-critical hot path with proof of safety
- Tests: `#[test]` in same file or `tests/` integration; `#[cfg(test)] mod tests` for unit
- Use `clippy` pedantic mode for new projects; `allow` specific rules with justification
```

Load via `skill("language-rules")` during BUILD or REVIEW. If `state.json` has `primaryLanguage`, only that language's rules load.
