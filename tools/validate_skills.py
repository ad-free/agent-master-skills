#!/usr/bin/env python3
"""Validate SKILL.md files under skills/ for frontmatter and risky content.

Checks:
- YAML frontmatter contains `name` and `description` and `description` starts with "Use when"
- Warns/errors on absolute local paths, inline secrets patterns, risky commands
- Validates allowedTools against whitelist (if present)

Exit code 0 on success, non-zero if errors found.
"""
import os
import re
import sys
from glob import glob

try:
    import yaml
except Exception:
    yaml = None

ROOT = os.path.dirname(os.path.dirname(__file__))
SKILLS_GLOB = os.path.join(ROOT, 'skills', '**', 'SKILL.md')

RE_ABSOLUTE_PATH = re.compile(r"(^|\s)(/|[A-Za-z]:\\)")
RE_SECRET_LIKE = re.compile(r"(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|GCLOUD|gcloud auth|ssh .*@|-----BEGIN PRIVATE KEY-----|API_KEY|SECRET_KEY)", re.I)
RE_RISKY_CMDS = re.compile(r"\b(curl|wget|scp|ssh|aws|gcloud|kubectl)\b", re.I)
ALLOWED_TOOLS = {'python','bash','git','docker','kubectl','none'}

errors = []
warnings = []


def parse_frontmatter(text):
    if not text.startswith('---'):
        return None, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return None, text
    fm_text = parts[1]
    body = parts[2]
    if yaml:
        try:
            data = yaml.safe_load(fm_text)
            return data or {}, body
        except Exception:
            return None, body
    # fallback simple parser
    data = {}
    for line in fm_text.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip().strip('"')
    return data, body


for path in glob(SKILLS_GLOB, recursive=True):
    rel = os.path.relpath(path, ROOT)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        errors.append(f'{rel}: failed to read: {e}')
        continue
    fm, body = parse_frontmatter(text)
    if fm is None:
        errors.append(f'{rel}: missing or invalid YAML frontmatter')
        continue
    # check required keys
    name = fm.get('name')
    desc = fm.get('description')
    if not name:
        errors.append(f'{rel}: frontmatter missing `name`')
    if not desc:
        errors.append(f'{rel}: frontmatter missing `description`')
    else:
        if not isinstance(desc, str) or not desc.strip().startswith('Use when'):
            warnings.append(f'{rel}: description should start with "Use when" (discovery guidance)')
    # allowedTools check
    atools = fm.get('allowedTools')
    if atools is not None:
        if not isinstance(atools, list):
            warnings.append(f'{rel}: `allowedTools` should be a YAML list')
        else:
            for t in atools:
                if t not in ALLOWED_TOOLS:
                    warnings.append(f'{rel}: `allowedTools` contains unknown tool: {t}')
    # scan body for risky patterns
    # detect fenced code blocks and treat secrets inside them as warnings
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith('```'):
            in_fence = not in_fence
            continue
        if RE_SECRET_LIKE.search(line):
            if in_fence:
                warnings.append(f'{rel}:{i}: possible secret or creds pattern (inside code fence)')
            else:
                errors.append(f'{rel}:{i}: possible secret or creds pattern')
        # skip absolute path and risky command warnings when inside fenced code blocks
        if not in_fence:
            # ignore absolute-path warnings when the line already uses project placeholder
            if '${PROJECT_ROOT}' not in line and RE_ABSOLUTE_PATH.search(line):
                warnings.append(f'{rel}:{i}: absolute path detected (non-portable)')
            if RE_RISKY_CMDS.search(line):
                # it's okay to mention kubectl/git, but flag for review
                warnings.append(f'{rel}:{i}: risky/exec command mentioned')

# summarize
if errors:
    print('ERRORS:')
    for e in errors:
        print(' -', e)
else:
    print('No blocking errors found.')

if warnings:
    print('\nWarnings:')
    for w in warnings:
        print(' -', w)

if errors:
    sys.exit(2)

sys.exit(0)
