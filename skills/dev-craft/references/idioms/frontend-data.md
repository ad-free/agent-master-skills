# Frontend data: server state, forms, routing

Use what the repo has; this is the default shape.
- **Server state:** TanStack Query. Query keys are structured and stable; handle loading, error and empty;
  invalidate precisely after mutations; optimistic updates only with rollback.
- **API types:** generate from the OpenAPI source (`openapi-typescript`, Orval, or the repo's tool); regenerate
  in the same change as the backend; never hand-duplicate response types.
- **Forms:** React Hook Form + Zod; schema is the single validation source; show field errors from the server
  error format too; disable submit while pending.
- **Tables:** TanStack Table; server-side pagination, sorting and filtering for large data; state in the URL
  so views are shareable.
- **Routing:** React Router or TanStack Router as detected; route-level code splitting and error elements.
- Traps: copying server data into local state, query keys missing parameters, ignoring 401/403 globally.
