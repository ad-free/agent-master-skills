# Security checklist (per slice and review minimum)

Fallback for `bug-hunting`. `plugins/security-audit` stays the deep pass at HARDEN; run it for auth, payment
or personal-data work. Each item is checkable in a diff or by one request.

## Access
- Authentication and authorization on every new route.
- Object-level check: the user may access this record (try another user's id).
- Multi-tenant data: a test proves tenant A cannot read tenant B.
- UI hiding is not authorization; the server enforces it.

## Input and output
- Input validated at the boundary (Pydantic models, bounded lengths, enums).
- Parameterized queries only; no string-built SQL.
- Response models never return raw ORM objects or secret/internal fields (mass assignment, over-exposure).
- Errors do not leak stack traces or SQL; logs carry request ids but no personal data.

## Secrets and sessions
- Secrets only from environment or a secret store; none in code, logs, test fixtures or screenshots.
- JWT/session: expiry set, signature algorithm fixed, revocation plan, passwords hashed with a modern algorithm.

## Regex and outbound calls
- No nested or overlapping quantifiers on user input (ReDoS); anchors or `fullmatch` for validation; never build a
  pattern from raw input (`re.escape`).
- URLs from user input: validate scheme and host. Webhook payloads signature-verified.
- Critical actions (delete, role change, payment) are logged.

## Frontend
- No `dangerouslySetInnerHTML` or unsanitized HTML.
- Tokens not stored where scripts can read them, unless the repo's design says so.
- CSRF protection if cookie auth.

## Surface
- CORS restricted to known origins.
- Rate limiting on login and expensive endpoints.
- File upload: size and type limits, stored outside the web root, served via signed URLs.
- CSV/Excel export neutralizes formula injection (cells starting with `=`, `+`, `-`, `@`).

## Data and dependencies
- Sensitive data (PII, salary, personal documents): field-level permission, not logged, encrypted where the
  repo requires, audit-logged on access.
- When dependencies change, run the repo's audit command (`pip-audit`, `npm audit`) and report the result.
