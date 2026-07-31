---
name: backend-patterns
description: |
  Apply proven backend architectural patterns — hexagonal/clean architecture,
  layered design, repository pattern, CQRS, event sourcing, saga pattern.
  Use when structuring backend services, choosing between architectural patterns,
  or refactoring existing code toward a cleaner structure. Do NOT use for
  API surface design (see api-design) or for database migration planning
  (see database-migrations).
  
model: nemotron-3-ultra-free
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "backend architecture"
  - "hexagonal architecture"
  - "clean architecture"
  - "repository pattern"
  - "CQRS pattern"
  - "event sourcing"
  - "saga pattern"
  - "layered architecture"
  - "backend structure"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.0.0
  domain: specialized-engineering
  integrates-with: [dev-craft, architecture-patterns]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# backend-patterns

## Relationship to existing skills

- architecture-patterns: Handles high-level pattern selection (hexagonal, DDD, event-driven, microservices). backend-patterns provides the concrete implementation patterns and code structure for those decisions.
- dev-craft: Provides the overall engineering pipeline; backend-patterns is invoked during the ARCH-SCAN and REFACTOR phases.
- api-design: Defines the API surface; backend-patterns ensures the internal structure supports the API contract cleanly.
- dev-craft/plugins/security-audit: Validates that backend patterns do not introduce security vulnerabilities (e.g., mass assignment, injection).

## When to Use

- Structuring a new backend service or module
- Refactoring an existing service toward a cleaner architecture
- Choosing between hexagonal, layered, or modular monolith patterns
- Implementing repository, CQRS, or event sourcing patterns
- Defining module boundaries and dependency direction
- Setting up dependency injection or service layer patterns

## When NOT to Use

- Choosing a high-level system architecture (hexagonal vs microservices) — see architecture-patterns
- Designing API endpoints or contracts — see api-design
- Database schema design or migration — see database-migrations
- Frontend or UI architecture — see ui-craft
- Performance optimization of existing queries — see dev-craft/plugins/performance-profiling

## Workflow

### Phase 1: Pattern Selection

1. **Assess the current structure**: read the codebase to understand the existing architecture (monolith, layered, ad-hoc)
2. **Identify pain points**: coupling, unclear boundaries, testability issues, dependency direction violations
3. **Match pattern to problem**:
   - Coupling between business logic and infrastructure → hexagonal/clean architecture
   - Complex read/write asymmetry → CQRS
   - Long-running business processes with compensation needs → saga pattern
   - Audit trail or event replay needed → event sourcing
   - Simple CRUD with clear boundaries → layered architecture with repository pattern
4. **Define scope**: which module/service is being restructured, and what are the boundaries
5. **Get user confirmation** on the chosen pattern before proceeding

### Phase 2: Structure Definition

Define the module/file structure for the chosen pattern:

**Hexagonal/Clean Architecture**:
```
<module>/
├── domain/
│   ├── entities/
│   ├── value-objects/
│   ├── ports/          (interfaces)
│   └── services/       (domain logic)
├── application/
│   ├── use-cases/
│   ├── dto/
│   └── ports/          (application interfaces)
├── infrastructure/
│   ├── persistence/
│   ├── external/
│   └── adapters/
└── presentation/
    ├── controllers/
    └── dto/
```

**Layered Architecture**:
```
<module>/
├── controllers/
├── services/
├── repositories/
├── models/
└── config/
```

**CQRS**:
```
<module>/
├── commands/
│   ├── handlers/
│   ├── validators/
│   └── models/
├── queries/
│   ├── handlers/
│   ├── projections/
│   └── models/
├── events/
└── domain/
```

### Phase 3: Dependency Mapping

1. **Draw dependency arrows**: which modules depend on which
2. **Enforce direction**: dependencies must point inward (toward domain) for hexagonal, or downward (toward data) for layered
3. **Identify violation points**: existing code that breaks the dependency rule
4. **Plan migration steps**: refactor violations in order of lowest risk first

### Phase 4: Implementation

1. **Create the skeleton**: directories, interfaces, base types
2. **Implement domain layer first**: entities, value objects, domain services
3. **Implement ports/interfaces**: define contracts that infrastructure will fulfill
4. **Implement infrastructure adapters**: database, external API, message queue clients
5. **Wire dependencies**: configure DI container, module exports, or service registration
6. **Write tests per layer**: domain tests (no infrastructure), application tests (mock ports), integration tests (real adapters)

### Phase 5: Validation

1. **Dependency check**: verify no dependency violations remain
2. **Test coverage**: domain layer must have >80% coverage; integration tests for infrastructure
3. **Build and lint**: ensure the new structure compiles and passes linting
4. **Document the pattern**: update architecture decision records (ADRs) with the chosen pattern and rationale

## Context Management

- Track pattern decisions in `.dev-craft/architecture/<module>/pattern.json` with fields: `module`, `pattern`, `rationale`, `date`, `violations`
- On session resume, check for any in-progress restructuring and continue from the last completed phase

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read existing code structure, dependency graph, test files | Only read project source files |
| Write | Create new module files, interfaces, adapters | Follow the module structure defined in Phase 2 |
| Edit | Refactor existing code into new structure | Preserve existing behavior; never change business logic during restructuring |
| Grep | Find dependency violations, coupling points | Search within the target module directory |
| Glob | Find existing files in the module | Pattern: `<module>/**/*.py` (or relevant extension) |

## Output Contract

On completion, the skill must produce:

1. A new module/file structure following the chosen pattern
2. Updated dependency graph showing clean direction
3. Test files for each layer (domain, application, infrastructure)
4. An architecture decision record (ADR) documenting the pattern choice and rationale
5. A migration plan for existing code to move into the new structure

## Quality Gates

- [ ] Dependency direction is enforced (no outward-pointing dependencies from domain)
- [ ] Domain layer has no infrastructure imports
- [ ] All ports/interfaces are defined before implementations
- [ ] Tests exist for each layer with >80% domain coverage
- [ ] Build and lint pass with the new structure
- [ ] ADR is created or updated with the pattern decision
- [ ] No existing behavior is changed during restructuring

## Error Handling

- **Circular dependency detected**: halt restructuring, report the cycle, and suggest a breaking point
- **Existing test failures after restructuring**: revert the structural changes to that module, investigate, and fix before proceeding
- **Pattern mismatch**: if the chosen pattern does not fit the problem, return to Phase 1 and re-evaluate
- **User rejects pattern choice**: do not proceed, document the rejection reason, and suggest alternatives