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
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 2.0.0
  domain: planning-execution
  integrates-with: [product-thinking, planning-and-task-breakdown, dev-craft, ui-craft]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# Agent Router — Bootstrap Skill

**This is the entry point for ALL work.** Load this skill first. It maps your request to the right agent + skill chain.

**User-invoked only** (`disable-model-invocation: true`) — zero context cost until you need it.

---

## Routing Table

| Your Request | Agent | Skills Loaded | Entry Point |
|--------------|-------|---------------|-------------|
| "I have an idea for..." / vague feature | `planner` → `product-thinking` → `planning-and-task-breakdown` → `dev-craft` | product-thinking, planning-and-task-breakdown, dev-craft | `skill("product-thinking")` |
| "Here's my requirements.xlsx" | `planner` → `project-discovery` → `planning-and-task-breakdown` → `dev-craft` | project-discovery, planning-and-task-breakdown, dev-craft | `skill("project-discovery")` |
| "Build the auth API per PLAN.md" | `implementer` → `dev-craft` | dev-craft, testing-strategies, code-review-and-quality | `skill("dev-craft")` |
| "Fix this failing test" | `debugger` → `debugging-and-error-recovery` → `implementer` | debugging-and-error-recovery, dev-craft, verification-before-completion | `skill("debugging-and-error-recovery")` |
| "Review this PR" | `code-reviewer` → `code-review-and-quality` → `quality-gates` | code-review-and-quality, quality-gates, verification-before-completion | `skill("code-review-and-quality")` |
| "Security audit before launch" | `security-auditor` → `bug-hunting` → `quality-gates` | bug-hunting, code-review-and-quality, quality-gates | `skill("bug-hunting")` |
| "Design the API for webhooks" | `api-designer` → `api-design` | api-design, dev-craft (CONTRACT phase) | `skill("api-design")` |
| "Set up CI/CD for microservices" | `devops-engineer` → `devops-automation` | devops-automation, dev-craft | `skill("devops-automation")` |
| "Weekly retrospective" | `retro-analyst` → `retro` → `learn` | retro, learn, context-engineering | `skill("retro")` |
| "Ship this release" | `shipper` → `ship` → `verification-before-completion` | ship, verification-before-completion, quality-gates | `skill("ship")` |
| "Optimize LLM costs" | `planner` → `cost-optimizer` | cost-optimizer, token-budget | `skill("cost-optimizer")` |
| "My context is full / rotate session" | `context-guard` → `context-engineering` → `handoff` | context-engineering, handoff, learn | `skill("context-engineering")` |
| "What did we learn last sprint?" | `retro-analyst` → `learn` | learn, retro | `skill("learn")` |

---

## Quick Start

```
You: "Build a payment integration with Stripe"
Agent: loads agent-router → routes to planner
Planner: "I'll run product-thinking to refine, then planning-and-task-breakdown, then dev-craft"
```

```
You: "Review PR #247"
Agent: loads agent-router → routes to code-reviewer
Code Reviewer: "Running code-review-and-quality with 8-axis review + pre-report gate"
```

```
You: "Debug the flaky login test"
Agent: loads agent-router → routes to debugger
Debugger: "Running debugging-and-error-recovery 4-phase investigation"
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

### Core Chains

**New Feature (vague):**
```
product-thinking → planning-and-task-breakdown → grilling → dev-craft
  → (per slice) code-review-and-quality → verification-before-completion
  → quality-gates → ship → learn
```

**New Feature (with specs):**
```
project-discovery → planning-and-task-breakdown → grilling → dev-craft
  → (per slice) ...
```

**Bug Fix:**
```
debugging-and-error-recovery → implementer → verification-before-completion
```

**Code Review:**
```
code-review-and-quality → quality-gates → verification-before-completion
```

**Security Audit:**
```
bug-hunting → code-review-and-quality → quality-gates → verification-before-completion
```

**Deployment:**
```
ship → verification-before-completion → quality-gates → learn
```

**Weekly Cadence:**
```
retro → learn → (feeds into next week's product-thinking)
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
1. `skill("planning-and-task-breakdown")` — create PLAN.md
2. `skill("grilling")` — adversarial review
3. `skill("ui-craft")` — 10-phase frontend pipeline
   - Plugins: `design-intelligence`, `anti-slop`
4. `skill("code-review-and-quality")` — per slice
5. `skill("verification-before-completion")` — per slice
6. `skill("quality-gates")` — pre-merge
7. `skill("ship")` — release
8. `skill("learn")` — capture learnings

**Estimated:** 3-5 slices over 1-2 weeks

**Confirm?** Reply "yes" to start, or clarify scope.
```

---

## Integration

- **Invoked by:** User (explicit) or `triage` agent
- **Loads:** First skill in chain
- **State:** Creates `.dev-craft/runs/<slug>/state.json` with routing metadata
- **Context Guard:** Monitors token usage, triggers `handoff` if >60%