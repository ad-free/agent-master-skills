#!/usr/bin/env python3
"""Suggest `allowedTools` for SKILL.md and agents/*.md based on heuristic mapping.
Runs in-place and prints files updated.
"""
import os
import re
import yaml
from glob import glob

ROOT = os.path.dirname(os.path.dirname(__file__))
SKILL_GLOB = os.path.join(ROOT, 'skills', '**', 'SKILL.md')
AGENT_GLOB = os.path.join(ROOT, 'agents', '*.md')

front_re = re.compile(r"^(---\s*\n)(.*?)(\n---\s*\n)", re.S)

# heuristic mapping by keyword
MAP = {
    'dev-craft': ['python','git','shell'],
    'devops': ['shell','docker','kubernetes','terraform','git'],
    'devops-automation': ['shell','docker','kubernetes','terraform','git'],
    'ui-craft': ['file','http'],
    'image': ['file','http'],
    'bug-hunting': ['shell','git','http'],
    'security': ['shell','git','http'],
    'observability': ['http','docker','shell'],
    'testing': ['python','shell'],
    'testing-strategies': ['python','shell'],
    'documentation': ['file','python'],
    'code-review': ['git','python'],
    'code-review-and-quality': ['git','python'],
    'product': ['http','file'],
    'project-discovery': ['http','file'],
    'agent-orchestration': ['ai','http','git','shell'],
    'quality-gates': ['git','python'],
}

# default fallback
DEFAULT = ['file','http']

updated = []

def suggest_for_name(name):
    if not name:
        return DEFAULT
    n = name.lower()
    for k, v in MAP.items():
        if k in n:
            return v
    # try keyword split
    parts = n.replace('-', ' ').split()
    for p in parts:
        if p in MAP:
            return MAP[p]
    return DEFAULT

for path in glob(SKILL_GLOB, recursive=True) + glob(AGENT_GLOB):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    m = front_re.search(text)
    if m:
        try:
            data = yaml.safe_load(m.group(2)) or {}
        except Exception:
            data = {}
        name = data.get('name') or os.path.splitext(os.path.basename(path))[0]
        current = data.get('allowedTools')
        if current:
            continue
        suggestion = suggest_for_name(name)
        data['allowedTools'] = suggestion
        new_front = yaml.safe_dump(data, sort_keys=False).strip() + '\n'
        new_text = m.group(1) + new_front + m.group(3) + text[m.end():]
    else:
        # create frontmatter
        name = os.path.splitext(os.path.basename(path))[0]
        suggestion = suggest_for_name(name)
        new_text = '---\nallowedTools:\n'
        for t in suggestion:
            new_text += f"  - {t}\n"
        new_text += '---\n\n' + text
    if new_text != text:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_text)
        updated.append(os.path.relpath(path, ROOT))
        print('Suggested allowedTools for', os.path.relpath(path, ROOT))

print('Done. Files updated:', len(updated))
