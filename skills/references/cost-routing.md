# Cost Routing Reference

Model routing logic for cost-aware LLM pipeline using ChatGPT (OpenAI) models.

## Model Catalog (OpenAI)

| Model ID | Context | Best For | Cost Tier |
|----------|---------|----------|-----------|
| `gpt-5.6-sol` | 256K | Complex reasoning, architecture, planning, code review | Flagship |
| `gpt-5.6-terra` | 256K | Balanced intelligence and cost, most agent work | Balanced |
| `gpt-5.6-luna` | 128K | Cost-sensitive, high-volume tasks, documentation | Cost-efficient |
| `gpt-5.4-mini` | 128K | Lighter tasks, subagents, interactive edits | Fast/Utility |
| `gpt-5.4-nano` | 128K | Quick tasks, simple routing, classification | Ultra-fast |
| `gpt-4.1` | 1M | Large context, complex analysis | Large context |
| `gpt-4.1-mini` | 1M | Large context, cost-effective | Large context value |
| `gpt-4.1-nano` | 1M | Large context, fastest | Large context fast |
| `o4-mini` | 200K | Reasoning tasks, math, code | Reasoning |
| `o3` | 200K | Complex reasoning, analysis | Premium reasoning |
| `o3-mini` | 200K | Fast reasoning | Reasoning fast |

## Routing Rules

### By Agent Role
| Role | Primary Model | Fallback |
|------|---------------|----------|
| Planner/Architect | `gpt-5.6-terra` | `gpt-5.6-sol` |
| Code Reviewer | `gpt-5.6-terra` | `gpt-5.6-luna` |
| Backend/Frontend Dev | `gpt-5.6-terra` | `gpt-5.6-luna` |
| TDD/Test Engineer | `gpt-5.6-terra` | `gpt-5.6-luna` |
| Debugger | `gpt-5.6-terra` | `gpt-5.6-luna` |
| DevOps/Database | `gpt-5.6-luna` | `gpt-5.4-nano` |
| Security Auditor | `gpt-5.6-terra` | `gpt-5.6-luna` |
| Docs/Tech Writer | `gpt-5.6-luna` | `gpt-5.4-nano` |
| Verifier | `gpt-5.6-luna` | `gpt-5.4-nano` |
| Orchestrator | `gpt-5.6-terra` | `gpt-5.6-luna` |

### By Task Complexity
```python
def select_model(text_length: int, item_count: int, force_model: str = None) -> str:
    if force_model:
        return force_model
    
    # Complex task thresholds
    COMPLEX_TEXT_THRESHOLD = 10_000   # chars
    COMPLEX_ITEM_THRESHOLD = 30       # items (files, functions, etc.)
    
    if text_length >= COMPLEX_TEXT_THRESHOLD or item_count >= COMPLEX_ITEM_THRESHOLD:
        return "gpt-5.6-terra"  # Complex: balanced intelligence/cost
    
    return "gpt-5.6-luna"       # Simple: cost-efficient
```

## Cost Tracking (Immutable)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CostSnapshot:
    model: str
    input_tokens: int
    output_tokens: int
    cached_read_tokens: int = 0
    cached_write_tokens: int = 0
    timestamp: str = ""
    
    def add(self, other: 'CostSnapshot') -> 'CostSnapshot':
        return CostSnapshot(
            model=self.model,
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            cached_read_tokens=self.cached_read_tokens + other.cached_read_tokens,
            cached_write_tokens=self.cached_write_tokens + other.cached_write_tokens,
        )

# Free models = $0, but tracking enables:
# - Usage analytics
# - Budget alerts (if paid models added later)
# - Optimization opportunities
```

## Prompt Caching Strategy

1. **System prompts** — Cache static instructions (agent persona, skill methodology)
2. **Context documents** — Cache PRODUCT.md, PLAN.md, api-contract.md
3. **Few-shot examples** — Cache representative examples
4. **Cache key** — Hash of cached content + model ID

## Budget Alerts

```python
BUDGET_LIMITS = {
    "session": 1_000_000,      # 1M tokens per session
    "daily": 10_000_000,       # 10M tokens per day
    "monthly": 100_000_000,    # 100M tokens per month
}

def check_budget(current: CostSnapshot, limit: int) -> bool:
    total = current.input_tokens + current.output_tokens
    if total > limit * 0.8:
        warn(f"Budget at {total/limit*100:.1f}% of limit")
    if total > limit:
        raise BudgetExceeded(f"Exceeded {limit} token limit")
```