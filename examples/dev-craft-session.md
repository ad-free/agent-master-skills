# Example: dev-craft session

Goal: scaffold a small task-tracker backend service and test harness.

Steps (agent-driven):

1. Load `product-thinking` with prompt: "Build a simple task-tracker API (CRUD tasks)" → outputs `PRODUCT.md`.
2. Run `planning-and-task-breakdown` on `PRODUCT.md` → outputs `PLAN.md` with vertical slice for an API server.
3. Run `dev-craft` with scope `backend`:
   - ARCH-SCAN: detect language (Python/FastAPI)
   - ALIGN: confirm database choice (SQLite for demo)
   - DESIGN: create API spec (OpenAPI) and minimal data model
   - BUILD: generate skeleton code, tests, and Dockerfile
   - TEST: run unit tests
   - REVIEW: run linters and quality checks

Example expected outputs:
- `PRODUCT.md` — short spec of endpoints: `GET /tasks`, `POST /tasks`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`
- `PLAN.md` — ordered tasks: API spec, DB model, tests, CI
- `openapi.yaml` — generated API spec
- `app/` — minimal FastAPI app and tests

Notes:
- Replace absolute paths in examples with `${PROJECT_ROOT}`.
- Keep examples runnable but small; use SQLite and in-memory fixtures for tests.
