---
name: grilling
description: |
  Adversarial stress-test of plans and designs. "What could go wrong?" systematic probing.
  Use before finalizing any plan, architecture, or design. Outputs risk register with mitigations.
  (from mattpocock grilling skill)
model: nemotron-3-ultra-free
tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
preamble-tier: 2
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "grill this plan"
  - "stress test this design"
  - "what could go wrong"
  - "adversarial review"
metadata:
  origin: agent-master-skills
  source: mattpocock grilling skill
  output: risk-register.md
  preferred-model: nemotron-3-ultra-free
  integrates-with: [planning-and-task-breakdown, architecture-patterns, dev-craft]
---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Grilling — Adversarial Plan/Design Review

Grill the plan relentlessly. Find every hole before implementation starts. The goal is not to be negative — it's to make the plan bulletproof.

## When to Use

- **MANDATORY** after `planning-and-task-breakdown` produces PLAN.md
- Before any major architecture decision
- Before committing to external dependencies
- When stakes are high (payments, auth, data migration, security)

## The Grilling Process

### Phase 1: Assumption Excavation

List every implicit assumption in the plan. For each:
- Is it documented?
- What happens if it's wrong?
- How would we know it's wrong?

```markdown
## Assumptions Found

| Assumption | Documented? | If Wrong → Impact | Detection |
|------------|-------------|-------------------|-----------|
| Stripe API v2024-06-20 stable | ❌ | Breaking changes → payment failures | Monitor Stripe changelog |
| PostgreSQL 16 supports feature X | ✅ (ADR-042) | Migration blocked | Test in staging |
| Team knows React Query v5 | ❌ | Slow implementation | Pair programming needed |
```

### Phase 2: Failure Mode Enumeration

For each slice/task in the plan, ask: **"How could this fail?"**

Categories:
1. **Technical** — bugs, performance, scalability, compatibility
2. **Operational** — deploy failures, rollback issues, monitoring gaps
3. **Security** — auth bypass, data leakage, injection, supply chain
3. **Product** — wrong UX, missed requirements, scope creep
4. **Team** — knowledge gaps, bus factor, review bottlenecks
5. **External** — API changes, vendor outages, dependency conflicts

```markdown
## Failure Modes by Slice

### Slice 1: Auth API
| Failure Mode | Likelihood | Impact | Detection | Mitigation |
|--------------|------------|--------|-----------|------------|
| JWT secret rotation breaks existing sessions | Medium | High (all users logged out) | Integration test | Graceful rotation with overlap period |
| Rate limiter blocks legitimate users | Low | Medium | Load test | Allow-list for known IPs |
| Password reset token leak via logs | Low | Critical | Code review + log audit | Never log tokens, use hashed storage |

### Slice 2: Payment Processing
| Failure Mode | Likelihood | Impact | Detection | Mitigation |
|--------------|------------|--------|-----------|------------|
| Stripe webhook duplicate processing | High | Critical (double charge) | Idempotency key test | Sort events by created, deduplicate |
| Network timeout during charge | Medium | High | Chaos test | Idempotency + retry with backoff |
| Currency rounding errors | Low | Medium | Property-based test | Use integer cents, banker's rounding |
```

### Phase 3: Dependency Risk Map

```
Plan Dependencies (External)
├── Stripe API
│   ├── Risk: Version deprecation (12-month notice)
│   ├── Mitigation: Pin version, monitor changelog
│   └── Contingency: 3-month migration buffer
├── PostgreSQL 16
│   ├── Risk: Managed service delay (RDS, Cloud SQL)
│   └── Mitigation: Test on Docker locally, abstract via ORM
├── React Query v5
│   ├── Risk: Team unfamiliarity
│   └── Mitigation: Internal workshop, pair programming
└── Terraform AWS Provider v5
    ├── Risk: Breaking changes
    └── Mitigation: Pin provider version in .terraform.lock.hcl
```

### Phase 4: Pre-Mortem

"Imagine it's 3 months post-launch. The project failed catastrophically. What happened?"

Generate 5-7 specific disaster scenarios. For each, trace back to a decision point in the plan.

```markdown
## Pre-Mortem Scenarios

1. **Payment data breach** → Root cause: Logged full Stripe event objects including card tokens
   - Plan gap: No log sanitization review in HARDEN phase
   - Fix: Add `bug-hunting` skill to review logging

2. **Auth system down for 4 hours** → Root cause: Single-point-of-failure in token validation service
   - Plan gap: No HA architecture review in DESIGN phase
   - Fix: Add `architecture-patterns` skill to DESIGN

3. **Mobile app crashes on iOS 18** → Root cause: Deprecated API used in networking layer
   - Plan gap: No mobile compatibility matrix
   - Fix: Add platform testing to TEST phase
```

### Phase 5: Risk Register Output

Consolidate into a risk register with owners and mitigations.

```markdown
# Risk Register: <Feature Name>

| ID | Risk | Likelihood | Impact | Score | Owner | Mitigation | Status |
|----|------|------------|--------|-------|-------|------------|--------|
| R-01 | Stripe webhook duplicate charges | High | Critical | 9 | Backend lead | Idempotency keys + event sorting | MITIGATED |
| R-02 | JWT rotation breaks sessions | Medium | High | 6 | Backend lead | Graceful rotation overlap | IN_PROGRESS |
| R-03 | Team unfamiliar with React Query v5 | High | Medium | 6 | Tech lead | Workshop + pairing | PLANNED |
| R-04 | PostgreSQL 16 not on RDS at launch | Low | High | 5 | DevOps | Test on Docker, ORM abstraction | ACCEPTED |
| R-05 | Mobile push notifications fail on iOS 18 | Medium | Medium | 6 | Mobile lead | Beta testing program | PLANNED |

**Score = Likelihood (1-3) × Impact (1-3) × Detectability (1-3)**

## Go/No-Go Decision

- [ ] All CRITICAL (score ≥8) risks have MITIGATED status
- [ ] All HIGH (score 6-7) risks have owner + mitigation plan
- [ ] Team acknowledges ACCEPTED risks
- [ ] Go/No-Go meeting scheduled with stakeholders
```

---

## Outputs / Handoffs

On completion, invokes: `skill("dev-craft")` with context:
  - `planPath`: "PLAN.md"
  - `riskRegisterPath`: "risk-register.md"
  - `grillingRisks`: [...]

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Wrong | Correction |
|--------------|----------------|------------|
| "This is too simple to need grilling" | Simple things have hidden complexity | Grill everything; scale depth to risk |
| "We'll handle it in code review" | Code review is too late for architecture | Grill at PLAN phase |
| "Let's just start and fix issues" | Reactive fixes cost 10x more | Proactive risk mitigation |
| Only looking at happy path | Failures happen on sad paths | Enumerate failure modes explicitly |
| Grilling becomes "nitpicking" | Focus on existential risks, not style | Use failure mode categories |