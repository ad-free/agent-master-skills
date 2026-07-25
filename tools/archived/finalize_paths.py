# Archived helper: finalize_paths.py
# Original moved to archived on 2026-07-25

#!/usr/bin/env python3
"""Aggressively replace remaining absolute paths in SKILL.md files with ${PROJECT_ROOT}/basename.

Use with caution: this rewrites examples that contain absolute paths.
"""
import os
import re
from glob import glob

ROOT = os.path.dirname(os.path.dirname(__file__))
GLOB = os.path.join(ROOT, 'skills', '**', 'SKILL.md')

RE_ABS = re.compile(r"([A-Za-z]:[\\/][^\s'\"]+|/[^\s'\"]+)")

modified = 0
for path in glob(GLOB, recursive=True):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    orig = text

    def repl(m):
        s = m.group(0)
        if '${PROJECT_ROOT}' in s or s.startswith('http://') or s.startswith('https://'):
            return s
        tail = os.path.basename(s.rstrip('/\\'))
        return '${PROJECT_ROOT}/' + tail

    new_text = RE_ABS.sub(repl, text)
    if new_text != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        modified += 1
        print('Finalized', os.path.relpath(path, ROOT))

print('Done. Files modified:', modified)
