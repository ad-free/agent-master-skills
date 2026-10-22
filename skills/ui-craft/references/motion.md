# Motion and micro-interactions

Folded from the former `animation-and-interactions` skill. How much motion to use is set by `MOTION_INTENSITY`
in `design-dials.md`; this file is how to build it without jank or harm.

## Pick the tool

| Need | Use |
|---|---|
| Hover, focus, active, open/close | CSS transitions |
| Multi-step or looping | CSS keyframes |
| React layout, gesture, exit animations | Framer Motion (`motion`), spring easing |
| Page / route transitions | View Transitions API (fallback: no animation) |

Use the project's duration and easing tokens; add them to the tokens file if missing, never inline magic values.

## Timing

| Interaction | Duration |
|---|---|
| Press / active feedback | under 100ms |
| Hover, focus, small state change | 150–300ms |
| Enter / exit of panels, dialogs | 200–400ms |
| Stagger between list items | 50–75ms per item, cap the total |

## Rules

- Animate only `transform`, `opacity`, `filter`. Never `width`, `height`, `top`, `left`, `margin`, `padding`.
- `will-change` only on elements about to animate; remove it after.
- Batch DOM reads before writes; no scroll listeners (use `animation-timeline` or IntersectionObserver).
- `prefers-reduced-motion: reduce` collapses every non-essential animation to instant or a fade.
- Never flash more than 3 times per second.
- Motion must not hide state: loading, error and success still read correctly with motion off.

## Verify

Record a Performance trace in DevTools for the heaviest animation: no long frames (over 16ms) during it.
Toggle reduced motion in the browser and check the screen still works. Check one low-end device profile
(CPU 4x throttle).
