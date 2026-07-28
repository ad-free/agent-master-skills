# Token Budget Reference

Token estimation heuristics and context budget management for skills and agents.

## Estimation Heuristics

| Content Type | Formula | Example |
|--------------|---------|---------|
| Prose (English) | `words × 1.3` | 1000 words ≈ 1300 tokens |
| Code-heavy | `chars / 4` | 4000 chars ≈ 1000 tokens |
| Mixed | Dominant type heuristic | Use primary content type |

## Depth Multipliers (for response planning)

| Depth Level | Multiplier | Use Case |
|-------------|------------|----------|
| Brief (25%) | 0.25 | TL;DR, summary, yes/no |
| Standard (100%) | 1.0 | Normal answer |
| Detailed (200%) | 2.0 | Explanation with examples |
| Exhaustive (400%) | 4.0 | Comprehensive guide, all edge cases |

## Context Budget Tiers

| Tier | Token Limit | Use Case |
|------|-------------|----------|
| Minimal | 4K | Quick lookup, single fact |
| Standard | 16K | Typical agent task |
| Extended | 64K | Complex analysis, full file reads |
| Maximum | 200K | Full codebase context (requires rotation) |

## Rotation Triggers

- **60% usage** → Generate handoff, suggest new session
- **80% usage** → Force context rotation (hard stop)
- **Repeated action 3x** → Checkpoint and summarize

## Skill Integration

Skills should declare their typical token budget in frontmatter:
```yaml
metadata:
  token-budget: standard  # minimal|standard|extended|maximum
```