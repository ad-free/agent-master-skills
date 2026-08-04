---
name: agent-router
description: |
  Primary entry point for all agent work. Single bootstrap skill that maps user requests to the
  correct agent and skill chain. Use FIRST in every session — routes vague ideas, specs, bugs,
  features, reviews, and deployments to the right specialist. User-invoked only.
  
model: gpt-5-nano
version: 2.0.0
preamble-tier: 1
allowed-tools:
  - Read
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "start work"
  - "route this"
  - "what agent do I need"
  - "begin"
  - "plan this"
  - "review this"
  - "ship this"
  - "debug this"
  - "test this"
  - "spec this"
  - "save progress"
  - "resume"
  - "retro"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 2.1.0
  domain: planning-execution
  integrates-with: [prompt-optimizer, product-thinking, planning-and-task-breakdown, dev-craft, ui-craft, debugging-and-error-recovery, code-review-and-quality, ship, verification-before-completion, retro, learn, context-engineering, handoff, project-discovery, api-design, devops-automation, cost-optimizer, token-budget, qa-and-edge-case-tester, testing-strategies, bug-hunting, secops-and-vulnerability-scanner, grilling, architecture-decision-records, documentation-engineering]
  source-enhancements: v2.1.0 prompt-optimizer integration
---
TOKEN CEILING: ~3K tokens. If skill exceeds, extract sections to references/.

# Agent Router — Bootstrap Skill

**This is the entry point for ALL work.** Load this skill first. It maps your request to the right agent + skill chain.

**User-invoked only** (`disable-model-invocation: true`) — zero context cost until you need it.

---

## Routing Table

| Your Request | Agent | Skills Loaded | Entry Point |
|--------------|-------|---------------|-------------|
| "I have an idea for..." / vague feature | `planner` → `prompt-optimizer` → `product-thinking` → `planning-and-task-breakdown` → `dev-craft` | prompt-optimizer, product-thinking, planning-and-task-breakdown, dev-craft | `skill("prompt-optimizer")` |
| "Here's my requirements.xlsx" | `planner` → `prompt-optimizer` → `project-discovery` → `planning-and-task-breakdown` → `dev-craft` | prompt-optimizer, project-discovery, planning-and-task-breakdown, dev-craft | `skill("prompt-optimizer")` |
| "Build the auth API per PLAN.md" | `implementer` → `prompt-optimizer` → `dev-craft` | prompt-optimizer, dev-craft, testing-strategies, code-review-and-quality | `skill("prompt-optimizer")` |
| "Fix this failing test" | `debugger` → `prompt-optimizer` → `debugging-and-error-recovery` → `implementer` | prompt-optimizer, debugging-and-error-recovery, dev-craft, verification-before-completion | `skill("prompt-optimizer")` |
| "Review this PR" | `code-reviewer` → `prompt-optimizer` → `code-review-and-quality` → `verification-before-completion` | prompt-optimizer, code-review-and-quality, verification-before-completion | `skill("prompt-optimizer")` |
| "Security audit before launch" | `security-auditor` → `prompt-optimizer` → `bug-hunting` → `verification-before-completion` | prompt-optimizer, bug-hunting, code-review-and-quality, verification-before-completion | `skill("prompt-optimizer")` |
| "Design the API for webhooks" | `api-designer` → `prompt-optimizer` → `api-design` | prompt-optimizer, api-design, dev-craft (CONTRACT phase) | `skill("prompt-optimizer")` |
| "Set up CI/CD for microservices" | `devops-engineer` → `prompt-optimizer` → `devops-automation` | prompt-optimizer, devops-automation, dev-craft | `skill("prompt-optimizer")` |
| "Weekly retrospective" | `retro-analyst` → `prompt-optimizer` → `retro` → `learn` | prompt-optimizer, retro, learn, context-engineering | `skill("prompt-optimizer")` |
| "Ship this release" | `shipper` → `prompt-optimizer` → `ship` → `verification-before-completion` | prompt-optimizer, ship, verification-before-completion | `skill("prompt-optimizer")` |
| "Optimize LLM costs" | `planner` → `prompt-optimizer` → `cost-optimizer` | prompt-optimizer, cost-optimizer, token-budget | `skill("prompt-optimizer")` |
| "My context is full / rotate session" | `context-guard` → `prompt-optimizer` → `context-engineering` → `handoff` | prompt-optimizer, context-engineering, handoff, learn | `skill("prompt-optimizer")` |
| "What did we learn last sprint?" | `retro-analyst` → `prompt-optimizer` → `learn` | prompt-optimizer, learn, retro | `skill("prompt-optimizer")` |

---

## Comprehensive Routing Rules (from gstack)

### Product & Planning
- **New idea, brainstorming, "is this worth building", pitch a concept** → `/plan` (invokes `product-thinking` → `planning-and-task-breakdown`)
- **Spec something out, file an issue, write up a ticket, "turn this into a GitHub issue", "backlog item"** → `/spec` (invokes `project-discovery` → `product-thinking` → `planning-and-task-breakdown`)
- **Strategy, scope, ambition, "think bigger", "what should we build"** → `/plan` (invokes `grilling` → `architecture-decision-records`)
- **Architecture review, lock in the plan, "does this design make sense"** → `/review` (invokes `grilling` → `architecture-decision-records`)

### Development & Implementation
- **Build feature per PLAN.md** → `dev-craft` (or `ui-craft` for frontend)
- **Frontend/UI work, design system, component library** → `ui-craft`
- **API design, contract, OpenAPI, GraphQL schema** → `api-design` → `api-contract-designer`
- **Backend service, database, infrastructure** → `dev-craft` → `backend-patterns`, `database-migrations`
- **Mobile app, React Native, Expo** → `dev-craft` → `ui-craft` (mobile plugins)

### Debugging & Investigation
- **Bug, error, broken behavior, "why is this broken", "this doesn't work", "wtf", "something's wrong"** → `/investigate` (invokes `debugging-and-error-recovery` → `verification-before-completion`)
- **Failing test, build break, unexpected behavior** → `/investigate` (invokes `debugging-and-error-recovery`)
- **Performance issue, slow query, bottleneck** → `performance-profiler-and-tuner`

### Testing & Quality Assurance
- **Test the site, find bugs, QA, "does this work", "check the deploy"** → `/qa` (invokes `qa-and-edge-case-tester` → `testing-strategies` → `verification-before-completion`)
- **Just report bugs without fixing** → `qa-and-edge-case-tester` (analysis only)
- **Generate tests, edge cases, boundary testing** → `qa-and-edge-case-tester`
- **Visual regression, screenshot comparison** → `visual-regression`

### Code Review
- **Review code, check the diff, pre-landing review, "look at my changes"** → `/review` (invokes `code-review-and-quality` → `verification-before-completion`)
- **Security review, OWASP, vulnerabilities, "is this secure"** → `bug-hunting` → `secops-and-vulnerability-scanner`

### Deployment & Shipping
- **Ship, deploy, push, create a PR, "let's land this", "send it"** → `/ship` (invokes `ship` → `verification-before-completion` → `verification-before-completion`)
- **Merge + deploy + verify as one flow** → `ship` (with full pipeline)
- **Configure deployment for the project** → `devops-automation`
- **Monitor prod after shipping, post-deploy checks** → `observability-engineering`
- **Update docs after shipping** → `documentation-engineering`

### Context & Session Management
- **Save progress, checkpoint, "save my work"** → `/context-save` (invokes `context-compressor-and-pruner` → `learn` → `handoff`)
- **Resume, restore, "where was I", "continue work"** → `/context-restore` (invokes `context-engineering` → `handoff` → `learn`)
- **Weekly retro, what did we ship, "how'd we do", "sprint retro"** → `/retro` (invokes `retro` → `learn`)

### Documentation
- **Write docs from scratch, generate documentation, "document this feature/module"** → `documentation-engineering`
- **Update docs after shipping** → `documentation-engineering`

### Cost & Optimization
- **Optimize LLM costs, model routing, API budget, prompt caching** → `cost-optimizer` → `token-budget`

---

## Quick Start

```
You: "Build a payment integration with Stripe"
Agent: loads agent-router → runs prompt-optimizer → routes to planner
Planner: "I'll run prompt-optimizer on your request, then product-thinking to refine, then planning-and-task-breakdown, then dev-craft"
```

```
You: "Review PR #247"
Agent: loads agent-router → runs prompt-optimizer → routes to code-reviewer
Code Reviewer: "Running prompt-optimizer on the PR context, then code-review-and-quality with 8-axis review + pre-report gate"
```

```
You: "Debug the flaky login test"
Agent: loads agent-router → runs prompt-optimizer → routes to debugger
Debugger: "Running prompt-optimizer on the bug report, then debugging-and-error-recovery 4-phase investigation"
```

---

## If Unsure: Triage First

If the request doesn't cleanly match a row above, the **Triage Agent** classifies it:

```
triage → classifies → routes to correct agent
```

Categories: Bug | Feature | Refactor | Security | Performance | Docs | Chore | Design | Test

---

## Skill Chain Reference

Every agent declares its **Skill Chain** in its file. The router invokes the first skill; subsequent skills are loaded by the agent as needed.

**Prompt-optimizer runs first in EVERY chain** — it optimizes the user request before any agent processes it.

### Core Chains

**New Feature (vague):**
```
prompt-optimizer → product-thinking → planning-and-task-breakdown → grilling → dev-craft
  → (per slice) code-review-and-quality → verification-before-completion
  → verification-before-completion → ship → learn
```

**New Feature (with specs):**
```
prompt-optimizer → project-discovery → planning-and-task-breakdown → grilling → dev-craft
  → (per slice) ...
```

**Bug Fix:**
```
prompt-optimizer → debugging-and-error-recovery → implementer → verification-before-completion
```

**Code Review:**
```
prompt-optimizer → code-review-and-quality → verification-before-completion → verification-before-completion
```

**Security Audit:**
```
prompt-optimizer → bug-hunting → code-review-and-quality → verification-before-completion → verification-before-completion
```

**Deployment:**
```
prompt-optimizer → ship → verification-before-completion → verification-before-completion → learn
```

**Weekly Cadence:**
```
prompt-optimizer → retro → learn → (feeds into next week's product-thinking)
```

---

## Usage

**You type:** `/agent-router "Build a user dashboard with charts"`

**Router responds:**
```markdown
## ROUTING DECISION

**Request:** Build a user dashboard with charts
**Category:** Feature (Frontend-heavy)
**Primary Agent:** `frontend-engineer` (with `planner` for planning)
**Pipeline:** `ui-craft`

**Skill Chain:**
1. `skill("prompt-optimizer")` — optimize user request for clarity and structure
2. `skill("planning-and-task-breakdown")` — create PLAN.md
3. `skill("grilling")` — adversarial review
4. `skill("ui-craft")` — 10-phase frontend pipeline
   - Plugins: `design-intelligence`, `anti-slop`
5. `skill("code-review-and-quality")` — per slice
6. `skill("verification-before-completion")` — per slice
7. `skill("verification-before-completion")` — pre-merge
8. `skill("ship")` — release
9. `skill("learn")` — capture learnings

**Estimated:** 3-5 slices over 1-2 weeks

**Confirm?** Reply "yes" to start, or clarify scope.
```

---

## Integration

- **Invoked by:** User (explicit) or `triage` agent
- **First step:** `skill("prompt-optimizer")` — runs on ALL requests before routing
- **Loads:** First skill in chain (after prompt-optimizer)
- **State:** Creates `.dev-craft/runs/<slug>/state.json` with routing metadata
- **Context Guard:** Monitors token usage, triggers `handoff` if >60%
- **Cost Tracking:** Reports prompt-optimizer token savings to `cost-optimizer`