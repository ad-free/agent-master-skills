#!/usr/bin/env python3
"""Validator for agent markdown files in `agents/`.

Checks YAML frontmatter for required keys and optional richer fields.
If `pyyaml` is available it will parse frontmatter robustly; otherwise
it falls back to a lightweight parser.
"""
import os
import re
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(__file__))
AGENTS_DIR = os.path.join(ROOT, "agents")

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)

REQUIRED = ["name", "description", "mode", "samplePrompts"]
OPTIONAL = ["version", "allowedTools"]
ALLOWED_TOOLS = {"python", "bash", "git", "docker", "kubectl", "none"}


def try_parse_yaml(text):
    try:
        import yaml
    except Exception:
        return None
    m = FRONTMATTER_RE.search(text)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return None


def parse_frontmatter_fallback(text):
    m = FRONTMATTER_RE.search(text)
    if not m:
        return {}
    body = m.group(1)
    data = {}
    for line in body.splitlines():
        if not line.strip() or line.strip().startswith('#'):
            continue
        if ':' not in line:
            continue
        key, val = line.split(':', 1)
        data[key.strip()] = val.strip().strip('"').strip("'")
    return data


def load_frontmatter(text):
    parsed = try_parse_yaml(text)
    if parsed is not None:
        return parsed
    return parse_frontmatter_fallback(text)


def validate_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()

    meta = load_frontmatter(text)
    if not meta:
        return False, "no frontmatter found"

    missing = [k for k in REQUIRED if not meta.get(k)]
    if missing:
        return False, f"missing metadata: {', '.join(missing)}"

    # mode sanity
    if meta.get('mode') not in ('subagent', 'assistant'):
        return False, "invalid mode (must be 'subagent' or 'assistant')"

    # optional validations
    if 'version' in meta:
        try:
            # simple semantic version-ish check
            _ = tuple(int(x) for x in str(meta.get('version')).split('.') if x)
        except Exception:
            return False, "invalid version format"

    if 'allowedTools' in meta:
        at = meta.get('allowedTools')
        if isinstance(at, str):
            items = [x.strip() for x in at.split(',') if x.strip()]
        elif isinstance(at, list):
            items = at
        else:
            return False, "allowedTools must be a list or comma-separated string"
        for item in items:
            if item not in ALLOWED_TOOLS:
                return False, f"allowedTools contains unknown tool: {item}"

    # samplePrompts must be a non-empty list
    sp = meta.get('samplePrompts')
    if not isinstance(sp, list) or not sp:
        return False, "samplePrompts must be a non-empty list of example prompts"

    return True, meta


def main():
    if not os.path.isdir(AGENTS_DIR):
        print("No agents directory found at agents/ — nothing to validate.")
        return 0

    failed = False
    for fname in sorted(os.listdir(AGENTS_DIR)):
        if not fname.endswith('.md'):
            continue
        # skip README which documents the agents directory
        if fname.lower() == 'readme.md':
            print(f"SKIP: {fname} (documentation)")
            continue
        path = os.path.join(AGENTS_DIR, fname)
        ok, info = validate_file(path)
        if ok:
            name = info.get('name') if isinstance(info, dict) else str(info)
            print(f"OK: {fname} — {name}")
        else:
            print(f"ERROR: {fname} — {info}")
            failed = True

    if failed:
        print('\nAgent validation FAILED')
        return 1

    print(f"\nAll agent files validated OK — {datetime.utcnow().isoformat()}Z")
    return 0


if __name__ == '__main__':
    sys.exit(main())
