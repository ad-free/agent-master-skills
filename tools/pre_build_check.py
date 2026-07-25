#!/usr/bin/env python3
"""Pre-build check: ensure .dev-craft session exists or create one.

Usage:
  python tools/pre_build_check.py /path/to/project --task "short task"
If .dev-craft/state.json or sessions are missing, this will create a session via
`dev_craft_init_session.py`.
"""
import os
import sys
import subprocess


def main():
    if len(sys.argv) < 3 or sys.argv[2] != '--task':
        print('Usage: python tools/pre_build_check.py /path/to/project --task "short task"')
        return 2
    root = sys.argv[1]
    task = sys.argv[3]
    dc = os.path.join(root, '.dev-craft')
    state = os.path.join(dc, 'state.json')
    if os.path.isdir(dc) and os.path.isfile(state):
        print('.dev-craft state exists — nothing to do')
        return 0
    print('.dev-craft missing or incomplete — creating session')
    script = os.path.join(os.path.dirname(__file__), 'dev_craft_init_session.py')
    cmd = [sys.executable, script, root, '--task', task]
    res = subprocess.run(cmd)
    return res.returncode


if __name__ == '__main__':
    sys.exit(main())
