# Refactor and cleanup (Refactor mode detail)

Folded from the former `refactor-and-cleanup` skill. Read with `workflow.md` §Modes "Refactor (safe)".

## Find, then rank

Use lint and type-checker output first, then search. Rank what you find and fix in this order:

| Rank | What | Why first |
|---|---|---|
| P0 | Dead code that confuses readers or causes import cycles | Cheapest, removes noise for every later step |
| P1 | Duplicated logic in core or hot paths | Divergent copies are where bugs hide |
| P2 | Names that hide intent | Makes the remaining work reviewable |
| P3 | Cosmetic (import order, whitespace) | Only if the formatter does not already own it |

Complexity worth splitting: a function above ~10 branches, or one a reviewer cannot hold in their head.

## Execute

- One group (same file or module) at a time; run the covering tests after each group. A red test means revert
  that group, not patch forward.
- Before deleting "unused" code, search for dynamic use: string lookups, reflection, registries, templates,
  config files, public exports. If any doubt remains, flag it instead of deleting.
- Renames never change a public interface or external API without the user's approval.
- No behavior change. If you find a bug, record it as a finding; fixing it is a separate Bug-mode task.

## Proof

Same tests pass before and after, lint and types report nothing new, and the diff holds only the intended
groups. Report what was removed, extracted, renamed, and simplified.
