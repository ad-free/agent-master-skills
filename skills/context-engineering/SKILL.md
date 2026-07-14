---
name: context-engineering
description: "Manage agent context: setup, memory hierarchy, session continuity, context rotation. Ensures agents have the right information at the right time."
metadata:
  origin: agent-master-skills
---

# Context Engineering

## Overview

Every agent session has a limited context window. Without discipline, context fills with irrelevant detail, quality degrades, and sessions collapse into incoherence.

This skill provides structured systems for: setup at session start, a five-level memory hierarchy, rotation before token limits, cross-session handoff, and context pollution prevention.

**Core principle:** Context is a finite resource. Budget it like memory, rotate it like logs, clean it like a surgical theatre.

---

## When to Activate

| Scenario | Action |
|----------|--------|
| **Starting a long session** | Initialize memory hierarchy, load domain.md + plan.md |
| **Switching between tasks** | Rotate working context, keep domain + plan + ADRs |
| **Context nearing token limit** | Generate handoff, split across sessions |
| **Resuming from handoff** | Load state.json + latest session + domain.md + plan.md |
| **Coordinating multiple agents** | Slice context per agent, master maintains holistic view |
| **Agent quality degradation** | Check context pollution — likely too much stale detail |

**When NOT to activate:** Single-turn queries, trivial lookups, sessions under 2k tokens.

---

## The Iron Law

```
NO AGENT WITHOUT CONTEXT DISCIPLINE
```

Context drift is the #1 cause of hallucination, missed requirements, and contradictory outputs. Every agent — autonomous, assisted, or embedded — must operate within a defined context budget.

---

## Memory Hierarchy

Five levels, each with distinct persistence and access cost.

### Level 1 — Working Context (~4k tokens)

Volatile. What the agent needs right now for the current phase.

```
Active phase requirements
Task details, partial results, immediate decisions
```

**Discard on phase completion.** Do not carry Phase 3 details into Phase 5.

### Level 2 — Project Context (persistent)

Long-lived project knowledge stored in `.dev-craft/`. Always available (compressed).

| File | Purpose |
|------|---------|
| `state.json` | Current phase, completed slices, stack |
| `domain.md` | Domain model, entities, glossary |
| `plan.md` | Architecture plan with ADRs |
| `build-order.md` | Module dependency sequencing |

### Level 3 — Skill Context (on-demand)

SKILL.md files loaded via `skill(name="...")`. Retained only while active, released on phase exit.

### Level 4 — Reference Context (external)

Fetched as needed: official docs, codebase files, MDN. Load only what's needed — never entire framework docs.

### Level 5 — Handoff History (archival)

Session records in `.dev-craft/sessions/session-YYYYMMDD-N.md`. Only the latest is loaded on resume.

```
Persistence:     Working < Project < Skill < Reference < Handoff
Token cost:      High    > Medium   > Low   > On-demand > Archival
```

---

## Context Budget Management

### Phase Budgets

```
Phase             Typical   Hard Limit   Collapse Action
REQUIRE           2k        4k           "Requirements too broad. Narrow scope."
ALIGN             3k        6k           "Too many assumptions. Reduce scope."
DESIGN            4k        8k           Handoff — split design across sessions.
BUILD             8k        16k          Handoff — split slices across sessions.
REVIEW            4k        8k           Handoff — review in batches.
HARDEN            6k        12k          Handoff — split audit across sessions.
```

### Protocol

- **< 50%** — Continue normally
- **50-70%** — Monitor
- **70-85%** — Warn user, prepare handoff
- **85-100%** — Generate handoff + stop. Resume in new session.

### Token Estimation

```
1 KB markdown text    ≈ 250 tokens
1 KB source code      ≈ 350 tokens
1 SKILL.md file       ≈ 2-4k tokens
1 handoff document    ≈ 1-2k tokens
1 file read via tool  ≈ 1-2k tokens
```

Estimate before loading. If a doc is 3k tokens and only 1k remains in budget, do not load — find a smaller reference.

---

## Context Rotation Protocol

### At 70% full (~5k tokens remaining in 16k window):

1. **Generate handoff** to `.dev-craft/sessions/session-YYYYMMDD-N.md`:
   - Current phase + completed phases
   - Completed slices/modules
   - Active decisions (ADRs in progress)
   - Next steps (ordered)
   - Known issues / blockers

2. **Save state.json** with `currentPhase`, `completed`, `currentSlice`, `handoff` reference

3. **Tell user:**
   ```
   Context nearing limit. Session saved to sessions/session-YYYYMMDD-N.md.
   Run same command to resume — state loads automatically.
   ```

### On Resume:

1. Detect `state.json` → load current phase + slices
2. Load latest handoff from `sessions/`
3. Load `domain.md` + `plan.md` into Level 2
4. Skip completed phases, resume at current phase
5. Report: "Resuming [phase]. Completed [list]. Next: [next step]."

---

## Cross-Agent Context

When using `agent-orchestration` or `dispatching-parallel-agents`, each agent gets only its slice:

```
Master Agent:    Full domain + plan + ADRs + integration view + shared contract
Backend Agent:   API contract + backend domain subset + data model + backend conventions
Frontend Agent:  API contract + UI domain subset + design tokens + frontend conventions
Mobile Agent:    API contract + mobile domain subset + platform conventions + glossary
```

**Rules:**
1. No agent needs the full project context — only what's relevant
2. Shared context is limited to: API contract, compressed domain model, conventions, glossary
3. Master agent maintains the holistic view and resolves conflicts
4. Per-agent handoffs stored in `.agent-orchestration/sessions/`
5. Context isolation prevents backend details leaking into frontend agent

---

## Context Pollution Prevention

### Sources of Pollution

| Source | Prevention |
|--------|------------|
| Stale phase details | Purge after phase completion |
| Overloaded references | Fetch only the needed API surface, not entire docs |
| Redundant file reads | Cache references, don't re-read |
| Debug output dumps | Summarize, don't paste raw |
| Obsolete decisions | Keep only latest ADR per topic |
| Q&A back-and-forth | Summarize decisions, discard conversation |

### Cleanup Protocol

**After every phase or slice:**
- Remove phase-specific detail (questions, alternatives, temporary results)
- Remove verbose tool output
- Compress domain.md and plan.md if > 3k tokens each
- Keep only: compressed domain model, plan + current ADRs, conventions + glossary, state.json

**ADR compression rule:**
- Keep only the latest ADR per topic
- Superseded ADRs: one-line note + reference to superseding ADR

**Chesterton's Fence:** Do not compress active decisions. Compress completed work summaries first, reference material second, active decisions last.

---

## Integration with Skills

### dev-craft

Every dev-craft phase has a context budget. The HANDOFF phase follows this skill's rotation protocol.

### agent-orchestration

Master agent loads this skill for context slicing. Each worker gets a Level 2 subset via `.agent-orchestration/state.json`.

### dispatching-parallel-agents

Each parallel task gets an isolated context slice. Shared context limited to: API contract, conventions, glossary.

### quality-gates

Gate 5 (LLM-Judge) operates within defined budget. If diff > 4k tokens, split into chunks per quality-gates chunking rules.

---

## Gotchas

### 1. Context Mixing

Backend details leak into frontend agent context, causing UI decisions based on API internals.

**Fix:** Partition domain model explicitly. Each agent gets only its slice.

### 2. Token Estimation Drift

Agents consistently misestimate token usage (e.g., a 50-line file with long lines = 1.5k tokens, not 0.5k).

**Fix:** Use estimation guidelines. Estimate high. Recalibrate if actual is consistently 2× estimate.

### 3. Stale Context

Agent uses outdated plan or superseded ADRs after project has evolved.

**Fix:** On every phase transition and resume, re-read plan.md, domain.md, latest ADRs. Discard cached versions.

### 4. Handoff Accumulation

15 handoff documents, none clearly the latest.

**Fix:** Strict naming: `session-YYYYMMDD-N.md`. Maintain `sessions/index.md` pointing to latest. state.json always references current handoff.

### 5. Over-Compression

Critical context compressed into vague summaries that lose decision rationale.

**Fix:** Compress completed work summaries, never active decisions. Reduce reference material first.

### 6. Cross-Session State Drift

state.json says BUILD but implementation hasn't caught up.

**Fix:** Update state.json only after demonstrable phase completion. Run verification-before-completion first. No optimistic state writes.

### 7. Tool Output Bloat

A single bash/read call returns 10k+ lines that bloat context.

**Fix:** Use output limits, grep for patterns, summarize. If output > 2k lines, summarize before adding to context. "If I wouldn't read it all, I shouldn't paste it all."

---

## Verification Checklist

- [ ] Memory hierarchy loaded: Level 1 (working) + Level 2 (domain.md, plan.md, state.json)
- [ ] Context budget tracked for current phase under hard limit
- [ ] Phase-completed working contexts purged (no stale detail)
- [ ] Handoff generated if context > 70% full with standard format
- [ ] State.json updated with current phase and handoff reference
- [ ] Latest handoff loaded on resume (not an old one)
- [ ] Cross-agent context sliced per role — no leaking across boundaries
- [ ] ADRs and decisions from latest session, not stale

---

## See Also

- `dev-craft` — Full-stack pipeline with HANDOFF phase
- `agent-orchestration` — Multi-agent builds with per-agent context slicing
- `dispatching-parallel-agents` — Parallel execution with isolated context
- `quality-gates` — LLM-Judge context budget for evaluation
- `verification-before-completion` — Evidence gates for state.json accuracy
- `skills/SHARED.md` — Cross-skill communication and handoff format
