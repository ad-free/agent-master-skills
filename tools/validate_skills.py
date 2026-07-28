#!/usr/bin/env python3
"""Validate SKILL.md files under skills/ for frontmatter and risky content.

Checks:
- YAML frontmatter contains required keys: name, description, version, preamble-tier, allowed-tools, triggers
- Warns/errors on absolute local paths, inline secrets patterns, risky commands
- Validates allowedTools against whitelist (if present)
- Validates gate patterns: HUMAN CHECKPOINT — Gate N
- Validates out-of-scope detection pattern

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
ALLOWED_TOOLS = {'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob', 'Agent', 'AskUserQuestion', 'WebSearch', 'Task'}

# Required frontmatter keys
REQUIRED_KEYS = ['name', 'description', 'version', 'preamble-tier', 'allowed-tools', 'triggers']

# Gate pattern to validate
GATE_PATTERN = re.compile(r'###\s*\[\d+(\.\d+)?\]\s*HUMAN CHECKPOINT\s*—\s*Gate\s+\d+:')

# Out-of-scope pattern
OUT_OF_SCOPE_PATTERN = re.compile(r'Out-of-scope detection.*runs at every gate')

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
    # version validation
    version = fm.get('version')
    if version:
        try:
            _ = tuple(int(x) for x in str(version).split('.') if x)
        except Exception:
            warnings.append(f'{rel}: `version` should be semantic version (e.g., 1.0.0)')
    # preamble-tier validation
    tier = fm.get('preamble-tier')
    if tier is not None:
        try:
            t = int(tier)
            if t < 1 or t > 4:
                warnings.append(f'{rel}: `preamble-tier` should be 1-4')
        except (ValueError, TypeError):
            warnings.append(f'{rel}: `preamble-tier` should be integer 1-4')
    # allowed-tools validation
    atools = fm.get('allowed-tools')
    if atools is not None:
        if not isinstance(atools, list):
            warnings.append(f'{rel}: `allowed-tools` should be a YAML list')
        else:
            for t in atools:
                if t not in ALLOWED_TOOLS:
                    warnings.append(f'{rel}: `allowed-tools` contains unknown tool: {t} (allowed: {", ".join(sorted(ALLOWED_TOOLS))})')
    # triggers validation
    triggers = fm.get('triggers')
    if triggers is not None:
        if not isinstance(triggers, list):
            warnings.append(f'{rel}: `triggers` should be a YAML list')
        elif len(triggers) == 0:
            warnings.append(f'{rel}: `triggers` list should not be empty')
    # validate gate patterns in body
    gate_matches = GATE_PATTERN.findall(text)
    if len(gate_matches) == 0:
        # Only warn for pipeline skills that should have gates
        if fm.get('name') in ('dev-craft', 'ui-craft'):
            warnings.append(f'{rel}: No HUMAN CHECKPOINT gate patterns found (expected for pipeline skills)')
    # validate out-of-scope pattern
    if 'Out-of-scope detection' not in text and fm.get('name') in ('dev-craft', 'ui-craft'):
        warnings.append(f'{rel}: No out-of-scope detection pattern found (expected for pipeline skills)')
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