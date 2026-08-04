# Prompt-Optimizer Metrics Reference

Cost-optimizer reads prompt-optimizer metrics from `.dev-craft/prompt-optimizer-metrics.jsonl` to calculate token savings and adjust budgets.

## Metrics File Format

Each line is a JSON object:

```json
{
  "timestamp": "2026-08-04T10:30:00Z",
  "agent": "triage",
  "stage": "pre-routing",
  "original_tokens": 1200,
  "optimized_tokens": 850,
  "savings_percent": 29
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO 8601 | When optimization occurred |
| `agent` | string | Agent that invoked prompt-optimizer |
| `stage` | string | `pre-routing` or `per-agent` |
| `original_tokens` | int | Tokens in original request |
| `optimized_tokens` | int | Tokens in optimized prompt |
| `savings_percent` | int | Percentage reduction (0-100) |

## Reading Metrics in Cost-Optimizer

```python
from skills.references.cost_routing import calculate_session_savings, report_savings_dashboard

# Get aggregated savings
savings = calculate_session_savings()

# Print dashboard
report_savings_dashboard()
```

## Integration Points

1. **Pre-routing** (triage/agent-router): Runs on every user request before classification
2. **Per-agent** (planner, implementer, debugger, etc.): Runs on each agent's task context
3. **Cost tracking**: Metrics appended to JSONL file after each optimization
4. **Budget calculation**: Effective tokens = original - savings
5. **Model routing**: Adjusted complexity thresholds based on savings percentage

## Expected Savings

Based on awesome-copilot prompt-optimizer patterns:

| Stage | Typical Savings | Reason |
|-------|-----------------|--------|
| Pre-routing | 20-40% | Structures vague requests, removes ambiguity |
| Per-agent (planner) | 20-30% | Adds structure, examples, grounding |
| Per-agent (implementer) | 25-35% | XML sections, examples, self-check |
| Per-agent (debugger) | 15-25% | Citations, structured hypothesis format |
| Per-agent (code-reviewer) | 20-30% | Examples, citations, structured findings |

## Cost Impact

For a typical session with 10 agent invocations:
- Without prompt-optimizer: ~50,000 input tokens
- With prompt-optimizer: ~35,000 input tokens
- **Savings: ~15,000 tokens (30%)**
- Model routing may drop 1-2 tiers cheaper due to lower complexity