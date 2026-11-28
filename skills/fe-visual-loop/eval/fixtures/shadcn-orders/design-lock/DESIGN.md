# DESIGN.md — Northwind Supply admin (locked)

Status: **locked**, approved by the product owner. Implement against this; do not invent a new look. A screen type
not covered here needs a new approved pattern first.

References picked by the owner: **Linear** (quiet chrome, compact density, monochrome with one accent, status as
icon + text) and **Stripe Dashboard** (tables: right-aligned tabular amounts, soft status pills, filter tabs with
counts, one clear primary action). Approved pattern screenshots: `design/list-pattern-1440.png`,
`design/list-pattern-390.png` (an Invoices screen; apply its structure to every list screen).

## Tokens (already in `src/styles/theme.css`)
- Font: Inter (loaded in `index.html`), `font-feature-settings: "cv11", "tnum"` on numbers (`tabular-nums`).
- Neutrals: slate-tinted greys from the theme (`background`, `muted`, `border`, `muted-foreground`).
- One accent: indigo `--primary`. Only for the primary action, links, focus ring and the active filter tab.
- Status colours only inside status pills: success (green), warning (amber), info (blue), neutral (grey),
  danger (red), each as a soft tint background + darker text + 6px dot.
- Radius 8px (`--radius: 0.5rem`). Borders 1px `border-border`. Shadows: none, except `shadow-xs` on cards.
- Spacing scale: 4 / 8 / 12 / 16 / 24 / 32. Page gutter 24px desktop, 16px under 768px.

## Type scale (5 sizes, each one job)
| Role | Size / weight |
|---|---|
| Page title | 24px / 600, tracking -0.01em |
| Section / card value | 20–24px / 600, tabular |
| Body, table cells | 14px / 400 |
| Labels, meta, table header | 13px / 500, `muted-foreground` |
| Small meta under a value (email, sub-label) | 12px / 400, `muted-foreground` |

## Page frame
- Top bar 56px: product name left (15px / 600), quiet nav links (14px, muted; active = foreground + 2px
  underline in accent), user avatar right. Under 768px: product name + a menu button; no wrapping nav.
- Content max width 1200px, centred.
- Page header: title + one-line description (muted, 14px) on the left; actions on the right: one **filled
  primary** (accent) and at most one **outline secondary**. Under 768px the actions go full-width in one row
  under the title.

## List screen pattern (orders, invoices, customers…)
1. **KPI row:** 4 cards, identical structure in every card: label (13px muted), value (24px / 600 tabular), one
   sub-line (12px muted). Never leave one card with a sub-line and others without. 4 columns desktop, 2x2 under
   768px.
2. **Filter bar:** status as **tabs with counts** ("All 12", "Paid 4", …) left; search input with a leading
   icon (width 280px) right. Active tab: foreground text + accent underline. Under 768px: tabs in their own
   horizontally scrolling row, search full width below.
3. **Table (≥ 768px):** inside a bordered card, rows 48px, header row `muted` background, 13px / 500 muted.
   - ID: 13px `font-mono`, foreground.
   - Primary entity (customer): name 14px / 500 with email under it (12px muted) in the same cell.
   - Date: "Nov 27, 2026".
   - Counts and amounts: right-aligned, `tabular-nums`; amount 14px / 500 with currency "$4,820.50".
   - Status: soft pill (dot + capitalised label).
   - Row actions: one ghost icon button (`…`, `aria-label="Actions for <id>"`) opening a dropdown
     (View, Edit, separator, Delete in destructive colour). Delete asks for confirmation (AlertDialog).
   - Footer inside the card: "Showing 12 of 12" left, 13px muted.
4. **List (< 768px): no table, no horizontal scroll.** Each record is a row card: line 1 ID (mono) + status pill
   right; line 2 customer name; line 3 date · items (muted) left, amount right (15px / 600 tabular); the `…`
   menu top-right.
5. **Empty state** (filters match nothing): icon, "No orders match these filters", a "Clear filters" button.

## Do not
- Raw hex or inline `style={{}}`; use theme tokens and shadcn/ui components from `src/components/ui`.
- Colour without a text label; more than one filled button per view; three buttons per row.
- Fixed pixel widths on containers or tables.
