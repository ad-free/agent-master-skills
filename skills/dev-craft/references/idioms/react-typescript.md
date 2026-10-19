# React and TypeScript

Detect React and TypeScript versions and the `tsconfig` strictness; do not flip `strict` globally.
- Function components and hooks; small components; state as close to use as possible; derived state computed,
  not stored; effects only for synchronizing with outside systems.
- Types: no `any` (use `unknown` and narrow), no unexplained `@ts-ignore`; type props and API data from
  generated types; handle `null`/`undefined` from the API.
- Lists need stable keys; avoid index keys on mutable lists. Memoize only after measuring.
- Accessibility: semantic elements, labels on every input and icon button, visible focus, keyboard operable,
  focus management in dialogs.
- Errors and loading handled at the boundary (error boundaries, suspense or explicit states).
- Traps: stale closures, missing effect cleanup, unhandled promise rejections, deriving state in effects.
