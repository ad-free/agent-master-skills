# dev-craft improvement plan

Status: **proposal, nothing in `skills/dev-craft/` has been edited.** Backup: `dev-craft.bak/` (byte-identical,
verified with `diff -r`). Baseline: `skills/dev-craft/eval/baseline/baseline.md` (static trace, see caveat there).

## 1. Inventory (Step 1)

Frontmatter description: ~900 chars, says when to use and when to skip (typos, one-liners, trivial config). Does
not mention reviewing code or PR comments. Very broad trigger verbs ("fix, change, add").

`SKILL.md` is **201 lines and contains the rules itself**. It is not a router.

| File | Purpose | Lines | Loaded when | Notes |
|---|---|---|---|---|
| SKILL.md | tiers, input gate, Standard path, modes, Large table, hard gates, layer rules, state, status, failures | 201 | always | Over the 150 target; ends with a mis-named link |
| references/phases-large.md | per-phase detail, Large path | 140 | Large, per phase | Good; only place with CONTRACT |
| references/build-protocol.md | SECURE + MATCH trees, worktree, branch script | 214 | BUILD | Stale "[5] BUILD" numbering; SECURE duplicates harden |
| references/harden-checks.md | 8 security checks | 225 | HARDEN | Overlaps build-protocol and security-audit plugin |
| references/phase-templates.md | spec/task/ADR/handoff/state templates | 234 | DESIGN | Run layout contradicts SKILL.md state path |
| references/lint-rules.md | deterministic lint gate | 134 | slice gate | Rust/Go/Ruby/PHP sections not in your stack |
| references/modern-patterns.md | per-language "modern" checklists | 117 | SOURCE/REVIEW | Hardcoded idiom lists; 4 languages not in your stack |
| references/clean-code-defaults.md | naming, errors, types | 39 | no project convention | Keep |
| references/codebase-map-template.md | SCAN template | 63 | SCAN | Keep |
| references/cross-skill.md | contract hand-off between skills | 50 | not routed | Cites nonexistent §0.2/§4.5 |
| references/folded-planning-and-task-breakdown.md | folded skill, own frontmatter | 41 | Large plan | Odd frontmatter inside a reference |
| plugins/{api-versioning,database-migrations,dependency-audit,language-rules,security-audit,tdd-enforcer} | optional sub-skills | 57/79/54/108/166(+36)/212 | on demand | tdd-enforcer overlaps `tdd-seam` skill |
| eval/cases/01-scope-mono-build.yaml, eval/state/state.json | harness state-topology case | 32/6 | eval harness | Only one case; checks state, not behavior |

## 2. Gap audit (Step 2)

**Structure.** Tiers exist (SKILL.md:15-23) but SKILL.md is not a router (201 lines). Precedence rule exists
(:12). UI/data rules are inline one-liners (:114-126), so they always load but also never get depth.
**Overlap.** Security in 4 places; TDD in 3; review axes duplicated with external `code-review-and-quality`.
**Scope (6).** Only a layer label (be/fe/fullstack). No write vs read-only, no "read the other side", no
boundary findings with options, no reverse rule for backend-only. Evals F2, F4, F6 FAIL.
**Requirements challenge (7).** Task Brief lists assumptions and questions but never tests the request against the
repo. No basis tags, no Unknown handling, no question cap or defaults, no proposal cap, no return-to-Spec, no
decision log. R1, R4 weak.
**Evidence (8).** Strong gate 5 (:104, after-last-relevant-edit) — keep. Missing: Evidence table, red-green
proof, AC-to-test mapping outside Large, "Not verified", try-to-break-it review.
**UI/UX (9).** Screenshot pass at two widths and state coverage exist (:114-117). Missing design step,
design.md, design-system choice, playbooks, checklist. U1, U2 FAIL.
**Full-stack (10).** CONTRACT phase and TEST conformance exist (Large, fullstack). Missing consumer search, stack
block, vertical-slice wording, boundary review axis, FE validates / BE enforces rule.
**Data/infra (11).** Migration safety is good (:119, plugin). Missing schema review, EXPLAIN, architecture
"start simple, 2 options". D1, D2 FAIL.
**Other.** No red-flags file, no incoming-PR-comments flow, no standalone review flow. State resumability is
**already better than the brief** (state.json + session.md); keep it. Idioms: hardcoded lists, wrong languages.
**Bloat.** ~140 lines of Rust/Go/Ruby/PHP content; four-way security duplication; stale numbering and two broken
links; `phase-templates.md` run-index layout nobody else uses.
**Tone.** Mostly explanatory. HARD-GATE items (:95-108) give few reasons; "Automatic fail" in lint-rules.
**Description.** Good skip clause; add review / PR-comment triggers; cut length.
**Keep (do not touch):** three tiers; vague-input gate (:25-33); Bug/Refactor/Investigate/Feature modes
(:51-60); one approval checkpoint; hard gates 1-6 (commit ban, branch guard, evidence); Large phase list and
phases-large.md structure; state.json/session.md and resume table; clean-code-defaults; codebase-map-template;
contract-conformance TEST step; two-failure stop rule; AGENTS.md precedence line.

**Where I disagree with the brief (you decide):** (1) brief wants `STATUS.md`; existing `state.json` +
`session.md` already do resumability. I propose keeping them and adding `decisions` and `assumptions` to
`session.md`. (2) Brief has Trivial/Small/Large; existing Trivial/Standard/Large already covers Small. Keep
three tiers.

## 3. Prioritized changes

Each is one reviewable step; I re-run the affected baseline cases after each (Step 5) and revert any that do
not help. "Cases" = baseline IDs.

| # | Change | Problem | Expected effect | Risk |
|---|---|---|---|---|
| 1 | **Fix broken refs** (`phase-template.md` link, §0.2/§4.5, stale `[5]/[8]` numbering, runs/<slug> vs state.json layout) | baseline defects | Agents stop loading missing files or two layouts | None; edits are text-only |
| 2 | **Evidence block** in Verify/Finish: new `references/verify.md` (Evidence table, after-last-edit, red-green proof, AC-to-test map, "Not verified", try-to-break review); SKILL.md gets 2 lines | G2 G3 R5 R6 | Reports carry real command output and honest gaps | More report text on Standard; keep table to rows actually run |
| 3 | **Challenge pass** in Standard/Large: new `references/challenge.md` (basis tags, 8 lenses, max 3 questions with defaults, assumptions + decision log in `session.md`, proposals max 3 never built unapproved, return-to-Spec). Standard gets a 5-line version inside the Task Brief; full format Large only | R1-R4 | Contradictions and unknowns surfaced, not silently chosen | Over-questioning; mitigated by cap and "Standard: state assumptions, don't interrogate" |
| 4 | **Scope line** (write vs read-only) in Task Brief and SCOPE; new `references/fullstack.md` (read other side's real API, boundary problems as findings with 3 options, escalation needs approval, backend-only reverse rule, consumer search, contract-change rules, FE validates / BE enforces, stack block). Absorbs `cross-skill.md` | F1-F6 | Fixes the three FAILs; no silent edits across the boundary | Duplicates CONTRACT phase text unless I move that text into fullstack.md (I will) |
| 5 | **SKILL.md to ~130 lines, true router.** Move input gate, modes table, Large phase table, state, status, failure table into `references/workflow.md` (new) with a "Phase/condition -> read X now" table in SKILL.md. Keep hard gates inline (short, with a reason each) | structure; 201 lines | Smaller always-loaded context | Moved text must be re-linked; I diff behavior with baseline G1-G4 |
| 6 | **De-duplicate security and TDD**: SECURE tree in build-protocol becomes a pointer to harden-checks (per-slice vs cross-slice split stated once); tdd-enforcer plugin kept, but SKILL.md step 3 points to it for red-green rules instead of restating | overlap | ~150 fewer lines of duplicate text | Per-slice security prompt gets less prominent; keep a 6-line per-slice checklist |
| 7 | **UI/UX, loaded only for UI tasks:** `references/frontend-design.md` (design step, `design.md` content, design-system choice per brief 9.2/9.3, visual critique pass), `references/ui-patterns/` (hrm, crm, catalog-showcase, admin-dashboard, erp, scm, bi; ~25 lines each), `references/checklists/ui.md`. Defer to `ui-craft` for a full pipeline, unchanged | U1 U2 | Concrete screens, charts, icons, states, palette chosen before code | Playbook text goes stale; keep each file to screens/components/chart types/mistakes |
| 8 | **Data model, loaded only on schema change:** `references/data-modeling.md` (schema review with findings-as-options, EXPLAIN on realistic data, migration up/down on a copy, 5 key queries) with schema checklist merged in; `references/architecture.md` (Large new service only: start simple, 2 options + default) | D1-D3 | Flawed schemas flagged with cost/options | EXPLAIN needs a DB; if absent, goes to "Not verified" |
| 9 | **Review + PR comments:** `references/review.md` (axes, severity, confidence, cap ~10, `file:line` + fix, do-not-flag list, boundary/UI/schema conditional axes, validate each incoming comment: fix / push back / ask) | G5 G6 | Standalone review and PR-comment flows exist | Overlaps external `code-review-and-quality`; review.md links to it rather than restating its axes |
| 10 | **Red flags:** `references/red-flags.md` (the 19 rows in brief 13, grouped by phase) | rationalization | Cheap, high-signal | Only loads at Review/Verify; ~35 lines |
| 11 | **Idioms by detection, your stack only** (brief section 12 Core): `references/idioms/README.md` (how to detect versions) plus python, fastapi, pydantic, sqlalchemy-alembic, testing-python, react-typescript, tailwind, shadcn-ui, material-ui, frontend-data, testing-frontend, charts, postgres (~20-30 lines each, original wording). Replace `modern-patterns.md` and trim `lint-rules.md` / `language-rules` plugin to Python + TypeScript | hardcoded lists; unused languages | Version-correct, load-one-file idioms | Deleting Go/Rust/Ruby/PHP loses lessons learned if you use them later; they remain in `dev-craft.bak/` (decision D2) |
| 12 | **Description + why:** rewrite description (<=~500 chars; add review code, PR comments, schema/UI; keep skip clause); add one-line "why" to each hard gate and to lint "automatic fail" | trigger, tone | Better triggering on review tasks | Wider trigger could fire on questions; I test 6 should/should-not prompts |

Order is impact-first, lowest risk first: 1, 2, 3, 4, 5, 6 are core behavior; 7-9 conditional-load additions;
10-12 polish. Net size estimate: SKILL.md 201 to ~130 lines; always-loaded text shrinks; new files load only
when their condition fires. New files: workflow, challenge, verify, fullstack, review, red-flags,
frontend-design, data-modeling, architecture (9) + 7 ui-patterns + checklists/ui + 13 idioms + README. Removed:
modern-patterns.md, cross-skill.md (merged), parts of lint-rules/language-rules.

## 4. Decisions I need from you

- **D1 Live evals?** Step 3 as written needs real with/without runs. I did a static trace instead. Live runs
  need ~22 subagent runs against small fixture repos (cost: substantial) before and after. Options: (a) accept
  static baseline and run live only on the 8 highest-risk cases (G2, R1, R4, F2, F4, U1, D1, D2), recommended;
  (b) run all 22; (c) static only.
- **D2 Language deletion.** Remove Rust/Go/Ruby/PHP content from modern-patterns, lint-rules, language-rules
  (you said use only section 12). Recommended: yes; backup keeps it.
- **D3 UI playbooks.** Brief section 12 lists 7 Core domains; section 9.4 says "at least" 3. Recommended: all 7,
  capped at ~25 lines each. Alternative: 3 now, 4 later.
- **D4 Keep state.json/session.md instead of adding STATUS.md.** Recommended: keep (see section 2).
- **D5 Where evals live.** I used the existing `eval/` (not `evals/`) to keep names stable; baseline cases are
  prose in `eval/baseline/` so the harness schema in `tools/` does not try to parse them. Say if you want
  harness-format yaml per case instead.

## 5. What I did and did not do

Done: backup, full read of SKILL.md, phases-large, build-protocol, phase-templates, clean-code-defaults,
cross-skill, folded-planning, eval files; skimmed (first ~45 lines + headings) modern-patterns, lint-rules,
harden-checks, codebase-map-template and plugin frontmatter. Added: `dev-craft.bak/`, `eval/baseline/baseline.md`,
this file. Not done: live eval runs; full read of the plugin bodies and harden-checks beyond the head, so the
dedupe in change 6 is sized from headings. No git commit or staging.
