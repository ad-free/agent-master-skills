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

1. **Pre-routing** (triage/agent-router): Runs on every user request before classification (Pipeline Mode)
2. **Per-agent** (debugger, code-reviewer, verifier, api-designer, frontend-engineer, database-engineer, devops-engineer, security-auditor, test-engineer, docs-engineer, retro-analyst): Runs on each agent's task context (Pipeline Mode)
3. **NOT used by:** planner, implementer (their skills handle requirement gathering directly)
4. **Cost tracking**: Metrics appended to JSONL file after each optimization
5. **Budget calculation**: Effective tokens = original - savings
6. **Model routing**: Adjusted complexity thresholds based on savings percentage

## Expected Savings

Based on awesome-copilot prompt-optimizer patterns:

| Stage | Typical Savings | Reason |
|-------|-----------------|--------|
| Pre-routing | 20-40% | Structures vague requests, removes ambiguity |
| Per-agent (debugger) | 15-25% | Citations, structured hypothesis format |
| Per-agent (code-reviewer) | 20-30% | Examples, citations, structured findings |
| Per-agent (verifier) | 15-25% | Quotes grounding, structured verification |
| Per-agent (api-designer) | 20-30% | Examples, quotes, structured API design |
| Per-agent (frontend-engineer) | 20-30% | Examples, role-specific structure |
| Per-agent (database-engineer) | 15-25% | Citations, structured schema context |
| Per-agent (devops-engineer) | 15-25% | Structured pipeline context |
| Per-agent (security-auditor) | 20-30% | Examples, citations, threat model structure |
| Per-agent (test-engineer) | 15-25% | Examples, structured test strategy |
| Per-agent (docs-engineer) | 15-25% | Markdown sections, examples |
| Per-agent (retro-analyst) | 10-20% | Markdown sections, analysis structure |

**Not applicable:** planner, implementer (skills handle requirement gathering)

## Cost Impact

For a typical session with 10 agent invocations (8 using prompt-optimizer):
- Without prompt-optimizer: ~50,000 input tokens
- With prompt-optimizer: ~37,000 input tokens (pre-routing + 7 per-agent)
- **Savings: ~13,000 tokens (26%)**
- Model routing may drop 1-2 tiers cheaper due to lower complexity