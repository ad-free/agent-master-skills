---
name: ui-component-builder
description: |
  Build modern, accessible, modular UI components using React/Vue/Tailwind
  adhering to design tokens and responsive design. Use when creating new
  UI components, refactoring component structure, or implementing a
  design system component. Do NOT use for general UI styling (see ui-craft)
  or for design token generation (see design-system-validate).
  
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
  - "build UI component"
  - "create component"
  - "ui component"
  - "build component library"
  - "design system component"
  - "responsive component"
  - "accessible component"
  - "tailwind component"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: frontend-ui
  integrates-with: [ui-craft, design-system-auditor]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# ui-component-builder

## Relationship to existing skills

- ui-craft: Provides the frontend development pipeline; ui-component-builder is invoked for individual component implementation within ui-craft's BUILD phase.
- design-system-validate: Validates components against design tokens; ui-component-builder produces components that must pass design-system-validate.
- accessibility-deep: Provides WCAG AAA compliance auditing; ui-component-builder must follow accessibility rules from the start.
- backend-patterns: Ensures the component's data layer follows clean architecture patterns when fetching or mutating data.

## When to Use

- Creating a new React/Vue component from a design spec or Figma file
- Building a reusable component library following design tokens
- Implementing responsive components that adapt across breakpoints
- Creating accessible components that meet WCAG 2.2 AAA standards
- Refactoring an existing component for better modularity or reusability
- Implementing a component that uses Tailwind CSS with design token consistency

## When NOT to Use

- General UI styling or layout — see ui-craft
- Generating design tokens or design system configuration — see design-system-validate
- WCAG accessibility auditing — see accessibility-deep
- Animating components — see animation-and-interactions
- API contract design for FE-BE integration — see api-contract-designer

## Workflow

### Phase 1: Component Specification

1. **Gather requirements**: read the design spec, Figma file, or design token reference
2. **Define the component contract**: props/inputs, outputs/events, children/slots
3. **Identify responsive breakpoints**: which breakpoints does the component need to support?
4. **Identify accessibility requirements**: ARIA roles, keyboard navigation, screen reader support
5. **Determine data dependencies**: does the component fetch data, accept props, or both?
6. **Write the component spec**: document the component's API, behavior, and edge cases

### Phase 2: Architecture

1. **Choose the component pattern**:
   - Simple presentational → function component with props
   - Compound component → parent + sub-components with shared state
   - Render prop → flexible composition pattern
   - Headless component → logic-only with consumer-controlled rendering
2. **Define the file structure**:
   - `<ComponentName>/index.tsx` — barrel export
   - `<ComponentName>/ComponentName.tsx` — main implementation
   - `<ComponentName>/ComponentName.styles.ts` — styles (Tailwind or CSS modules)
   - `<ComponentName>/ComponentName.types.ts` — TypeScript types/interfaces
   - `<ComponentName>/ComponentName.test.tsx` — unit tests
   - `<ComponentName>/ComponentName.stories.tsx` — Storybook stories (if applicable)
3. **Set up the component directory** following the project's existing conventions

### Phase 3: Implementation

1. **Implement types first**: define all props, events, and slot types
2. **Implement the component shell**: structure, props destructuring, state setup
3. **Implement styling**: use design tokens, Tailwind classes, or CSS modules
4. **Implement responsive behavior**: use Tailwind responsive prefixes or media queries
5. **Implement accessibility**: ARIA attributes, keyboard handlers, focus management
6. **Implement data fetching** (if needed): use the project's existing data layer patterns
7. **Implement error and loading states**: skeleton, error boundary, empty state

### Phase 4: Validation

1. **Run design-system-validate**: check token consistency and design compliance
2. **Run accessibility-deep**: verify WCAG 2.2 AAA compliance
3. **Run unit tests**: all tests pass with >80% coverage
4. **Test responsive behavior**: verify at all breakpoints
5. **Test keyboard navigation**: verify all interactive elements are reachable and operable
6. **Test screen reader**: verify ARIA labels and roles are correct

### Phase 5: Documentation

1. **Write component documentation**: props table, usage examples, accessibility notes
2. **Update the component index**: add the component to the library exports
3. **Add Storybook stories** if the project uses them
4. **Update the design system docs** if the component is part of the shared library

## Context Management

- Track component state in `.ui-craft/components/<component-name>/state.json` with fields: `component_name`, `status` (spec/implement/validate/done), `props_defined`, `tests_passing`
- On session resume, check state.json for any in-progress component and continue from the last completed phase

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read design specs, existing components, design tokens | Only read project source and design files |
| Write | Create new component files | Follow the file structure defined in Phase 2 |
| Edit | Refactor existing component code | Preserve existing behavior; never change the public API without updating docs |
| Bash | Run tests, lint, typecheck, build | Must run tests after each phase |
| Grep | Find component references, design token usage | Search within the target component directory |
| Glob | Find existing component files | Pattern: `components/**/*` |
| Task | Spawn subagent for accessibility audit or design token validation | Subagent must report findings, not make edits |

## Output Contract

On completion, the skill must produce:

1. A complete component implementation following the file structure from Phase 2
2. Unit tests with >80% coverage
3. Accessibility audit results from accessibility-deep
4. Design token compliance report from design-system-validate
5. Component documentation with props table and usage examples
6. Updated state.json with the component status

## Quality Gates

- [ ] Component follows the project's existing file structure conventions
- [ ] All props have TypeScript types defined
- [ ] Component is responsive at all required breakpoints
- [ ] Component passes WCAG 2.2 AAA accessibility checks
- [ ] Component uses design tokens for colors, spacing, typography
- [ ] All unit tests pass with >80% coverage
- [ ] Keyboard navigation works for all interactive elements
- [ ] ARIA labels and roles are correct
- [ ] Loading and error states are implemented
- [ ] Component documentation is complete

## Error Handling

- **Design token not found**: halt implementation, check the design token source, and add the missing token or use the closest match with a comment
- **Accessibility audit failure**: fix the accessibility issue before proceeding; do not ship components with accessibility violations
- **Test failure after implementation**: debug the specific test, fix the issue, and re-run
- **Responsive breakpoint missing**: add the missing breakpoint to the component's responsive rules
- **TypeScript compilation error**: fix type errors before proceeding; do not use `any` to suppress errors