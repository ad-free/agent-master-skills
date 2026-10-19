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

## 2. `design.md` (before implementing; user confirms the direction)

1. **Users and goals:** who, and what they do most.
2. **Information architecture:** pages, navigation, the 3-5 most important screens.
3. **Per-screen composition:** what is on each key screen and why. Pick the domain file in `ui-patterns/`.
4. **Design-system choices, explicit:** component library, icon set (Lucide, Heroicons, Material Icons), chart
   library (Recharts, ECharts, Tremor; `idioms/charts.md`), palette (primary, neutrals, semantic
   success/warning/danger, dark mode yes/no), typography, spacing scale, radius. Record the library chosen.
5. **States per screen:** loading (skeletons), empty (message + call to action), error, success,
   permission-denied.
6. **Responsive behavior and accessibility basics** (contrast, keyboard, labels).

Small UI change inside an existing screen: three lines in the brief instead of a file.

## 3. Build

Reuse existing components; tokens only; realistic sample data (names, dates, amounts), never "Lorem ipsum".
Data shown visually where useful: charts for trends, badges for status, progress, avatars; not tables only.
Trends = lines, comparisons = bars, parts of a whole = donut (few slices), never a pie with many slices.

## 4. Visual critique (required, in Verify)

Run the app, screenshot each key screen at desktop (~1440) and mobile (~390), look at them, compare with
`design.md` and `checklists/ui.md`, fix gaps, include screenshots in the Evidence table. Browser unavailable:
list under Not verified and give preview commands.

Example of a finding from this pass: "Dashboard at 390px: KPI cards overflow the viewport and the table has no
horizontal scroll. Fix: stack cards in one column, wrap the table in a scrolling container."
