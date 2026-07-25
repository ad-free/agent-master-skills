#!/usr/bin/env python3
"""Validate a .dev-craft state directory for integrity.

Usage: python tools/validate_dev_craft_state.py /path/to/project
Checks:
 - .dev-craft/state.json exists and is valid JSON
 - state.json contains `currentPhase` and `sessionFile`
 - referenced session file exists under .dev-craft/sessions/
 - if 'BUILD' in completedPhases then `slices` should be non-empty
"""
import json
import os
import sys


def err(msg):
    print("ERROR:", msg)
    return 1


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/validate_dev_craft_state.py /path/to/project")
        return 2
    root = sys.argv[1]
    dc = os.path.join(root, ".dev-craft")
    state_path = os.path.join(dc, "state.json")
    if not os.path.isdir(dc):
        return err(f".dev-craft not found at {dc}")
    if not os.path.isfile(state_path):
        return err(f"state.json not found at {state_path}")

    try:
        with open(state_path, encoding='utf-8') as f:
            state = json.load(f)
    except Exception as e:
        return err(f"failed reading state.json: {e}")

    if 'currentPhase' not in state:
        return err("state.json missing 'currentPhase'")
    if 'sessionFile' not in state:
        return err("state.json missing 'sessionFile'")

    session_file = os.path.join(dc, state['sessionFile']) if not os.path.isabs(state['sessionFile']) else state['sessionFile']
    if not os.path.isfile(session_file):
        return err(f"session file referenced in state.json not found: {session_file}")

    completed = state.get('completedPhases', [])
    slices = state.get('slices', [])
    if 'BUILD' in completed and not slices:
        print("WARNING: BUILD marked complete but 'slices' is empty")

    print(".dev-craft state OK")
    return 0


if __name__ == '__main__':
    sys.exit(main())
