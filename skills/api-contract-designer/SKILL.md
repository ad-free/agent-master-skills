---
name: api-contract-designer
description: |
  Design OpenAPI/Swagger specs, GraphQL schemas, type definitions, and
  mock data for clean frontend-backend integration. Use when designing
  API contracts, generating TypeScript types from API specs, or creating
  mock data for frontend development. Do NOT use for implementing API
  endpoints (see api-design) or for general API design decisions (see
  api-design).
  
model: big-pickle
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "design API contract"
  - "OpenAPI spec"
  - "GraphQL schema"
  - "API types"
  - "mock data"
  - "API contract"
  - "type definitions"
  - "FE-BE integration"
  - "contract first"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: specialized-engineering
  integrates-with: [api-design, dev-craft, ui-craft]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# api-contract-designer

## Relationship to existing skills

- api-design: Handles the high-level API design decisions (REST vs GraphQL, versioning, auth); api-contract-designer produces the concrete contract artifacts (specs, types, mocks).
- backend-patterns: Ensures the backend implementation follows clean architecture; api-contract-designer defines the contract that the backend must fulfill.
- ui-component-builder: Consumes the API contract to build type-safe frontend components; api-contract-designer produces the types that ui-component-builder imports.
- dev-craft: Provides the engineering pipeline; api-contract-designer is invoked during the CONTRACT phase.

## When to Use

- Designing OpenAPI/Swagger specs for REST APIs
- Designing GraphQL schemas with types, queries, mutations, and subscriptions
- Generating TypeScript/Flow type definitions from API specs
- Creating mock data for frontend development against a not-yet-built API
- Defining the FE-BE integration contract before implementation begins
- Generating client SDKs or API hooks from a contract
- Validating that frontend and backend are aligned on the API contract

## When NOT to Use

- Deciding API architecture (REST vs GraphQL vs gRPC) — see api-design
- Implementing API endpoints — see api-design or dev-craft BUILD phase
- General database design or migration — see database-migrations
- Frontend component implementation — see ui-component-builder
- Security auditing of API endpoints — see bug-hunting

## Workflow

### Phase 1: Contract Requirements

1. **Identify the consumers**: who (frontend team, mobile team, external partners) will consume this API?
2. **Identify the resources**: what entities, operations, and data flows does the API expose?
3. **Define the contract style**: REST (OpenAPI) or GraphQL (SDL) or both?
4. **Gather existing constraints**: authentication, rate limiting, pagination, versioning requirements
5. **Define the contract format**: OpenAPI 3.0/3.1 YAML, GraphQL SDL, Protobuf, or TypeScript types
6. **Get user confirmation** on the contract style and format before proceeding

### Phase 2: Schema Design

**For OpenAPI (REST)**:
1. Define paths, methods, and operation IDs
2. Define request bodies with schemas (JSON Schema)
3. Define response schemas for each status code (200, 201, 400, 401, 403, 404, 500)
4. Define query parameters, path parameters, and header parameters
5. Define security schemes (OAuth2, API key, Bearer token)
6.Define pagination, filtering, and sorting patterns
7. Define error response envelope (consistent error shape)

**For GraphQL**:
1. Define types with fields and relationships
2. Define queries, mutations, and subscriptions
3. Define input types for mutations
4. Define enums and interfaces for shared types
5. Define pagination patterns (cursor-based or offset-based)
6. Define error handling conventions

### Phase 3: Type Generation

1. **Generate TypeScript types** from the OpenAPI spec or GraphQL schema
2. **Generate API client hooks** (e.g., React Query, SWR, TanStack Query)
3. **Generate mock data** that conforms to the schema
4. **Generate validation schemas** (Zod, Yup, Joi) for runtime validation
5. **Generate documentation** (Swagger UI, GraphQL Playground, or TypeDoc)

### Phase 4: Mock Data Generation

1. **Create mock data files** for each resource/type
2. **Define mock scenarios**: happy path, error cases, edge cases, empty states
3. **Set up mock server** (MSW, Prism, json-server, or Apollo MockLink)
4. **Define delay profiles**: simulate network latency for realistic testing
5. **Validate mocks against the schema**: ensure mock data conforms to the contract

### Phase 5: Contract Validation

1. **Validate OpenAPI spec** with a spec validator (spectral, swagger-parser)
2. **Validate GraphQL schema** with schema validation tools
3. **Run contract tests**: verify that mock data matches the schema
4. **Share the contract** with frontend and backend teams for review
5. **Get sign-off** from both teams before implementation begins

### Phase 6: Contract Maintenance

1. **Version the contract**: use semantic versioning for the API contract
2. **Track breaking changes**: document any changes that break existing consumers
3. **Update generated types** when the contract changes
4. **Regenerate mocks** when the contract changes
5. **Archive old contract versions** for backward compatibility reference

## Context Management

- Track contract state in `.dev-craft/contracts/<project>/state.json` with fields: `contract_id`, `format` (openapi/graphql/protobuf), `version`, `status` (draft/review/signed/implemented), `last_updated`
- On session resume, check state.json for any in-progress contract and continue from the last completed phase

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read existing API specs, schemas, and type definitions | Only read project source and contract files |
| Write | Create OpenAPI specs, GraphQL schemas, type definitions, mock data | Follow the project's naming and directory conventions |
| Edit | Update existing contract artifacts | Never break backward compatibility without a version bump |
| Bash | Run spec validators, type generators, mock servers | Use established tools (spectral, swagger-parser, graphql-cli) |
| Grep | Find API references, type usage, mock data references | Search within the contract scope |
| Glob | Find contract files | Pattern: `contracts/**/*` |
| Task | Spawn subagent for contract validation or type generation | Subagent must report findings, not make edits |

## Output Contract

On completion, the skill must produce:

1. An API contract artifact (OpenAPI YAML or GraphQL SDL)
2. Generated TypeScript/Flow type definitions
3. Generated API client hooks
4. Mock data files for all resources
5. A mock server setup (if applicable)
6. A validation report confirming the contract is valid and consistent
7. Updated state.json with the contract status
8. A contract review summary with sign-off status

## Quality Gates

- [ ] OpenAPI spec passes spectral validation (or GraphQL schema passes validation)
- [ ] All response schemas include error responses (400, 401, 403, 404, 500)
- [ ] TypeScript types are generated and compile without errors
- [ ] Mock data conforms to the schema
- [ ] Pagination, filtering, and sorting patterns are consistent
- [ ] Error response envelope is consistent across all endpoints
- [ ] Security schemes are defined for all authenticated endpoints
- [ ] Contract is versioned with semantic versioning
- [ ] Both frontend and backend teams have signed off on the contract

## Error Handling

- **Spec validation failure**: fix the schema error before proceeding; do not generate types from an invalid spec
- **Type generation failure**: check for circular references or unsupported schema features; simplify the schema
- **Mock data does not conform to schema**: fix the mock data to match the schema
- **Contract change breaks existing consumers**: bump the version, document the breaking change, and get explicit sign-off
- **Frontend and backend disagree on the contract**: facilitate a negotiation meeting, document the agreed contract, and get sign-off from both teams