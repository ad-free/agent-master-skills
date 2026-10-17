# Clean code defaults

**Precedence:** project conventions always win. Use these defaults only where the project has no convention,
for example in a new module or a greenfield project. Match the nearest existing code first. Do not rewrite
existing code to match these defaults.

## Naming
- Descriptive names. No abbreviations unless universal (`id`, `url`, `err`).
- Functions: verb-noun (`getUserById`, `validate_email`). Avoid vague names (`process`, `handle`, `doStuff`).
- Types and classes: PascalCase nouns (`User`, `CreateUserRequest`, `UserService`).
- Constants: SCREAMING_SNAKE_CASE for true constants.
- Files and casing: follow the project's convention (language and framework norms apply).

## Structure
- One responsibility per function. Prefer small functions; split when a function mixes responsibilities or
  needs a comment to explain its sections. Treat ~20 lines for functions and ~200 for files as a smell
  threshold to look at, not a hard limit.
- Imports grouped: stdlib, third-party, internal, with blank lines between groups. No unused or wildcard imports.

## Error handling (follow the language's idiom)
- Never signal failure with `null`/`undefined`/`None` where a value is expected.
- Python: typed exceptions per domain, raised early. TypeScript: typed errors or a `Result` type, whichever
  the project already uses. Do not introduce a second pattern.
- Errors are typed, not strings. Messages say what failed, why, and what to do.
- Never swallow errors. Log, re-raise, or handle explicitly.
- Validate external input at boundaries: API handlers, DB queries, file I/O.

## Defensive programming
- Guard clauses over nested conditionals. Assert invariants at the start of critical functions.
- Handle every branch. Use exhaustive checks for enums and unions (`never` in TypeScript, `assert_never` in
  Python).
- Fail fast and loudly; recover gracefully at the boundary.
- Use `X | None` / `Option`-style types for absent values and check them.

## Type safety
- New code is fully typed with explicit return types on public functions and APIs.
- No `any`; use `unknown` and narrow. No `@ts-ignore` or `# type: ignore` without a one-line reason.
- Strictness: new modules follow the strictest setting the project already enables. On an existing codebase do
  not flip `strict` or `mypy --strict` globally. Ratchet it up per module in a separate, approved change.
