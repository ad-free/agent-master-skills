#!/usr/bin/env python3
"""Remove `owner` and `allowedTools` keys from YAML frontmatter of SKILL and agent files."""
import os
import re
import yaml
from glob import glob

ROOT = os.path.dirname(os.path.dirname(__file__))
SKILL_GLOB = os.path.join(ROOT, 'skills', '**', 'SKILL.md')
AGENT_GLOB = os.path.join(ROOT, 'agents', '*.md')
front_re = re.compile(r"^(---\s*\n)(.*?)(\n---\s*\n)", re.S)

updated = []
for path in glob(SKILL_GLOB, recursive=True) + glob(AGENT_GLOB):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    m = front_re.search(text)
    if not m:
        continue
    try:
        data = yaml.safe_load(m.group(2)) or {}
    except Exception:
        continue
    changed = False
    if 'owner' in data:
        del data['owner']
        changed = True
    if 'allowedTools' in data:
        del data['allowedTools']
        changed = True
    if changed:
        new_front = yaml.safe_dump(data, sort_keys=False).strip() + '\n'
        new_text = m.group(1) + new_front + m.group(3) + text[m.end():]
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_text)
        updated.append(os.path.relpath(path, ROOT))
        print('Updated', os.path.relpath(path, ROOT))

print('Done. Files updated:', len(updated))
