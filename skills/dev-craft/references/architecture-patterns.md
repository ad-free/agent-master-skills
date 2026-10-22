TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# architecture-patterns

## Relationship to existing skills

dev-craft's ARCH-SCAN phase detects existing codebase smells; its DESIGN phase produces the spec. This skill is what DESIGN should invoke when the change requires a structural pattern decision — it supplies the trade-off analysis, DESIGN still owns the final spec output. This skill never recommends a pattern without stating what it costs, since every pattern here trades simplicity for some other property.

## Iron Law

**NO PATTERN WITHOUT A STATED TRADE-OFF.**

Every pattern below buys something at a cost. If you can't state the cost in one sentence, you're pattern-matching to familiarity, not solving the actual problem.

## Decision tree

1. **Is business logic getting tangled with infrastructure concerns (DB, HTTP, third-party SDKs) in the same layer?**
   - Yes → **Hexagonal/Clean Architecture** (ports & adapters) isolates domain logic behind interfaces. Cost: more indirection, more files for simple CRUD. Don't apply to a project that's genuinely just CRUD. → `reference/hexagonal-architecture.md`

2. **Is the domain itself complex** (many business rules, not just data shuffling)?
   - Yes → **DDD** — entities/value objects/aggregates, bounded contexts to stop one team's model leaking into another's. Cost: upfront modeling effort; overkill for a thin CRUD service. → `reference/domain-driven-design.md`

3. **Do multiple parts of the system need to react to the same event independently, or does an operation span multiple services/aggregates?**
   - Yes → **Event-driven** (event sourcing/CQRS if audit history matters, saga pattern if the operation spans services with no single transaction). Cost: eventual consistency, harder to reason about linearly. → `reference/event-driven-architecture.md`

4. **Is this being split into independently deployable services?**
   - Only if team/deploy boundaries actually require it — not by default. If yes: API gateway, service mesh for cross-cutting concerns, circuit breaker at every network call. Cost: operational complexity, network failure modes that didn't exist in a monolith. → `reference/microservices-patterns.md`

## Output

A short trade-off memo: pattern chosen, what it costs, and why the alternative (usually: staying simpler) was rejected for this specific case — handed to DESIGN as input, filed as an ADR via documentation-engineering.