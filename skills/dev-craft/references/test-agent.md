# Test agent

The agent that writes the code also writes its tests and its verification, so it shares its own misreadings.
This file is a thin contract for separating those roles. It routes to sibling skills and does not repeat them.

Uses, when installed: `testing-strategies` (what kind of test, edge cases), `tdd-seam` (public seams), `fe-visual-loop` / `playwright-skill` (screenshots), `dispatching-parallel-agents` (running
subagents). If one is absent, follow this file and `checklists/testing.md` alone.

## When to use

| Tier | Use |
|---|---|
| Trivial | never |
| Standard | only with a risk flag: money, authorization, personal data, migration, contract change, concurrency, or the user asks |
| Large | always, unless the user opts out |

## Roles (separate subagents or sessions when the environment supports them)

1. **Test Designer** (after TRACE, before BUILD)
   - Input: brief with `REQ-n`, examples and `Invariants:`, contract, schema, test conventions. It must **not**
     see the implementation.
   - Output: a plan table `REQ -> cases (happy, edge, error, authorization, concurrency)`, failing acceptance
     and contract tests in the project's style, and a test or check per invariant.
   - The main agent implements until they pass. It may not weaken or delete them. A disputed test goes back to
     the brief (Challenge), not into a silent edit.
2. **Verifier** (in TEST, after Implement)
   - Input: brief, the diff, how to run things, the stack block. Read-only on production code; may add tests
     in test directories.
   - Runs fresh: full suite, lint, type check, migration up/down/up, contract check, end-to-end checks, and the
     "3 most likely to break" cases. Spot-checks test strength by reverting or altering the fix and confirming
     a test fails (then restores it). Checks every `REQ` has a test and every contract error has a UI path.
     Fills the `Independent check` column of the requirement matrix (`verify.md`).
   - Reproduces every finding before reporting it and tags it Confirmed / Cited / Suspected (`review.md`).
3. **UI Verifier** (UI tasks, in TEST)
   - Runs the app, screenshots at 1440 and 390, reads console errors, walks `checklists/ui.md`, returns
     screenshot paths and findings.

## Handoff packet (main agent fills one per subagent)

```markdown
Role: <Test Designer | Verifier | UI Verifier>
Goal and REQs: <REQ-n with examples and sources, Invariants>
Scope: <write/read-only line>
Stack block: <commands for tests, lint, types, migrations, e2e>
Files/diff: <paths or git range>   (Test Designer: do NOT include implementation)
Allowed edits: <test directories only | none>
Must not: weaken tests, edit production code, commit, touch files outside scope
Return: <format below>
```

## Return format

Evidence table rows (command, real output trimmed), findings list
`[severity | confidence | state] path:line, reproduction, suggested fix`, "Not verified" with reasons, and the
exact commands to reproduce.

## Reconciliation (main agent)

- Re-run at least the single most important command yourself; record `verified by: <role>, re-run by main: yes`.
- Triage every finding: fix, push back with code or test evidence, or ask. Log decisions in the decision list.
- At most two fix-and-reverify loops, then summarize and ask.
- Subagent output is evidence only if it contains real command output from this session produced after the last
  edit. "All tests pass" without output is Weak.

## Fallback (no subagents)

Write the test plan from the brief before re-reading the implementation, then run the Verifier checklist. Under
"Not verified" write: `independence not achieved: same agent`.

## Cost

Verifier and UI Verifier may use a smaller or faster model where the environment allows; the main agent keeps
the decisions.
