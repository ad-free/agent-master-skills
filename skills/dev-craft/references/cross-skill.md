# Cross-Skill Workflow Orchestration

Driven by dev-craft SCOPE gate (§0.2). The contract artifact is ALWAYS named
**`api-contract.md`** and lives at repo root or `docs/`.

## Workflow Types

| Workflow | Pipeline | When |
|----------|----------|------|
| SaaS MVP | product-thinking → planning-and-task-breakdown → dev-craft + ui-craft | New SaaS product |
| Admin Dashboard | dev-craft + ui-craft | Internal tool |
| E-commerce | product-thinking → planning-and-task-breakdown → dev-craft + ui-craft | Online store |
| API Service | dev-craft only | Backend API |
| Mobile App | dev-craft (backend) + agent-orchestration (mobile) | Mobile with backend |
| Landing Page | ui-craft only | Marketing site |
| Multi-module | product-thinking → planning-and-task-breakdown → dev-craft + agent-orchestration | Large project |

## Orchestration Pattern

1. THINK — Vague prompt → product-thinking for PRODUCT.md
2. DISCOVER — Spec files → project-discovery for DOMAIN.md
3. PLAN — planning-and-task-breakdown for PLAN.md
4. REQUIRE — Load PRODUCT.md / DOMAIN.md into dev-craft
5. ALIGN — Domain-calibrated questions
6. DESIGN — Spec + ADRs + task list
7. BUILD-ORDER — Dependency-based sequencing
8. SOURCE — Official docs verification
9. BUILD — Large: agent-orchestration with git worktree; Small: single-agent vertical slices
10. TEST — Full suite
11. REVIEW — code-review-and-quality
12. HARDEN — Cross-cutting security
13. SHIP — Commit + docs

## Cross-Skill Communication

**dev-craft (`scope: fullstack`) needs UI:**
1. Run CONTRACT (§4.5) → write `api-contract.md` (in `contractRepo` for `multi`)
2. Record in state.json: `crossSkill.uiSliceNeeded`, `apiContract: "<path>"`
3. Hand off to ui-craft: must consume `api-contract.md`, may not invent endpoints
4. On ui-craft return, run HARDEN Check 7 (contract conformance) before SHIP

**ui-craft (`scope: fullstack`) needs backend:**
1. If `api-contract.md` exists (dev-craft produced it), consume it directly
2. If not, generate `api-contract.md` from UI's data needs, hand to dev-craft
3. dev-craft MUST implement only what the contract declares

**dev-craft needs mobile (agent-orchestration):**
1. Produce `api-contract.md`; record `crossSkill.mobileSliceNeeded`; hand to agent-orchestration

**Verification before switching skills:** confirm `api-contract.md` exists at its recorded path and is readable from the consuming repo (for `multi`, the mirror is in sync). Never switch with an implied/unwritten contract.
