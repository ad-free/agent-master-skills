# Charts

Use the library the repo has. New project: Recharts (simple React charts), ECharts (large or complex data,
heatmaps), Tremor (dashboard-ready blocks on Tailwind).
- Match chart to question: trend = line, comparison = bar, composition = donut with few slices, correlation =
  scatter, density over time/day = heatmap. Avoid 3D, dual axes, and pies with many slices.
- Colors from the theme, colorblind-safe, with direction not color-only (labels, patterns); consistent color per category.
- Every chart has a title, units, a legend when more than one series, readable axes, a tooltip, and
  loading, empty and error states. Use a text summary or table for accessibility.
- Recharts: v3 enables `accessibilityLayer` (keyboard + screen-reader tooltip) by default, v2 needs the prop; wrap in
  `ResponsiveContainer` (ResizeObserver). ECharts heatmaps use progressive rendering above 3000 points (tune
  `progressive`); there is no separate `large` mode for heatmap. `@tremor/react` bundles Recharts.
- Format numbers, currency and dates for the locale; keep the data fetch separate from the chart component.
