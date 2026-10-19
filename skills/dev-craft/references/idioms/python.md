# Python

Detect the version first; use what it supports.
- Typing: `X | None`, builtin generics (`list[str]`), `collections.abc`; annotate public functions. No `Optional`/`List`.
- Prefer `pathlib`, f-strings, `dataclass`/Pydantic for data, `enum.StrEnum`, context managers for resources.
- Tooling: `uv` (or the repo's manager) with a lockfile; `ruff` for lint+format; `mypy` or `pyright` as the repo
  does; `pytest`. Run via the project runner (`uv run ...`), not bare `python`.
- Errors: specific exceptions, never bare `except:` or `except: pass`; raise early, validate at the boundary.
- Traps: mutable default arguments; naive datetimes (use time zones); blocking calls inside `async def`;
  catching `Exception` to hide failures; relying on dict/set ordering for logic.
