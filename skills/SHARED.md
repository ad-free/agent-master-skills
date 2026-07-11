# Shared Documentation for dev-craft and ui-craft

## Plugin System

Both dev-craft and ui-craft support a plugin system for extending functionality.

### Plugin Architecture

```
skills/
├── dev-craft/
│   ├── SKILL.md                    # Core pipeline
│   ├── plugins/                    # dev-craft plugins
│   │   ├── security-audit/
│   │   ├── database-migrations/
│   │   └── api-versioning/
│   ├── scripts/
│   └── references/
├── ui-craft/
│   ├── SKILL.md                    # Core pipeline
│   ├── plugins/                    # ui-craft plugins
│   │   ├── figma-sync/
│   │   ├── visual-regression/
│   │   └── design-system-validate/
│   ├── scripts/
│   └── references/
└── SHARED.md                       # This file
```

### Plugin Format

Each plugin is a directory with:

```
plugin-name/
├── SKILL.md              # Plugin instructions
├── scripts/              # Optional scripts
└── references/           # Optional reference docs
```

### Plugin Registration

Plugins are registered in `state.json`:

```json
{
  "plugins": ["security-audit", "figma-sync"],
  "pluginConfig": {
    "security-audit": { "severity": "high" },
    "figma-sync": { "fileKey": "abc123" }
  }
}
```

### Available Plugins

#### dev-craft Plugins

| Plugin | Description | Use Case |
|--------|-------------|----------|
| `security-audit` | Deep security scanning with STRIDE | Production deployments |
| `database-migrations` | Safe migration patterns | Schema changes |
| `api-versioning` | API version management | Public APIs |
| `performance-profiling` | Performance bottleneck detection | Optimization |
| `dependency-audit` | Dependency vulnerability scanning | Security |

#### ui-craft Plugins

| Plugin | Description | Use Case |
|--------|-------------|----------|
| `figma-sync` | Sync design tokens from Figma | Design-to-code |
| `visual-regression` | Playwright screenshot comparison | Visual testing |
| `design-system-validate` | Validate against design system | Consistency |
| `accessibility-deep` | WCAG 2.2 AAA compliance | Accessibility |
| `animation-craft` | Advanced animation patterns | Micro-interactions |

---

## Workflow Bundles

Pre-configured workflows for common project types.

### SaaS MVP Bundle

**Pipelines:** dev-craft + ui-craft
**Phases:** 12-16 slices
**Duration:** 2-4 sessions

```
Phase 1: DESIGN SYSTEM (ui-craft)
  ├── Design tokens (colors, typography, spacing)
  ├── Component library (shadcn/ui)
  └── HTML style guide preview

Phase 2: AUTH SYSTEM (dev-craft)
  ├── User model + migrations
  ├── Auth API (login, signup, reset)
  ├── JWT/session management
  └── Protected routes

Phase 3: CORE UI (ui-craft)
  ├── Login/signup pages
  ├── Dashboard layout
  ├── Navigation
  └── Settings page

Phase 4: CORE API (dev-craft)
  ├── CRUD endpoints
  ├── Data validation
  ├── Error handling
  └── Rate limiting

Phase 5: BILLING (dev-craft + ui-craft)
  ├── Stripe integration
  ├── Pricing page
  ├── Checkout flow
  └── Webhook handling

Phase 6: INTEGRATION (dev-craft)
  ├── E2E tests
  ├── Performance testing
  └── Security audit
```

### Admin Dashboard Bundle

**Pipelines:** ui-craft + dev-craft
**Phases:** 8-12 slices
**Duration:** 1-2 sessions

```
Phase 1: DESIGN SYSTEM (ui-craft)
  ├── Data-focused design tokens
  ├── Table/card components
  └── Dashboard layout

Phase 2: DATA API (dev-craft)
  ├── List/endpoints with pagination
  ├── Filter/search API
  └── Export endpoints

Phase 3: DASHBOARD UI (ui-craft)
  ├── Data tables with sorting
  ├── Charts/graphs
  ├── Filter panels
  └── Export UI

Phase 4: CRUD UI (ui-craft)
  ├── Create/edit modals
  ├── Form validation
  └── Bulk actions

Phase 5: INTEGRATION (dev-craft)
  ├── E2E tests
  └── Performance testing
```

### E-commerce Bundle

**Pipelines:** ui-craft + dev-craft
**Phases:** 14-18 slices
**Duration:** 3-4 sessions

```
Phase 1: DESIGN SYSTEM (ui-craft)
  ├── Product-focused design tokens
  ├── Product card components
  └── Storefront layout

Phase 2: PRODUCT API (dev-craft)
  ├── Product catalog API
  ├── Search/filter API
  └── Inventory management

Phase 3: STOREFRONT UI (ui-craft)
  ├── Product listing page
  ├── Product detail page
  ├── Search/filter UI
  └── Cart UI

Phase 4: CHECKOUT (dev-craft + ui-craft)
  ├── Cart API
  ├── Checkout flow
  ├── Payment integration
  └── Order confirmation

Phase 5: ORDER MANAGEMENT (dev-craft + ui-craft)
  ├── Order history API
  ├── Order detail page
  └── Admin order management

Phase 6: INTEGRATION (dev-craft)
  ├── E2E tests
  ├── Performance testing
  └── Security audit
```

### Landing Page Bundle

**Pipelines:** ui-craft only
**Phases:** 4-6 slices
**Duration:** 1 session

```
Phase 1: DESIGN SYSTEM (ui-craft)
  ├── Marketing-focused design tokens
  ├── Typography (bold headlines)
  └── Color palette

Phase 2: PAGE STRUCTURE (ui-craft)
  ├── Hero section
  ├── Features section
  ├── Testimonials section
  ├── Pricing section
  └── CTA section

Phase 3: FORMS (ui-craft)
  ├── Contact form
  ├── Newsletter signup
  └── Form validation

Phase 4: POLISH (ui-craft)
  ├── Responsive design
  ├── Animations
  ├── Dark mode
  └── Accessibility
```

---

## Cross-Skill Communication Protocol

### State File Schema

Both dev-craft and ui-craft use compatible `state.json` formats:

```json
{
  "currentPhase": 3,
  "completed": [0, 1, 2],
  "stack": {
    "react": "19.0.0",
    "tailwind": "4.0.0"
  },
  "slices": ["auth", "dashboard", "settings"],
  "currentSlice": 1,
  "plugins": ["security-audit"],
  "crossSkill": {
    "backendSliceNeeded": ["auth-api"],
    "apiContract": ".dev-craft/api-contract.md"
  }
}
```

### Handoff Document Format

When switching between pipelines, generate a handoff document:

```markdown
# Handoff: [Pipeline] → [Pipeline]

## Context
- Feature: User authentication
- Current state: Backend API complete
- Next: Frontend login UI

## API Contract
- POST /api/auth/login
- POST /api/auth/signup
- POST /api/auth/reset

## Design System
- Colors: .ui-craft/tokens/tokens.css
- Components: src/components/ui/

## Requirements
- Form validation with React Hook Form + Zod
- Error handling with toast notifications
- Loading states with skeleton UI
```

### Shared Glossary

Both pipelines share `context.md` for consistent terminology:

```markdown
# Glossary

- **User**: Authenticated person using the application
- **Session**: JWT token stored in httpOnly cookie
- **Dashboard**: Main landing page after login
- **Settings**: User profile and preferences page
```

---

## Best Practices

### Plugin Development

1. **Single responsibility** — One plugin, one concern
2. **Idempotent** — Running twice should not change results
3. **Configurable** — Accept config via `state.json`
4. **Documented** — Clear SKILL.md with examples
5. **Tested** — Include test cases in plugin

### Workflow Selection

1. **Start small** — Use the simplest workflow that fits
2. **Extend as needed** — Add phases/slices as scope grows
3. **Customize** — Modify workflows for your project's needs
4. **Document changes** — Track workflow customizations in ADRs

### Cross-Skill Coordination

1. **Design system first** — ui-craft creates tokens, dev-craft uses them
2. **API contract early** — dev-craft defines API, ui-craft consumes it
3. **Shared state** — Keep both pipelines' state files in sync
4. **Regular handoffs** — Switch pipelines at natural boundaries
5. **Unified testing** — Both pipelines contribute to E2E tests
