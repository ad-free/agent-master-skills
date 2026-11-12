# Example: api-design session

Goal: design an API for a notes service with versioning and pagination.

Steps:
1. Load `api-design` with brief: "Notes API with versioning and cursor pagination".
2. `api-design` outputs: API contract, example requests/responses, and versioning strategy.
3. `dev-craft` can then scaffold server and OpenAPI spec from the contract.

Expected artifacts:
- `API-CONTRACT.md` — endpoints, auth model, pagination schema
- `openapi.yaml` — machine-readable spec
- `CHANGELOG.md` — versioning policy notes

Tips:
- Keep examples minimal and avoid organization-specific URLs or absolute paths.
- Use `${PROJECT_ROOT}` placeholders in any file paths shown.
