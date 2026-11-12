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

REQUIRED = ["name", "description", "tools"]

# Fields Claude Code reads for agents/*.md (https://code.claude.com/docs/en/sub-agents)
KNOWN = set(REQUIRED) | {
    "disallowedTools", "model", "permissionMode", "maxTurns", "autoCompactWindow", "skills",
    "mcpServers", "hooks", "memory", "background", "effort", "isolation", "color",
    "initialPrompt", "omitClaudeMd", "experimental",
}
# Old fields Claude Code ignores; their presence means the limits they describe are not enforced
DEAD = {"allowed-tools", "max-steps", "mode", "triggers", "samplePrompts", "preamble-tier", "owner", "version"}

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Claude Code subagent models: aliases, or a full model ID (claude-*)
MODEL_ALIASES = {"sonnet", "opus", "haiku", "fable", "inherit"}

# Built-in tools agents may request; MCP tools (mcp__<server>__<tool>) are also accepted
ALLOWED_TOOLS = {
    "Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent", "AskUserQuestion",
    "WebSearch", "WebFetch", "NotebookEdit",
}


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
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        data[key.strip()] = val.strip().strip('"').strip("'")
    return data


def load_frontmatter(text):
    parsed = try_parse_yaml(text)
    if parsed is not None:
        return parsed
    return parse_frontmatter_fallback(text)


def validate_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    meta = load_frontmatter(text)
    if not meta:
        return False, "no frontmatter found"

    dead = sorted(DEAD & set(meta))
    if dead:
        return False, f"unsupported fields (ignored by Claude Code): {', '.join(dead)}"
    unknown = sorted(set(meta) - KNOWN)
    if unknown:
        return False, f"unknown fields: {', '.join(unknown)}"

    missing = [k for k in REQUIRED if not meta.get(k)]
    if missing:
        return False, f"missing metadata: {', '.join(missing)}"

    if not NAME_RE.match(str(meta["name"])):
        return False, f"name '{meta['name']}' must be kebab-case"

    model = meta.get("model")
    if model is not None and model not in MODEL_ALIASES and not str(model).startswith("claude-"):
        return (
            False,
            f"model '{model}' is not a Claude Code model ({', '.join(sorted(MODEL_ALIASES))}, or a claude-* ID)",
        )

    tools = meta["tools"]
    tool_list = tools if isinstance(tools, list) else [x.strip() for x in str(tools).split(",") if x.strip()]
    for t in tool_list:
        if t not in ALLOWED_TOOLS and not str(t).startswith("mcp__"):
            return False, f"tools contains unknown tool: {t} (allowed: {', '.join(sorted(ALLOWED_TOOLS))}, mcp__*)"

    if "maxTurns" in meta:
        mt = str(meta["maxTurns"])  # str: the fallback parser has no ints
        if not mt.isdigit() or not 1 <= int(mt) <= 100:
            return False, "maxTurns must be an integer between 1 and 100"

    return True, meta


def main():
    if not os.path.isdir(AGENTS_DIR):
        print("No agents directory found at agents/ — nothing to validate.")
        return 0

    failed = False
    for fname in sorted(os.listdir(AGENTS_DIR)):
        if not fname.endswith(".md"):
            continue
        # skip README which documents the agents directory
        if fname.lower() == "readme.md":
            print(f"SKIP: {fname} (documentation)")
            continue
        path = os.path.join(AGENTS_DIR, fname)
        ok, info = validate_file(path)
        if ok:
            name = info.get("name") if isinstance(info, dict) else str(info)
            print(f"OK: {fname} — {name}")
        else:
            print(f"ERROR: {fname} — {info}")
            failed = True

    if failed:
        print("\nAgent validation FAILED")
        return 1

    print(f"\nAll agent files validated OK — {datetime.utcnow().isoformat()}Z")
    return 0


if __name__ == "__main__":
    sys.exit(main())
