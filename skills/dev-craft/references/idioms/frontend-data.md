# Frontend data: server state, forms, routing

Use what the repo has; this is the default shape.
- **Server state:** TanStack Query. Query keys are structured and stable; handle loading, error and empty;
  invalidate precisely after mutations; optimistic updates only with rollback.
- **API types:** generate from the OpenAPI source (`openapi-typescript`, Orval, or the repo's tool); regenerate
  in the same change as the backend; never hand-duplicate response types.
- **Forms:** React Hook Form + Zod via `zodResolver` from `@hookform/resolvers/zod`; schema is the single
  validation source (when it transforms values, pass `useForm<z.input<typeof schema>, unknown, z.output<typeof schema>>`); show field errors from the server
  error format too; disable submit while pending.
- **Tables:** TanStack Table (detect v8 vs the v9 alpha, whose API differs); server-side pagination and sorting
  need `manualPagination`/`manualSorting` plus `rowCount`, and those flags only skip client work: you must fetch
  the sorted page yourself; use server-side for large data; state in the URL
  so views are shareable.
- **Routing:** React Router or TanStack Router as detected; route-level code splitting and error elements.
- Traps: copying server data into local state, query keys missing parameters, ignoring 401/403 globally.
