#!/usr/bin/env python3
"""Redact secret-like patterns inside fenced code blocks and normalize remaining absolute paths.

Run: python tools/redact_skill_secrets.py
"""
import os
import re
from glob import glob

ROOT = os.path.dirname(os.path.dirname(__file__))
GLOB = os.path.join(ROOT, 'skills', '**', 'SKILL.md')

RE_ABS = re.compile(r"([A-Za-z]:[\\/][^\s'\"]+|/[^\s'\"]+)")
RE_AWS = re.compile(r"(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN|API_KEY|SECRET_KEY)", re.I)
RE_BEGIN_PRIV = re.compile(r"-----BEGIN .*PRIVATE KEY-----")
RE_END_PRIV = re.compile(r"-----END .*PRIVATE KEY-----")

modified = 0

for path in glob(GLOB, recursive=True):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    orig = ''.join(lines)
    out_lines = []
    in_fence = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('```'):
            # toggle fence
            in_fence = not in_fence
            out_lines.append(line)
            i += 1
            continue
        if in_fence:
            # redact private key blocks
            if RE_BEGIN_PRIV.search(line):
                out_lines.append('# REDACTED_PRIVATE_KEY\n')
                # skip until end marker
                i += 1
                while i < len(lines) and not RE_END_PRIV.search(lines[i]):
                    i += 1
                # if end marker present, skip it too
                if i < len(lines):
                    i += 1
                continue
            # redact known secret-like env assignments
            if RE_AWS.search(line):
                out_lines.append('# REDACTED_SECRET\n')
                i += 1
                continue
            out_lines.append(line)
            i += 1
            continue
        # outside fence: aggressively normalize absolute paths to ${PROJECT_ROOT}/basename
        def abs_repl(m):
            s = m.group(0)
            # don't touch URLs
            if s.startswith('http://') or s.startswith('https://'):
                return s
            tail = os.path.basename(s.rstrip('/\\'))
            return '${PROJECT_ROOT}/' + tail
        new_line = RE_ABS.sub(abs_repl, line)
        out_lines.append(new_line)
        i += 1

    new_text = ''.join(out_lines)
    if new_text != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        modified += 1
        print('Redacted', os.path.relpath(path, ROOT))

print('Done. Files modified:', modified)
