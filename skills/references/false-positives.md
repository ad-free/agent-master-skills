# Common False Positives Reference

Patterns that LLM reviewers commonly mis-flag. Skip unless you have evidence specific to this codebase.

## Security Theater (ALWAYS SKIP)

- `Math.random()` in non-cryptographic context (animation, jitter, sampling)
- `eval`/`Function` in explicit plugin systems that are code-loading surfaces
- `innerHTML` with sanitized content (DOMPurify.sanitize())
- Self-signed certs in development-only configs

## Error Handling (SKIP if handled upstream)

- "Consider adding error handling" on calls whose error path is handled by caller/framework:
  - Express error middleware
  - React error boundaries
  - Top-level `try/catch`
  - Promise chains with `.catch` upstream
- "Missing input validation" when function is internal and callers already validate — trace at least one caller first

## Style/Naming (SKIP unless violates project convention)

- "Magic number" for well-known constants: `200`, `404`, `1000` ms, `60`, `24`, `1024`, array index `0`/`-1`, HTTP status codes, single-use local constants with obvious names
- "Function too long" for exhaustive `switch`, config objects, test tables, generated code — length ≠ complexity
- "Missing JSDoc" on single-purpose internal helpers whose name/signature are self-describing
- "Prefer `const` over `let`" when variable IS reassigned — read whole function first
- "Inconsistent formatting" — run formatter instead of flagging

## Type Safety (SKIP if type flow proves safe)

- "Possible null dereference" when preceding line narrows type or `if` guard in scope — trace type flow
- "Missing await" on fire-and-forget calls (logging, metrics, background queues) — check for `void` prefix or comment
- "Should use TypeScript" or "Should have types" in JavaScript-only file — match project language

## Performance (SKIP if not a real bottleneck)

- "N+1 query" on fixed-cardinality loops (enum iteration, 4-element array) or paths using `DataLoader`/batching
- "Large bundle" for importing entire lib when tree-shakeable alternative exists but adds complexity

## Testing (SKIP)

- "Hardcoded value" in test fixtures, example code, documentation snippets — tests NEED hardcoded expectations
- "Missing test" for trivial getters/setters, generated code, or framework boilerplate

## Architecture (SKIP unless causing real problems)

- "Should use pattern X" when current pattern works and team knows it
- "Extract to service" for 50-line module with single responsibility

## Decision Rule

> **When tempted to flag one of the above, ask: "Would a senior engineer on THIS team actually change this in review?" If no, skip.**

## Language-Specific False Positives

### Python

| Pattern | When to Skip | Real Example |
|---------|-------------|--------------|
| "Use `pathlib` instead of `os.path`" | In scripts/glue code where `os.path` is already imported and `pathlib` adds no readability | `os.path.join(dir, f"prefix_{x}.csv")` in a 50-line ETL script |
| "Consider type hints" | For throwaway scripts, legacy code with no type infrastructure, or when the function is 3 lines and called once | `def get_config(key): return os.environ.get(key, "default")` |
| "Use `f-string` instead of `.format()`" | When the string is a template loaded from a config file or i18n resource, not a literal | `msg = template.format(name=user.name)` where `template` is from `messages.json` |
| "Missing `__init__.py`" | In Python 3.3+ namespace packages or when the dir is not a package | `services/email/` used as a namespace package |
| "Use `@dataclass` instead of manual `__init__`" | When the class has custom validation in `__init__` or inherits complex mutable state that dataclass `__post_init__` doesn't cleanly model | `class User: def __init__(self, name, age): self._validate(name)` |
| "Consider `Enum` over string constants" | When constants are used in only one module or are input values from external systems | `STATUS_MAP = {"active": 1, "inactive": 0}` used only in one mapper |
| "Use `async/await` instead of synchronous" | When the function is CPU-bound, uses blocking libraries, or is called in a non-async context | `def compute_checksum(data): return hashlib.md5(data).hexdigest()` |
| "Missing `__all__`" | For internal modules where consumers import by explicit path | `from db import engine` — not `from db import *` |
| "Use `zoneinfo` instead of `pytz`" | When Python < 3.9 is required, or `pytz` is pinned in requirements and migration is out of scope | `import pytz; tz = pytz.timezone("UTC")` in a legacy app on Python 3.8 |
| "Consider `|` union syntax instead of `Union[]`" | When Python < 3.10 is required or the codebase uses `from __future__ import annotations` only partially | `def get(id: Union[int, str]) -> Optional[User]` in a Python 3.9 codebase |

### Go

| Pattern | When to Skip | Real Example |
|---------|-------------|--------------|
| "Error should be checked" | When the error is explicitly discarded with `_` and a comment explains why (metrics, logging, best-effort cleanup) | `_ = conn.Close() // closed elsewhere on error path` |
| "Use `errors.Is` instead of `==`" | When comparing a sentinel error that is defined as a `var ErrFoo = errors.New("foo")` and is never wrapped | `if err == io.EOF { break }` |
| "Missing context deadline/timeout" | For local, synchronous operations that complete in microseconds (map lookups, struct field access) | `val := m[key]` |
| "Use `context.Context` as first parameter" | For unexported helpers called only internally where the caller already has the context | `func parse(r io.Reader) (*Result, error)` called from `func Do(ctx, r)` |
| "Consider `sync.Map`" | For read-heavy maps with infrequent writes, where `sync.RWMutex` is simpler and `sync.Map` is optimized for different access patterns | `var mu sync.RWMutex; m := make(map[string]int)` |
| "Shadowed variable" | In short test functions or `if` blocks where the shadow is intentional and clear | `if err := json.Decode(r, &v); err != nil { return err }` |
| "Use table-driven test" | For a single test case or a test with complex setup that doesn't fit the table pattern | `func TestAdd(t *testing.T) { got := Add(1,2); want := 3; if got != want { t.Fatalf(...) } }` |
| "Missing `defer` for cleanup" | When the resource is closed at the natural end of the function and there is no panic/return-between risk | `f, _ := os.Create(path); f.Write(data); f.Close()` on last 3 lines of function |
| "Use `int64` explicit conversion" | When the constant fits in `int` on all target platforms and the code is not doing arithmetic that could overflow | `const maxRetries = 3; for i := 0; i < maxRetries; i++` |
| "Goroutine leak" | When the goroutine is part of a long-lived worker pool with proper shutdown via context/channel, and the reviewer missed the `<-ctx.Done()` branch | `go func() { for { select { case <-ctx.Done(): return; case job := <-ch: process(job) } } }()` |

### Rust

| Pattern | When to Skip | Real Example |
|---------|-------------|--------------|
| "Use `expect` instead of `unwrap`" | In test code, example code, or prototypes where panicking on error is the intended behavior | `let val = map.get(&key).unwrap(); // test: key guaranteed to exist` |
| "Consider `map_err` before `?`" | When the error type is the same or implements `From` for automatic conversion | `fn read() -> Result<String, io::Error> { Ok(fs::read_to_string(path)?) }` |
| "Missing `impl Display` for error type" | For internal error enums that are never surfaced to the user and only used with `?` in `Result<T, InternalError>` | `enum InternalError { NotFound, PermissionDenied }` used only inside the module |
| "Use `thiserror` / `anyhow`" | In library code where controlling dependencies matters, or when the error type is a simple unit enum | `#[derive(Debug)] enum AppError { Io(io::Error), Parse(String) }` |
| "Consider `Cow<str>` instead of `String`" | When the function is not performance-critical and `Cow` adds complexity without measurable gain | `fn greet(name: &str) -> String { format!("Hello, {name}!") }` |
| "Missing `#[must_use]`" | For functions with clear side effects (mutate, write, send) where ignoring the return value is intentional | `fn log_error(e: &Error) -> usize { eprintln!("{e}"); 0 }` |
| "Use `const` instead of `static`" | When the value is a `Mutex`, `Atomic`, or any type that `const` cannot represent in stable Rust | `static COUNTER: AtomicU64 = AtomicU64::new(0)` |
| "Consider `impl Trait` in argument position" | When the function signature is part of a trait definition or needs named types for documentation | `fn process(items: Vec<String>)` (not `fn process(items: impl IntoIterator<Item = String>)`) |
| "Use `as` instead of `From`/`TryFrom`" | When converting between numeric types where truncation is impossible or explicitly desired | `let idx = i as usize; // i is always non-negative u32` |
| "Missing `#[derive(Clone)]`" | When the type contains `Rc`, `Arc`, or other non-Clone fields by design | `struct Shared(T) where T: ?Sized` |

## Decision Rule

> **When tempted to flag one of the above, ask: "Would a senior engineer on THIS team actually change this in review?" If no, skip.**

## Output Format for Skipped Items

```markdown
## Skipped (False Positive Candidates)

- [SKIPPED] "Consider adding error handling" on `fetchUser()` — handled by React error boundary at `App.tsx:15`
- [SKIPPED] "Magic number 200" — HTTP OK status code, well-known constant
- [SKIPPED] "Function too long (85 lines)" — exhaustive switch on 20 enum values, generated
```