# BUILD: per-slice loop

Per slice, in order: failing test, minimal code, SECURE, MATCH, lint (read-only check), type check, tests.
Red-green rules: `plugins/tdd-enforcer`. Idioms: `idioms/README.md`. Worktrees and the multi-repo branch script:
`build-extras.md` (only when parallel agents or multiple repos).

## SECURE (this slice only)

Read the slice's files, note which of these they touch, and run the matching items in `checklists/security.md`:
auth/sessions, data access, user input/uploads, regex, business-logic permissions, outbound calls/webhooks.
`harden-checks.md` is the cross-slice pass at HARDEN; do not repeat it here.
Output one line per touched area: `SECURE <slice>: auth PASS | data FLAG <issue> | ...`. Fix every FLAG before MATCH.

## MATCH (follow the repo, not your habits)

Read 3-5 existing files in the same area and note: file layout and test location, naming (files, functions,
types), import style, error handling and response format, code structure, test style and mocking approach. Then
read your slice and list each violation as `file:line: convention -> fix`. Fix them before lint; a convention
violation is a required fix, not a suggestion.

## Rules

- Edit only inside the scope line; report anything outside it (`fullstack.md`).
- Three similar lines beat a premature abstraction. One slice at a time. Do not touch code outside the slice.
- Test at public seams. Mock only at boundaries (real, then fakes, then stubs, then mocks).
- Feature flag risky production changes. Use design tokens, no ad-hoc values. React forms: React Hook Form + Zod.
- Order: SECURE, then MATCH, then lint.
