---
name: language-rules
description: Use when you need language-specific coding conventions and style enforcement for TypeScript or Python during the BUILD or REVIEW phase.
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

Writing/reviewing code in TypeScript or Python. Version-specific idioms for the rest of the stack live in `references/idioms/`.

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

Load via `skill("language-rules")` during BUILD or REVIEW. If `state.json` has `primaryLanguage`, only that language's rules load.
