---
name: tdd-enforcer
description: Use when you need to enforce strict Test-Driven Development (RED-GREEN-REFACTOR) in the dev-craft BUILD phase. No production code without a failing test first.
version: 1.0.0
preamble-tier: 1
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "tdd"
  - "test driven development"
  - "red green refactor"
  - "test first"
  - "enforce tdd"
metadata:
  origin: agent-master-skills
  plugin-for: dev-craft
  phase: BUILD
  preferred-model: big-pickle
---

<!-- TOKEN CEILING: ~2K -->

# TDD Enforcer Plugin

Makes test-first non-optional for each dev-craft slice: **RED, VERIFY RED, GREEN, VERIFY GREEN, REFACTOR**.
A test that never failed proves nothing, which is why the "watch it fail" steps are the point of this plugin.
Seam and public-interface choice: `tdd-seam`. What kind of test to write: `testing-strategies`.

The red-green cycle still applies inside each slice; Test Designer tests (`references/test-agent.md`) are the
outer acceptance tests the slices must satisfy.

## Iron law

No production code without a failing test first. Code written before its test is deleted and redone from the
test; keeping it "as reference" means the test is shaped by the code instead of the requirement.
Relaxation (pure config, generated code): say so and prove the behavior another way (`workflow.md`).

## Cycle (use the project's own test runner)

1. **RED:** one minimal test, one behavior, a name that states it, real code (mock only external boundaries).
   Example: `test('retries a failing operation 3 times')` asserting both the result and the attempt count.
2. **VERIFY RED (mandatory):** run it. It must *fail*, for the right reason (feature missing, not a typo or
   setup error). It passes? You are testing existing behavior; fix the test. It errors? Fix the error until it
   fails correctly.
3. **GREEN:** the simplest code that passes. No extra features, no refactoring of other code.
4. **VERIFY GREEN (mandatory):** the test passes, the rest of the suite still passes, output has no new
   errors or warnings. Failing test means fix the code, not the test.
5. **REFACTOR:** only when green: remove duplication, improve names, extract helpers. No new behavior.
   Re-run tests.

Bug found: write the failing reproduction first, then follow the cycle; the test stays as the regression test.

## Red flags: stop, delete the code, restart from the test

Code before test; test added "later"; test passed immediately; cannot explain why it failed; "I tested it
manually"; "keep as reference"; "just this once"; "deleting is wasteful". Each is a rationalization for
skipping the one step that gives the test meaning.

## When stuck

| Problem | Do |
|---|---|
| Don't know how to test | Write the wished-for API call and the assertion first |
| Test too complicated | The design is too complicated; simplify the interface |
| Must mock everything | Code is too coupled; inject dependencies |
| Huge test setup | Extract helpers; still complex means simplify the design |

## Slice done when

Every new function has a test; each test was seen failing for the expected reason; all tests pass; edge cases
and error paths covered. Stage the files and propose a message; do not commit (`SKILL.md` hard gate 1).
