# Cross-link edits to existing skills

Paste these one-liners into the named phase/section. Don't rewrite
surrounding content — these are pointers, not replacements.

## dev-craft/SKILL.md

**In the `DESIGN` phase** (wherever it currently describes producing spec + ADRs):
> Before finalizing the spec: if this change adds/reshapes an API surface,
> invoke `api-design`. If it requires a structural pattern decision, invoke
> `architecture-patterns`. Write resulting ADRs per `documentation-engineering`'s
> format.

**In the `TEST` phase**:
> Before writing tests, invoke `testing-strategies` to decide test type and
> stated failure mode per test — do not default to unit tests without
> checking its decision tree.

**In the `HARDEN` phase** (alongside the existing 7 security checks):
> Also invoke `observability-engineering` — security hardening and
> observability are separate concerns; a hardened system that fails silently
> in production is still a gap.

**In the `SHIP` phase** (where it currently says "commit + rollback plan"):
> For the rollback plan and deployment mechanics, invoke `devops-automation`
> rather than deciding deployment strategy ad hoc.

## quality-gates/SKILL.md

**In Gate 2 (Deterministic) description**:
> Gate 2 runs the test plan `testing-strategies` produced — it does not
> decide test type or shape; that decision happens upstream, before BUILD.

## code-review-and-quality/SKILL.md

**Wherever test coverage is one of the 8 review axes**:
> Judge tests against the failure mode stated when they were written (see
> `testing-strategies`) — a test with no stated failure mode is itself a
> review finding, not just a coverage gap.

## bug-hunting/SKILL.md

**Wherever API attack surface is discussed** (if it is — check first):
> If the API's auth/rate-limit model was never explicitly decided (see
> `api-design`), that absence is itself a finding, not something to infer
> and move past.

---

# SHARED.md router update

Add all 6 new skills to the inventory table with their Iron Law column
filled in (matching the existing format for other skills). In the decision
tree section, make sure these don't collide with existing trigger conditions:

- `testing-strategies` fires on "what test should I write," NOT "did tests
  pass" (→ verification-before-completion) or "review my test coverage"
  (→ code-review-and-quality).
- `api-design` fires on "design this API," NOT "implement this endpoint"
  (→ dev-craft BUILD) or "is this API secure" (→ bug-hunting).
- `documentation-engineering` fires on "how should this be documented," NOT
  "write this ADR's content" (→ dev-craft DESIGN).
- `devops-automation` fires on "how does this deploy," NOT "is this ready to
  deploy" (→ quality-gates).
- `observability-engineering` fires on "what should we monitor," NOT "is
  this secure" (→ bug-hunting) or "is this hardened" (→ dev-craft HARDEN,
  which now also invokes this skill).
- `architecture-patterns` fires on "what structural pattern," NOT "scan
  existing code for smells" (→ dev-craft ARCH-SCAN).

# README.md update

Add a new table section, matching existing format (Skill | Purpose | Iron
Law), e.g.:

| Skill | Purpose | Iron Law |
|---|---|---|
| `testing-strategies` | Decide test type/shape before writing tests | NO TEST WITHOUT A STATED FAILURE MODE |
| `api-design` | Decide API contract shape before implementation | NO ENDPOINT WITHOUT A CONSUMER-STATED CONTRACT |
| `documentation-engineering` | Decide doc format/process (ADRs, docs-as-code) | NO UNDOCUMENTED IRREVERSIBLE DECISION |
| `devops-automation` | Decide deployment mechanics and rollback path | NO DEPLOY WITHOUT A TESTED ROLLBACK PATH |
| `observability-engineering` | Decide what to log/measure/alert on | NO ALERT WITHOUT AN OWNER AND A RUNBOOK LINK |
| `architecture-patterns` | Decide structural pattern with stated trade-offs | NO PATTERN WITHOUT A STATED TRADE-OFF |

Update the Pipeline Flow diagram's DESIGN/TEST/HARDEN/SHIP annotations to
show these as call-outs from the relevant phase (see dev-craft edits above),
not as parallel top-level entries competing with dev-craft.

---

# Verification checklist (Step 4)

Run these before considering this done:

- [ ] All 6 new SKILL.md files parse, valid front-matter, `metadata.origin` present
- [ ] No file exceeds ~150 lines (subtopics live in reference/*.md)
- [ ] No broken symlinks in ~/.config/opencode/skills after copying
- [ ] Router disambiguation test — try these prompts and confirm the intended
      skill fires, not a neighboring one:
  - "what kind of test should I write for this new validator" → testing-strategies
  - "is this ready to merge" → quality-gates / verification-before-completion, NOT testing-strategies
  - "design the API for the new webhook endpoint" → api-design
  - "review this endpoint for security holes" → bug-hunting, NOT api-design
  - "how should we roll this out" → devops-automation
  - "did the deploy actually succeed" → verification-before-completion, NOT devops-automation
  - "what should we alert on for this service" → observability-engineering
  - "is this service hardened against attack" → dev-craft HARDEN / bug-hunting, NOT observability-engineering
  - "should this be one service or three" → architecture-patterns
  - "what's wrong with the current codebase structure" → dev-craft ARCH-SCAN, NOT architecture-patterns
- [ ] Each new skill's "Relationship to existing skills" section double-checked
      against the actual current content of dev-craft/quality-gates/
      code-review-and-quality/bug-hunting (I drafted these from your public
      README's phase descriptions, not the live file content — verify before merging)
