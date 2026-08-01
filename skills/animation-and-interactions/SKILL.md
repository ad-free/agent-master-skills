---
name: animation-and-interactions
description: |
  Craft smooth CSS/Framer Motion animations, micro-interactions, and
  visual polish without performance degradation. Use when adding
  animations to UI components, creating page transitions, or implementing
  micro-interactions. Do NOT use for general UI styling (see ui-craft)
  or for accessibility auditing (see accessibility-deep).
  
model: big-pickle
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "add animation"
  - "create micro-interaction"
  - "page transition"
  - "CSS animation"
  - "Framer Motion"
  - "animation performance"
  - "visual polish"
  - "interaction design"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: frontend-ui
  integrates-with: [ui-craft, design-system-auditor]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# animation-and-interactions

## Relationship to existing skills

- animation-craft: Provides advanced animation patterns for micro-interactions, page transitions, and motion design; animation-and-interactions applies these patterns with performance constraints.
- ui-component-builder: Produces components that may need animations; animation-and-interactions adds motion to components built by ui-component-builder.
- accessibility-deep: Ensures animations respect `prefers-reduced-motion` and do not cause accessibility issues; animation-and-interactions must follow accessibility rules.
- design-system-auditor: Validates animation consistency with design tokens; animation-and-interactions must use design tokens for animation timing and easing.
- ui-craft: The frontend pipeline; animation-and-interactions is invoked during ui-craft's BUILD phase for animated components.

## When to Use

- Adding CSS animations or transitions to UI components
- Implementing Framer Motion animations for page transitions
- Creating micro-interactions (hover, focus, press, drag)
- Adding visual polish to existing components
- Optimizing animation performance (reducing jank, avoiding layout thrashing)
- Implementing gesture-based interactions
- Creating loading/empty/error state animations

## When NOT to Use

- General UI styling or layout — see ui-craft
- Building new UI components from scratch — see ui-component-builder
- Accessibility auditing — see accessibility-deep
- Design token generation — see design-system-validate
- Performance profiling of non-animation code — see dev-craft/plugins/performance-profiling

## Workflow

### Phase 1: Animation Specification

1. **Gather the design intent**: what is the animation supposed to communicate? (feedback, transition, delight, attention)
2. **Define the animation trigger**: what user action or system event triggers the animation?
3. **Define the animation target**: which element(s) are being animated?
4. **Define the animation properties**: duration, easing, delay, iteration, direction
5. **Define the accessibility requirements**: does the animation respect `prefers-reduced-motion`? Does it avoid motion that could cause vestibular disorders?
6. **Define the performance budget**: what is the acceptable frame rate and rendering cost?

### Phase 2: Animation Implementation

1. **Choose the animation approach**:
   - CSS transitions → simple state changes (hover, focus, active)
   - CSS keyframe animations → complex multi-step animations
   - Framer Motion → React-based animations with gestures and layout animations
   - View Transitions API → page-level transitions (modern browsers)
2. **Implement using design tokens**: use design token values for duration, easing, and spacing
3. **Use hardware-accelerated properties**: `transform`, `opacity`, `filter` — avoid animating `width`, `height`, `top`, `left`, `margin`, `padding`
4. **Implement `prefers-reduced-motion`**: provide a static or simplified fallback for users who prefer reduced motion
5. **Implement will-change hints**: add `will-change` sparingly for elements that will be animated
6. **Avoid layout thrashing**: batch DOM reads and writes, use `transform` instead of layout-affecting properties

### Phase 3: Micro-Interaction Implementation

1. **Hover interactions**: implement hover states with smooth transitions (150-300ms)
2. **Focus interactions**: implement focus rings and focus transitions that meet accessibility standards
3. **Press interactions**: implement press/active states with instant feedback (<100ms)
4. **Drag interactions**: implement drag with momentum, snap-back, and boundary constraints
5. **Loading states**: implement skeleton screens, shimmer effects, or progress indicators
6. **Error states**: implement shake, fade, or slide animations for error feedback
7. **Success states**: implement checkmark draw, confetti, or pulse animations for success feedback

### Phase 4: Performance Optimization

1. **Profile animations**: use browser DevTools Performance panel to identify jank
2. **Check frame rate**: ensure animations maintain 60fps (or 120fps on high-refresh displays)
3. **Check paint complexity**: avoid animating properties that trigger expensive paint operations
4. **Check layer promotion**: ensure animated elements are promoted to their own compositor layer
5. **Check animation frame budget**: ensure total animation work fits within 16ms per frame
6. **Optimize or simplify**: if an animation exceeds the budget, simplify it or reduce its scope

### Phase 5: Validation

1. **Run accessibility check**: verify `prefers-reduced-motion` is respected, animations don't cause vestibular issues
2. **Run performance check**: verify animations maintain the frame rate budget
3. **Run design consistency check**: verify animation tokens match the design system
4. **Test across browsers**: verify animations work in target browsers
5. **Test on low-end devices**: verify animations perform acceptably on lower-end hardware

## Context Management

- Track animation state in `.ui-craft/animations/<project>/state.json` with fields: `animation_id`, `status` (spec/implement/optimize/validate/done), `properties_defined`, `performance_budget_met`
- On session resume, check state.json for any in-progress animation and continue from the last completed phase

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read existing animation code, design tokens, accessibility guidelines | Only read project source and design files |
| Write | Create new animation files, keyframes, or motion configurations | Follow the project's animation conventions |
| Edit | Refactor animation code for performance or consistency | Preserve existing animation behavior |
| Bash | Run performance audits, accessibility checks, browser tests | Use established tools (Lighthouse, axe, DevTools) |
| Grep | Find animation properties, hardcoded values, or missing prefers-reduced-motion | Search within the animation scope |
| Glob | Find animation-related files | Pattern: `**/*.{css,tsx,jsx,ts,js}` |
| Task | Spawn subagent for performance profiling or accessibility audit | Subagent must report findings, not make edits |

## Output Contract

On completion, the skill must produce:

1. Animation implementation following the project's conventions
2. `prefers-reduced-motion` fallback for all animations
3. Performance validation report (frame rate, paint complexity, layer promotion)
4. Accessibility validation report (WCAG compliance, vestibular safety)
5. Design token compliance report (animation tokens used correctly)
6. Updated state.json with the animation status

## Quality Gates

- [ ] Animations use design tokens for duration, easing, and spacing
- [ ] Hardware-accelerated properties are used (`transform`, `opacity`, `filter`)
- [ ] `prefers-reduced-motion` is respected for all animations
- [ ] Animations maintain 60fps (or 120fps on high-refresh displays)
- [ ] No layout thrashing or forced synchronous layouts
- [ ] Animations do not cause vestibular disorders (no large-scale motion, no parallax on scroll)
- [ ] Focus states are visible and accessible
- [ ] Animations work across target browsers
- [ ] Animations perform acceptably on low-end devices

## Error Handling

- **Animation causes jank**: profile with DevTools, identify the bottleneck, simplify or optimize the animation
- **`prefers-reduced-motion` not respected**: add the media query and provide a static fallback
- **Animation breaks in a target browser**: check browser compatibility, add vendor prefixes or fallbacks
- **Performance budget exceeded**: simplify the animation, reduce the scope, or remove it entirely
- **Animation causes vestibular issues**: remove or reduce the motion, provide a static alternative