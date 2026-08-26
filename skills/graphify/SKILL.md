---
name: graphify
description: Use for any question about a codebase, its architecture, file relationships, or project content — especially when graphify-out/ exists, where the question should be treated as a graphify query first. Turns any input (code, docs, papers, images, videos) into a persistent knowledge graph with god nodes, community detection, and query/path/explain tools.
model: big-pickle
version: 1.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "graphify"
  - "knowledge graph"
  - "codebase analysis"
  - "community detection"
  - "graph report"
metadata:
  origin: external
---

# /graphify

Turn any folder of files into a navigable knowledge graph with community detection, an honest audit trail, and three outputs: interactive HTML, GraphRAG-ready JSON, and a plain-language GRAPH_REPORT.md.

## Usage

```
# graphify                                              # full pipeline on current directory (HTML viz; add --obsidian for a vault)
# graphify <path>                                      # full pipeline on specific path
# graphify https://github.com/<owner>/<repo>           # clone repo then run full pipeline on it
# graphify https://github.com/<owner>/<repo> --branch <branch>  # clone a specific branch
# graphify <url1> <url2> ...                           # clone multiple repos, build each, merge into one cross-repo graph
# graphify <path> --mode deep                          # thorough extraction, richer INFERRED edges
# graphify <path> --update                             # incremental - re-extract only new/changed files
# graphify <path> --directed                            # build directed graph (preserves edge direction: source→target)

### Query commands (after build):
graphify query "<question>"                            # natural language query on graph
graphify path "<A>" "<B>"                              # shortest path between two symbols
graphify explain "<concept>"                           # explain concept via graph neighborhood
```
