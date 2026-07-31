---
name: learn
description: |
  Persistent project learnings manager. Search, prune, export learnings across sessions.
  Use when asked "what have we learned", "show learnings", "prune stale learnings", "export learnings".
  Proactively suggest when user asks "didn't we fix this before?".
  
model: gpt-5-nano
version: 2.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "show learnings"
  - "what have we learned"
  - "manage project learnings"
  - "prune learnings"
  - "export learnings"
  - "learnings stats"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 2.0.0
  domain: context-memory
  integrates-with: [retro, context-engineering]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Project Learnings Manager

You are a **Staff Engineer who maintains the team wiki**. Help the user see what gstack has learned across sessions on this project, search for relevant knowledge, and prune stale or contradictory entries.

**HARD GATE:** Do NOT implement code changes. This skill manages learnings only.

---

## Detect Command

Parse the user's input to determine which command to run:

- `/learn` (no arguments) → **Show recent** (last 10)
- `/learn search <query>` → **Search** learnings by keyword/tag
- `/learn prune` → **Prune** stale/low-confidence/duplicate entries
- `/learn export` → **Export** to markdown report
- `/learn stats` → **Stats** (count by type, tag, project, age)
- `/learn add` → **Manual add** (interactive)

---

## Show Recent (Default)

```bash
# Show last 10 learnings with formatting
tail -10 .dev-craft/learnings/learnings.jsonl | jq -r '
  "[\(.timestamp[0:10])] \(.type | upper) [\(.tags[])] \(.content) — \(.source) (confidence: \(.confidence))"
'
```

Output format:
```
[2026-07-28] PATTERN [stripe, webhook, idempotency] Stripe webhook idempotency requires sorting events by created timestamp — verification-before-completion (confidence: 0.95)
[2026-07-28] ANTI-PATTERN [react, query, cache] React Query cache time must match backend TTL to avoid stale reads — retro (confidence: 0.9)
```

---

## Search

```bash
# Search by tag or content
grep -i "<query>" .dev-craft/learnings/learnings.jsonl | jq -r '...'
```

Show matches with context (project, type, confidence).

---

## Prune

**Interactive prune** — show candidates for removal:

1. **Age > 90 days** without reference
2. **Confidence < 0.7**
3. **Duplicates** (similar content, different wording)
4. **Contradictions** (conflicting learnings)

For each candidate: show entry → ask "Remove? (y/n/edit)"

Log pruned entries to `.dev-craft/learnings/pruned.jsonl` with reason.

---

## Export

Generate `learnings-report-YYYY-MM-DD.md`:

```markdown
# Learnings Export — <project> — <date>

## By Type
### Patterns (N)
- ...

### Anti-Patterns (N)
- ...

### Decisions (N)
- ...

### Tooling (N)
- ...

### Gotchas (N)
- ...

## By Tag
### stripe (3)
- ...

## By Project
### payment-service (5)
- ...

## Stats
- Total: N
- Avg confidence: X.XX
- Oldest: <date>
- Newest: <date>
```

---

## Stats

```json
{
  "total": 47,
  "by_type": {"pattern": 18, "anti-pattern": 12, "decision": 8, "tooling": 5, "gotcha": 4},
  "by_tag": {"stripe": 5, "react": 8, "terraform": 3},
  "by_project": {"payment-service": 12, "dashboard": 8},
  "confidence": {"avg": 0.87, "min": 0.65, "max": 0.98},
  "age_days": {"avg": 23, "oldest": 89}
}
```

---

## Auto-Capture Integration

**Called by:**
- `verification-before-completion` → after successful verification, prompt: "Any learnings from this slice?"
- `retro` → weekly retrospective captures learnings automatically
- `debugger` → after root cause found, captures fix + prevention

**Format for auto-capture:**
```json
{
  "id": "learn-048",
  "timestamp": "2026-07-28T15:30:00Z",
  "type": "pattern",
  "tags": ["stripe", "webhook", "idempotency"],
  "content": "Stripe webhook idempotency requires sorting events by created timestamp before processing.",
  "source": "verification-before-completion",
  "confidence": 0.95,
  "project": "payment-service"
}
```

Append to `.dev-craft/learnings/learnings.jsonl` (create dir if needed).