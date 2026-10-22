# Confidence Calculation Algorithm

Detailed specification for instinct confidence scoring.

## Formula

```
confidence = clamp(
  base_confidence 
  + application_bonus 
  + confirmation_bonus 
  + cross_session_bonus 
  - failure_penalty 
  - time_decay,
  0.0, 1.0
)
```

## Components

### Base Confidence (by trigger source)

| Trigger | Base | Rationale |
|---------|------|-----------|
| explicit | 0.7 | User explicitly validated |
| retro | 0.6 | Human-reviewed in retrospective |
| code-review | 0.5 | Found in structured review |
| bug-fix | 0.4 | Extracted from root-cause fix |
| handoff | 0.4 | Documented in handoff |
| session-end | 0.3 | Auto-extracted, needs validation |

### Application Bonus
```
application_bonus = min(applications * 0.1, 0.4)
```
- Each successful application adds 0.1
- Capped at 0.4 (4+ applications)
- Only counts confirmed successes (not just attempts)

### Confirmation Bonus
```
confirmation_bonus = min(explicit_confirmations * 0.1, 0.2)
```
- User explicitly says "this pattern worked" or similar
- Capped at 0.2 (2 confirmations)

### Cross-Session Bonus
```
cross_session_bonus = 0.1 if (sessions_with_pattern >= 3) else 0
```
- Pattern appears in 3+ independent sessions
- Indicates genuine recurrence, not session-specific

### Failure Penalty
```
failure_penalty = min(failed_applications * 0.05, confidence * 0.5)
```
- Each failed application reduces by 0.05
- Capped at 50% of current confidence (prevents zeroing out)
- Failed = pattern applied but caused issue or didn't apply

### Time Decay
```
days_since_use = (now - last_used).days
time_decay = min(days_since_use * 0.01, confidence - 0.1)
```
- 1% per day since last successful use
- Minimum confidence floor of 0.1 (never fully decays)
- Resets to 0 on successful application

## Status Thresholds

| Status | Confidence Range | Min Applications | Description |
|--------|------------------|------------------|-------------|
| quarantined | [0.0, 0.5) | 0 | Needs validation, not injected |
| active | [0.5, 0.8) | 1 | Injected at session start |
| reliable | [0.8, 0.9) | 3 | High confidence, frequently used |
| promoted | [0.9, 1.0] | 5 | Cross-project ready |
| archived | N/A | N/A | Superseded or stale (>90 days unused) |

## Promotion Criteria

An instinct is promoted to global when:
1. Confidence ≥ 0.9
2. Applications ≥ 5
3. Used in ≥ 3 different projects (different project_hash)
4. Not project-specific (context.project_patterns includes generic patterns)
5. No project-specific tags

## Archival Criteria

An instinct is archived when:
1. Not used for 90+ days (last_used > 90 days ago)
2. Confidence decayed below 0.3
3. Explicitly superseded by a newer instinct (same context, higher confidence)
4. Project deleted/archived and instinct not promoted

## Implementation

```python
def calculate_confidence(instinct: Instinct, now: datetime) -> float:
    base = BASE_CONFIDENCE[instinct.source.trigger]
    
    app_bonus = min(instinct.applications * 0.1, 0.4)
    conf_bonus = min(instinct.explicit_confirmations * 0.1, 0.2)
    cross_bonus = 0.1 if instinct.cross_session_count >= 3 else 0
    
    fail_penalty = min(instinct.failed_applications * 0.05, instinct.confidence * 0.5)
    
    days = (now - instinct.last_used).days
    decay = min(days * 0.01, instinct.confidence - 0.1)
    
    new_confidence = base + app_bonus + conf_bonus + cross_bonus - fail_penalty - decay
    return clamp(new_confidence, 0.0, 1.0)

def update_status(instinct: Instinct):
    c = instinct.confidence
    a = instinct.applications
    
    if c >= 0.9 and a >= 5 and instinct.cross_project_count >= 3:
        instinct.status = "promoted"
    elif c >= 0.8 and a >= 3:
        instinct.status = "reliable"
    elif c >= 0.5 and a >= 1:
        instinct.status = "active"
    elif c < 0.5:
        instinct.status = "quarantined"
    
    # Check archival
    days_unused = (now - instinct.last_used).days
    if days_unused > 90 or c < 0.1:
        instinct.status = "archived"
```

## Injection Ranking

At SessionStart, rank instincts by:
```
injection_score = confidence * relevance_score * recency_factor
```

Where:
- `relevance_score`: 0-1 based on context match (project, stack, task, files)
- `recency_factor`: 1.0 if used < 7 days, 0.8 if < 30 days, 0.5 if < 90 days, 0.2 otherwise

Inject top 5 instincts with injection_score > 0.3.

## Persistence

Instincts stored as JSONL (one per line) for append-only durability:
```jsonl
{"id": "inst-a1b2c3d4e5f6", "pattern": "...", "confidence": 0.87, "status": "reliable", ...}
```

Index maintained separately for fast context-based lookup:
```json
{
  "by_project": { "proj-hash": ["inst-id1", "inst-id2"] },
  "by_stack": { "TypeScript": ["inst-id1"], "Python": ["inst-id3"] },
  "by_task": { "bugfix": ["inst-id2"], "feature": ["inst-id1", "inst-id4"] },
  "by_status": { "active": [...], "promoted": [...] }
}
```