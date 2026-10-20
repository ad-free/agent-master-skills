# shadcn/ui

Load only if the repo uses it (`components.json`, `components/ui/`). Never mix with Material-UI.
- Components are copied into the repo: add with the CLI, then edit locally; extend the existing wrappers
  instead of forking a second copy.
- Theming via CSS variables / Tailwind tokens; change tokens, not individual components.
- Forms: the repo's form pattern, usually React Hook Form + Zod with the `Form` primitives; tables: TanStack
  Table with the data-table pattern.
- Primitives are Radix or Base UI (Base UI is the CLI default since July 2026; detect which from `components.json`
  and imports, do not mix). Keep their accessibility props; wire dialogs, menus and toasts through them.
- Traps: editing generated components inconsistently; one-off colors outside tokens; custom buttons beside `Button`.
