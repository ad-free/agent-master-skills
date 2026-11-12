---
name: example-agent
description: What this agent does and when the main agent should delegate to it. Name the input it expects.
tools: Read, Grep, Glob, Bash
model: inherit
maxTurns: 15
---

# Example Agent

Template for agent files under `agents/`. Frontmatter follows the Claude Code subagent schema:
`name` (kebab-case) and `description` required; `tools`, `model`, `maxTurns` expected. Grant only the tools the
role needs: a reviewer gets no Edit/Write. MCP tools are named `mcp__<server>__<tool>`.

## Input
What the main agent passes in (brief, diff, commands). The agent must not need anything else.

## Rules
What it may and may not touch.

## Checks
The steps it runs, in order.

## Return format
The exact shape of its reply, so the main agent can use it without re-asking.
