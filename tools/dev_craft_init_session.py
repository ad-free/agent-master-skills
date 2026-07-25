#!/usr/bin/env python3
"""Create or resume a .dev-craft session.

Usage: python tools/dev_craft_init_session.py /path/to/project --task "short task"

Creates `.dev-craft/` if missing, initializes `state.json` and creates a
`sessions/session-YYYYMMDD-N.md` file, then writes `sessionFile` into state.json.
"""
import json
import os
import sys
from datetime import datetime


def usage():
    print("Usage: python tools/dev_craft_init_session.py /path/to/project --task \"short task\"")


def main():
    if len(sys.argv) < 4:
        usage(); return 2
    root = sys.argv[1]
    if sys.argv[2] != '--task':
        usage(); return 2
    task = sys.argv[3]

    dc = os.path.join(root, '.dev-craft')
    sessions_dir = os.path.join(dc, 'sessions')
    os.makedirs(sessions_dir, exist_ok=True)

    state_path = os.path.join(dc, 'state.json')
    state = {}
    if os.path.isfile(state_path):
        try:
            with open(state_path, encoding='utf-8') as f:
                state = json.load(f)
        except Exception:
            state = {}

    # create a new session file
    date = datetime.utcnow().strftime('%Y%m%d')
    # find next index
    idx = 1
    while True:
        name = f'session-{date}-{idx}.md'
        path = os.path.join(sessions_dir, name)
        if not os.path.exists(path):
            break
        idx += 1

    content = f"# Session {date}-{idx}\n\n**Task:** {task}\n**Created:** {datetime.utcnow().isoformat()}Z\n\n"
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    # update state
    state['sessionFile'] = os.path.join('sessions', name)
    state.setdefault('currentPhase', 'SCOPE')
    state.setdefault('completedPhases', [])
    state.setdefault('slices', [])
    state['task'] = task

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)

    print(f"Created session: {path}")
    print(f"Updated state: {state_path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
