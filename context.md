# Glossary

Shared terminology for agent-master-skills pipelines. Used by dev-craft, ui-craft, and product-thinking for consistent language across phases.

| Term | Definition |
|------|------------|
| **User** | Authenticated person using the application |
| **Session** | JWT token stored in httpOnly cookie |
| **Dashboard** | Main landing page after login |
| **Settings** | User profile and preferences page |
| **Slice** | A vertical feature unit: DB + API + UI |
| **Module** | A cohesive group of related features |
| **G1 / G2 / G3** | Priority tiers: Core (G1), Important (G2), Nice-to-have (G3) |
| **REQ-ID** | Stable requirement identifier (e.g., REQ-001) |
| **COVERAGE GATE** | Hard gate: every P1/G1 requirement traced to a task with acceptance criteria |
| **Iron Law** | Non-negotiable discipline rule encoded in a skill |
| **Handoff** | Structured context transfer between skills/phases |
| **Contract** | Canonical `api-contract.md` shared by BE and FE |
| **State** | Persistent pipeline state in `.dev-craft/runs/<slug>/state.json` |

---

## Pipeline Terminology

| Term | Meaning |
|------|---------|
| **Phase** | A numbered pipeline stage (LOAD, ALIGN, DESIGN, BUILD, etc.) |
| **Slice** | One vertical feature unit built in BUILD phase |
| **Gate** | A verification checkpoint (e.g., COVERAGE GATE) |
| **HARDEN** | Cross-cutting security/audit phase |
| **SHIP** | Final commit + merge + rollback plan |

---

## Skill Terminology

| Term | Meaning |
|------|---------|
| **Skill** | A `SKILL.md` file loaded via `skill()` tool |
| **Plugin** | Optional extension registered in `state.json` |
| **Scope** | Topology (mono/multi) × Domain (be/fe/fullstack) × Mode (build/ticket) |
| **Topology** | `mono` (single repo) or `multi` (separate BE/FE repos) |
| **ContractRepo** | Repo that owns `api-contract.md` (usually BE repo) |