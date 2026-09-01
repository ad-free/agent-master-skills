---
name: ui-pattern-extractor
description: "Use when you need to understand existing UI patterns, design tokens, component conventions, and responsive behavior BEFORE writing any UI code. Mandatory pre-flight for all UI work on existing codebases. Prevents wrong buttons, inconsistent styles, broken responsive layout by extracting what exists first."
model: big-pickle
version: 1.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
triggers:
  - "build this UI component"
  - "add a button"
  - "style this"
  - "make it look like"
  - "create a form"
  - "add responsive"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 1.0.0
  domain: frontend
  integrates-with: [ui-craft, ui-component-builder, image-to-code]
---

# UI Pattern Extractor — Understand Before You Write

**Agent often creates wrong buttons, inconsistent styles, broken responsive layouts because it writes code WITHOUT understanding what already exists.**

This skill runs MANDATORY before any UI work on existing codebases. It extracts exactly how the codebase works so new code matches perfectly.

---

## 1. WHY THIS SKILL EXISTS

Common failures without pattern extraction:

| Failure | Root Cause | This Skill Prevents |
|---------|-----------|---------------------|
| Wrong button style | Agent guesses instead of reading existing Button component | Extract existing Button props, variants, styles |
| Inconsistent spacing | Agent uses 8px gap, codebase uses 12px | Extract spacing tokens from CSS/config |
| Broken responsive | Agent uses wrong breakpoints | Extract actual breakpoints in use |
| Wrong color | Agent picks random blue, codebase has specific primary | Extract color tokens/variables |
| Wrong font size | Agent uses 14px, codebase standard is 13px | Extract typography scale |
| Doesn't match existing | Agent creates new pattern, not extends existing | Extract component naming/structure |

---

## 2. MANDATORY PRE-FLIGHT CHECKLIST

Before writing ANY UI code, run this checklist:

```
- [ ] Framework detected (React/Vue/Svelte/vanilla)
- [ ] CSS approach identified (Tailwind/CSS Modules/Styled Components/etc)
- [ ] Component library identified (shadcn/radix/antd/custom)
- [ ] Existing button/link/card/input components found
- [ ] Design tokens extracted (colors, spacing, typography, radii, shadows)
- [ ] Responsive breakpoints extracted
- [ ] Naming conventions identified (PascalCase/kebab-case)
- [ ] Dark mode approach identified (if any)
```

**If any item is unchecked → DO NOT WRITE CODE. Extract it first.**

---

## 3. EXTRACTION WORKFLOW

### Step 1: Framework & Styling Detection

```bash
# Detect framework
cat package.json | grep -E '"react"|"vue"|"svelte"|"angular"|"next"|"nuxt"'

# Detect CSS approach
cat package.json | grep -E '"tailwind"|"styled-components"|"emotion"|"vanilla-extract"|"css-modules"'
find src -name "*.module.css" -o -name "*.module.scss" | head -3
find src -name "tailwind.config.*" | head -1

# Detect component library
cat package.json | grep -E '"shadcn"|"@radix-ui"|"@headlessui"|"antd"|"@mantine"|"@chakra-ui"'
ls src/components/ui/ 2>/dev/null | head -10
```

**Output:**
```
Framework: React 19
CSS: Tailwind CSS v4
Components: shadcn/ui (new-york style)
```

### Step 2: Extract Existing Components

```bash
# Find component files
find src/components -name "*.tsx" -o -name "*.jsx" | head -20

# Find specific components (buttons, inputs, cards)
find src -name "*button*" -o -name "*Button*" | head -5
find src -name "*input*" -o -name "*Input*" | head -5
find src -name "*card*" -o -name "*Card*" | head -5

# Check for shared/common components
ls src/components/ui/ 2>/dev/null
ls src/components/common/ 2>/dev/null
ls src/components/shared/ 2>/dev/null
```

**Read 2-3 existing components to understand patterns:**
- How are props typed?
- How are variants handled?
- How is className composed?
- How are icons integrated?

### Step 3: Extract Design Tokens

```bash
# Tailwind v4 (CSS-first)
cat src/app/globals.css 2>/dev/null | grep -E "@theme|:root|--" | head -20

# Tailwind v3 (JS config)
cat tailwind.config.ts 2>/dev/null | head -50
cat tailwind.config.js 2>/dev/null | head -50

# CSS variables
find src -name "*.css" -exec grep -l ":root" {} \; | head -3
cat src/app/globals.css 2>/dev/null | grep -E "hsl|rgb|--" | head -30
```

**Extract these tokens:**

```markdown
## Colors
- Primary: [value]
- Secondary: [value]
- Background: [value]
- Foreground: [value]
- Muted: [value]
- Border: [value]

## Spacing
- xs: [value]
- sm: [value]
- md: [value]
- lg: [value]
- xl: [value]

## Typography
- Font family: [value]
- Font sizes: [list with values]
- Font weights: [list]
- Line heights: [list]

## Border Radius
- sm: [value]
- md: [value]
- lg: [value]
- full: [value]

## Shadows
- sm: [value]
- md: [value]
- lg: [value]
```

### Step 4: Extract Responsive Breakpoints

```bash
# Check tailwind config for breakpoints
cat tailwind.config.ts 2>/dev/null | grep -A 20 "screens:"
cat tailwind.config.js 2>/dev/null | grep -A 20 "screens:"

# Check CSS for breakpoints
grep -r "@media" src/ --include="*.css" --include="*.scss" | head -10

# Check for breakpoint utilities in use
grep -r "sm:\|md:\|lg:\|xl:\|2xl:" src/ --include="*.tsx" --include="*.jsx" | head -10
```

**Extract breakpoints:**
```
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

### Step 5: Extract Component Patterns

**Read 2-3 existing components and document:**

```markdown
## Button Pattern (from src/components/ui/button.tsx)
- Variants: default, destructive, outline, secondary, ghost, link
- Sizes: default, sm, lg, icon
- Uses: cva for variants, cn() for className
- Props: variant, size, className, asChild

## Input Pattern (from src/components/ui/input.tsx)
- Variants: default, file
- Props: type, className

## Card Pattern (from src/components/ui/card.tsx)
- Parts: Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter
- Pattern: Compound components with context
```

### Step 6: Extract Naming Conventions

```bash
# Check naming patterns
ls src/components/ | head -20
ls src/components/ui/ | head -20
ls src/components/ | grep -E "^[a-z]" | head -10
ls src/components/ | grep -E "^[A-Z]" | head -10
```

**Document:**
```
Component names: PascalCase (Button, Card, Input)
File names: kebab-case (button.tsx, card.tsx)
Utility names: camelCase (cn, formatDate)
```

---

## 4. OUTPUT: ui-patterns.md

After extraction, save to `.ui-craft/ui-patterns.md` (or `patterns.md` in project root):

```markdown
# UI Patterns - [Project Name]

## Framework & Stack
- Framework: React 19
- CSS: Tailwind CSS v4
- Components: shadcn/ui
- TypeScript: 5.x

## Design Tokens

### Colors
[extracted values]

### Spacing
[extracted values]

### Typography
[extracted values]

### Border Radius
[extracted values]

### Shadows
[extracted values]

## Responsive Breakpoints
[extracted values]

## Existing Components

### Button
[extracted pattern]

### Input
[extracted pattern]

### Card
[extracted pattern]

## Naming Conventions
[extracted patterns]

## Dark Mode (if exists)
[extracted approach]
```

---

## 5. USING EXTRACTED PATTERNS

When writing new UI code, reference the extracted patterns:

```markdown
## DO THIS (follow extracted patterns):
- Use extracted Button component, not create new one
- Use extracted color tokens, not hardcoded values
- Use extracted spacing tokens, not random values
- Use extracted breakpoints, not invented ones
- Follow extracted naming conventions

## DON'T DO THIS (ignoring patterns):
- Create new Button when existing one exists
- Use #3b82f6 when primary token is defined
- Use 8px gap when spacing scale starts at 4px
- Use 768px breakpoint when codebase uses 768px via Tailwind md:
- Use camelCase filenames when codebase uses kebab-case
```

---

## 6. VERIFICATION CHECKLIST

After writing UI code, verify against extracted patterns:

```
- [ ] Used existing components (not created new ones unnecessarily)
- [ ] Used design tokens (not hardcoded values)
- [ ] Used correct responsive breakpoints
- [ ] Followed naming conventions
- [ ] Matched existing component structure
- [ ] Tested at extracted breakpoints (sm/md/lg/xl)
- [ ] Dark mode works (if applicable)
```

---

## 7. INTEGRATION WITH PIPELINE

### In ui-craft:
```
Phase 0: LOAD
Phase 1: AUDIT
Phase 1.5: TECH-ADVISOR (research alternatives)
Phase 1.75: UI-PATTERN-EXTRACTOR ← ADD HERE
  - Extract existing patterns
  - Save to ui-patterns.md
Phase 2: ALIGN (reference extracted patterns)
Phase 3: DESIGN (use extracted tokens)
...
```

### In ui-component-builder:
```
Before building any component:
1. Load ui-patterns.md (or extract if not exists)
2. Check if similar component exists
3. If exists → extend/modify, don't create new
4. If not exists → create following extracted patterns
```

---

## 8. QUICK REFERENCE

### Before writing UI, always:

1. **Check:** Does this component already exist?
2. **Extract:** What tokens/patterns does the codebase use?
3. **Follow:** Match existing patterns exactly
4. **Verify:** Test at extracted breakpoints

### Common mistakes to avoid:

| Mistake | Correct Approach |
|---------|-----------------|
| Create new Button | Use existing Button, add variant if needed |
| Hardcode #3b82f6 | Use primary color token |
| Use 8px gap | Use spacing token (usually 2 = 8px) |
| Use 768px directly | Use md: breakpoint |
| Use camelCase files | Follow existing kebab-case convention |

---

## 9. RULES

1. **NEVER skip pattern extraction** — even if you "think" you know Tailwind
2. **ALWAYS read existing components first** — before creating new ones
3. **ALWAYS use design tokens** — never hardcode colors/spacing/typography
4. **ALWAYS follow naming conventions** — match existing file/component names
5. **ALWAYS test at breakpoints** — verify responsive at sm/md/lg/xl
6. **NEVER create new component if similar exists** — extend, don't duplicate
7. **ALWAYS save extracted patterns** — to ui-patterns.md for reuse
8. **ALWAYS reference patterns when coding** — open ui-patterns.md in context

---

## 10. EXAMPLE SCENARIO

**User:** "Add a submit button to the form"

**Wrong approach (without this skill):**
```tsx
// Agent creates random button with wrong style
<button className="bg-blue-500 text-white px-4 py-2 rounded">
  Submit
</button>
```

**Correct approach (with this skill):**
```tsx
// 1. Extract patterns first
// Found: src/components/ui/button.tsx
// - Uses cva for variants
// - Has 'default' variant with primary colors
// - Uses cn() for className composition

// 2. Use extracted pattern
import { Button } from "@/components/ui/button"

// 3. Follow existing patterns
<Button type="submit">Submit</Button>
```

**Result:** Button matches existing style, uses correct tokens, follows patterns.
