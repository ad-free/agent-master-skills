# Full-stack and scope

Read when two or more sides (backend, frontend, database, infra) are touched, or when a single-side task depends
on another side. Replaces the old cross-skill hand-off notes.

## Single-side tasks (write scope vs read scope)

1. Scope line in Frame: `Scope: frontend; write: frontend; read-only: backend, database`. "FE only, don't touch
   the backend" is a hard boundary.
2. **Read the other side, don't guess.** Before building screens, find the real endpoints, response shapes,
   error codes, auth behavior in the repo or schema file. No API yet? Say so.
3. **Boundary problems are findings, not edits.** The UI needs a field, filter, or endpoint the backend lacks:
   list options: (a) ask for a backend change, (b) work around in the UI with the cost, (c) build against a
   mock from a proposed contract, labeled unverified. If the real API differs from the description, report the
   difference with `file:line`.
4. Out-of-scope edits need approval. If approved the task becomes full-stack: use the rest of this file.
5. Out-of-scope problems (a backend bug, a bad schema) are reported, not fixed quietly.
6. **Backend-only** is the same in reverse: search for consumers of the endpoint/type (frontend, jobs, other
   services), flag the ones a change would break, and do not edit them without approval.

## Full-stack tasks

- **Spec by user flow**, not by layer: acceptance criteria describe end-to-end behavior including error, empty,
  loading, and permission states. List "surfaces touched".
- **Contract step.** The repo's OpenAPI/GraphQL/shared types/protobuf is the source of truth; generate types
  from it, do not hand-write duplicates. With none, write `api-contract.md` (repo root or `docs/`; in
  `contractRepo` for multi-repo; path in state as `apiContract`). Cover: method + path, request and response
  shapes, status codes, each error and what the UI shows, auth (401/403), pagination/order/nullability,
  date/number/money formats. Tag new endpoints `[NEW]`. Extract existing endpoints from source; do not guess.
- **Vertical slices:** database -> API -> UI per slice, not "all backend then all frontend". Within a slice:
  contract, backend with tests, frontend against the real contract, cross-boundary check. Frontend first? Use a
  mock generated from the contract and replace it before the slice is done.
- **Changing a contract is the riskiest edit:** search for the endpoint and type, list every consumer, update
  all in the same change, prefer additive changes if other clients exist, note deploy order or flags.
- **Validation:** frontend validates for UX; backend validates for correctness and security; authorization is
  server-side.
- **One source** for enums and constants (statuses, roles, limits); agree on naming and formats once.
- **Errors end to end:** every error the contract lists has a defined UI behavior.
- Load only the `idioms/` files for each side; run commands from the right directory in monorepos.

## Handing off to other skills

`ui-craft` consumes `api-contract.md` and may not invent endpoints. If `ui-craft` has UI data needs and no
contract exists, generate it and implement only what it declares. Mobile via `conductor` gets the same contract.
Before switching skills, confirm the contract exists at its recorded path and is readable from the consuming
repo. Never switch with an implied contract. Worktree isolation for parallel sides: `build-extras.md`.

## Boundary checks (REVIEW and TEST)

Frontend uses only fields the backend returns and handles nullable ones; every backend error has a UI path; no
`any` or casts hiding a mismatch; loading/empty/error handled; server-side authorization; every consumer of a
changed contract updated; types in sync (`gen:types` then `git diff --exit-code`); the running app matches the
contract.
