# Cost Routing Reference

Model routing logic for cost-aware LLM pipeline using OpenCode Zen free models.

## Free Model Catalog (OpenCode Zen)

| Model ID | Context | Best For | Cost Tier |
|----------|---------|----------|-----------|
| `nemotron-3-ultra-free` | 1M | Complex reasoning, architecture, planning | High capability |
| `nemotron-3-super-free` | 1M | Complex reasoning, large context | High capability |
| `deepseek-v4-flash-free` | 200K | Fast coding, general utility, debugging | Fast/Utility |
| `mimo-v2.5-free` | 200K | Fast coding, reasoning | Fast/Utility |
| `big-pickle` | 200K | **Coding agent optimized** | Coding specialist |
| `gpt-5-nano` | 128K | Quick tasks, simple routing, classification | Ultra-fast |
| `minimax-m2.5-free` | 200K | Coding, agentic tool use | Balanced |
| `ling-3.0-flash-free` | 200K | Fast responses | Fast |
| `north-mini-code-free` | 200K | Code-focused | Code specialist |
| `laguna-s-2.1-free` | 200K | General | General |
| `glm-5-free` | 204K | General | General |

## Routing Rules

### By Agent Role
| Role | Primary Model | Fallback |
|------|---------------|----------|
| Planner/Architect | `nemotron-3-ultra-free` | `nemotron-3-super-free` |
| Code Reviewer | `big-pickle` | `nemotron-3-ultra-free` |
| Backend/Frontend/Mobile Dev | `big-pickle` | `deepseek-v4-flash-free` |
| TDD/Test Engineer | `big-pickle` | `mimo-v2.5-free` |
| Build Error Resolver | `deepseek-v4-flash-free` | `mimo-v2.5-free` |
| DevOps/Database | `deepseek-v4-flash-free` | `mimo-v2.5-free` |
| Security Auditor | `big-pickle` | `nemotron-3-ultra-free` |
| Performance Engineer | `nemotron-3-ultra-free` | `big-pickle` |
| Router/Classifier | `gpt-5-nano` | `ling-3.0-flash-free` |
| Docs/Tech Writer | `gpt-5-nano` | `ling-3.0-flash-free` |

### By Task Complexity
```python
def select_model(text_length: int, item_count: int, force_model: str = None) -> str:
    if force_model:
        return force_model
    
    # Complex task thresholds
    COMPLEX_TEXT_THRESHOLD = 10_000   # chars
    COMPLEX_ITEM_THRESHOLD = 30       # items (files, functions, etc.)
    
    if text_length >= COMPLEX_TEXT_THRESHOLD or item_count >= COMPLEX_ITEM_THRESHOLD:
        return "nemotron-3-ultra-free"  # Complex: 1M context, best reasoning
    
    return "deepseek-v4-flash-free"      # Simple: fast, 200K context
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