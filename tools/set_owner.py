#!/usr/bin/env python3
"""Set `owner:` field in YAML frontmatter for SKILL.md and agents/*.md files.
Usage: python tools/set_owner.py "owner-identifier"
"""
import os
import re
import sys
from glob import glob
import yaml

if len(sys.argv) < 2:
    print('Usage: set_owner.py "owner-identifier"')
    sys.exit(2)

owner = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(__file__))

# files to update
skill_glob = os.path.join(ROOT, 'skills', '**', 'SKILL.md')
agents_glob = os.path.join(ROOT, 'agents', '*.md')

front_re = re.compile(r"^(---\s*\n)(.*?)(\n---\s*\n)", re.S)

updated = []
for path in glob(skill_glob, recursive=True) + glob(agents_glob):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    m = front_re.search(text)
    if m:
        front = m.group(2)
        try:
            data = yaml.safe_load(front) or {}
        except Exception:
            data = {}
        if data.get('owner') == owner:
            continue
        data['owner'] = owner
        new_front = yaml.safe_dump(data, sort_keys=False).strip() + '\n'
        new_text = m.group(1) + new_front + m.group(3) + text[m.end():]
    else:
        # create frontmatter
        import_text = f"---\nowner: {owner}\n---\n\n" + text
        new_text = import_text
    if new_text != text:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_text)
        updated.append(os.path.relpath(path, ROOT))
        print('Updated', os.path.relpath(path, ROOT))

print('Done. Files updated:', len(updated))
