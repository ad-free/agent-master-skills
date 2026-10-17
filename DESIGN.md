# DESIGN.md — Global UI Defaults

Fallback baseline for admin and data-heavy web apps. A project's own `DESIGN.md`, theme, or tokens
override anything here. This file holds principles and defaults, not brand values.

## 1. Default stack (use only what the project does not already define)

- React + TypeScript + Vite. Tailwind CSS v4: tokens live in CSS (`@theme` / CSS variables), not in
  scattered utility values.
- **shadcn/ui** is the component layer (Radix primitives + class-variance-authority + tailwind-merge + clsx).
  Add components with the shadcn CLI (`npx shadcn@latest add <name>`, needs `components.json`). Never
  hand-roll a control that shadcn provides.
- Icons: lucide-react. Toasts: sonner. Command palette: cmdk. Enter/exit animation: `tw-animate-css`.
  framer-motion only for meaningful transitions, not decoration.
- Tables: TanStack Table (shadcn data-table pattern). Forms: react-hook-form + zod + shadcn Form.
  Dates: date-fns + react-day-picker. Charts: Recharts via shadcn chart.
- Typography: one variable font (Inter or Geist) loaded locally via `@fontsource-variable/*`.
- UI verification: Playwright (screenshots, e2e), `@axe-core/playwright` (accessibility), MSW (mock API
  states so loading/empty/error can be rendered on demand).
- Routing, i18n, and client-state libraries are project choices. Follow the project.

## 2. Principles

- Clarity over decoration. One primary action per view. Consistency beats novelty.
- Dense, scannable layouts for data-heavy screens. Align everything to the spacing scale.
- Hierarchy through size, weight, and spacing before color. Prefer borders over shadows.
- Copy: sentence case, verb-led buttons ("Save changes"), plain error messages that say what to do next.

## 3. Tokens

- **Spacing:** 4px base, Tailwind scale only. No arbitrary values such as `w-[137px]` or `mt-[13px]`.
- **Type:** at most 5 sizes in use (`text-xs` to `text-2xl`), base 14px for dense admin UI. Weights 400/500/600.
- **Color:** shadcn semantic variables (`background`, `foreground`, `card`, `muted`, `border`, `primary`,
  `destructive`, `ring`). Neutrals plus one accent. Status colors (success, warning, danger, info) are
  tokens too. Define light and dark values. Contrast AA. No raw hex in components.
- **Radius:** one base `--radius`, at most two derived values. **Elevation:** shadow only for overlays
  (popover, dialog, toast).

## 4. Layout patterns

- **App shell:** sidebar + top bar + content area with a max width. Page header: title, short description,
  primary action on the right. Breadcrumbs when depth exceeds two levels.
- **Tables:** filters and search above, sticky header, sortable columns, pagination, row actions in a
  dropdown menu, bulk actions appear on selection, density suited to scanning.
- **Forms:** labels above inputs, inline validation on blur and submit, helper text for non-obvious fields,
  primary action bottom-right, group related fields with section headings. Long forms use sections or tabs.
- **Dashboards:** KPI row, then charts, then detail tables. Every number has a label and a period.
- **Detail pages:** header with key facts and actions, tabs for sections, activity or history last.
- **Destructive actions:** AlertDialog that names the object, with a danger-styled confirm button.
- **Feedback:** toast for transient success, inline messages for field errors, banner for page-level problems.

## 5. Required states

Every screen and component handles all of these, and all are viewed before handoff:

- Loading (skeletons matching the final layout, not spinners over blank pages)
- Empty (explains what belongs here and offers the next action)
- Error (says what failed and offers retry)
- Disabled and read-only
- Long text, many rows, and narrow widths (truncate with tooltip or wrap deliberately)

## 6. Accessibility

Semantic elements, associated labels, visible focus ring, full keyboard operation, AA contrast, no
information conveyed by color alone, icon-only buttons have accessible names. Respect
`prefers-reduced-motion`. Run an axe check on each new screen.

## 7. Motion

150–200ms, ease-out, used to explain change (open, close, reorder), never to decorate.

## 8. Anti-patterns

Hand-rolled controls that shadcn provides, magic numbers, raw hex, more than one accent color,
modal-on-modal, native `alert()`/`confirm()`, icon-only buttons without labels, spinners on empty
screens, text that breaks the layout when translated or lengthened, tables without empty states.

## 9. Review checklist (before handoff)

1. Screenshots at mobile (~390px) and desktop (~1440px) widths.
2. Compared with the nearest existing screen for spacing, type, and component consistency.
3. Every state in §5 viewed (use MSW or fixtures to force them).
4. No console errors; axe reports no new violations.
5. Only tokens and existing components used.
