---
name: architecture-decision-records
description: |
  Draft, evaluate, and maintain ADRs, technical trade-off matrices,
  and system architecture blueprints. Use when making architecture
  decisions, documenting trade-offs, or creating/updating ADRs.
  Do NOT use for implementing architecture (see architecture-patterns)
  or for general code refactoring (see refactor-and-cleanup).
  
model: nemotron-3-ultra-free
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
  - "architecture decision record"
  - "ADR"
  - "trade-off matrix"
  - "architecture blueprint"
  - "document architecture decision"
  - "evaluate architecture options"
  - "ADR template"
  - "architecture trade-off"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.0.0
  domain: specialized-engineering
  integrates-with: [dev-craft, planning-and-task-breakdown]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# architecture-decision-records

## Relationship to existing skills

- architecture-patterns: Provides the pattern options and trade-off analysis; architecture-decision-records documents the decision and rationale.
- documentation-engineering: Provides the ADR format and docs-as-code pipeline; architecture-decision-records applies it specifically to architecture decisions.
- dev-craft: Provides the engineering pipeline; architecture-decision-records is invoked during the DESIGN phase for architecture decisions.
- backend-patterns: Provides implementation patterns; architecture-decision-records documents why a pattern was chosen.

## When to Use

- Making an architecture decision that affects multiple modules or services
- Documenting why a specific pattern or technology was chosen over alternatives
- Creating a trade-off matrix for architecture options
- Maintaining an ADR log for the project
- Onboarding new team members to architecture decisions
- Reviewing past architecture decisions for relevance or deprecation
- Preparing for an architecture review or audit

## When NOT to Use

- Implementing an architecture pattern — see architecture-patterns
- General documentation writing — see documentation-engineering
- Code refactoring or cleanup — see refactor-and-cleanup
- Security vulnerability assessment — see secops-and-vulnerability-scanner
- Performance optimization — see performance-profiler-and-tuner

## Workflow

### Phase 1: Decision Context

1. **Identify the decision**: what architecture decision needs to be made?
2. **Gather context**: what is the problem domain, constraints, and timeline?
3. **Identify stakeholders**: who is affected by this decision?
4. **Define the decision scope**: is this a local module decision or a system-wide decision?
5. **Document the problem statement**: what problem does this decision solve?
6. **Gather requirements**: functional and non-functional requirements that constrain the decision

### Phase 2: Option Generation

1. **List all viable options**: enumerate every reasonable architectural approach
2. **For each option, document**:
   - Description of the approach
   - Pros and cons
   - Estimated cost (implementation time, complexity, maintenance)
   - Estimated risk (technical risk, adoption risk, operational risk)
   - Fit with existing architecture and patterns
   - Alignment with team skills and tooling
3. **Eliminate clearly inferior options**: remove options that violate constraints or have unacceptable risk
4. **Narrow to 2-4 options** for detailed evaluation

### Phase 3: Trade-Off Analysis

1. **Define evaluation criteria**: scalability, maintainability, performance, security, cost, team familiarity, ecosystem maturity
2. **Weight each criterion**: assign relative importance (1-5 scale)
3. **Score each option** against each criterion (1-5 scale)
4. **Compute weighted scores**: multiply score by weight, sum across criteria
5. **Identify the trade-off matrix**: document where each option wins and loses
6. **Document the analysis**: present the trade-off matrix with clear rationale

### Phase 4: Decision and ADR Drafting

1. **Make the decision**: choose the option with the best weighted score or the one that best fits the constraints
2. **Write the ADR** following the standard format:
   - **Title**: descriptive name for the decision
   - **Status**: Proposed, Accepted, Deprecated, Superseded
   - **Context**: the problem and constraints
   - **Decision**: what was decided
   - **Alternatives considered**: the options that were evaluated
   - **Consequences**: what are the positive and negative consequences
   - **Trade-offs**: the key trade-offs and why they were accepted
   - **Related ADRs**: links to related decisions
3. **Get peer review**: have at least one other team member review the ADR
4. **Update status**: move from Proposed to Accepted (or Reject and document why)

### Phase 5: Maintenance

1. **Track ADR status**: update status as decisions evolve (Accepted → Deprecated → Superseded)
2. **Link related ADRs**: maintain cross-references between related decisions
3. **Periodic review**: review ADRs quarterly for relevance and accuracy
4. **Deprecation process**: when an ADR is superseded, document the new ADR and link to the deprecated one
5. **Archive old ADRs**: move superseded ADRs to an archive directory

## Context Management

- Track ADR state in `.dev-craft/adr/<project>/index.json` with fields: `adr_id`, `title`, `status`, `date`, `related_adrs`, `option_chosen`, `option_rejected`
- On session resume, check index.json for any in-progress ADRs and continue from the last completed phase
- Persist the ADR document in `docs/adr/YYYYMMDD-title.md`

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read existing ADRs, architecture docs, and project context | Only read project source and docs |
| Write | Create new ADR files | Follow the ADR format and naming convention |
| Edit | Update ADR status or content | Never alter the decision history; only update status |
| Bash | Run ADR validation, list ADRs | Use established tools |
| Grep | Search ADRs for related decisions or patterns | Search within the ADR directory |
| Glob | Find ADR files | Pattern: `docs/adr/**/*.md` |
| AskUserQuestion | Get user input on trade-off weights and decision preferences | Use for criteria weighting and option selection |

## Output Contract

On completion, the skill must produce:

1. A completed ADR document in `docs/adr/` following the standard format
2. An updated ADR index in `.dev-craft/adr/<project>/index.json`
3. A trade-off matrix documenting the evaluation of all options
4. A summary of the decision with rationale and consequences
5. Cross-references to related ADRs

## Quality Gates

- [ ] ADR follows the standard format (Title, Status, Context, Decision, Alternatives, Consequences, Trade-offs, Related)
- [ ] At least 2 alternatives were considered and documented
- [ ] Trade-off matrix includes weighted criteria and scores
- [ ] Decision rationale is clear and justified
- [ ] ADR status is updated correctly (Proposed → Accepted or Rejected)
- [ ] Related ADRs are linked
- [ ] Peer review has been completed
- [ ] ADR is stored in the correct location with the correct naming convention

## Error Handling

- **No viable options found**: expand the search for alternatives, reconsider constraints, and re-evaluate
- **Trade-off analysis is inconclusive**: escalate to the team for discussion, document the uncertainty, and make a provisional decision
- **ADR format is incomplete**: ensure all required sections are filled before marking as Accepted
- **Peer review rejects the ADR**: address the review comments, revise, and re-submit for review
- **ADR is superseded**: update the status to Superseded, link to the new ADR, and document the reason for the change