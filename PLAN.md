# Implementation Plan: High-Value Skills from External Repositories

## Overview
Add 6 high-value top-level skills identified from analysis of external skill repositories (ECC, Agency Agents, Superpowers) to agent-master-skills.

## Collected Requirements

### Core Requirement
Add missing high-value skills that provide specialized capabilities not currently covered in our 16 core skills + 10 plugins.

### Constraints
- Follow existing skill structure (SKILL.md with front-matter, proper sections)
- Maintain consistency with AGENTS.md principles
- Skills must be loadable via `skill()` tool
- Update SHARED.md router and README.md

### Assumptions
- ECC's skill patterns are well-tested and production-ready
- Our existing plugin system can accommodate new top-level skills
- User wants practical, immediately usable skills

### Gaps Identified
- No API design skill (critical for backend work)
- No comprehensive testing strategies skill
- No documentation engineering skill
- No DevOps automation skill
- No observability engineering skill
- No architecture patterns skill

---

## Dependency Graph

```
Skill Structure (foundation)
    │
    ├── api-design (independent)
    ├── testing-strategies (independent)
    ├── documentation-engineering (independent)
    ├── devops-automation (depends on: api-design for deployment APIs)
    ├── observability-engineering (depends on: devops-automation for deployment)
    └── architecture-patterns (independent, but informs all others)
```

**Implementation Order**: Foundation skills first (api-design, testing-strategies, documentation-engineering), then dependent skills (devops-automation, observability-engineering), then architecture-patterns.

---

## Task Breakdown

### Task 1: Create api-design Skill
**Acceptance Criteria:**
- [ ] SKILL.md with proper front-matter (name, description, metadata.origin)
- [ ] Covers REST, GraphQL, gRPC design principles
- [ ] Includes versioning strategies (URL, header, media type)
- [ ] Covers API documentation (OpenAPI/Swagger, GraphQL schema)
- [ ] Includes security considerations (auth, rate limiting, CORS)
- [ ] Provides practical patterns and anti-patterns
- [ ] Loads successfully via `skill("api-design")`

### Task 2: Create testing-strategies Skill
**Acceptance Criteria:**
- [ ] SKILL.md with proper front-matter
- [ ] Covers unit testing (AAA pattern, test doubles, isolation)
- [ ] Covers integration testing (database, external services, contracts)
- [ ] Covers e2e testing (Playwright/Cypress, test data management)
- [ ] Covers contract testing (Pact, schema validation)
- [ ] Covers property-based testing (fast-check, hypothesis)
- [ ] Includes testing pyramid/ice-cream cone strategies
- [ ] Loads successfully via `skill("testing-strategies")`

### Task 3: Create documentation-engineering Skill
**Acceptance Criteria:**
- [ ] SKILL.md with proper front-matter
- [ ] Covers ADR (Architecture Decision Records) format and process
- [ ] Covers API documentation (OpenAPI, GraphQL introspection)
- [ ] Covers docs-as-code (Markdown, MkDocs, Docusaurus, VitePress)
- [ ] Covers technical writing principles (clarity, audience, structure)
- [ ] Includes documentation review process
- [ ] Loads successfully via `skill("documentation-engineering")`

### Task 4: Create devops-automation Skill
**Acceptance Criteria:**
- [ ] SKILL.md with proper front-matter
- [ ] Covers CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins)
- [ ] Covers Infrastructure as Code (Terraform, Pulumi, CloudFormation)
- [ ] Covers deployment strategies (blue-green, canary, rolling)
- [ ] Covers rollback patterns and disaster recovery
- [ ] Includes secrets management and environment promotion
- [ ] Loads successfully via `skill("devops-automation")`

### Task 5: Create observability-engineering Skill
**Acceptance Criteria:**
- [ ] SKILL.md with proper front-matter
- [ ] Covers structured logging (JSON, correlation IDs, log levels)
- [ ] Covers metrics (RED/USE methods, Prometheus, OpenTelemetry)
- [ ] Covers distributed tracing (W3C Trace Context, Jaeger, Zipkin)
- [ ] Covers alerting (SLO/SLI, error budgets, alert fatigue prevention)
- [ ] Includes dashboard design principles (Grafana, Datadog)
- [ ] Loads successfully via `skill("observability-engineering")`

### Task 6: Create architecture-patterns Skill
**Acceptance Criteria:**
- [ ] SKILL.md with proper front-matter
- [ ] Covers Hexagonal/Clean Architecture (ports & adapters)
- [ ] Covers Domain-Driven Design (entities, value objects, aggregates, bounded contexts)
- [ ] Covers Event-Driven Architecture (event sourcing, CQRS, saga pattern)
- [ ] Covers Microservices patterns (API gateway, service mesh, circuit breaker)
- [ ] Includes when to use each pattern and trade-offs
- [ ] Loads successfully via `skill("architecture-patterns")`

### Task 7: Update Documentation
**Acceptance Criteria:**
- [ ] SHARED.md skill router updated with 6 new skills
- [ ] README.md skills table updated
- [ ] All new skills discoverable via skill router

### Task 8: Verification
**Acceptance Criteria:**
- [ ] All 6 skills load without error via `skill()`
- [ ] No broken symlinks in ~/.config/opencode/skills
- [ ] Front-matter valid on all new SKILL.md files

---

## Risk Areas
- **Scope creep**: Each skill could become massive; must scope to "essential patterns only"
- **Duplication**: Check against existing dev-craft/ui-craft plugins to avoid overlap
- **Quality**: External skills (ECC) may have different conventions; must adapt to our style

---

## Success Metrics
- All 6 skills load and provide actionable guidance
- Skills follow our conventions (modern Python, top-level imports, self-documenting names)
- Skills integrate with existing workflow (planning → dev-craft → quality-gates)