# Learnings Reference

Persistent learning format for cross-session knowledge accumulation.

## Learning Entry Format (JSONL)

```jsonl
{"id": "learn-001", "timestamp": "2026-07-28T10:30:00Z", "type": "pattern", "tags": ["stripe", "webhook", "idempotency"], "content": "Stripe webhook idempotency requires sorting events by created timestamp before processing. Use `event.created` for ordering.", "source": "verification-before-completion", "confidence": 0.95, "project": "payment-service"}
{"id": "learn-002", "timestamp": "2026-07-28T14:15:00Z", "type": "anti-pattern", "tags": ["react", "query", "cache"], "content": "React Query cache time must match backend TTL to avoid stale reads. If backend caches for 5min, set `staleTime: 5 * 60 * 1000`.", "source": "retro", "confidence": 0.9, "project": "dashboard-app"}
```

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique: `learn-<NNN>` |
| `timestamp` | ISO8601 | Yes | When learned |
| `type` | enum | Yes | `pattern` \| `anti-pattern` \| `decision` \| `tooling` \| `gotcha` |
| `tags` | string[] | Yes | Searchable categories |
| `content` | string | Yes | The learning — one actionable insight |
| `source` | string | Yes | Skill/agent that captured it |
| `confidence` | float | Yes | 0.0-1.0 |
| `project` | string | No | Project context |

## Storage Locations

- **Per-project**: `.dev-craft/learnings/learnings.jsonl`
- **Global**: `~/.opencode/learnings/learnings.jsonl` (merged view)

## Search & Retrieval

```bash
# Search by tag
grep '"tags".*stripe' .dev-craft/learnings/learnings.jsonl

# Search by type
grep '"type": "anti-pattern"' .dev-craft/learnings/learnings.jsonl

# Recent learnings (last 10)
tail -10 .dev-craft/learnings/learnings.jsonl

# Stats
wc -l .dev-craft/learnings/learnings.jsonl
```

## Capture Points

| Skill/Agent | When to Capture |
|-------------|-----------------|
| `verification-before-completion` | After successful verification — what worked? |
| `retro` | Weekly — patterns, anti-patterns, decisions |
| `debugger` | After root cause found — the fix and prevention |
| `code-review-and-quality` | Recurring review findings |
| `shipper` | Release — what broke, what went well |

## Pruning Rules

- **Age**: Entries > 90 days without reference → archive
- **Confidence**: < 0.7 → review or remove
- **Duplicates**: Same content, different wording → merge
- **Contradictions**: Conflicting learnings → flag for review

## Integration with `learn` Skill

The `learn` skill provides CLI:
```bash
/learn                    # Show recent
/learn search stripe      # Search
/learn prune              # Remove stale/low-confidence
/learn export             # Export to markdown
/learn stats              # Count by type/tag/project
```