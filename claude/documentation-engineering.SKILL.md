---
name: documentation-engineering
description: Use when deciding HOW to document a decision, API, or system — ADR format, docs-as-code setup, technical writing structure. Do NOT use to write the ADR content itself for a specific design decision (dev-craft's DESIGN phase owns that content; this skill owns the format/process it should follow).
metadata:
  origin: adapted from ECC
  version: 1
---

# documentation-engineering

## Relationship to existing skills

dev-craft's DESIGN phase already produces ADRs as an output. This skill does
NOT replace that — it defines the *format and review process* DESIGN's ADRs
should follow, so "write an ADR" doesn't get reinvented differently each time.
If you're deciding "should we use approach A or B," that decision-making
belongs in DESIGN; this skill governs how that decision gets written down.

## Iron Law

**NO UNDOCUMENTED IRREVERSIBLE DECISION.**

If a decision would be expensive to reverse (schema choice, API contract,
dependency with lock-in), it gets an ADR before or immediately after the
decision is made — not "eventually," not "if someone asks."

## Decision tree

1. **What kind of documentation is this?**
   - A decision with alternatives considered and a chosen trade-off →
     **ADR**. → `reference/adr-format.md`
   - A contract for callers (API) → generated from source, not hand-written
     prose. → `reference/api-doc-generation.md`
   - A guide/how-to for humans (onboarding, runbook) → docs-as-code, lives
     next to the code it describes, reviewed like code.
     → `reference/docs-as-code.md`

2. **Before publishing, check against the technical writing checklist**:
   stated audience, one clear structure (not a stream of consciousness),
   no unexplained jargon for the stated audience.
   → `reference/technical-writing-principles.md`

3. **Is this documentation reviewed the same way code is?**
   - If a doc describes a decision someone will rely on later, it should go
     through the same review gate as the code — not skip review because
     "it's just docs." → `reference/documentation-review.md`

## Output

For ADRs: a numbered decision record (context, options considered, decision,
consequences) filed alongside dev-craft's DESIGN output — not a separate
undiscoverable document.
