#!/usr/bin/env python3
"""Lightweight eval harness runner.

Discovers eval test cases under `skills/**/eval/cases/*.yaml`, executes
deterministic checks (file existence, JSON-path assertions) against skill
state, and emits pass/fail results. Serves as the CI gate for skill changes.

Commands:
  eval_harness.py run --skill <name>     # run cases for one skill
  eval_harness.py ci                     # run all cases, fail on any regression
  eval_harness.py list                   # list discovered cases

Verification kinds supported in a case's `verification` block:
  files: [{path, mustExist}]             # file presence checks
  assertions: [{type, path, expected}]   # equals | contains | not_contains
                                         #   (path applied to state.json)

Note: this is the deterministic skeleton. Model-based graders and pass@k
trials are orchestrated by the eval-harness/agent-eval skills, not here.
"""
import argparse
import json
import os
import re
import sys
from glob import glob

try:
    import yaml
except Exception:
    yaml = None

ROOT = os.path.dirname(os.path.dirname(__file__))
CASES_GLOB = os.path.join(ROOT, 'skills', '**', 'eval', 'cases', '*.yaml')


def discover_cases():
    return sorted(glob(CASES_GLOB, recursive=True))


def load_case(path):
    if yaml is None:
        raise RuntimeError('pyyaml is required to load eval cases')
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def get_value(state, json_path):
    """Resolve a JSONPath-ish path like `$.state.topology` in state dict."""
    if not json_path or not json_path.startswith('$.'):
        return None
    current = state
    for part in json_path[2:].split('.'):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def run_case(path):
    case = load_case(path)
    name = case.get('name', os.path.basename(path))
    verification = case.get('verification', {})
    results = []

    # File presence checks
    for fspec in verification.get('files', []):
        fpath = fspec.get('path', '')
        full = os.path.join(ROOT, fpath)
        exists = os.path.isfile(full)
        want = fspec.get('mustExist', True)
        results.append((f'file exists: {fpath}', exists == want))

    # Assertions against a state.json if the case provides one
    # under eval/state.json or eval/state/state.json
    state = {}
    eval_dir = os.path.dirname(os.path.dirname(path))
    state_path = None
    for candidate in ('state.json', os.path.join('state', 'state.json')):
        candidate_path = os.path.join(eval_dir, candidate)
        if os.path.isfile(candidate_path):
            state_path = candidate_path
            break
    if state_path:
        with open(state_path, encoding='utf-8') as f:
            try:
                state = json.load(f)
            except Exception:
                state = {}
    for assertion in verification.get('assertions', []):
        atype = assertion.get('type')
        a_path = assertion.get('path', '')
        expected = assertion.get('expected')
        actual = get_value(state, a_path)
        if atype == 'equals':
            ok = actual == expected
        elif atype == 'contains':
            ok = expected in str(actual)
        elif atype == 'not_contains':
            ok = expected not in str(actual)
        elif atype == 'matches':
            ok = bool(re.search(str(expected), str(actual or '')))
        elif atype == 'not_empty':
            ok = bool(actual)
        else:
            ok = False
        results.append((f'assertion[{atype}] {a_path} == {expected}', ok))

    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    return name, passed, total, results


def run_all():
    cases = discover_cases()
    if not cases:
        print('No eval cases found under skills/**/eval/cases/')
        return 0
    failures = []
    report = {'cases': [], 'passed': 0, 'total': 0}
    for path in cases:
        name, passed, total, results = run_case(path)
        report['cases'].append({'name': name, 'passed': passed, 'total': total})
        report['passed'] += passed
        report['total'] += total
        status = 'PASS' if passed == total else 'FAIL'
        print(f'[{status}] {name} ({passed}/{total})')
        for check, ok in results:
            if not ok:
                print(f'    - FAIL: {check}')
                failures.append(f'{name}: {check}')
    report['ok'] = report['passed'] == report['total']
    with open(os.path.join(ROOT, 'eval-results.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print(f'\nTotal: {report["passed"]}/{report["total"]} checks passed')
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description='Eval harness runner')
    parser.add_argument('command', choices=['ci', 'list', 'run'])
    parser.add_argument('--skill', default=None, help='Filter by skill name')
    args = parser.parse_args()

    if args.command == 'list':
        for path in discover_cases():
            print(os.path.relpath(path, ROOT))
        return 0

    return run_all()


if __name__ == '__main__':
    sys.exit(main())
