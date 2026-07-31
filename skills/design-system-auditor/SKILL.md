---
name: design-system-auditor
description: |
  Audit UI code for design consistency, responsiveness, performance, and
  WCAG accessibility standards. Use when validating UI against design
  tokens, checking accessibility compliance, or auditing a component
  library for consistency. Do NOT use for building new components
  (see ui-component-builder) or for generating design tokens (see
  design-system-validate).
  
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
  - "audit design system"
  - "check design consistency"
  - "design token audit"
  - "WCAG audit"
  - "accessibility audit"
  - "responsive audit"
  - "component library audit"
  - "design compliance check"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: frontend-ui
  integrates-with: [ui-craft, ui-component-builder]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# design-system-auditor

## Relationship to existing skills

- design-system-validate: Validates UI code against design system tokens and component library specs; design-system-auditor provides a broader audit covering consistency, responsiveness, performance, and accessibility.
- accessibility-deep: Provides WCAG 2.2 AAA compliance auditing; design-system-auditor includes accessibility as one of its audit dimensions.
- ui-component-builder: Produces components that must pass design-system-auditor validation.
- ui-craft: The frontend pipeline; design-system-auditor is invoked during ui-craft's AUDIT and REVIEW phases.

## When to Use

- Validating UI code against design tokens and component library specs
- Checking design consistency across a feature or module
- Auditing accessibility compliance (WCAG 2.2 AAA)
- Checking responsive behavior across breakpoints
- Auditing component library for consistency and completeness
- Validating performance of UI components (rendering, paint, layout)
- Pre-release UI quality check

## When NOT to Use

- Building new UI components — see ui-component-builder
- Generating design tokens or design system configuration — see design-system-validate
- Animating components — see animation-and-interactions
- General frontend development — see ui-craft
- Security vulnerability discovery — see bug-hunting

## Workflow

### Phase 1: Audit Scope Definition

1. **Define the audit scope**: which components, pages, or modules are being audited?
2. **Identify the audit dimensions**:
   - Design token consistency (colors, spacing, typography, shadows)
   - Responsive behavior (all breakpoints)
   - Accessibility (WCAG 2.2 AAA)
   - Performance (rendering, paint, layout)
   - Component API consistency (props, naming, patterns)
3. **Gather reference materials**: design tokens file, component library docs, accessibility checklist
4. **Set audit criteria**: define pass/fail thresholds for each dimension
5. **Get user confirmation** on the audit scope and criteria

### Phase 2: Design Token Consistency Audit

1. **Extract all design tokens used** in the audited codebase
2. **Compare against the canonical design token source**: check for hardcoded values that should use tokens
3. **Check token naming consistency**: are tokens used according to the naming convention?
4. **Check token value consistency**: are the same tokens used for the same semantic purpose?
5. **Identify token violations**: hardcoded values, wrong tokens, missing tokens
6. **Report findings**: list each violation with location, expected token, and actual value

### Phase 3: Responsive Behavior Audit

1. **Check breakpoint usage**: are all required breakpoints handled?
2. **Check responsive patterns**: are Tailwind responsive prefixes or media queries used correctly?
3. **Test layout at each breakpoint**: verify no horizontal scroll, overlapping elements, or truncated content
4. **Check touch targets**: are interactive elements at least 44x44px on mobile?
5. **Check text readability**: is font size appropriate at each breakpoint?
6. **Report findings**: list each responsive issue with the breakpoint and description

### Phase 4: Accessibility Audit

1. **Check ARIA attributes**: are roles, labels, and descriptions correct and complete?
2. **Check keyboard navigation**: can all interactive elements be reached and operated via keyboard?
3. **Check color contrast**: do text/background combinations meet WCAG AAA contrast ratios?
4. **Check focus management**: is focus visible and logical? Are focus traps avoided?
5. **Check screen reader support**: are semantic HTML elements used correctly? Are live regions used for dynamic content?
6. **Check reduced motion**: does the UI respect `prefers-reduced-motion`?
7. **Report findings**: list each accessibility violation with severity (critical/serious/moderate/minor)

### Phase 5: Performance Audit

1. **Check rendering performance**: are there unnecessary re-renders, large component trees, or inefficient patterns?
2. **Check paint performance**: are there expensive CSS properties (e.g., `box-shadow` on many elements)?
3. **Check layout performance**: are there layout thrashing patterns or forced synchronous layouts?
4. **Check image/media optimization**: are images properly sized, lazy-loaded, and in modern formats?
5. **Check bundle impact**: does the component add unnecessary bundle size?
6. **Report findings**: list each performance issue with estimated impact

### Phase 6: Component API Consistency Audit

1. **Check naming conventions**: are component names, prop names, and event names consistent?
2. **Check prop types**: are all props typed and documented?
3. **Check default values**: do all optional props have sensible defaults?
4. **Check composition patterns**: are compound components, render props, and slots used consistently?
5. **Report findings**: list each inconsistency with the expected pattern

### Phase 7: Report and Remediation

1. **Compile the audit report**: all findings organized by dimension and severity
2. **Prioritize findings**: critical and serious issues first
3. **Propose remediation**: for each finding, suggest the specific fix
4. **Get user confirmation** on the remediation plan
5. **Execute remediation**: fix the issues in priority order
6. **Re-audit**: run the audit again to confirm all issues are resolved

## Context Management

- Track audit state in `.ui-craft/audit/<project>/state.json` with fields: `audit_id`, `scope`, `dimensions`, `findings`, `status`, `remediation_plan`
- On session resume, check state.json for any in-progress audit and continue from the last completed phase

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read component source, design tokens, accessibility checklists | Only read project source and design files |
| Write | Create audit report and remediation plan | Follow the audit report format |
| Edit | Fix audit findings | One fix at a time; re-run relevant audit after each fix |
| Bash | Run accessibility tools, performance audits, test suites | Use established tools (axe, Lighthouse, etc.) |
| Grep | Find hardcoded values, ARIA attributes, breakpoint usage | Search within the audit scope |
| Glob | Find component files, design token files | Pattern: `components/**/*` |
| Task | Spawn subagent for deep accessibility or performance audit | Subagent must report findings, not make edits |

## Output Contract

On completion, the skill must produce:

1. An audit report organized by dimension (design tokens, responsive, accessibility, performance, API consistency)
2. A prioritized remediation plan with specific fixes for each finding
3. Updated state.json with the audit results
4. Re-audit confirmation that all critical and serious issues are resolved

## Quality Gates

- [ ] All design token violations are identified and reported
- [ ] All responsive breakpoints are tested
- [ ] WCAG 2.2 AAA accessibility checklist is complete
- [ ] Performance audit covers rendering, paint, and layout
- [ ] Component API consistency is checked
- [ ] Remediation plan is prioritized by severity
- [ ] Re-audit confirms all critical and serious issues are resolved
- [ ] No new violations introduced during remediation

## Error Handling

- **Audit tool failure**: retry once; if it fails again, use manual inspection for that dimension
- **Design token source not found**: halt the design token audit, locate the token source file, and retry
- **Accessibility tool false positive**: document the false positive, manually verify, and exclude from findings
- **Performance audit inconclusive**: run extended profiling and re-audit
- **Remediation introduces new violations**: revert the remediation, investigate the cause, and try a different fix approach