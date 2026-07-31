---
{}

---

Agents directory

Place agent persona files in this folder as Markdown files with YAML frontmatter.
Required frontmatter keys (v2.0.0):
- `name`
- `description`
- `model`
- `allowed-tools` (v2.0.0) or `tools` (legacy)
- `mode` (subagent | assistant)
- `max-steps`
- `samplePrompts`
- `version`
- `owner`

Optional v2.0.0 fields: `preamble-tier`, `triggers`, `metadata`.

Validator: `tools/validate_agents.py` checks the frontmatter and exits non-zero on errors.
Each agent should include `samplePrompts` (non-empty list) and `owner`.
Run locally:

```bash
python tools/validate_agents.py
```
