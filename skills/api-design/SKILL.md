---
name: api-design
description: "Use when designing a new API surface or changing an existing one — choosing REST vs GraphQL vs gRPC, versioning strategy, auth/rate-limiting shape. Do NOT use for implementing an endpoint inside an already-decided API shape (that's plain BUILD work). Do NOT use for reviewing an existing API's security posture after the fact (see bug-hunting)."
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
  - AskUserQuestion
triggers:
  - "design api"
  - "api contract"
  - "api design"
  - "rest api"
  - "graphql"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: specialized-engineering
  integrates-with: [dev-craft, planning-and-task-breakdown, bug-hunting]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# api-design

## Relationship to existing skills

dev-craft's DESIGN phase should invoke this skill's decision tree whenever a change adds or reshapes an API surface, rather than deciding the shape ad hoc. This skill does not duplicate DESIGN's spec/ADR output — it feeds into it: the API shape decided here becomes one input to the DESIGN spec. It also does not own security review (bug-hunting) or deployment (devops-automation) — it owns the contract shape only.

## Iron Law

**NO ENDPOINT WITHOUT A CONSUMER-STATED CONTRACT.**

Before designing a shape, state who consumes it and what breaks for them if this contract changes later. An API designed without a named consumer in mind is a guess, not a contract.

## Decision tree

1. **Who calls this, and how many independent clients?**
   - Single internal caller, tight coupling acceptable → plain internal function/RPC may be enough; don't over-engineer a public API for it.
   - Multiple/external clients, resource-oriented data → **REST**. → `reference/rest-design.md`
   - Multiple clients with divergent data needs (mobile wants less, web wants more) → **GraphQL**. → `reference/graphql-design.md`
   - Internal service-to-service, performance-sensitive, strongly-typed → **gRPC**. → `reference/grpc-design.md`

2. **Will this contract need to change before all consumers upgrade?**
   - Yes → decide versioning strategy now, before shipping v1.
     → `reference/versioning-strategies.md` (URL path vs header vs media type — pick one and state why, don't leave it implicit)

3. **What's the trust boundary?**
   - Public/external → auth model, rate limiting, and CORS must be decided before the shape is finalized, not bolted on after. → `reference/api-security.md`
   - Internal only → still state the trust boundary explicitly so a later change to "internal only" doesn't silently become public.

4. **How will consumers discover the contract?**
   - REST → OpenAPI/Swagger spec generated from the design, not written by hand after the fact.
   - GraphQL → schema is the contract; document deprecations in-schema. → `reference/api-documentation-generation.md`

## Output

A one-page contract doc: consumer(s), style chosen and why, versioning strategy, auth/rate-limit model, and the generated spec (OpenAPI/GraphQL schema) — handed to dev-craft's DESIGN phase as an input, not a replacement for it.