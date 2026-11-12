# Agents

Subagent files for Claude Code, Markdown with YAML frontmatter (schema: https://code.claude.com/docs/en/sub-agents).

| Agent | Role | Tools |
|---|---|---|
| `code-reviewer` | Read-only review of a diff file against the brief | Read, Grep, Glob (no shell) |
| `verifier` | Fresh full run, mutation spot-check, REQ-to-test check | Read, Grep, Glob, Bash, Edit, Write (tests only) |
| `ui-verifier` | Browser screenshots at 1440/390, console errors, compare to reference | Read, Grep, Glob, Bash, Playwright MCP |

`dev-craft/references/test-agent.md` says when each is dispatched. Unused agents live in `_archive/`.

Frontmatter: `name` (kebab-case) and `description` required; `tools`, `model`, `maxTurns` expected. Old fields
(`allowed-tools`, `max-steps`, `mode`, `triggers`, `samplePrompts`, `preamble-tier`, `owner`, `version`) are
rejected because Claude Code ignores them. Start from `AGENT_TEMPLATE.md`.

```bash
python3 tools/validate_agents.py
```
