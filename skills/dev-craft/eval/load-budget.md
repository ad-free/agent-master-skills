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
