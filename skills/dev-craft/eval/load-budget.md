# Loading budget (WP7)

Script: `eval/measure-load.sh [skill_dir]` sums the lines of the files the `SKILL.md` read-now table loads per
scenario (worst case: includes fallback checklists even when the related skill is installed). Counts are lines of
references only, not tokens.

| Scenario | Before WP7 | After build-protocol split | After Large-only move | Target (Standard) |
|---|---|---|---|---|
| Trivial edit | 106 | 107 | 107 | n/a |
| Standard bug fix | 810 | 623 | 575 (583 at final audit) | ~450 |
| Standard FE-only feature | 910 | 723 | 675 | ~450 |
| Standard schema change (risk flag) | 993 | 806 | 758 | ~450 |
| Large full-stack feature | 1853 | 1672 | 1677 | n/a |
| Large UI app | 1769 | 1582 | 1587 | n/a |

The third column moved the Large path, State and Resume sections from `workflow.md` (149 to 101 lines) to
`phases-large.md` (147 to 200). Proposal 2 (count fallback checklists only when the skill is missing) was
declined: it changes the count, not the skill.

"Before" = state at the end of round 5 (after WP1-WP3 and the eval fixes), measured with the same script.

## Done (approved)

`build-protocol.md` 215 -> 27 lines. The SECURE decision tree duplicated `checklists/security.md`; its unique items
(regex/ReDoS, outbound URLs, webhooks, critical-action logging) moved into that checklist. Worktree mode and the
multi-repo branch script moved verbatim to `build-extras.md` (72 lines), routed from `SKILL.md` only for parallel
agents, 3+ modules or multi-repo work. MATCH and the rules were condensed, not dropped.

## Still above target; proposals (not applied, need your approval)

Standard bug fix is 623 lines for a ~450 target.
1. Move the Large-only parts of `workflow.md` (Large path, State, Resume, Failure handling) into `phases-large.md`:
   about -55 lines for every Standard task.
2. `checklists/bugs.md` and `checklists/testing.md` are fallbacks used only when the related skill is missing. With
   those skills installed the real Standard load is about 77 lines lower (about 546).
3. After 1 and 2, Standard is about 490: close to target. Further cuts would trim `SKILL.md` (107) or `verify.md` (80);
   I would not do that without eval evidence.

Final-audit re-measure: Standard bug fix 583, FE-only 683, schema 769, Large full-stack 1685, Large UI 1595. The +8 to +11
lines come from later rule edits in `verify.md` and `workflow.md` (red-proof wording, demo-script scope, characterization step).

## Round 3 trim (2026-11-12, applied)

After the Phase 2 skill pruning the checklists always load (their skills are archived), so the fallback
discount above no longer applies. Standard bug fix 607 -> 490 by moving content, not removing rules:
idioms verification log -> `idioms/VERIFIED.md`; Input gate -> `input-gate.md`; `workflow.md` layer rules and
failure handling cut to what `AGENTS.md` and other loaded files do not already say; requirement matrix ->
`test-agent.md`, demo script -> `phases-large.md` §SHIP-PREP; `verify.md` "By kind of change" points at the files
that own each check; 11 red-flag rows that restate loaded rules removed. One rule change:
`clean-code-defaults.md` loads only when the repo has no linter config or settled pattern (529 in that case).
Evals (2 headless runs per arm per case, before = `7948d26`): t07, t12 4/4 in both arms; t09 equal; t11 equal or
better (independent check 0/2 -> 1/2). t02 and t04 re-run with hooks off for the eval runs only (the
`skill-gate.sh` hook blocks edits when the Skill tool is disallowed): t04 4/4 in all four runs; t02 before 5/5
and 4/5, after 5/5 and 5/5 (mutation check in 3 of 4 runs). Local detail: `results/load-budget-trim.md` (gitignored).

## Round 4: workflow gates (2026-11-24, branch `feat/workflow-gates`)

Load: Standard bug fix 493 -> 498 (rules that must fire on small tasks moved into `SKILL.md` rows, no new lines).
Runner `eval/run_behavior.py`, Sonnet, headless, hooks and Skill tool off; 33 runs, $3.98 total ($0.12 average).
"Before" = live master copy. Rubric items passed on the final skill text (latest runs per case):

| Case | Before (master) | After (final text) | Note |
|---|---|---|---|
| t13 no AGENTS.md | 1/4 | 12/12 (3 runs) | first run 1/4: rule lived only in `workflow.md`, which small tasks never read |
| t14 authz failure cases | 3/4 | 12/12 (3 runs) | planted `get_note` owner gap found only after the "neighbouring endpoints" clause |
| t15 ui-verifier dispatch | 1/4 | 8/8 (2 runs) | one earlier miss traced to `frontend-design.md` §5 telling the main agent to screenshot (fixed) |
| t12 runnable gate (regression) | - | 12/12 (3 runs) | |
| t01 misread requirement (regression) | 3/4 | 8/12 (3 runs) | R1 `Source:` tags 0/3 in both arms: no run shows a brief |
| t02 money split (regression) | 3/4 | 12/16 (4 runs) | R4 verifier 0/4: now named under "Not done", never dispatched |

Total after: 64/72 (89%). Open: (1) headless Sonnet never prints a Task Brief (`REQ-n`, `Source:`), master
and branch alike, despite hard gate 3; (2) `verifier` is not dispatched on risk-flagged work after two wording
attempts. Both need a mechanical check, not more text.
