# Tailwind

Detect v3 (`tailwind.config.js`) vs v4 (CSS-first `@theme`); follow what the repo has.
- Design tokens (colors, spacing, radius, fonts) live in the theme; use them, not arbitrary values
  (`w-[137px]`, `#3b82f6`) unless a one-off is justified.
- Semantic color names (primary, muted, danger) over raw palette names where the repo does.
- Consistent spacing scale; responsive prefixes mobile-first; dark mode through the repo's mechanism.
- Extract repeated class strings into components, not `@apply` sprawl; keep class order tool-sorted if the
  repo uses the prettier plugin.
- Traps: dynamic class names built by string concatenation (purged away); color-only meaning; missing focus styles.
