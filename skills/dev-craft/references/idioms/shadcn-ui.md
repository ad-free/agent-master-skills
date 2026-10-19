# shadcn/ui

Load only if the repo uses it (`components.json`, `components/ui/`). Never mix with Material-UI.
- Components are copied into the repo: add with the CLI, then edit locally; extend the existing wrappers
  instead of forking a second copy.
- Theming via CSS variables / Tailwind tokens; change tokens, not individual components.
- Forms: the repo's form pattern, usually React Hook Form + Zod with the `Form` primitives; tables: TanStack
  Table with the data-table pattern.
- Built on Radix primitives: keep their accessibility props; wire dialogs, menus and toasts through them.
- Traps: editing generated components inconsistently; one-off colors outside tokens; custom buttons beside `Button`.
