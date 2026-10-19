# FastAPI

Default backend framework, but detect: if the repo uses Django or Flask, follow that instead.
- Routers per module; thin handlers, logic in services, data access in repositories (match the repo's layers).
- Dependency injection (`Depends`) for DB session, current user, settings; override in tests.
- Pydantic request and response models on every endpoint (`response_model`); never return ORM objects raw.
- Errors: raise `HTTPException` or a project exception handler producing the repo's error format; correct
  status codes (409 duplicates, 422 validation, 401 vs 403).
- OpenAPI is the contract source of truth: keep schemas accurate, tags and operation ids stable (frontend
  types are generated from it).
- Authorization on every route; pagination, filtering and sorting params on list endpoints.
- Traps: sync DB calls in async routes without a threadpool; session leaks; changing response shape without
  searching consumers (`fullstack.md`).
