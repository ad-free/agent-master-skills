# Skill Authoring Guide

Quick rules to write discoverable, safe, and CI-friendly SKILL.md files.

- Frontmatter:
  - `name` (required): hyphenated lowercase identifier
  - `description` (required): start with "Use when" and describe trigger conditions only
  - `owner` (recommended): contact/email for maintainers
  - `allowedTools` (optional): list from `{python,bash,git,docker,kubectl,none}`

- Structure:
  - Sections: Overview, When to Use, Implementation/Examples, Common Mistakes
  - Keep examples small (<100 lines); prefer linking to scripts in `scripts/`

- Safety:
  - Never include secrets or full credentials
  - Avoid absolute local paths in examples; use `${PROJECT_ROOT}` or `./` relative paths
  - Prefer showing commands without executing credentials (no inline `aws configure` with keys)

- Persistence & Files:
  - If skill writes files, explicitly document `--output-dir` and `--persist` usage

- Tests & TDD:
  - Include at least one pressure scenario or example that an automated test could run

- CI:
  - Keep commands reproducible; prefer `python -m` or `py -3` over relying on `python` ambiguity

This repo validates frontmatter and scans for risky patterns. Run locally:

```bash
python tools/validate_skills.py
python tools/validate_agents.py
pytest -q
```
