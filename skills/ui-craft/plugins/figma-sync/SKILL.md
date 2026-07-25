---
owner: noname.spyware@gmail.com
allowedTools:
- file
- http

---

---
name: figma-sync
description: Use when sync design tokens and components from Figma via MCP or API integration.
metadata:
  origin: agent-master-skills---

# Figma Sync Plugin

## Overview

Synchronizes design tokens, color palettes, typography, and component specifications from Figma into project design tokens.

## When to Use

- Figma MCP server is configured
- Design team has published design tokens in Figma
- Starting a new project from Figma designs
- Design system updates need to be reflected in code

## Integration

Requires Figma MCP server in `mcp-configs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/mcp-servers.json`.

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