#!/usr/bin/env python3
"""Audit SKILL.md frontmatter across skills/ and emit a CSV report.
Columns: path,name,description_present,description_starts_with_use_when,owner_present,allowedTools_present,allowedTools_count
"""
import os
import re
import csv
import yaml
from glob import glob

ROOT = os.path.dirname(os.path.dirname(__file__))
GLOB = os.path.join(ROOT, 'skills', '**', 'SKILL.md')

FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

rows = []
for path in glob(GLOB, recursive=True):
    rel = os.path.relpath(path, ROOT)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    m = FRONT_RE.search(text)
    data = {}
    if m:
        try:
            data = yaml.safe_load(m.group(1)) or {}
        except Exception:
            data = {}
    name = data.get('name')
    desc = data.get('description')
    owner = data.get('owner')
    atools = data.get('allowedTools')
    desc_ok = bool(desc and isinstance(desc, str) and desc.strip()!='')
    desc_start = False
    if desc_ok:
        desc_start = desc.strip().lower().startswith('use when')
    atools_count = len(atools) if isinstance(atools, list) else 0
    rows.append({
        'path': rel.replace('\\','/'),
        'name': name or '',
        'description_present': 'yes' if desc_ok else 'no',
        'description_starts_with_use_when': 'yes' if desc_start else 'no',
        'owner_present': 'yes' if owner else 'no',
        'allowedTools_present': 'yes' if atools else 'no',
        'allowedTools_count': atools_count,
    })

outdir = os.path.join(ROOT, 'REPORTS')
os.makedirs(outdir, exist_ok=True)
out = os.path.join(outdir, 'skills_audit.csv')
with open(out, 'w', newline='', encoding='utf-8') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=['path','name','description_present','description_starts_with_use_when','owner_present','allowedTools_present','allowedTools_count'])
    writer.writeheader()
    for r in sorted(rows, key=lambda x: x['path']):
        writer.writerow(r)
print('Wrote', out)
