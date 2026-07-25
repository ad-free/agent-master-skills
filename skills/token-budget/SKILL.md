---
name: token-budget
description: Use when you need to enforce per-phase token caps, hard stops, and handoff triggers to prevent runaway context consumption.
metadata:
  origin: agent-master-skills
---

# Token Budget

## Overview

Enforces hard token limits per phase. When budget exhausted, forces handoff/compaction. Prevents runaway agents from burning tokens on low-value work.

**Core principle:** Budget is a constraint, not a suggestion. Hard stop means hard stop.

---

## Per-Phase Token Caps (Default)

| Phase | Cap (tokens) | Warning At | Purpose |
|-------|--------------|------------|---------|
| `ALIGN` | 8,000 | 6,400 | Scope, assumptions, design dials |
| `DESIGN` | 12,000 | 9,600 | Design system, tokens, ADRs |
| `SOURCE` | 6,000 | 4,800 | Doc fetching, version verification |
| `BUILD/slice` | 12,000 | 9,600 | Per component/page implementation |
| `REVIEW` | 8,000 | 6,400 | Multi-axis audit |
| `HARDEN` | 6,000 | 4,800 | Polish, dark mode, responsive |
| `SHIP` | 4,000 | 3,200 | Commit, docs, rollback plan |
| `HANDOFF` | 2,000 | 1,600 | Session save + resume prep |

**Total per run (dev-craft full pipeline): ~64,000 tokens max**

---

## Budget Enforcement Rules

### Warning (80%)
- Log: `TOKEN WARNING: Phase X at 80% (Y/Z tokens). Prepare to wrap up.`
- Agent MUST start closing current work
- No new sub-tasks allowed

### Hard Stop (100%)
- Log: `TOKEN LIMIT: Phase X exhausted (Y/Z tokens). HANDOFF REQUIRED.`
- Agent MUST:
  1. Save current progress to state.json
  2. Generate handoff doc
  3. Stop all work
  4. Report status to human
- **No exceptions.** Continue = budget violation.

### Overspend Penalty
If agent exceeds cap:
- Next phase budget reduced by 20%
- Human must approve continuation
- Logged in state.json for audit

---

## Budget Tracking

Track in `state.json`:

```json
{
  "tokenBudget": {
    "phase": "BUILD",
    "slice": "dashboard",
    "cap": 12000,
    "used": 9800,
    "warning": 9600,
    "status": "OK"  // OK | WARNING | EXCEEDED
  }
}
```

Update after each major tool call (Read, Write, Edit, Bash, Task).

---

## Phase Budget Allocation Strategy

| Phase | Typical Items | Buffer |
|-------|--------------|--------|
| ALIGN (8k) | Questions (500ea), stack detection (1k), scope (2k) | ~4k |
| DESIGN (12k) | Design system (4k), ADRs (1.5k×3), tokens (2k), preview (2k) | ~2.5k |
| BUILD (12k/slice) | Component (3k), tests (2k), security/lint/type (2.5k), preview (1k) | ~3.5k |
| REVIEW (8k) | Code review axes (4k), UI axes (3k), findings (1k) | — |
| HARDEN (6k) | Dark mode (1.5k), responsive (1.5k), animation (1k), cleanup (1k), security (1k) | — |

---

## Compaction Triggers

| Trigger | context-engineering Action |
|---------|---------------------------|
| Budget > 80% | Prep handoff doc, identify L0 to drop |
| Budget = 100% | Force compaction, generate handoff |
| Phase complete < 60% budget | Surplus rolls to next phase (max +20%) |
| Phase complete > 100% budget | Next phase -20%, human approval |

---

## Integration with context-engineering

Integration mirrors Compaction Triggers above: budget warning → prep handoff, hard stop → force compaction, phase complete → archive to L2, session resume → load handoff + reset budget.

---



---

## Configuration Override

Per-project `.token-budget.json`:

```json
{
  "phases": {
    "BUILD": { "cap": 15000, "warning_pct": 0.8 },
    "DESIGN": { "cap": 10000 }
  },
  "global_cap": 80000
}
```


