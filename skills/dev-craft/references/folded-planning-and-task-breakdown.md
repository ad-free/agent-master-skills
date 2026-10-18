---
name: planning-and-task-breakdown
description: |
  Use when you have a spec (PRODUCT.md/DOMAIN.md) and need implementable units with DAG-based
  dependency mapping and Gherkin/Given-When-Then acceptance criteria.
model: nemotron-3-ultra-free
version: 2.1.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "create plan"
  - "break down work"
  - "task breakdown"
  - "planning"
  - "implementation plan"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.1.0
  domain: planning
  integrates-with: [product-thinking, project-discovery, grilling, dev-craft]
---
TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# Planning and Task Breakdown

Decompose specs into ordered, verifiable tasks with DAG-based dependency
mapping and Gherkin/Given-When-Then acceptance criteria. Use when you have a
spec (PRODUCT.md/DOMAIN.md) and need implementable units. Invoked by: planner
→ implementer.

## Iron Law

**NO IMPLEMENTATION WITHOUT A WRITTEN PLAN**
