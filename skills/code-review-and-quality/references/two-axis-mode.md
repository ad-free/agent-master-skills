# Two-Axis Review Mode (folded from `two-axis-review`)

Lightweight alternative to the 8-axis pass. Run **Standards** and **Spec** as
two parallel, non-interfering reviews; report side by side, never merged or
reranked. A change can pass one axis and fail the other — reporting them
separately stops one from masking the other.

## 1. Pin the fixed point

Whatever the user named (SHA, branch, tag, `main`, `HEAD~5`). Capture once:

```bash
git diff <fixed-point>...HEAD
git log <fixed-point>..HEAD --oneline
```

Confirm the fixed point resolves and the diff is non-empty. If no fixed point
was given, ask for it.

## 2. Identify the spec source

In order: issue refs in commit messages (`#123`, `Closes #45`); a user-passed
path; a spec under `docs/`, `specs/`, `.scratch/` matching the branch name.
If nothing found, ask. With no spec, the Spec axis reports "no spec available."

## 3. Identify the standards sources

`CODING_STANDARDS.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `.cursorrules` —
plus this always-on smell baseline (repo docs override; each smell is a
judgement call, never a hard violation):

Mysterious Name · Duplicated Code · Feature Envy · Data Clumps · Primitive
Obsession · Repeated Switches · Shotgun Surgery · Divergent Change ·
Speculative Generality · Message Chains · Middle Man · Refused Bequest.

## 4. Run both reviews

**Standards:** per hunk — check documented standards (cite file + rule), then
smells (name + quote), separate hard violations from judgement calls, skip what
tooling enforces.

**Spec:** per requirement — implemented? matches? scope creep? Quote the spec
line per finding (missing requirement §, wrong implementation, unrequested
behaviour).

## 5. Aggregate

Present under `## Standards` and `## Spec` headings, then one line per axis:

```
Standards: 3 findings (worst: Shotgun Surgery in auth.ts)
Spec: 2 findings (worst: Missing requirement §2.3)
```

## 6. Quick review

Standards axis only: `git diff <fixed-point>...HEAD | head -200`, checking
smells, naming, missing error handling, hardcoded values, missing tests.
