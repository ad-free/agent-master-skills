# Codebase Map Template

## Project Structure

```
<project-root>/
├── frontend/
│   ├── src/
│   │   ├── App.tsx              — Root component, providers, routing
│   │   ├── features/            — Feature modules
│   │   ├── components/ui/       — Shared UI components
│   │   ├── i18n/                — Internationalization files
│   │   └── lib/                 — Utilities, API client, hooks
│   ├── public/                  — Static assets
│   └── tailwind.config.ts       — Tailwind configuration
├── backend/
│   ├── app/
│   │   ├── main.py              — Application entry point, middleware, routers
│   │   ├── core/                — Config, security, permissions, bootstrap
│   │   ├── modules/             — Feature modules (each with models, routers, schemas, services)
│   │   └── seed.py              — Database seeding
│   ├── tests/
│   └── requirements.txt         — Python dependencies
└── docs/
    └── <spec-files>
```

## API Contracts

```markdown
## METHOD /path
Auth: public|authenticated|admin
Request:  { field: type, ... }
Response: { field: type, ... }
Errors:   { status: code, message: string }
```

## Database Models

```markdown
ModelName: field1(type, constraints), field2(type, constraints), ...
```

## Component Tree

```markdown
App → Provider1 → Provider2 → Router → Layout → Routes
  ├── Route1 → Page1 → ComponentTree
  └── Route2 → Page2 → ComponentTree
```

## Conventions

```markdown
├── File organization: [features/ modules/ pages/]
├── Naming: files=[kebab/snake] functions=[camel/snake] types=[Pascal/I]
├── Imports: [absolute/relative] exports=[named/default]
├── Styling: [Tailwind/CSS Modules/styled-components] + [cn()/clsx]
├── API: [custom hook / fetch / axios]
├── State: [React Query / Redux / Zustand / Context]
├── Error handling: [try-catch / Result types / error boundaries]
├── Testing: [framework] + [library] (colocated / __tests__/)
└── Type checking: [strict / partial / none]
```