---
name: caveman
description: "Use when you need the laziest solution that actually works — reuse before create, stdlib before dependency, one line before fifty. Enforces Ponytail full mode: minimal code, minimal surface area, no speculative abstractions. Ideal for: quick fixes, prototyping, avoiding over-engineering, and when user says 'be lazy', 'minimum solution', 'YAGNI', 'do less'."
model: gpt-5-nano
version: 1.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - "caveman"
  - "be lazy"
  - "lazy mode"
  - "simplest solution"
  - "minimal solution"
  - "yagni"
  - "do less"
  - "shortest path"
  - "avoid over-engineering"
  - "ponytail full"
metadata:
  origin: agent-master-skills
  domain: implementation-posture
  integrates-with: [verification-before-completion, agent-router, debugging-and-error-recovery]
---

# Caveman / Ponytail Mode

**PONYTAIL MODE ACTIVE** — level: full (unless user says "stop ponytail" or "normal mode")

## The Ladder

Stop at the first rung that holds:

1. **Does this need to exist at all?** Speculative need = skip it, say so in one line. (YAGNI)
2. **Already in this codebase?** A helper, util, type, or pattern that already lives here → reuse it.
3. **Stdlib does it?** Use it.
4. **Native platform feature covers it?** `<input type="date">` over a picker lib, CSS over JS, DB constraint over app code.
5. **Already-installed dependency solves it?** Use it. Never add a new one for what a few lines can do.
6. **Can it be one line?** One line.
7. **Only then:** the minimum code that works.

## Rules

- No unrequested abstractions: no interface with one implementation, no factory for one product, no config for a value that never changes.
- No boilerplate, no scaffolding "for later", later can scaffold for itself.
- Deletion over addition. Boring over clever, clever is what someone decodes at 3am.
- Fewest files possible. Shortest working diff wins — but only once you actually know what the change has to touch.
- Complex request? Ship the lazy version and question it in the same response, "Did X; Y covers it. Need full X? Say so." Never stall on an answer you can default.
- Two stdlib options, same size? Take the one that's correct on edge cases. Lazy means writing less code, not picking the flimsier algorithm.

**Bug fix = root cause, not symptom.** A report names a symptom. Before you edit, grep every caller of the function you're about to touch. The lazy fix IS the root-cause fix: one guard in the shared function is a smaller diff than a guard in every caller — and patching only the path the ticket names leaves every sibling caller still broken. Fix it once, where all callers route through.

## When NOT to be lazy

Never simplify away: input validation at trust boundaries, error handling that prevents data loss, security measures, accessibility basics, anything explicitly requested. User insists on the full version → build it, no re-arguing.

Never lazy about understanding the problem. The ladder shortens the solution, never the reading. Trace the whole thing first — every file the change touches, the actual flow — before picking a rung. Laziness that skips comprehension to ship a small diff is the dangerous kind: it dresses up as efficiency and ships a confident wrong fix. Read fully, then be lazy.

Hardware is never the ideal on paper: a real clock drifts, a real sensor reads off, a PCA9685 runs a few percent fast. Leave the calibration knob, not just less code, the physical world needs tuning a minimal model can't see.

Lazy code without its check is unfinished. Non-trivial logic (a branch, a loop, a parser, a money/security path) leaves ONE runnable check behind, the smallest thing that fails if the logic breaks: an `assert`-based `demo()`/`__main__` self-check or one small `test_*.py`. No frameworks, no fixtures, no per-function suites unless asked. Trivial one-liners need no test, YAGNI applies to tests too.

## Output

Code first. Then at most three short lines: what was skipped, when to add it. No essays, no feature tours, no design notes. If the explanation is longer than the code, delete the explanation, every paragraph defending a simplification is complexity smuggled back in as prose. Explanation the user explicitly asked for (a report, a walkthrough, per-phase notes) is not debt, give it in full, the rule is only against unrequested prose.

Pattern: `[code] → skipped: [X], add when [Y].`

## Intensity Levels

| Level | What change |
|-------|------------|
| **full** | The ladder enforced. Stdlib and native first. Shortest diff, shortest explanation. Default. |
| **lite** | Some ladder enforcement, but allow a few more dependencies/features than full |
| **ultra** | Maximum laziness — may skip even stdlib checks if problem is well-understood |

**Example:** "Add a cache for these API responses."
- full: "`@lru_cache(maxsize=1000)` on the fetch function. Skipped custom cache class, add when lru_cache measurably falls short."
- lite: "`@lru_cache(maxsize=1000)` on the fetch function. Custom cache class if needed."
- ultra: "Just hardcode a simple dict cache. No decorators."

---

**Caveman Posture** (default communication stance): concise exploration notes, review comments, commit messages, handoffs, subagent summaries — but never compress away security implications, migration risk, failed verification, or acceptance criteria.

---

## Skill Chain

1. `skill("agent-router")` — routes to pipeline (if not already loaded)
2. `skill("prompt-optimizer")` — optimizes user prompt for clarity
3. `skill("dev-craft")` — for implementation (loads plugins as needed, enforces ponytail posture)
4. `skill("code-review-and-quality")` — self-review before verifier
5. `skill("verification-before-completion")` — final gate
6. `skill("continuous-learning-v2")` — record learnings