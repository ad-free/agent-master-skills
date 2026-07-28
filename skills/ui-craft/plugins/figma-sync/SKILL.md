---
name: figma-sync
description: Use when you need to sync design tokens and components from Figma via MCP or API integration.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 1
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion]
triggers:
  - "figma sync"
  - "design tokens sync"
  - "figma to code"
  - "design import"
  - "token export"
disable-model-invocation: true
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
---

<!-- TOKEN CEILING: ~2K -->

# Figma Sync Plugin

## Overview

Synchronizes design tokens, color palettes, typography, and component specifications from Figma into project design tokens.

## When to Use

- Figma MCP server is configured
- Design team has published design tokens in Figma
- Starting a new project from Figma designs
- Design system updates need to be reflected in code

## Integration

Requires Figma MCP server in `mcp-configs/mcp-servers.json`.

Registered in `state.json`:
```json
{
  "plugins": ["figma-sync"],
  "pluginConfig": {
    "figma-sync": {
      "fileKey": "abc123",
      "pageName": "Design Tokens"
    }
  }
}
```