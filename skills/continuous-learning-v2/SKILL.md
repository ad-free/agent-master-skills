---
name: continuous-learning-v2
description: |
  Instinct-based continuous learning system with confidence scoring.
  Automatically extracts patterns from sessions, stores them as instincts,
  and injects relevant instincts at session start. Use for persistent
  cross-session learning and pattern recognition.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
triggers:
  - "learn from this session"
  - "extract patterns"
  - "save instinct"
  - "show instincts"
  - "prune instincts"
  - "import instincts"
  - "export instincts"
  - "evolve instincts"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 1.0.0
  domain: context-memory
  integrates-with: [context-engineering, retro, handoff, agent-router]
---
TOKEN CEILING: ~4K tokens. If skill exceeds, extract sections to references/.

# Continuous Learning v2 — Instinct-Based Learning

Instinct-based learning system that automatically extracts reusable patterns from sessions,
stores them with confidence scores, and injects relevant instincts at session start.

## Core Concepts

### Instinct
A learned pattern with:
- **pattern**: The recurring pattern (code, workflow, decision, convention)
- **context**: When/where it applies (file patterns, task types, tech stack)
- **confidence**: 0.0-1.0 score based on successful applications
- **source**: Session ID, timestamp, trigger
- **applications**: Count of successful uses
- **last_used**: Timestamp of last successful application

### Instinct Lifecycle
1. **Extracted** → From session analysis (retro, handoff, explicit save)
2. **Quarantined** → Low confidence (<0.5), needs validation
3. **Active** → Confidence ≥0.5, injected at session start
4. **Promoted** → Cross-project ready (confidence ≥0.8, 5+ applications)
5. **Archived** → Superseded or stale (not used in 90 days)

## Storage

```
~/.agent-master-skills/learning/
├── instincts.jsonl          # All instincts (append-only)
├── instincts-index.json     # Searchable index by context
├── project-learnings/       # Per-project instincts
│   └── <project-hash>/
│       ├── instincts.jsonl
│       └── index.json
└── global-promoted/         # Promoted cross-project instincts
    └── instincts.jsonl
```

## Extraction Triggers

| Trigger | When | What it captures |
|---------|------|------------------|
| SessionEnd | Every session | Decisions, patterns, conventions, fixes |
| Retrospective | Weekly/milestone | Cross-session patterns, architectural decisions |
| Explicit save | User says "save this pattern" | Specific pattern with context |
| Bug fix | debugging-and-error-recovery | Root cause pattern, fix pattern |
| Code review | code-review-and-quality | Convention violations, good patterns |

## Confidence Scoring

```
base_confidence = 0.3 (initial extraction)
+ 0.1 per successful application (max +0.4)
+ 0.1 per explicit user confirmation (max +0.2)
+ 0.1 per cross-session validation (max +0.1)
- 0.05 per failed application (min 0.0)
- 0.01 per day since last use (decay, min 0.1)
```

**Thresholds:**
- Quarantined: < 0.5
- Active: 0.5 - 0.79
- Reliable: 0.8 - 0.89
- Promoted: ≥ 0.9

## Session Start Injection

At SessionStart, inject top 5 instincts matching current context:
- Project path patterns
- Tech stack (from package.json, requirements.txt, etc.)
- Task type (from recent messages)
- File types being worked on

Format injected:
```
## Injected Instincts (from continuous-learning-v2)
1. [0.87] Use `Result<T, E>` for error handling in TypeScript services
   Context: backend, TypeScript, error-handling
   Source: session-20260815, 12 applications
2. [0.82] Always run lint + typecheck before committing
   Context: all, git, quality-gates
   Source: session-20260820, 8 applications
```

## Commands

### instinct-status
Show all instincts with confidence scores, filterable by project/context.

### instinct-save <pattern> --context <context> --confidence <0-1>
Explicitly save an instinct from current session.

### instinct-import <file>
Import instincts from another project/team (JSONL format).

### instinct-export [--project <hash>] [--promoted-only]
Export instincts for sharing/backup.

### instinct-prune [--days <90>] [--min-confidence <0.3>]
Remove stale/low-confidence instincts.

### instinct-evolve
Cluster related instincts into skills (calls skill-creator).

## Integration Points

- **context-engineering**: Instincts loaded at SessionStart, saved at SessionEnd
- **retro**: Cross-session pattern extraction feeds instinct creation
- **handoff**: Instincts included in handoff documents
- **agent-router**: Instincts can suggest skill/agent choices
- **dev-craft/ui-craft**: Phase patterns extracted as instincts

## Implementation

The skill provides these functions (called by hooks):

```javascript
// Extract instincts from session transcript
async function extractInstincts(sessionFile, projectHash) { }

// Score and update instinct confidence
async function updateConfidence(instinctId, success) { }

// Get relevant instincts for current context
async function getRelevantInstincts(context) { }

// Inject instincts into session start
async function injectInstincts(sessionStartContext) { }

// Promote instincts to global
async function promoteInstincts() { }
```

## Hooks Integration

Add to `.opencode-plugin/hooks.json`:

```json
{
  "SessionStart": ["hooks/learning-inject.js"],
  "SessionEnd": ["hooks/learning-extract.js"]
}
```

## References

- `references/instinct-schema.json` — Instinct data structure
- `references/extraction-rules.md` — Patterns to extract
- `references/confidence-calculation.md` — Detailed scoring algorithm