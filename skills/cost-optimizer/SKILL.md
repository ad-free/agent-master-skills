---
name: cost-optimizer
description: |
  Use when you need to optimize LLM API costs through model routing by task complexity,
  budget tracking, retry logic, and prompt caching.
model: nemotron-3-ultra-free
version: 2.1.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "optimize llm cost"
  - "model routing"
  - "api budget"
  - "prompt caching"
  - "token budget"
  - "token count"
  - "response length"
  - "short version"
  - "brief answer"
  - "detailed answer"
  - "exhaustive answer"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.1.0
  domain: context-memory
  integrates-with: [prompt-optimizer, context-engineering, dev-craft, agent-router]
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Cost-Aware LLM Pipeline

Patterns for controlling LLM API costs while maintaining quality. Combines model routing, budget tracking, retry logic, and prompt caching into a composable pipeline.
(from ECC cost-aware-llm-pipeline)

## Response Depth Budget (merged from `token-budget`)

Offer the user a choice about response depth **before** answering when they mention tokens, budget, depth, or response length ("short version", "brief", "detailed", "exhaustive"). Do not trigger when a level is already set this session (maintain it silently) or the answer is trivially one line — and never when "token" means auth/payment.

1. **Estimate input**: prose `words × 1.3`; code-heavy `chars / 4` (dominant type wins for mixed content).
2. **Estimate response**: Trivial 0.1–0.3x, Simple 0.5–1.0x, Standard 1.5–3.0x, Complex 3.0–6.0x.
3. **Offer choice**: Brief (25%) / Standard (100%) / Detailed (200%) / Exhaustive (400%) with token projections; wait for selection, maintain it for the session, enforce via progressive disclosure.
4. Called by `agent-router` at session start on depth-preference hints; invokable mid-session via `/token-budget`; respects `context-engineering` token ceilings.
