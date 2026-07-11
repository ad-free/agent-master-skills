# UI Patterns Reference

Common UI patterns and best practices for ui-craft.

## Component Patterns

### Button
- Use `cva` (class-variance-authority) for variant management
- Support variants: default, secondary, outline, ghost, destructive, link
- Support sizes: default, sm, lg, icon
- Include focus-visible ring for keyboard navigation
- Disabled state with reduced opacity

### Card
- Consistent border-radius (12px default)
- Shadow for depth (sm default, md/lg on hover for interactive)
- Padding: 24px (p-6)
- Optional interactive variant with hover lift

### Modal
- Overlay with backdrop blur
- Escape key to close
- Click outside to close
- Focus trap for accessibility
- Animate in/out

### Input
- Label with htmlFor
- Error state with aria-invalid
- Hint text support
- Focus ring with ring-offset
- Disabled state

### Navbar
- Sticky with backdrop blur
- Responsive (mobile menu hidden)
- Active state with aria-current
- Semantic nav element

## Forms
- **Validation**: React Hook Form + Zod schema for type-safe validation
- **Common patterns**:
  - Login form (email/password)
  - Sign-up form (name, email, password, confirm)
  - Contact form (name, email, message)
  - Settings form (editable fields)
  - Password reset form (email input)
- **Features**:
  - Inline validation with clear error messages
  - Form state management (touched/dirty/valid)
  - Loading states during submission
  - Success/error toasts or notifications
  - Optimistic updates for fast feedback
  - Server-side validation support

## Page Templates
- **Landing**: Hero section with CTA, features grid, testimonials, pricing
- **Dashboard Layout**: Sidebar navigation, main content area, header, responsive
- **Auth**: Login/signup pages with form, optional social auth, redirect logic
- **Settings**: Profile, security, notifications, billing tabs sections
- **404**: Minimal design with navigation back to home

## Component Tests
- **Testing approach**: Vitest + React Testing Library + jest-axe
- **Test coverage**:
  - Button: variants, states, keyboard interactions
  - Card: content, hover states, accessibility
  - Input: validation, focus states, error messages
  - Modal: open/close, escape key, focus trap
  - Navbar: responsive behavior, navigation items
- **Accessibility tests**:
  - Color contrast validation
  - Screen reader compatibility (jest-axe)
  - Keyboard navigation coverage
  - Focus management tests

## Icons
- **Libraries**: lucide-react (#1), heroicons (#2), phosphor, tabler, react-icons
- **Usage**: Auto-detection of available libraries, wrapper component generation
- **Consistency**: Consistent icon size (24px default), stroke width (2px), family
- **Platform**: SVG icons with proper accessibility (aria-label, roles)

## UX Best Practices

### Forms
- Inline validation (not just on submit)
- Clear error messages with role="alert"
- Labels associated via htmlFor/id
- Hint text for complex fields
- Disabled state for loading

### Navigation
- Current page marked with aria-current="page"
- Consistent placement across pages
- Mobile hamburger menu for < 768px
- Keyboard navigable

## UX Best Practices

### Forms
- Inline validation (not just on submit)
- Clear error messages with role="alert"
- Labels associated via htmlFor/id
- Hint text for complex fields
- Disabled state for loading

### Navigation
- Current page marked with aria-current="page"
- Consistent placement across pages
- Mobile hamburger menu for < 768px
- Keyboard navigable

### Feedback
- Loading states (skeleton/spinner)
- Success/error toasts
- Optimistic updates for fast feel
- Disabled buttons during submission

### Accessibility
- Focus-visible ring on all interactive elements
- Touch targets >= 44px
- Color contrast >= 4.5:1
- prefers-reduced-motion respected
- Semantic HTML (nav, main, button, heading hierarchy)
- aria-label on icon-only buttons
- aria-current on active nav items
- aria-invalid on error fields
- role="alert" on error messages

## Responsive Breakpoints

| Breakpoint | Width | Target |
|------------|-------|--------|
| xs | < 640px | Small phones |
| sm | >= 640px | Large phones |
| md | >= 768px | Tablets |
| lg | >= 1024px | Desktop |
| xl | >= 1280px | Wide desktop |
| 2xl | >= 1536px | Ultra-wide |

## Dark Mode Strategy

- Use CSS variables for all colors
- Define `:root` (light) and `.dark` or `[data-theme="dark"]` (dark) variants
- Use Tailwind `dark:` prefix for component-level overrides
- Respect `prefers-color-scheme` media query
- Test contrast independently in both modes

## Animation Guidelines

| Type | Duration | Easing | Use Case |
|------|----------|--------|----------|
| Micro-interaction | 150-200ms | ease-out | Button hover, focus, toggle |
| Transition | 200-300ms | ease-in-out | Modal, drawer, page |
| Stagger | 50-100ms per item | ease-out | List animations, cards |
| Page transition | 300-500ms | ease-in-out | Route changes |
| Loading skeleton | 1.5-2s loop | ease-in-out | Content loading |
| Notification | 300ms in, 200ms out | ease-out | Toast, snackbar |

### Animation Principles
- **Purposeful** — Every animation should communicate state change or guide attention
- **Performant** — Use `transform` and `opacity` only (avoid layout-triggering properties)
- **Respectful** — Always respect `prefers-reduced-motion`
- **Consistent** — Use the same duration/easing for similar interactions

### CSS Animation Patterns

```css
/* Hover lift effect */
.card {
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Focus ring animation */
button:focus-visible {
  outline: 2px solid var(--color-ring);
  outline-offset: 2px;
  transition: outline-offset 150ms ease-out;
}

/* Page transition */
.page-enter {
  opacity: 0;
  transform: translateY(8px);
}
.page-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 300ms ease-in-out, transform 300ms ease-in-out;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Tailwind Animation Classes

```html
<!-- Hover lift -->
<div class="transition-all duration-200 ease-out hover:-translate-y-0.5 hover:shadow-lg">

<!-- Focus ring -->
<button class="focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ring">

<!-- Fade in -->
<div class="animate-in fade-in duration-300">

<!-- Slide in -->
<div class="animate-in slide-in-from-bottom-2 duration-300">

<!-- Stagger children -->
<div class="[&>*:nth-child(1)]:animate-in [&>*:nth-child(1)]:fade-in [&>*:nth-child(1)]:delay-75
            [&>*:nth-child(2)]:animate-in [&>*:nth-child(2)]:fade-in [&>*:nth-child(2)]:delay-150
            [&>*:nth-child(3)]:animate-in [&>*:nth-child(3)]:fade-in [&>*:nth-child(3)]:delay-200">
```

## Accessibility Checklist

- [ ] Color contrast >= 4.5:1 (body), >= 3:1 (large text)
- [ ] Focus-visible ring on all interactive elements
- [ ] Touch targets >= 44x44px
- [ ] aria-label on icon-only buttons
- [ ] aria-current on active nav items
- [ ] aria-invalid on error fields
- [ ] role="alert" on error messages
- [ ] role="dialog" + aria-modal on modals
- [ ] Semantic HTML (nav, main, button, heading hierarchy)
- [ ] prefers-reduced-motion respected
- [ ] Keyboard navigable (Tab, Enter, Escape)
- [ ] Screen reader focus order matches visual order
