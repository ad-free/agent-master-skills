# GBrain Configuration

```yaml
# Required
backend: "pglite" | "supabase" | "mcp"
project_id: "string"  # auto-generated from git remote
trust_tier: "read-write" | "read-only" | "deny"
auto_sync: "true" | "false"
incremental: "true" | "false"

# PGLite backend (no additional config)

# Supabase backend
supabase_url: "https://xxx.supabase.co"
pooler_url: "postgresql://user:pass@host:5432/db"

# MCP backend
mcp_url: "http://localhost:3000/mcp"
mcp_token: "bearer-token"  # optional
```

## Configuration Locations

| Scope | Path |
|-------|------|
| Global | `~/.gbrain/config.yaml` |
| Project (overrides) | `.gbrain/config.yaml` |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GBRAIN_BACKEND` | Override backend |
| `GBRAIN_POOLER_URL` | Override Supabase pooler URL |
| `GBRAIN_MCP_URL` | Override MCP URL |
| `GBRAIN_MCP_TOKEN` | Override MCP token |
| `GBRAIN_TRUST_TIER` | Override trust tier |
| `GBRAIN_PROJECT_ID` | Override project ID |