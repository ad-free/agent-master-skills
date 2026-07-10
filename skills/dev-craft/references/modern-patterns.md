# Modern Patterns Reference

This file tells dev-craft how to detect and enforce modern coding patterns for any detected stack. Consumed during Phase 4 (SOURCE) and Phase 7 (REVIEW).

## Detection Strategy

The agent must determine what is "modern" for the detected stack by:

1. **Reading the dependency file** to get exact versions
2. **Fetching official docs** for that version — not for the version in training data
3. **Checking migration guides** for deprecation warnings
4. **Checking CHANGELOGs** for breaking changes and new patterns

## Common Detection Targets

### Python Ecosystem

| File | Tool | How to Verify |
|---|---|---|
| `pyproject.toml` | Python version | Check `requires-python` field |
| `pyproject.toml` | ruff version | Check `ruff` in `[project.optional-dependencies]` or lockfile |
| `pyproject.toml` | mypy version | Check lockfile |
| `Pipfile` / `poetry.lock` / `uv.lock` | All deps | Read exact versions |

**Modern Python checklist (apply after fetching current-version docs):**
- Uses `from __future__ import annotations` everywhere
- Uses `|` syntax for unions (`str | None`, not `Optional[str]`)
- Uses builtin generics (`list[str]`, not `List[str]`)
- Uses `from collections.abc import Sequence, Callable, Iterator` instead of typing aliases
- Uses `zoneinfo` instead of `pytz`
- Uses `pathlib.Path` instead of `os.path`
- Uses f-strings, not `.format()` or `%`
- Uses `Self` return type for classmethods
- Uses `match`/`case` instead of `if/elif` chains on tagged types
- Uses Pydantic v2 model syntax (not v1 `BaseSettings`)
- Uses SQLAlchemy 2.0 `select()` style (not `.query()`)
- Google-style or PEP 257 docstrings, not Sphinx `:param:`

### JavaScript/TypeScript Ecosystem

| File | Tool | How to Verify |
|---|---|---|
| `package.json` | Package versions | Read `dependencies` + `devDependencies` |
| `package.json` | TypeScript version | Read `devDependencies.typescript` |
| `.eslintrc*` | ESLint config | Read config |
| `.prettierrc*` | Prettier config | Read config |
| `tsconfig.json` | TS strict mode | Check `strict: true` |

**Modern TypeScript checklist:**
- Uses `strict: true` in tsconfig
- Uses `import type` for type-only imports
- Prefers `interface` over `type` for object shapes
- Uses `const`, not `let` where possible; never uses `var`
- Uses `async/await`, not `.then()` chains
- Uses `unknown` instead of `any` for uncertain types
- Named exports over default exports
- React 19: `useActionState` over manual `useState` for form state
- React 19: `use()` hook over useContext in render

### Rust Ecosystem

| File | Tool | How to Verify |
|---|---|---|
| `Cargo.toml` | Edition | Check `edition = "2024"` |
| `Cargo.toml` | Dependencies | Read `[dependencies]` |
| `rustfmt.toml` | Formatter | Read config |

### Go Ecosystem

| File | Tool | How to Verify |
|---|---|---|
| `go.mod` | Go version | Read `go 1.NN` directive |
| `go.mod` | Dependencies | Read `require` blocks |

### Ruby Ecosystem

| File | Tool | How to Verify |
|---|---|---|
| `Gemfile` | Rails version | Read gem spec |
| `.rubocop.yml` | RuboCop | Read config |

### PHP Ecosystem

| File | Tool | How to Verify |
|---|---|---|
| `composer.json` | PHP version | Read `require.php` |
| `composer.json` | Symfony/Laravel | Read `require` |

## Pattern Migration Heuristic

When reviewing code in Phase 7 (REVIEW), apply this heuristic to every hunk:

```
Given dependency X at version Y:
1. Check if the pattern used is shown in the CURRENT docs for X at Y
2. If the pattern is absent from current docs:
   a. Search migration guide X/Y for the pattern name
   b. If found as deprecated → flag as "use modern replacement"
   c. If not found → check training data confidence:
      - High confidence (used in 10+ places in codebase) → flag as "verify against docs"
      - Low confidence → flag as "UNVERIFIED — check docs"
```

## General Modern Patterns (Applies to Every Language)

| Old / Avoid | Modern / Prefer |
|---|---|
| Synchronous file I/O (blocking) | Async I/O where ecosystem supports it |
| Exception swallowing (`except: pass`) | Specific exception handling |
| Global mutable state | Dependency injection |
| Stringly-typed interfaces | Well-typed interfaces (generics, discriminated unions) |
| Manual serialization | Schema-driven serialization (Pydantic, Zod, Serde) |
| Long functions (>50 lines) | Small, focused functions |
| Deep nesting (>3 levels) | Early returns, guard clauses |
| Magic strings/numbers | Named constants, enums |
| Comments restating code | Comments explaining WHY, not WHAT |
| Silent fallbacks that hide errors | Explicit error handling |
