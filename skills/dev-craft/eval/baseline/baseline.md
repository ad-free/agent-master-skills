# Baseline: existing dev-craft v3.0.0 vs brief section 14.1

**Method (read this first):** STATIC TRACE, not live runs. For each case I read the existing SKILL.md and
references and wrote down what an agent following them would be told to do, then scored it against the brief's
rubric. No agent was executed. Live with/without runs need subagent dispatch and fixture repos; they are
proposed in IMPROVEMENT-PLAN.md (decision D1). Treat these scores as predictions, not measurements.

Scale: PASS = the skill instructs the right behavior; PARTIAL = only by accident or in part; FAIL = no instruction,
so the agent's default (the weakness the brief targets) wins.

Rubric per run: evidence real? assumptions stated? questions few and design-changing? scope respected?
contract consistent? UI quality? schema findings useful? tokens/steps.

## General
| # | Case (prompt shape) | Score | Why (file evidence) |
|---|---|---|---|
| G1 | Trivial: rename a var / fix typo | PASS | SKILL.md:21 Trivial = no pipeline; description skips typos. Risk: description fires on "fix/change" broadly (:3). |
| G2 | Small bug fix | PARTIAL | Bug mode reproduces first (:58); gate 5 wants evidence (:104). No Evidence table, no "Not verified", no red-green proof (only in plugins/tdd-enforcer, never routed from SKILL.md). |
| G3 | Medium single-side feature | PARTIAL | Standard path ok (:35-49). No requirement-to-test mapping (TRACE is Large only), no edge/error-path rule, no decision log. |
| G4 | Large refactor | PARTIAL | Refactor mode is good (:59). Then Large path forces REQUIRE/ALIGN/TRACE/HARDEN: 13 phases for a no-new-behavior change. |
| G5 | Review a given diff | FAIL | No standalone review flow. 7 axes live inside Large REVIEW (phases-large.md:~110) and defer to external skill; no cap, no file:line+fix format, no "do not flag". |
| G6 | Incoming PR comments (one wrong) | FAIL | Not mentioned anywhere. |

## Requirements and evidence
| # | Case | Score | Why |
|---|---|---|---|
| R1 | Built-in contradiction | PARTIAL | Brief has "open questions" (:39) but nothing says to hunt contradictions; Standard "proceed if no open question blocks" lets the agent pick silently. |
| R2 | Missing error case handled by repo in a specific way | PARTIAL | API layer rule "extract existing contract from source" (:122) and "nearest similar feature" (:41). Not generalized, no finding format. |
| R3 | Asks for something that already exists | PARTIAL | Reads nearest similar feature; no instruction to stop and cite it. |
| R4 | Unverifiable claim in the task | FAIL | Gate 5 covers the agent's own claims only. No Code/Docs/Run/Logic/Unknown tagging. |
| R5 | Hidden edge-case trap | PARTIAL | Failing-test-first slices help; nothing requires edge/error-path tests. |
| R6 | Part cannot be verified | PARTIAL | UI-only: "say so, report remaining risk" (:117). No general "Not verified" section. |

## Full-stack and scope
| # | Case | Score | Why |
|---|---|---|---|
| F1 | New field DB->API->UI | PARTIAL | Large + CONTRACT + TEST contract conformance (phases-large.md CONTRACT/TEST) are good. No consumer search, no generated-types-in-sync check. |
| F2 | Changed response shape, update consumers | FAIL | No consumer-search instruction. |
| F3 | Backend error handled in UI, proven | PARTIAL | Nothing maps each contract error to a UI behavior; e2e run not required. |
| F4 | FE-only needs a field backend lacks | FAIL | SCOPE records `fe` only (phases-large.md SCOPE). "Frontend does not invent endpoints" exists only in references/cross-skill.md, which SKILL.md never routes to for this. No options, no escalation rule. |
| F5 | FE-only, real API differs from description | PARTIAL | "Never guess the contract" (:122) is under API layer, not triggered for FE-only work. |
| F6 | Backend change breaks FE consumer | FAIL | No reverse read-scope rule. |

## UI/UX
| # | Case | Score | Why |
|---|---|---|---|
| U1 | "Build an HRM dashboard" | FAIL | Vague-input gate stops building (:29, good) but UI rules are one bullet (:114-118): no design.md, no icon/chart/palette choices, no playbook, no checklist. Screenshots at two widths are required (good). Quality depends on a separate ui-craft invocation. |
| U2 | "Build a PPE product/news/contact site" | FAIL | Same as U1; no catalog structure guidance. |

## Data and infrastructure
| # | Case | Score | Why |
|---|---|---|---|
| D1 | Flawed schema (free-text dept, float money, overwritten history) | FAIL | Data rule (:119) is about migrations, not about questioning the schema. Agent builds on it. |
| D2 | Slow list query | FAIL | Says "indexes on FK and filtered columns" but nothing runs EXPLAIN. |
| D3 | New service architecture | PARTIAL | DESIGN writes ADRs with alternatives table (phase-templates.md ADR). No "start simple, 2 options + default" rule. |

## Tally (predicted)
PASS 1 | PARTIAL 12 | FAIL 9 (of 22). Weakest areas: requirements challenge (R4), scope (F2/F4/F6), review and
PR comments (G5/G6), UI design (U1/U2), schema (D1/D2). Strongest: tiers, hard gates, bug/refactor modes,
contract-conformance test, vague-input gate.

## Defects found while reading (independent of the brief)
- SKILL.md:191 points to `references/phase-template.md`; the file is `phase-templates.md` (broken link).
- `phase-templates.md` state path `.dev-craft/runs/<slug>/state.json` + `index.json` contradicts SKILL.md:142
  `.dev-craft/state.json`. Agent gets two layouts.
- `cross-skill.md` cites "§0.2" and "§4.5"; `build-protocol.md` and `harden-checks.md` cite "[5] BUILD" and
  "[8] HARDEN", "9-step loop skeleton in SKILL.md". None exist in current SKILL.md (stale numbering).
- Security checks exist in 4 places: SKILL.md:133, build-protocol.md SECURE tree, harden-checks.md,
  plugins/security-audit.
- TDD: SKILL.md step 3, plugins/tdd-enforcer (212 lines), and external `tdd-seam` skill overlap.
- Languages outside the stated stack: modern-patterns.md (Rust/Go/Ruby/PHP, ~45 lines), lint-rules.md
  (same, ~50 lines), plugins/language-rules (Go, Rust, ~40 lines).

---
# After (dev-craft v4.0.0): STATIC TRACE, same caveat

Re-traced the same cases against the new files. Not executed; live runs still pending (plan decision D1).

| Case | Before | After | Instruction now responsible |
|---|---|---|---|
| G1 | PASS | PASS | SKILL.md §1 Trivial; description skip clause kept |
| G2 | PARTIAL | PASS | workflow.md Bug mode (failing test, same-bug-elsewhere), verify.md red-green + Evidence table |
| G3 | PARTIAL | PASS | challenge.md in brief, REQ examples, verify.md REQ-to-test map |
| G4 | PARTIAL | PARTIAL | Refactor mode now says not to run full Large path unless it crosses modules; still heavy if it does |
| G5 | FAIL | PASS | review.md (axes, cap, file:line + fix, do-not-flag) |
| G6 | FAIL | PASS | review.md PR comments: fix / push back / ask |
| R1 | PARTIAL | PASS | challenge.md lenses + question format with defaults |
| R2 | PARTIAL | PASS | challenge.md Code-basis findings; fullstack.md |
| R3 | PARTIAL | PASS | challenge.md "already exists: point to it" |
| R4 | FAIL | PASS | challenge.md Unknown becomes a question |
| R5 | PARTIAL | PASS | verify.md edge/error paths required |
| R6 | PARTIAL | PASS | verify.md "Not verified" |
| F1 | PARTIAL | PASS | fullstack.md vertical slice + types in sync + e2e per criterion |
| F2 | FAIL | PASS | fullstack.md consumer search |
| F3 | PARTIAL | PASS | fullstack.md errors end to end; verify.md exercises each contract error |
| F4 | FAIL | PASS | SKILL.md §2, fullstack.md options (a)(b)(c), no silent edit |
| F5 | PARTIAL | PASS | fullstack.md rule 2-3 |
| F6 | FAIL | PASS | fullstack.md rule 6 |
| U1 | FAIL | PASS (predicted) | frontend-design.md + ui-patterns/hrm.md + checklists/ui.md + screenshot critique |
| U2 | FAIL | PASS (predicted) | ui-patterns/catalog-showcase.md |
| D1 | FAIL | PASS | data-modeling.md findings-as-options |
| D2 | FAIL | PASS | data-modeling.md EXPLAIN step; "Not verified" if no DB |
| D3 | PARTIAL | PASS | architecture.md start simple, 2 options + default |

Predicted tally: PASS 21 | PARTIAL 1 | FAIL 0 (of 22). Static traces over-predict: a rule that exists can still be
ignored by a model. Only live runs show that.

Size: SKILL.md 201 -> ~100 lines. New reference files load only on their condition (SKILL.md §5).
