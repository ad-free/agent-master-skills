# Multi-Repo Variant (folded from `agent-orchestration`)

## Topology

| Layout | Shape | Isolation |
|--------|-------|-----------|
| `mono` | One repo with BE + FE (`backend/` + `frontend/`) | `git worktree` per slice (this skill's default) |
| `multi` | Separate BE / FE repos (two checkouts) | Separate clones + paired branches — worktrees can't span repos |

## SCOPE alignment

Read from the active dev-craft SCOPE record so agents branch and read the
contract consistently: `topology`, `scope`, `mode`, `repos`, `contractRepo`,
`linkedBranches`. Do NOT maintain a separate long-lived `contract` branch; the
contract travels on the feature branch(es).

## Multi-repo rules

- **Contract:** `api-contract.md` lives in `contractRepo` (BE repo); FE reads
  from there (or a synced mirror). Never two drifting copies.
- **State:** each repo keeps its own `.dev-craft/` / `.ui-craft/`;
  `linkedBranches` in SCOPE ties them together.
- **Integration:** per-repo suites first, then contract conformance. Merge/PR
  each repo's branch; ship together.
- Master agent still owns the contract and the integration merge.

## Branch strategy (mono)

```
main ──────┬────────────── api-slice ──────────┐
           ├────────────── web-slice ─────────────┤───► integration
           ├────────────── mobile-slice ──────────┘
           └─ contract (master-owned, on feature branch)
```
