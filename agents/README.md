---
owner: noname.spyware@gmail.com
allowedTools:
- file
- http

---

Agents directory

Place agent persona files in this folder as Markdown files with YAML frontmatter.
Required frontmatter keys:
- `name`
- `description`
- `mode` (subagent | assistant)

Validator: `tools/validate_agents.py` checks the frontmatter and exits non-zero on errors.
Each agent should include `samplePrompts` (non-empty list) and `owner`.
Run locally:

```bash
python tools/validate_agents.py
```
