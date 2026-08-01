---
name: systematic-debugging
description: |
  Systematic root-cause investigation for bugs, failing tests, and unexpected
  behavior. Use when something is broken and the cause is unknown. Do NOT use
  for adding new features (see dev-craft), for security audits (see bug-hunting),
  or for one-off fixes without understanding the root cause.
  
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
  - Task
triggers:
  - "debug this"
  - "investigate bug"
  - "failing test"
  - "unexpected behavior"
  - "root cause"
  - "systematic debugging"
  - "why is this broken"
  - "trace the error"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 2.0.0
  domain: quality-safety
  integrates-with: [debugging-and-error-recovery, dev-craft]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# systematic-debugging

## Relationship to existing skills

- debugging-and-error-recovery: Handles general debugging workflows; systematic-debugging enforces a structured root-cause methodology.
- dev-craft: Provides the engineering pipeline; systematic-debugging is invoked when a bug blocks a dev-craft phase.
- bug-hunting: Security-focused vulnerability discovery; systematic-debugging is for functional/behavioral bugs.
- code-review-and-quality: Validates that the fix does not introduce new issues; systematic-debugging produces the fix that code-review-and-quality then reviews.

## When to Use

- A test is failing and the cause is not obvious
- Application behavior does not match expectations
- An error occurs intermittently or under specific conditions
- A performance regression was introduced and the cause is unknown
- A bug has been reported and the root cause has not been identified
- After a merge that introduced a regression and the scope of the problem is unclear

## When NOT to Use

- Adding new features or functionality — see dev-craft
- Security vulnerability discovery — see bug-hunting
- Performance optimization of working code — see dev-craft/plugins/performance-profiling
- One-off fixes where the root cause is already known and the fix is trivial
- Reviewing an existing fix for quality — see code-review-and-quality

## Workflow

### Phase 1: Reproduce

1. **Confirm the bug exists**: run the failing test or reproduce the unexpected behavior
2. **Isolate the conditions**: what inputs, environment, or state trigger the bug?
3. **Minimize the reproduction**: reduce the test case or scenario to the smallest possible example
4. **Document the reproduction**: write down the exact steps, inputs, and observed output vs. expected output
5. **Check recent changes**: what was changed recently that could have introduced this?

### Phase 2: Hypothesize

1. **List all possible causes**: brainstorm every plausible explanation for the observed behavior
2. **Rank hypotheses by likelihood**: consider recent changes, code complexity, and known failure modes
3. **Define a falsification test for each hypothesis**: what would prove each hypothesis wrong?
4. **Select the most likely hypothesis to test first**

### Phase 3: Investigate

1. **Add instrumentation**: add logging, tracing, or assertions to narrow down the problem
2. **Execute the falsification test**: run the test that should prove or disprove the leading hypothesis
3. **If hypothesis is falsified**: move to the next hypothesis and repeat
4. **If hypothesis is confirmed**: narrow down to the exact line or condition causing the bug
5. **Trace the execution path**: follow the code from the symptom back to the root cause
6. **Identify the root cause**: what is the fundamental issue, not just the symptom?

### Phase 4: Fix

1. **Write the fix**: make the minimal change that addresses the root cause
2. **Do not treat symptoms**: if the fix only addresses the symptom, re-evaluate the root cause
3. **Run the reproduction test**: confirm the bug is fixed
4. **Run the full test suite**: ensure no regressions were introduced
5. **Check edge cases**: does the fix handle boundary conditions and error paths correctly?

### Phase 5: Prevent Recurrence

1. **Add a test**: write a test that would catch this bug if it regresses
2. **Update documentation**: if the bug revealed a misunderstanding, update relevant docs or comments
3. **Add a lint/typecheck rule** if the bug was caused by a pattern that could be statically detected
4. **Update the changelog or ADR** if the fix represents a significant architectural decision
5. **Root cause analysis**: document what caused the bug and how it was found

## Context Management

- Track debugging state in `.dev-craft/debug/<project>/state.json` with fields: `session_id`, `bug_description`, `hypotheses`, `confirmed_root_cause`, `fix_applied`, `tests_added`, `status`
- On session resume, check state.json for any in-progress debugging session and continue from the last completed phase
- Persist reproduction steps and root cause analysis for future reference

## Tool Definitions

| Tool | Purpose | Constraints |
|------|---------|-------------|
| Read | Read source code, test files, and configuration | Focus on the area around the bug and recent changes |
| Write | Create reproduction tests and documentation | Follow existing test conventions |
| Edit | Make the minimal fix | Only fix the root cause; do not refactor unrelated code |
| Bash | Run tests, add instrumentation, execute reproduction steps | Run the reproduction test first, then the full suite |
| Grep | Search for related code, error messages, or patterns | Search within the affected module and its dependencies |
| Glob | Find test files and related source files | Pattern: `<module>/**/*.py` (or relevant extension) |
| Task | Spawn subagent for deep code investigation | Subagent must report findings, not make edits |

## Output Contract

On completion, the skill must produce:

1. A root cause analysis document including: reproduction steps, hypotheses tested, confirmed root cause, and fix applied
2. The minimal code fix addressing the root cause
3. A regression test that would catch this bug if it recurs
4. Updated state.json with the debugging session results
5. A summary of any documentation or lint rules added to prevent recurrence

## Quality Gates

- [ ] Bug is reproduced before any fix is attempted
- [ ] Root cause is identified, not just the symptom
- [ ] Fix is minimal and addresses the root cause
- [ ] Reproduction test passes after the fix
- [ ] Full test suite passes with no regressions
- [ ] Edge cases are handled correctly
- [ ] Root cause analysis is documented
- [ ] A regression test was added

## Error Handling

- **Cannot reproduce the bug**: document the conditions that failed to reproduce, escalate to the user with the observed discrepancy
- **Hypothesis elimination takes too long**: escalate to a deeper investigation (Task subagent for codebase exploration, or bug-hunting for security-related issues)
- **Fix introduces a regression**: revert the fix, re-evaluate the root cause, and try a different approach
- **Root cause is in a dependency**: document the dependency issue, check for patches or workarounds, and escalate if needed
- **Bug is intermittent**: add more instrumentation, increase test coverage for the affected area, and run extended test cycles