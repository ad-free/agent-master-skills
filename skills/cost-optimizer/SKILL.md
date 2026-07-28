---
name: cost-optimizer
description: |
  Cost optimization patterns for LLM API usage — model routing by task complexity, budget tracking,
  retry logic, and prompt caching. Use when building applications that call LLM APIs, processing batches
  with varying complexity, need to stay within API budget, or optimizing cost without sacrificing quality.
  (from ECC cost-aware-llm-pipeline)
model: nemotron-3-ultra-free
tools: Read, Write, Edit, Bash, Grep, Glob
preamble-tier: 4
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - "optimize llm cost"
  - "model routing"
  - "api budget"
  - "prompt caching"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  source: ECC cost-aware-llm-pipeline
---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Cost-Aware LLM Pipeline

Patterns for controlling LLM API costs while maintaining quality. Combines model routing, budget tracking, retry logic, and prompt caching into a composable pipeline.

## When to Activate

- Building applications that call LLM APIs (Claude, GPT, etc.)
- Processing batches of items with varying complexity
- Need to stay within a budget for API spend
- Optimizing cost without sacrificing quality on complex tasks

---

## Core Concepts

### 1. Model Routing by Task Complexity

Automatically select cheaper models for simple tasks, reserving expensive models for complex ones.

```python
# Model definitions (OpenCode Zen free models)
MODEL_NEMOTRON_ULTRA = "nemotron-3-ultra-free"    # 1M context, best reasoning
MODEL_NEMOTRON_SUPER = "nemotron-3-super-free"    # 1M context, high capability
MODEL_DEEPSEEK_FLASH = "deepseek-v4-flash-free"   # 200K context, fast/cheap
MODEL_BIG_PICKLE = "big-pickle"                   # 200K context, coding optimized
MODEL_GPT5_NANO = "gpt-5-nano"                    # 128K context, ultra-fast

# Complexity thresholds
_ULTRA_TEXT_THRESHOLD = 10_000      # chars
_ULTRA_ITEM_THRESHOLD = 30          # items (files, functions, etc.)
_SUPER_TEXT_THRESHOLD = 5_000
_SUPER_ITEM_THRESHOLD = 15

def select_model(
    text_length: int = 0,
    item_count: int = 0,
    force_model: str | None = None,
    prefer_coding: bool = False,
) -> str:
    """Select model based on task complexity."""
    if force_model is not None:
        return force_model
    
    # Coding tasks → big-pickle or nemotron
    if prefer_coding:
        if text_length >= _ULTRA_TEXT_THRESHOLD or item_count >= _ULTRA_ITEM_THRESHOLD:
            return MODEL_NEMOTRON_ULTRA
        return MODEL_BIG_PICKLE
    
    # General routing
    if text_length >= _ULTRA_TEXT_THRESHOLD or item_count >= _ULTRA_ITEM_THRESHOLD:
        return MODEL_NEMOTRON_ULTRA  # Complex: 1M context, best reasoning
    if text_length >= _SUPER_TEXT_THRESHOLD or item_count >= _SUPER_ITEM_THRESHOLD:
        return MODEL_NEMOTRON_SUPER  # Medium: 1M context, high capability
    return MODEL_DEEPSEEK_FLASH      # Simple: fast, 200K context
```

**Routing Examples:**
| Task | Text Len | Items | Coding? | Model |
|------|----------|-------|---------|-------|
| "Fix typo in README" | 500 | 1 | No | deepseek-v4-flash-free |
| "Review this PR" | 8,000 | 5 | Yes | big-pickle |
| "Design architecture for payment system" | 15,000 | 20 | No | nemotron-3-ultra-free |
| "Write unit tests for auth module" | 3,000 | 10 | Yes | nemotron-3-super-free |

### 2. Immutable Cost Tracking

Track cumulative spend with frozen dataclasses. Each API call returns a new tracker — never mutates state.

```python
from dataclasses import dataclass, replace
from typing import Optional
import time

@dataclass(frozen=True)
class CostSnapshot:
    model: str
    input_tokens: int
    output_tokens: int
    cached_read_tokens: int = 0
    cached_write_tokens: int = 0
    timestamp: float = 0.0
    request_id: str = ""
    
    # Free models = $0, but tracking enables:
    # - Usage analytics
    # - Budget alerts (if paid models added later)
    # - Optimization opportunities
    
    def add(self, other: 'CostSnapshot') -> 'CostSnapshot':
        return CostSnapshot(
            model=self.model,  # assumes same model; for multi-model, track separately
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            cached_read_tokens=self.cached_read_tokens + other.cached_read_tokens,
            cached_write_tokens=self.cached_write_tokens + other.cached_write_tokens,
            timestamp=max(self.timestamp, other.timestamp),
        )

@dataclass(frozen=True)
class Budget:
    session_limit: int = 1_000_000      # tokens
    daily_limit: int = 10_000_000       # tokens
    monthly_limit: int = 100_000_000    # tokens
    
    def check(self, snapshot: CostSnapshot) -> tuple[bool, str]:
        total = snapshot.input_tokens + snapshot.output_tokens
        if total > self.session_limit * 0.8:
            return False, f"Session at {total/self.session_limit*100:.1f}% of limit"
        if total > self.daily_limit * 0.8:
            return False, f"Daily at {total/self.daily_limit*100:.1f}% of limit"
        return True, "OK"

# Usage
budget = Budget()
tracker = CostSnapshot(model="deepseek-v4-flash-free", input_tokens=0, output_tokens=0)

# After each API call:
call_cost = CostSnapshot(
    model="deepseek-v4-flash-free",
    input_tokens=1500,
    output_tokens=800,
    timestamp=time.time(),
    request_id="req-123"
)
tracker = tracker.add(call_cost)
ok, msg = budget.check(tracker)
if not ok:
    warn(msg)  # or raise BudgetExceeded
```

### 3. Retry Logic with Exponential Backoff

```python
import asyncio
import random
from typing import Callable, TypeVar

T = TypeVar('T')

async def retry_with_backoff(
    fn: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    retriable_exceptions: tuple = (ConnectionError, TimeoutError, RateLimitError),
) -> T:
    """Retry with exponential backoff + jitter."""
    last_exception = None
    for attempt in range(max_retries + 1):
        try:
            return await fn()
        except retriable_exceptions as e:
            last_exception = e
            if attempt == max_retries:
                break
            delay = min(base_delay * (2 ** attempt) + random.uniform(0, 0.5), max_delay)
            await asyncio.sleep(delay)
    raise last_exception
```

### 4. Prompt Caching

Cache static portions of prompts (system instructions, few-shot examples, context documents).

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=128)
def cached_system_prompt(agent_name: str, skill_name: str) -> str:
    """Cache static system prompts by agent+skill."""
    key = f"{agent_name}:{skill_name}"
    # Load from file or build
    return build_system_prompt(agent_name, skill_name)

def cache_key(content: str) -> str:
    """Generate cache key for prompt content."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]

class PromptCache:
    def __init__(self, max_size: int = 500):
        self._cache = {}
        self._max_size = max_size
    
    def get(self, key: str) -> Optional[str]:
        return self._cache.get(key)
    
    def set(self, key: str, value: str):
        if len(self._cache) >= self._max_size:
            # Remove oldest (simple FIFO)
            oldest = next(iter(self._cache))
            del self._cache[oldest]
        self._cache[key] = value

# Usage
prompt_cache = PromptCache()

async def call_llm_with_cache(
    model: str,
    system: str,
    user: str,
    cache: PromptCache,
) -> str:
    sys_key = cache_key(system)
    cached_system = cache.get(sys_key)
    if cached_system is None:
        cached_system = system
        cache.set(sys_key, system)
    
    # Call API with cached system prompt
    return await api_call(model, cached_system, user)
```

---

## Integration with Agent System

### Agent Model Assignment (from SHARED.md Agent Registry)

| Agent | Model | Rationale |
|-------|-------|-----------|
| `planner`, `architect`, `orchestrator` | `nemotron-3-ultra-free` | Complex reasoning, 1M context |
| `code-reviewer`, `security-auditor`, `implementer` | `big-pickle` | Coding-optimized |
| `debugger`, `performance-engineer` | `nemotron-3-ultra-free` | Deep analysis |
| `api-designer`, `frontend-engineer`, `database-engineer`, `test-engineer` | `big-pickle` | Coding tasks |
| `devops-engineer`, `docs-engineer`, `triage`, `gatekeeper` | `deepseek-v4-flash-free` | Fast utility |
| `product-manager`, `retro-analyst` | `gpt-5-nano` | Quick classification |

### Automatic Routing in Skills

Each skill declares its typical complexity in frontmatter metadata:

```yaml
metadata:
  token-budget: standard  # minimal|standard|extended|maximum
  prefer-model: big-pickle  # hint for router
```

The `agent-router` skill reads this and applies `select_model()` automatically.

---

## Budget Alerts

```python
def check_and_alert(tracker: CostSnapshot, budget: Budget):
    ok, msg = budget.check(tracker)
    if not ok:
        alert_level = "WARNING" if "80%" in msg else "CRITICAL"
        print(f"[{alert_level}] Budget: {msg}")
        # Could also: log to file, send webhook, update state.json
```

---

## References

- `skills/references/token-budget.md` — User-facing depth control
- `skills/references/cost-routing.md` — Detailed routing logic
- `skills/references/learnings.md` — Captured cost optimizations