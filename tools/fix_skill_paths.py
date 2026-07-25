#!/usr/bin/env python3
"""Fix SKILL.md files: normalize frontmatter description to start with 'Use when' and replace absolute paths with ${PROJECT_ROOT} placeholders.

Run: python tools/fix_skill_paths.py
"""
import os
import re
from glob import glob

ROOT = os.path.dirname(os.path.dirname(__file__))
GLOB = os.path.join(ROOT, 'skills', '**', 'SKILL.md')

RE_DRIVE = re.compile(r"[A-Za-z]:[\\/][^\s'\"]+")
# match unix-like absolute paths but avoid matching URLs (http/https)
RE_UNIX_ABS = re.compile(r"(/[^\s'\"\)]+)")
RE_RISKY = re.compile(r"\b(curl|wget|scp|ssh|aws|gcloud|kubectl)\b", re.I)

count=0

for path in glob(GLOB, recursive=True):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    orig = text
    # frontmatter description normalization
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]
            # find description line
            new_fm_lines = []
            changed_fm = False
            for line in fm.splitlines():
                if line.strip().startswith('description:'):
                    # extract value
                    m = re.match(r"description:\s*(?:\"|')?(.*?)(?:\"|')?$", line.strip())
                    if m:
                        desc = m.group(1).strip()
                        if not desc.startswith('Use when'):
                            desc = 'Use when ' + desc[0].lower() + desc[1:] if desc and desc[0].isupper() else 'Use when ' + desc
                            new_fm_lines.append(f'description: {desc}')
                            changed_fm = True
                            continue
                new_fm_lines.append(line)
            if changed_fm:
                new_fm = '\n'.join(new_fm_lines)
                text = '---' + new_fm + '---' + body
    # replace Windows drive paths with placeholder
    def drive_repl(m):
        s = m.group(0)
        tail = os.path.basename(s)
        return '${PROJECT_ROOT}/' + tail
    text = RE_DRIVE.sub(drive_repl, text)
    # replace unix abs paths of common roots
    def unix_repl(m):
        s = m.group(1)
        tail = os.path.basename(s)
        return '${PROJECT_ROOT}/' + tail
    # skip replacing unix-like paths on lines that contain http(s) to avoid URL corruption
    new_lines = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith('```'):
            # toggle fenced block state and preserve fence line
            in_fence = not in_fence
            new_lines.append(line)
            continue
        if 'http://' in line or 'https://' in line:
            new_lines.append(line)
            continue
        # first, replace typical absolute paths
        processed = RE_UNIX_ABS.sub(unix_repl, line)
        # then, prefix any remaining '/some/path' fragments that aren't already using ${PROJECT_ROOT}
        if '${PROJECT_ROOT}' not in processed:
            processed = re.sub(r"(?<!\$\{PROJECT_ROOT\})(/[-\w\./]+)", r"${PROJECT_ROOT}\1", processed)

        # if outside a fenced block and the line mentions risky exec commands, wrap as an example code fence
        if not in_fence and RE_RISKY.search(processed):
            new_lines.append('```bash')
            new_lines.append('# EXAMPLE (do not run)')
            new_lines.append(processed)
            new_lines.append('```')
        else:
            new_lines.append(processed)
    text = '\n'.join(new_lines)
    if text != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        count += 1
        print('Patched', os.path.relpath(path, ROOT))

print('Done. Files modified:', count)
