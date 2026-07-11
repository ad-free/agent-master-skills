#!/usr/bin/env python3
"""
Stack version detection and resolution for ui-craft.
Detects exact framework versions from project files or prompts user.
"""

import json
import re
import subprocess
from pathlib import Path

STACK_RULES = {
    "react": {
        "detect": {"file": "package.json", "key": "react"},
        "docs_url": "https://react.dev/reference/react",
        "patterns": {
            "19": {
                "use": [
                    "useActionState",
                    "use()",
                    "Server Components",
                    "useOptimistic",
                ],
                "avoid": ["Class components", "legacy context", "UNSAFE_*"],
            },
            "18": {
                "use": ["useTransition", "useDeferredValue", "Suspense", "useId"],
                "avoid": ["UNSAFE_componentWillMount", "legacy lifecycle"],
            },
        },
    },
    "nextjs": {
        "detect": {"file": "package.json", "key": "next"},
        "docs_url": "https://nextjs.org/docs",
        "patterns": {
            "15": {
                "use": ["App Router", "Server Actions", "next/navigation"],
                "avoid": ["Pages Router", "getServerSideProps"],
            },
            "14": {
                "use": ["App Router", "getServerSideProps"],
                "avoid": ["getInitialProps", "next/router"],
            },
        },
    },
    "tailwindcss": {
        "detect": {"file": "package.json", "key": "tailwindcss"},
        "docs_url": "https://tailwindcss.com/docs",
        "patterns": {
            "4": {
                "use": [
                    '@import "tailwindcss"',
                    "CSS-first config",
                    "@theme directive",
                ],
                "avoid": ["@tailwind directives", "JS config"],
            },
            "3": {
                "use": ["tailwind.config.js", "@tailwind directives"],
                "avoid": ["v1/v2 syntax"],
            },
        },
    },
    "typescript": {
        "detect": {"file": "package.json", "key": "typescript"},
        "docs_url": "https://www.typescriptlang.org/docs/",
        "patterns": {
            "5": {
                "use": ["satisfies", "const type parameters", "decorators"],
                "avoid": ["legacy enum patterns"],
            }
        },
    },
}


def detect_from_package_json(filepath: str) -> dict:
    """Detect versions from package.json"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    versions = {}
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

    for stack, config in STACK_RULES.items():
        key = config["detect"]["key"]
        if key in deps:
            version_str = deps[key].lstrip("^~>=<")
            versions[stack] = version_str

    return versions


def detect_from_config_files(project_dir: str) -> dict:
    """Detect versions from config files beyond package.json"""
    versions = {}
    project_path = Path(project_dir)

    # Tailwind v4 detection (CSS-first config)
    css_files = list(project_path.rglob("*.css")) + list(project_path.rglob("*.pcss"))
    for css_file in css_files:
        try:
            content = css_file.read_text(encoding="utf-8")
            if '@import "tailwindcss"' in content or "@import 'tailwindcss'" in content:
                versions["tailwindcss"] = "4"
                break
        except Exception:
            pass

    # Tailwind v3 detection (JS config)
    if "tailwindcss" not in versions:
        for pattern in [
            "tailwind.config.js",
            "tailwind.config.ts",
            "tailwind.config.mjs",
        ]:
            if (Path(project_dir) / pattern).exists():
                versions["tailwindcss"] = "3"
                break

    return versions


def fetch_latest_version(package_name: str) -> str:
    """Fetch latest version from npm registry"""
    try:
        result = subprocess.run(
            ["npm", "view", package_name, "version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return "latest"


def resolve_versions(project_dir: str, user_stack: dict | None = None) -> dict:
    """
    Resolve stack versions for the project.

    Args:
        project_dir: Project directory to scan
        user_stack: Optional user-provided stack overrides

    Returns:
        dict of {stack_name: version_string}
    """
    project_path = Path(project_dir)
    versions = {}

    # Detect from package.json
    pkg_json = project_path / "package.json"
    if pkg_json.exists():
        versions.update(detect_from_package_json(str(pkg_json)))

    # Detect from config files
    config_versions = detect_from_config_files(project_dir)
    versions.update(config_versions)

    # Apply user overrides
    if user_stack:
        versions.update(user_stack)

    return versions


def get_docs_url(stack: str, version: str) -> str | None:
    """Get the official docs URL for a specific stack version."""
    config = STACK_RULES.get(stack)
    if not config:
        return None

    base_url = config["docs_url"]
    version_specific = {
        "react": {
            "19": "https://react.dev/reference/react",
            "18": "https://react.dev/reference/react",
        },
        "nextjs": {
            "15": "https://nextjs.org/docs/app",
            "14": "https://nextjs.org/docs/app",
        },
        "tailwindcss": {
            "4": "https://tailwindcss.com/docs",
            "3": "https://v3.tailwindcss.com/docs",
        },
        "typescript": {
            "5": "https://www.typescriptlang.org/docs/",
        },
    }
    stack_docs = version_specific.get(stack, {})
    return stack_docs.get(version, base_url)


def get_version_patterns(stack: str, version: str) -> dict:
    """Get the patterns to use/avoid for a specific stack version."""
    config = STACK_RULES.get(stack)
    if not config:
        return {"use": [], "avoid": []}

    # Match major version
    major = version.split(".")[0]
    patterns = config["patterns"]
    if major in patterns:
        return patterns[major]
    # Fallback to latest known
    if patterns:
        latest = max(patterns.keys())
        return patterns[latest]
    return {"use": [], "avoid": []}


def format_version_summary(versions: dict) -> str:
    """Format version summary for display."""
    lines = ["STACK DETECTED:"]
    for stack, version in versions.items():
        config = STACK_RULES.get(stack, {})
        docs = get_docs_url(stack, version)
        lines.append(f"- {stack.title()} {version}")
        if docs:
            lines.append(f"  Docs: {docs}")
    return "\n".join(lines)
