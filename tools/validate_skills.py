#!/usr/bin/env python3
"""Validate SKILL.md files under skills/ for frontmatter and risky content.

Checks:
- YAML frontmatter contains required keys: name, description (the only keys hosts need; others are optional)
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

# Machine-local roots only: a bare "/" also matched "A / B" prose and "/>" in JSX
RE_ABSOLUTE_PATH = re.compile(r"(^|[\s`'\"(])(/(home|Users|root|mnt|opt|var|tmp|etc|usr|private)/|[A-Za-z]:\\)")
RE_SECRET_LIKE = re.compile(r"(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|GCLOUD|gcloud auth|ssh .*@|-----BEGIN PRIVATE KEY-----|API_KEY|SECRET_KEY)", re.I)
RE_RISKY_CMDS = re.compile(r"\b(curl|wget|scp|ssh|aws|gcloud|kubectl)\b", re.I)
ALLOWED_TOOLS = {'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob', 'Agent', 'AskUserQuestion', 'WebSearch', 'Task'}

# Required frontmatter keys
REQUIRED_KEYS = ['name', 'description']
# Fields Claude Code ignores for skills; version belongs under metadata
DEAD_KEYS = ('triggers', 'preamble-tier', 'version', 'preferred-model')

# Archived skills and the claude.ai sync folder are not part of the library
SKIP_DIRS = ('_archive', 'synced')

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
    if any(part in SKIP_DIRS for part in rel.split(os.sep)):
        continue
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
    if 'model' in fm:
        errors.append(f'{rel}: top-level `model` switches the model for that turn, and each switch and switch-back '
                      'drops the prompt cache (costs more, not less); remove it')
    for key in DEAD_KEYS:
        if key in fm:
            errors.append(f'{rel}: `{key}` is not a skill field Claude Code reads; remove it (version: under metadata)')
    if 'preferred-model' in (fm.get('metadata') or {}):
        errors.append(f'{rel}: `metadata.preferred-model` is unused; remove it')
    for key in REQUIRED_KEYS:
        if key not in fm:
            errors.append(f'{rel}: frontmatter missing required key `{key}`')
    # name validation
    name = fm.get('name')
    if not name:
        errors.append(f'{rel}: frontmatter missing `name`')
    # description validation
    desc = fm.get('description')
    if desc:
        if not isinstance(desc, str) or not desc.strip().startswith('Use when'):
            warnings.append(f'{rel}: description should start with "Use when" (discovery guidance)')
    else:
        errors.append(f'{rel}: frontmatter missing `description`')
    # allowed-tools validation
    atools = fm.get('allowed-tools')
    if atools is not None:
        if not isinstance(atools, list):
            warnings.append(f'{rel}: `allowed-tools` should be a YAML list')
        else:
            for t in atools:
                if t not in ALLOWED_TOOLS:
                    warnings.append(f'{rel}: `allowed-tools` contains unknown tool: {t} (allowed: {", ".join(sorted(ALLOWED_TOOLS))})')
    # scan body for risky patterns
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith('```'):
            in_fence = not in_fence
        if in_fence:
            if RE_SECRET_LIKE.search(line):
                warnings.append(f'{rel}:{i}: possible secret in fenced code block')
        if RE_ABSOLUTE_PATH.search(line):
            warnings.append(f'{rel}:{i}: absolute path detected (prefer relative paths)')
        if RE_RISKY_CMDS.search(line):
            warnings.append(f'{rel}:{i}: risky command detected (curl, wget, scp, ssh, aws, gcloud, kubectl)')

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

sys.exit(1 if errors else 0)