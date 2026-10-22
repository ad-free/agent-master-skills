# Architecture proposal (new service or large feature only)

Rule: **start simple, justify complexity.** Write a short `architecture.md` (or an ADR) covering only what
applies. Each topic gets 2 options with trade-offs, a default, and a request for the user's choice. Leave out
anything the repo already decided.

- Style: a modular monolith is the right default for most business apps; justify splitting into services.
- Auth and roles (SSO-ready, RBAC at API and UI), secrets management.
- Database, caching, background jobs and queues (idempotent for retries), file storage, search.
- Environments (dev / staging / prod), containers, CI/CD, migrations in the pipeline.
- Observability: structured logs, error tracking, health checks, metrics (`observability-engineering`).
- Backups and restore tests; security headers, rate limiting, input validation.
- Cost and operational burden of each option.

Example: "Jobs: (A) in-process worker table + cron, simplest, fine under ~100 jobs/min; (B) Redis queue, scales,
adds a service to run. Default A; revisit at 1k jobs/min."

## Pick a structure by the problem, not by fashion

Folded from the former `backend-patterns` skill. Keep the repo's existing layering unless one of these pains is
real and named.

| Pain you can point to | Pattern |
|---|---|
| Simple CRUD, clear boundaries | Layered (router → service → repository). The default |
| Business logic tangled with DB/HTTP/vendor code | Hexagonal / clean: domain has no infra imports, adapters implement ports |
| Reads and writes have very different shapes or load | CQRS (separate command and query models) |
| Long multi-step process that needs compensation on failure | Saga |
| Full audit trail or replay required by the business | Event sourcing (high cost; needs a stated reason) |

Dependencies point inward (toward the domain) or downward (toward data), never back up. Deeper detail on DDD,
event-driven and service decomposition: `architecture-patterns.md`.

## Weighing options (ADR)

Folded from the former `architecture-decision-records` skill. When a choice is hard to reverse:

1. Narrow to 2–4 viable options; drop any that break a stated constraint.
2. List criteria (e.g. operability, cost, team familiarity, performance, security), weight each 1–5.
3. Score each option 1–5 per criterion; show the matrix and say where each option wins and loses.
4. Record the decision with the ADR template in `phase-templates.md`, including what would make you revisit it.

The matrix supports the decision; it does not make it. If the top two are close, say so and ask.
