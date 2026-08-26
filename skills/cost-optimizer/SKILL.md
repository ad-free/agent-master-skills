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
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.1.0
  domain: context-memory
  integrates-with: [prompt-optimizer, token-budget, dev-craft]
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Cost-Aware LLM Pipeline

Patterns for controlling LLM API costs while maintaining quality. Combines model routing, budget tracking, retry logic, and prompt caching into a composable pipeline.
(from ECC cost-aware-llm-pipeline)
