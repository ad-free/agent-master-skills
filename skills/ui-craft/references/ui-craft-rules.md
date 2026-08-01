# ui-craft Rules — Design Token Usage, WCAG 2.1 AA, Component Contracts

## Design Token Usage Alignment

Every component must consume design tokens, not hardcoded values:

- **Colors:** Use `color-primary`, `color-surface`, `color-text` tokens — never hex/rgb literals in component code
- **Spacing:** Use `space-xs`, `space-sm`, `space-md`, `space-lg`, `space-xl` tokens
- **Typography:** Use `font-size-body`, `font-size-heading`, `line-height`, `font-weight` tokens
- **Radii:** Use `radius-sm`, `radius-md`, `radius-lg` tokens
- **Shadows:** Use `shadow-sm`, `shadow-md`, `shadow-lg` tokens
- **Breakpoints:** Use `breakpoint-sm`, `breakpoint-md`, `breakpoint-lg`, `breakpoint-xl` tokens

**Component contract rule:** If a component accepts a `className` prop, it must forward it. If it accepts a `variant` prop, it must map to design tokens — never inline styles for variants.

## WCAG 2.1 AA Accessibility Checklist

Every component must pass these checks before BUILD completes:

- [ ] **Color contrast:** All text meets 4.5:1 contrast ratio (3:1 for large text)
- [ ] **Focus indicators:** All interactive elements have visible focus states
- [ ] **Keyboard navigation:** All interactive elements reachable and operable via keyboard
- [ ] **ARIA labels:** Interactive elements have descriptive `aria-label` or visible text
- [ ] **Semantic HTML:** Use appropriate elements (`button`, `nav`, `main`, `article`, etc.)
- [ ] **Heading hierarchy:** Headings follow h1 → h2 → h3 order, no skipping levels
- [ ] **Touch targets:** All interactive elements have minimum 44x44px touch target
- [ ] **Text resize:** Text scales to 200% without loss of content or functionality
- [ ] **Reduced motion:** `prefers-reduced-motion` respected; no essential animations blocked
- [ ] **Screen reader:** Content makes sense when read in DOM order; no `aria-hidden` on interactive elements
- [ ] **Error handling:** Form errors are associated with fields via `aria-describedby`; error messages are programmatically linked
- [ ] **Landmarks:** Page has `main`, `nav`, and `aside` landmarks where appropriate

## Component Contract Standards

Every component must adhere to these contracts (from `design-system-validate`):

1. **Props interface:** All props typed with an explicit interface, no `any`
2. **Default props:** All optional props have sensible defaults
3. **Children:** Components that accept children must handle `undefined` gracefully
4. **Event handlers:** All event handlers are optional unless the component requires them
5. **Ref forwarding:** Components that need DOM access forward refs via `React.forwardRef`
6. **Test contract:** Every component has a test file that validates the contract (props, rendering, events, accessibility)
7. **Story contract:** Every component has a Storybook story that demonstrates all variants

## Token-First Development Rules

1. Define tokens before writing component code
2. Tokens live in `tokens.css`, `tailwind.config.ts`, `theme.ts`, and `tokens.json` — keep them in sync
3. No hardcoded color values in component files — always use token references
4. No hardcoded spacing values — always use `space-*` tokens
5. No hardcoded font sizes — always use `font-size-*` tokens
6. Responsive breakpoints use token-defined values, not magic numbers
7. Dark mode tokens must have a light-mode equivalent defined

## Violation Detection

Run these checks during BUILD and REVIEW:

```bash
# Check for hardcoded colors in component files
grep -rnE '#[0-9a-fA-F]{3,8}|rgb\(|hsl\(|color:' src/ --include='*.tsx' --include='*.ts'

# Check for hardcoded spacing values
grep -rnE 'px\s*[:=]|margin|padding|top|left|right|bottom' src/ --include='*.tsx' --include='*.ts' | grep -v 'token\|var(--'

# Check for missing aria labels on interactive elements
grep -rnE '<(button|a|input|select|textarea|div\[role)' src/ --include='*.tsx' | grep -v 'aria-label\|aria-labelledby'
```