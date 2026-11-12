# UI quality checklist

Each item is checkable in a diff or a screenshot.

- Icons used consistently, with labels where meaning is not obvious; not a wall of plain-text buttons.
- Real hierarchy: page title, section headings, grouping in cards, spacing from the scale.
- Data shown visually where useful (charts, badges, progress, avatars), not only tables.
- Colors and spacing from tokens; enough contrast; no raw hex or magic numbers; one primary action per view.
- Loading (skeleton), empty (message + action), error, disabled, success, long-content, permission-denied states.
- Responsive at mobile (~390), tablet (~768), desktop (~1440); wide tables scroll inside their own container.
- Realistic sample data; no "Lorem ipsum" or "Test 1".
- Forms: labels, inline validation messages, disabled and loading submit button, keyboard order.
- Accessibility: semantic elements, visible focus ring, labels on inputs and icon buttons, color is not the only signal.
- Console is free of errors on every changed route.
- Compared against the nearest existing screen for consistency.
- New screen or redesign: built from a picked reference; reference and build screenshots side by side at the same
  widths, no high-severity difference left (`fe-visual-loop` Step 7).
- Content is real or realistic and varied: no item repeated to fill a grid, no grey placeholder where an image
  belongs.
