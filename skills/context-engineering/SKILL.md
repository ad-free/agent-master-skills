---
name: context-engineering
description: |
  Context management system: memory hierarchy, rotation, handoff, pollution prevention.
  Use for long sessions, multi-agent coordination, session resumption, and context budgeting.
  Invoked by: all agents at session start, context-guard, orchestrator.
version: 2.0.0
preamble-tier: 1
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "manage context"
  - "session context"
  - "prevent context drift"
  - "resume session"
  - "handoff context"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  memory-levels: 5
  integrates-with: [learn, retro, dev-craft, agent-orchestration, token-budget, cost-optimizer, handoff, context-guard]
---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

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

Long-lived project knowledge stored per run in `.dev-craft/` (registry in `.dev-craft/index.json`). Always available (compressed).

> **Multi-repo note:** when dev-craft's SCOPE gate reports `topology: multi` (separate BE + FE repos), each repo keeps its own `.dev-craft/` / `.ui-craft/` state. Shared knowledge (the API contract, the SCOPE record) lives in `contractRepo` (the BE repo) and is referenced by the other repo — do not duplicate it per repo. Handoffs that span repos must name which repo's `.dev-craft/` they live in.

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

Session records in `.dev-craft/session-YYYYMMDD-N.md`. Only the latest is loaded on resume.

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

 1. **Generate handoff** to `.dev-craft/session-YYYYMMDD-N.md`:
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

When using `agent-orchestration` or `dispatching-parallel-agents`, each agent gets only its slice. Shared context is limited to: API contract, compressed domain model, conventions, glossary. Master agent maintains the holistic view; per-agent handoffs stored in `.agent-orchestration/`. See `agent-orchestration` for per-role context breakdown.

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

| Gotcha | Fix |
|--------|-----|
| Context Mixing — backend details leak into frontend | Partition domain model explicitly per agent |
| Token Estimation Drift — misestimating token usage | Estimate high; recalibrate if consistently 2× off |
| Stale Context — outdated plan or ADRs | Re-read plan.md, domain.md, latest ADRs on every phase transition |
| Handoff Accumulation — many docs, none clearly latest | `session-YYYYMMDD-N.md` naming; `state.json` always references current |
| Over-Compression — critical context lost in vague summaries | Compress completed work only; never active decisions |
| Cross-Session State Drift — state.json out of sync | Update only after demonstrable phase completion |
| Tool Output Bloat — 10k+ lines from single call | Use output limits, grep, summarize |

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
- [ ] Token budget tracked via `token-budget` skill
- [ ] Cost tracking via `cost-optimizer` skill

---

## Outputs / Handoffs

On context rotation (>70%): invokes `skill("handoff")` with context:
  - `handoffPath`: ".dev-craft/runs/<slug>/handoff-<timestamp>.md"
  - `statePath`: ".dev-craft/runs/<slug>/state.json"

On session resume: loads `handoff` + `state.json` + `domain.md` + `plan.md`

On cross-agent coordination: invokes `skill("agent-orchestration")` for context slicing

---

## See Also

- `dev-craft` — Full-stack pipeline with HANDOFF phase
- `agent-orchestration` — Multi-agent builds with per-agent context slicing
- `dispatching-parallel-agents` — Parallel execution with isolated context
- `quality-gates` — LLM-Judge context budget for evaluation
- `verification-before-completion` — Evidence gates for state.json accuracy
- `skills/references/handoff-protocol.md` — Standardized handoff format
- `skills/SHARED.md` — Cross-skill communication and handoff format