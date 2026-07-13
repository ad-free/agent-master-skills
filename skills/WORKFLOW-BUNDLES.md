# Workflow Bundles

Pre-configured workflows for common project types.

## SaaS MVP Bundle

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

## Admin Dashboard Bundle

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

## E-commerce Bundle

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

## Landing Page Bundle

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

## Workflow Selection

1. **Start small** — Use the simplest workflow that fits
2. **Extend as needed** — Add phases/slices as scope grows
3. **Customize** — Modify workflows for your project's needs
4. **Document changes** — Track workflow customizations in ADRs
