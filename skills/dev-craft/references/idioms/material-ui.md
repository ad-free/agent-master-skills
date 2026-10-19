# Material-UI (MUI)

Load only if the repo uses it (`@mui/*`). Never mix with shadcn/ui. Detect the major version; APIs differ.
- One theme (`createTheme`) for palette, typography, spacing, component overrides; use `sx` and theme values,
  not hard-coded colors.
- Use MUI's inputs, `DataGrid`, `Dialog`, `Snackbar` before hand-rolling. DataGrid is open-core: Community
  (`@mui/x-data-grid`) is MIT; multi-sort, column pinning/resizing need Pro, and row grouping/aggregation/Excel
  export need Premium, both commercial. Check the repo's package and license before promising a feature.
- Forms: the repo's pattern (often React Hook Form with `Controller`); show `helperText` errors.
- Responsive through breakpoints; keep layout with `Grid`/`Stack`.
- Traps: inline styles that bypass the theme; mixing styling engines; missing `aria-label` on icon buttons.
