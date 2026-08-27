---
name: gbrain-sync
description: |
  GBrain integration - persistent vector knowledge base for AI agents.
  Syncs codebase to GBrain (PGLite local or Supabase remote) for cross-session
  code search, symbol lookup, and architectural memory. Use when you need
  persistent code intelligence across sessions and machines.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 2
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
triggers:
  - "sync gbrain"
  - "setup gbrain"
  - "index codebase"
  - "search code"
  - "code intelligence"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 1.0.0
  domain: context-memory
  integrates-with: [context-engineering, continuous-learning-v2, dev-craft, ui-craft, codegraph]
---
TOKEN CEILING: ~3K tokens. If skill exceeds, extract sections to references/.

# GBrain Sync — Persistent Code Intelligence

GBrain is a persistent vector knowledge base that gives AI agents long-term memory
across sessions and machines. This skill manages the sync pipeline between your
codebase and GBrain.

## What GBrain Provides

- **Cross-session code search** — Semantic search across your entire codebase history
- **Symbol lookup** — Find definitions, references, call graphs instantly
- **Architectural memory** — Remember decisions, patterns, conventions across projects
- **Multi-machine sync** — Same brain on laptop, desktop, CI, teammates' machines
- **Incremental indexing** — Only re-index changed files (fast!)

## Storage Options

| Backend | Use Case | Setup Time |
|---------|----------|------------|
| PGLite (local) | Solo, offline, privacy-first | ~30 seconds |
| Supabase (cloud) | Team sharing, multi-machine | ~90 seconds |
| Remote MCP | Existing GBrain server | ~10 seconds |

## Quick Start

```bash
# One-time setup (interactive)
gbrain-sync init

# Or quick PGLite local
gbrain-sync init --local

# Sync current repo
gbrain-sync sync

# Search
gbrain-sync search "authentication flow"
```

## Commands

### gbrain-sync init
Interactive setup wizard:
1. Choose backend: PGLite local / Supabase existing / Supabase auto-provision / Remote MCP
2. For Supabase: paste Personal Access Token or URL
3. Registers as MCP server for Claude Code
4. Writes `## GBrain Search Guidance` block to CLAUDE.md

### gbrain-sync sync
Incremental sync of current repo to GBrain:
- Detects changed files via git
- Extracts symbols, docs, patterns
- Updates vector index
- `--full` for complete reindex
- `--dry-run` to preview

### gbrain-sync search
Semantic search across indexed code:
```
gbrain-sync search "how does authentication work"
gbrain-sync search "UserService" --type symbols
gbrain-sync search "PIT calculation" --type docs
```

### gbrain-sync status
Shows sync status, index health, last sync time, file counts.

## Per-Repo Trust Policy

Each repo gets a trust tier (sticky across worktrees/branches):
- **read-write** — Search AND write new knowledge from this repo
- **read-only** — Search only (consultant mode: don't contaminate shared brain)
- **deny** — No GBrain interaction

## Integration with Skills

### dev-craft / ui-craft
- **ARCH-SCAN phase**: Auto-sync before analysis for better codebase map
- **SOURCE phase**: Use GBrain for official docs lookup
- **BUILD phase**: Query similar patterns in codebase
- **REVIEW phase**: Check for similar issues in history

### continuous-learning-v2
- Instincts can be backed by GBrain vectors
- Cross-project pattern recognition via promoted instincts

### context-engineering
- GBrain provides long-term context beyond session limits
- Handoff documents enriched with code references

## MCP Tools (when registered)

| Tool | Description |
|------|-------------|
| `gbrain search` | Semantic code search |
| `gbrain code-def` | Find symbol definition |
| `gbrain code-refs` | Find all references to symbol |
| `gbrain put` | Store knowledge (read-write tier) |
| `gbrain sync` | Trigger incremental sync |

## Configuration

GBrain config at `~/.gbrain/config.yaml`:
```yaml
backend: supabase  # pglite | supabase | mcp
supabase_url: "https://xxx.supabase.co"
pooler_url: "postgresql://..."
project_id: "my-project"
trust_tier: "read-write"  # per-repo, stored in brain
auto_sync: true  # sync on git push
incremental: true
```

## CLI Usage

```bash
# Install globally
npm install -g @agent-master-skills/gbrain-sync

# Or use via npx
npx gbrain-sync init
npx gbrain-sync sync
npx gbrain-sync search "error handling pattern"
```

## References

- `references/gbrain-config.yaml` — Configuration schema
- `references/sync-strategy.md` — Incremental sync algorithm
- `references/trust-policy.md` — Per-repo trust tiers
- `references/mcp-tools.md` — MCP tool definitions

## Related

- `continuous-learning-v2` — Instinct-based learning (can use GBrain as backend)
- `context-engineering` — Context management (GBrain extends context window)
- `codegraph` — Local code graph (GBrain is remote/persistent alternative)