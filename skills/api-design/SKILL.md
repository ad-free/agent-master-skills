---
name: api-design
description: Use when designing a new API surface or changing an existing one — choosing REST vs GraphQL vs gRPC, versioning strategy, auth${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/rate-limiting shape. Do NOT use for implementing an endpoint inside an already-decided API shape (that's plain BUILD work). Do NOT use for reviewing an existing API's security posture after the fact (see bug-hunting).
metadata:
  origin: adapted from ECC and addyosmani${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/agent-skills (api-and-interface-design)
  version: 1
---

# api-design

## Relationship to existing skills

dev-craft's DESIGN phase should invoke this skill's decision tree whenever a change adds or reshapes an API surface, rather than deciding the shape ad hoc. This skill does not duplicate DESIGN's spec${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ADR output — it feeds into it: the API shape decided here becomes one input to the DESIGN spec. It also does not own security review (bug-hunting) or deployment (devops-automation) — it owns the contract shape only.

## Iron Law

**NO ENDPOINT WITHOUT A CONSUMER-STATED CONTRACT.**

Before designing a shape, state who consumes it and what breaks for them if this contract changes later. An API designed without a named consumer in mind is a guess, not a contract.

## Decision tree

1. **Who calls this, and how many independent clients?**
   - Single internal caller, tight coupling acceptable → plain internal function${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/RPC may be enough; don't over-engineer a public API for it.
   - Multiple${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/external clients, resource-oriented data → **REST**. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/rest-design.md`
   - Multiple clients with divergent data needs (mobile wants less, web wants more) → **GraphQL**. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/graphql-design.md`
   - Internal service-to-service, performance-sensitive, strongly-typed → **gRPC**. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/grpc-design.md`

2. **Will this contract need to change before all consumers upgrade?**
   - Yes → decide versioning strategy now, before shipping v1.
     → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/versioning-strategies.md` (URL path vs header vs media type — pick one and state why, don't leave it implicit)

3. **What's the trust boundary?**
   - Public${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/external → auth model, rate limiting, and CORS must be decided before the shape is finalized, not bolted on after. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/api-security.md`
   - Internal only → still state the trust boundary explicitly so a later change to "internal only" doesn't silently become public.

4. **How will consumers discover the contract?**
   - REST → OpenAPI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Swagger spec generated from the design, not written by hand after the fact.
   - GraphQL → schema is the contract; document deprecations in-schema. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/api-documentation-generation.md`

## Output

A one-page contract doc: consumer(s), style chosen and why, versioning strategy, auth${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/rate-limit model, and the generated spec (OpenAPI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/GraphQL schema) — handed to dev-craft's DESIGN phase as an input, not a replacement for it.