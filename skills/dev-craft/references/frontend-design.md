# Frontend design (UI tasks only)

Agents build the functional minimum because nothing asks for more and tests pass on an ugly page. So decide the
design before coding, and look at the result after. Repo design system and tokens win over everything here.

## 1. Frame the UI

Check for an existing design system, component library, tokens, `DESIGN.md` (project, then
`~/.config/agents/DESIGN.md`). Follow what exists. Detect the library from `package.json`, imports and theme
files; the choice is **per project, never global**; load only its `idioms/` file; never mix shadcn/ui and
Material-UI unless the repo already does.

New project with neither: propose 2-3 options with a one-line trade-off and a recommendation, and let the user
choose. Example: shadcn/ui + Tailwind (highly custom design, speed) vs Material-UI (ready consistent set,
built-in theming and data grid). Starting from a proven template and adapting beats generating layout blank.
For a full pipeline use `ui-craft`; you decide when, and check its result.

## 2. Direction (before implementing; user confirms)

**New screen, new page or redesign:** run the `fe-visual-loop` skill. It starts from real reference sites the user
picks, extracts them into `DESIGN.md`, fills real content and mocks from the reference; the user approves
screenshots, not a text description. Do not invent directions from adjectives.

**Small change inside an existing screen:** three lines in the brief (what changes, which existing pattern it
follows, states affected).

Large tasks also write `design.md` with:

1. **Users and goals:** who, and what they do most.
2. **Information architecture:** pages, navigation, the 3-5 most important screens.
3. **Per-screen composition:** what is on each key screen and why. Pick the domain file in `ui-patterns/`.
4. **Design-system choices, explicit:** component library, icon set (Lucide, Heroicons, Material Icons), chart
   library (Recharts, ECharts, Tremor; `idioms/charts.md`), palette (primary, neutrals, semantic
   success/warning/danger, dark mode yes/no), typography, spacing scale, radius. Record the library chosen.
5. **States per screen:** loading (skeletons), empty (message + call to action), error, success,
   permission-denied.
6. **Responsive behavior and accessibility basics** (contrast, keyboard, labels).
7. **Reference:** the picked reference and mock screenshot paths from `fe-visual-loop`.

## 3. Visual quality (what finished looks like)

- **Type hierarchy:** 4-5 sizes, each with one job (page title, section heading, body, label/meta, numbers).
  Contrast comes from size and weight first, colour last. Body line length 60-75 characters.
- **Spacing rhythm:** one scale; more space between groups than inside them; section padding consistent on a
  page. Uneven gaps are the most visible sign of an unfinished page.
- **Density per screen type:** admin tables and dashboards dense (14px base, compact rows); forms medium;
  storefront and marketing airy, with large imagery and fewer items per row.
- **One accent:** primary actions, links and the active state only. Status colours only for status. Neutrals do
  the rest.
- **Numbers:** tabular figures (`font-variant-numeric: tabular-nums`) in tables, prices and KPIs; right-aligned
  in columns; units and periods labelled.
- **Finished table:** sticky header, aligned numeric columns, status as badges, row actions in a menu, empty
  state, pagination or virtualised rows, scrolls in its own container at 390.
- **Finished form:** labels above fields, grouped sections, helper text where needed, inline errors, primary
  action last and disabled while submitting.
- **Finished empty state:** says what belongs here, why it is empty, and offers the one next action.
- **Images:** one aspect ratio per collection, consistent crop and background; no stretched or mixed-size cards.
- **Compare, do not imagine:** judge against the reference screenshots at the same width, not against a memory
  of "good design".

## 4. Build

Reuse existing components; tokens only; realistic sample data (names, dates, amounts), never "Lorem ipsum".
Data shown visually where useful: charts for trends, badges for status, progress, avatars; not tables only.
Trends = lines, comparisons = bars, parts of a whole = donut (few slices), never a pie with many slices.

## 5. Visual critique (required, in Verify)

Run the app, screenshot each key screen at desktop (~1440) and mobile (~390), look at them, compare with the
picked reference, `design.md` and `checklists/ui.md`, fix gaps, include screenshots in the Evidence table. New
screens and redesigns: the `ui-verifier` agent does this pass (`fe-visual-loop` Step 7). Browser unavailable:
list under Not verified and give preview commands.

Example of a finding from this pass: "Dashboard at 390px: KPI cards overflow the viewport and the table has no
horizontal scroll. Fix: stack cards in one column, wrap the table in a scrolling container."
