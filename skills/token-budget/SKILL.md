---
name: token-budget
description: |
  Token budget management: user chooses response depth before answer. Use when user wants to control
  response length, mentions tokens/budget/depth, or says "brief/detailed/exhaustive".
  TRIGGER: "token budget", "token count", "response length", "short version", "brief", "detailed", "exhaustive".
  DO NOT TRIGGER when: user already set level this session, answer is trivially one line, "token" means auth/payment.
  
model: gpt-5-nano
version: 2.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Bash
  - AskUserQuestion
triggers:
  - "token budget"
  - "token count"
  - "response length"
  - "short version"
  - "brief answer"
  - "detailed answer"
  - "exhaustive answer"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 2.0.0
  domain: context-memory
  integrates-with: [context-engineering, cost-optimizer]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# Token Budget Advisor (TBA)

Intercept the response flow to offer the user a choice about response depth **before** answering.

## When to Use

- User wants to control how long or detailed a response is
- User mentions tokens, budget, depth, or response length
- User says "short version", "tldr", "brief", "al 25%", "exhaustive", etc.
- Any time the user wants to choose depth/detail level upfront

**Do not trigger** when: user already set a level this session (maintain it silently), or the answer is trivially one line.

## How It Works

### Step 1 — Estimate Input Tokens

Use the repository's canonical context-budget heuristics:

- Prose: `words × 1.3`
- Code-heavy or mixed/code blocks: `chars / 4`

For mixed content, use the dominant content type and keep the estimate heuristic.

### Step 2 — Estimate Response Size by Complexity

Classify the prompt, then apply the multiplier range to get the full response window:

| Complexity | Multiplier Range | Example Prompts |
|------------|------------------|-----------------|
| Trivial (fact lookup, yes/no) | 0.1 – 0.3x | "What's 2+2?", "Is this valid JSON?" |
| Simple (explain concept, short code) | 0.5 – 1.0x | "Explain useReducer", "Write a regex for email" |
| Standard (implement feature, debug) | 1.5 – 3.0x | "Build auth API", "Fix this test failure" |
| Complex (architect system, refactor) | 3.0 – 6.0x | "Design microservices for X", "Refactor legacy auth" |

### Step 3 — Offer User Choice

Present four depth levels. User picks ONE. Maintain choice for session.

```
## Token Budget — Choose Response Depth

**Estimated input**: ~2,400 tokens
**Complexity**: Standard (1.5–3.0x multiplier)
**Projected full response**: 3,600 – 7,200 tokens

Choose depth:

1. **Brief (25%)** — TL;DR, key points only, ~900–1,800 tokens
2. **Standard (100%)** — Full answer with examples, ~3,600–7,200 tokens
3. **Detailed (200%)** — Comprehensive + alternatives + reasoning, ~7,200–14,400 tokens
4. **Exhaustive (400%)** — Everything: edge cases, trade-offs, full code, ~14,400–28,800 tokens

Reply with: 1, 2, 3, or 4 (or "brief"/"standard"/"detailed"/"exhaustive")
```

### Step 4 — Enforce Budget

Once user chooses, tailor response to fit. Use progressive disclosure:
- Brief: Answer only, no fluff
- Standard: Answer + key examples
- Detailed: Answer + examples + alternatives + reasoning
- Exhaustive: Everything above + edge cases + full code + trade-off tables

## Integration

- Called by `agent-router` at session start if user hints at depth preference
- Can be invoked mid-session via `/token-budget` command
- Respects `context-engineering` token ceiling guardrails

## Output Format

Always output the choice menu first. Wait for user selection. Then answer at chosen depth.