---
name: product-thinking
description: |
  Transform vague ideas into structured product specifications through 4-round refinement.
  Use when input is vague, incomplete, or "I have an idea..." — before planning.
  Invoked by: triage, planner.
  
model: nemotron-3-ultra-free
version: 2.0.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "I have an idea"
  - "vague requirements"
  - "help me plan this product"
  - "refine this concept"
  - "create a spec from idea"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.0.0
  domain: product-discovery
  integrates-with: [planning-and-task-breakdown, project-discovery]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Product Thinking — Idea Refinement Engine

## Overview

Turns vague scraps into a structured, actionable specification — progressive refinement through 4 rounds of narrowing.

---

## When to Activate

Load this skill when **any** of these are true:

| Signal | Example |
|--------|---------|
| Prompt is short or vague | "Build me a CRM" |
| User says "I have an idea..." | "I have an idea for a platform" |
| Key details are missing | No users, no workflow, no scope |
| Before `planning-and-task-breakdown` | You sense the spec isn't solid enough to plan |
| User says "something like X but for Y" | "Like Airbnb but for boat rentals" |
| Non-technical stakeholder input | "We need a system to manage stuff" |
| Ambiguous success criteria | "Make it better" or "Modernize it" |

**When NOT to use:** Spec is already detailed, user stories exist, wireframes are attached, or the request is a well-defined feature in an existing codebase.

---

## Core Process — Four-Round Refinement

Each round has a clear goal, output artifact, and user checkpoint before proceeding.

```
Round 1 ──→ Round 2 ──→ Round 3 ──→ Round 4
Domain &      Scope       Feature     Priority &
Problem     Triangulation Extraction  Sequencing
```

### Round 1: Domain & Problem

**Goal:** Identify what kind of system this is, who it serves, and what core problem it solves.

**Process:**

1. **Domain identification** — Detect from keywords. If ambiguous, ask one clarifying question.
2. **User identification** — List the distinct user roles that interact with the system.
3. **Problem statement** — Write a single-sentence problem statement: "X needs a way to Y because Z."
4. **Existing context** — Is this greenfield? Replacing an existing system? An idea stage?

**Output:** Section 1 of PRODUCT.md (Domain, Users, Problem Statement)

**User checkpoint:** "Here's what I understand so far about the domain and problem. Does this align with your vision?"

### Round 2: Scope Triangulation

**Goal:** Define the module structure that maps to the domain. Establish hard boundaries.

**Process:**

1. **Suggest module structure** — Based on the detected domain template (see Domain Templates below), propose a list of modules. Each module is a coherent group of features.
2. **Verify with user** — "Here are the modules I think we need. Are there any I'm missing? Any that don't belong?"
3. **Mark In/Out** — Explicitly list what's in scope and what's out of scope. This is the single most important de-risking step.
4. **Identify integration points** — Does this system need to talk to external services (payment gateways, email, SMS, calendar APIs)?

**Scope Rules:**
- If a module is optional, mark it `[OPTIONAL]`
- If out of scope but likely needed later, mark it `[FUTURE]`
- Be brutal about out-of-scope — vague scope is the #1 cause of failed projects

**Output:** Section 2 of PRODUCT.md (Module List with In/Out boundaries)

**User checkpoint:** "Are these the right modules? Anything you'd add or remove?"

### Round 3: Feature Extraction

**Goal:** For each module, enumerate concrete features with user stories and acceptance criteria.

**Process:**

1. **Per-module feature brainstorm** — For each module from Round 2, identify 3–10 concrete features.
2. **User stories** — For key features, write a user story: "As a [role], I want to [action] so that [benefit]."
3. **Acceptance criteria** — For complex features, add 1–3 conditions of satisfaction.
4. **Examples & edge cases** — Note specific examples ("A manager can approve leave requests up to 5 days; >5 days needs director approval").
5. **UI hints** — Optionally note if a feature is list/etc.

**Output:** Section 3 of PRODUCT.md (Features per Module, with User Stories)

**User checkpoint:** "These are the features I've identified for each module. Does this capture what you need?"

### Round 4: Priority & Sequencing

**Goal:** Determine what gets built first and what dependencies exist between modules.

**Process:**

1. **Assign priority tiers:**

   | Tier | Label | Definition |
   |------|-------|------------|
   | G1 | Core/Foundation | Required for MVP. Nothing ships without this. |
   | G2 | Important | High value but can wait for v1.1 or v2. |
   | G3 | Nice-to-have | Polish, analytics, advanced features. Future. |

2. **Identify dependencies** — Module A needs Module B to function. Capture as: `Auth ← All modules`, `Orders ← Products`.

3. **Suggest a build sequence** — Recommend which modules to tackle first, second, third based on priorities and dependencies.

4. **Estimate complexity** — Rough: Small / Medium / Large per module (purely directional, not a commitment).

**Output:** Section 4 of PRODUCT.md (Priority, Dependencies, Build Sequence)

**User checkpoint:** "Here's my recommended build order and priorities. Does this feel right?"

## Domain Detection Heuristics

When the user gives keywords, map them to a domain template. If keywords span multiple domains, ask which is primary.

| Keywords | Likely Domain | Primary Entity |
|----------|---------------|----------------|
| employees, payroll, attendance, hiring, onboarding, performance review, leave, timesheet | **HRM** | Employee |
| leads, deals, pipeline, contacts, accounts, opportunities, territory, quota | **CRM** | Contact/Lead |
| products, cart, checkout, orders, inventory, shipping, returns, reviews | **E-commerce** | Product |
| purchase order, vendor, procurement, warehouse, BOM, production, work order | **ERP** | Inventory Item |
| users, organizations, teams, billing, subscription, roles, permissions, API keys | **SaaS** | Account |
| patients, appointments, prescriptions, billing, insurance, charts, lab results | **Healthcare** | Patient |
| courses, lessons, students, enrollment, grades, assessments, certificates | **EdTech** | Course/Student |
| transactions, accounts, budgets, invoices, expenses, reconciliation, reports | **Fintech** | Transaction |
| bookings, reservations, inventory, pricing, availability, calendar, reviews | **Logistics/Hospitality** | Booking |
| articles, pages, media, categories, tags, authors, publishing, SEO | **CMS** | Content Item |

**If no match:** Ask the user to describe the primary entity in their system. That usually reveals the domain.

**Ambiguity rule:** If keywords could match 2+ domains (e.g., "users, payments, courses"), ask: "I see elements of both EdTech and Fintech — which is the primary domain? Or is this one platform with both?"

---

## Domain Templates

Reference skeletons. Adapt, don't copy blindly.

| Template | Modules | Primary Actors |
|----------|---------|---------------|
| HRM | Employee Mgmt, Attendance, Leave, Payroll, Recruitment, Performance, Training | Employee, Manager, HR Admin, Payroll Specialist |
| CRM | Contact, Lead, Opportunity, Quote, Contract, Marketing, Support, Reports | Sales Rep, Manager, Marketer, Support Agent, Admin |
| E-commerce | Catalog, Cart, Checkout, Orders, Accounts, Reviews, Shipping, Inventory | Shopper, Customer Service, Warehouse Op, Admin |
| ERP | Purchase, Inventory, BOM, Production, Accounting, Fixed Assets, HR | Procurement, Warehouse Mgr, Planner, Accountant, Admin |
| SaaS | Auth, Org Mgmt, User Mgmt, Billing, Feature Flags, API Keys, Analytics, Notifications | End User, Org Admin, Super Admin, Developer |
| Fintech | Account Mgmt, Transactions, Budgeting, Invoicing, Expenses, Reports, Integrations | Individual User, Business User, Accountant, Admin |
| Healthcare | Patient Mgmt, Appointments, EHR, Prescriptions, Billing, Lab, Telehealth | Patient, Doctor, Nurse, Admin, Billing Specialist |

---

## Output Format — PRODUCT.md

The skill MUST produce `PRODUCT.md` (project root or user-specified location). See `references/PRODUCT.md` for the full template.

---

## When to Hand Off

Hand off when ALL of these are true:

1. **PRODUCT.md is complete** — All 6 sections are populated
2. **User has confirmed** — "Yes, this looks right" or equivalent
3. **Spec is stable** — No major open questions that block planning

**Handoff artifact:** Pass the `PRODUCT.md` file path and a summary of the domain, key modules, and build sequence.

**Handoff message template:**
```
Product spec is ready at [path/PRODUCT.md].

Domain: [domain]
Modules: [module list — N modules]
Primary users: [roles]
Suggested build: [Phase 1 → Phase 2 → Phase 3]
Open questions: [count] — documented in spec

Ready for [planning-and-task-breakdown / dev-craft].
```

---

## Guidelines

### Interaction Principles

1. **One question at a time.** Never dump a list of 10 questions. Ask 1–2, get answers, then proceed.
2. **Verify assumptions out loud.** "I'm assuming this is a B2B SaaS because you mentioned organizations and billing. Is that right?"
3. **Be explicit about what's out of scope.** Undefined boundaries are the #1 source of scope creep. Write it down.
4. **Use concrete examples.** "When you say 'approval workflow', do you mean a manager sees a pending item and clicks approve/reject, or is there a multi-step chain?"
5. **Suggest, don't dictate.** "A typical CRM has these modules..." not "You need these modules."
6. **Match user vocabulary.** If the user says "workers" instead of "employees", use "workers" in the spec unless they agree to standardize.
7. **Document decisions.** When the user makes a call, capture it in PRODUCT.md immediately.

### Question Quality

| Avoid | Prefer |
|-------|--------|
| "What features do you want?" | "Let's start with your users — who will use this system?" |
| "Tell me everything about your idea" | "What's the one problem you need to solve first?" |
| "How should it work?" | "Do users create content, or just consume it?" |
| "What tech stack?" | "Let's nail the requirements first, tech comes later." |

---

## Gotchas

See `Interaction Principles` and `Question Quality` above for anti-patterns.

### Red Flags

Watch for these signals that the spec needs more refinement:

- User says "I'll know it when I see it" — means unclear vision, need wireframes or references
- User says "All of it" — means no priority, need to force trade-offs
- User gives contradictory answers — means the idea is still forming, document both and flag
- User can't name primary users — means the problem isn't well understood
- "Just like X but better" — need concrete differentiators documented

---

## Integration with Other Skills

```
User says "I have an idea" or vague prompt
    │
    ▼
┌─────────────────────────────────────────────────┐
│  product-thinking (THIS SKILL)                   │
│  Output: PRODUCT.md                              │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│  planning-and-task-breakdown                     │
│  Input: PRODUCT.md                               │
│  Output: Task list with acceptance criteria      │
│  Invoke: skill(name="planning-and-task-breakdown")│
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│  dev-craft or ui-craft                           │
│  Input: Task list + PRODUCT.md                   │
│  Output: Working code                            │
│  Invoke: skill(name="dev-craft")                 │
└─────────────────────────────────────────────────┘
```

### When to Skip product-thinking

| Scenario | Go Directly To |
|----------|---------------|
| Bug fix with clear reproduction steps | `debugging-and-error-recovery` |
| Well-documented feature request | `planning-and-task-breakdown` |
| Screenshot with visible changes | `image-to-design-spec` → `ui-craft` |
| Security audit request | `bug-hunting` |
| Single-file change with obvious scope | Direct implementation |

## Example Walkthrough

**User says:** "I want to build something like Upwork but for graphic designers."

| Round | Key Output |
|-------|-----------|
| 1 Domain & Problem | Marketplace / Freelance Platform. Users: Client, Designer, Admin. Problem: Designers need curated clients without race-to-bottom pricing; clients need vetted designers. |
| 2 Scope Triangulation | Modules: Profiles, Job Listings, Proposals, Contracts, Payments, Reviews, Messaging, Admin Dashboard. Out: time tracking, design tools, escrow (future). |
| 3 Feature Extraction | Job Listings → "As a client, I want to post a job with budget/deliverables so designers can apply." AC: requires title, desc, budget, category; auto-post or admin approval. Proposals → "As a designer, I want to submit a proposal with rate and portfolio so clients can evaluate me." |
| 4 Priority & Sequencing | G1: Auth, Profiles, Listings, Proposals. G2: Contracts, Payments, Messaging. G3: Reviews, Analytics, Escrow. Dependencies: Payments ← Contracts ← Proposals ← Profiles ← Auth |

**Handoff:** PRODUCT.md → `planning-and-task-breakdown`