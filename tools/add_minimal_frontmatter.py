#!/usr/bin/env python3
"""Add minimal frontmatter (name, description) to SKILL.md files missing them."""
import os
import re
from glob import glob
import yaml

ROOT = os.path.dirname(os.path.dirname(__file__))
SKILL_GLOB = os.path.join(ROOT, 'skills', '**', 'SKILL.md')
front_re = re.compile(r"^(---\s*\n)(.*?)(\n---\s*\n)", re.S)

updated = []
for path in glob(SKILL_GLOB, recursive=True):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    m = front_re.search(text)
    if m:
        try:
            data = yaml.safe_load(m.group(2)) or {}
        except Exception:
            data = {}
        need = False
        if not data.get('name'):
            # derive name from path
            name = os.path.basename(os.path.dirname(path))
            data['name'] = name
            need = True
        if not data.get('description'):
            data['description'] = f"Use when you need the {data.get('name')} skill (plugin)."
            need = True
        if need:
            new_front = yaml.safe_dump(data, sort_keys=False).strip() + '\n'
            new_text = m.group(1) + new_front + m.group(3) + text[m.end():]
            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(new_text)
            updated.append(os.path.relpath(path, ROOT))
            print('Added frontmatter to', os.path.relpath(path, ROOT))
    else:
        # no frontmatter at all
        name = os.path.basename(os.path.dirname(path))
        front = {'name': name, 'description': f"Use when you need the {name} skill (plugin)."}
        new_front = yaml.safe_dump(front, sort_keys=False).strip() + '\n'
        new_text = '---\n' + new_front + '---\n\n' + text
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_text)
        updated.append(os.path.relpath(path, ROOT))
        print('Created frontmatter for', os.path.relpath(path, ROOT))

print('Done. Files updated:', len(updated))
