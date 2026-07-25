#!/usr/bin/env python3
"""Normalize YAML frontmatter: ensure 'name' and 'description' appear first, then other keys sorted.
Preserves content after frontmatter.
"""
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
    # reorder keys
    ordered = {}
    for k in ('name','description'):
        if k in data:
            ordered[k] = data.pop(k)
    for k in sorted(data.keys()):
        ordered[k] = data[k]
    new_front = yaml.safe_dump(ordered, sort_keys=False).strip() + '\n'
    new_text = m.group(1) + new_front + m.group(3) + text[m.end():]
    if new_text != text:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_text)
        updated.append(os.path.relpath(path, ROOT))
        print('Formatted', os.path.relpath(path, ROOT))

print('Done. Files formatted:', len(updated))
