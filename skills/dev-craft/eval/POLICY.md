# Eval policy (dev-craft)

Goal: at least 95% of rubric items pass across trials, and no case scores 0 in any arm. Evals measure known
failure kinds; the weekly real-task sample finds new ones.

## When to run what (cost-balanced)

| Moment | Cases | Trials | Arms |
|---|---|---|---|
| A skill file changed (quick check) | cases covering the changed section | 1 | after |
| Before merging a skill change | same cases | 2-3 | before (master copy) and after (branch) |
| Weekly or before a release | all cases plus the held-out set | 2 | after |
| New case added | the new case | 1 before, 2 after | proves the case can tell the two apart |

Runner: `uv run --no-project --with pyyaml python skills/dev-craft/eval/run_behavior.py <case> <skill_dir>
<label> --run N` (Sonnet, `--max-budget-usd 2.5` per run by default, hooks and the Skill tool off). "Before" points
`<skill_dir>` at `~/.local/share/agent-master-skills-live/skills/dev-craft` (master); "after" at this branch. Runs
that need the browser (t15) go one at a time; the others can run in parallel.
Runs are **not sandboxed** (`bypassPermissions`, your real `$HOME`, network and MCP servers, hooks off): run
only cases and skill copies you have read, and never a skill branch from someone else without reading its diff.

Grading: read `report.md`, `tools.txt`, `tests.txt` and `git -C repo diff` per run against the case rubric.
Deterministic checks (`files`, `not_contains`, tests exit code, tool names in `tools.txt`) first; judgment only for
the rest. Record pass counts and `total_cost_usd` per run in `load-budget.md` or the round's results file.

## Held-out cases

`t03-false-positive-trap`, `t08-business-rule`, `t10-mutation-spot-check`. Do not open them while editing a skill;
run them only at the weekly or release check. If they drop while the others rise, the edits fit the tests, not the
behavior.

## Real-task sample

Weekly, rate 3 real tasks (pass / partial / fail on: brief matched intent, gate passed, nothing broken). Every
fail becomes a new case through `/lessons`.
