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
