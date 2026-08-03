#!/usr/bin/env python3
"""Validate eval test case YAML files under `skills/**/eval/cases/`.

Checks each case against the eval-harness test-case schema
(skills/eval-harness/references/test-case-schema.json). Falls back to
structural checks if jsonschema is unavailable.

Exit code 0 on success, non-zero if errors found.
"""
import json
import os
import sys
from glob import glob

try:
    import jsonschema
    HAVE_JSONSCHEMA = True
except Exception:
    HAVE_JSONSCHEMA = False

try:
    import yaml
    HAVE_YAML = True
except Exception:
    HAVE_YAML = False

ROOT = os.path.dirname(os.path.dirname(__file__))
SCHEMA_PATH = os.path.join(ROOT, 'skills', 'eval-harness', 'references', 'test-case-schema.json')
CASES_GLOB = os.path.join(ROOT, 'skills', '**', 'eval', 'cases', '*.yaml')

REQUIRED_KEYS = ['name', 'skill', 'setup', 'input', 'execution', 'verification']


def load_schema():
    if not os.path.isfile(SCHEMA_PATH):
        return None
    with open(SCHEMA_PATH, encoding='utf-8') as f:
        return json.load(f)


def load_case(path):
    if not HAVE_YAML:
        return None, 'pyyaml not installed'
    with open(path, encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data, None


def structural_check(data):
    """Minimal structural validation (works without jsonschema)."""
    problems = []
    for key in REQUIRED_KEYS:
        if key not in data:
            problems.append(f'missing required key `{key}`')
    if 'assertions' in data.get('verification', {}):
        assertions = data['verification']['assertions']
        if not isinstance(assertions, list) or not assertions:
            problems.append('verification.assertions must be a non-empty list')
    return problems


def main():
    schema = load_schema()
    cases = sorted(glob(CASES_GLOB, recursive=True))
    if not cases:
        print('No eval case YAML files found under skills/**/eval/cases/ — nothing to validate.')
        return 0

    errors = []
    warnings = []
    for path in cases:
        rel = os.path.relpath(path, ROOT)
        data, err = load_case(path)
        if err:
            errors.append(f'{rel}: {err}')
            continue
        if data is None:
            errors.append(f'{rel}: empty or invalid YAML')
            continue
        if schema and HAVE_JSONSCHEMA:
            try:
                jsonschema.validate(instance=data, schema=schema)
            except jsonschema.ValidationError as e:
                errors.append(f'{rel}: schema violation: {e.message}')
        else:
            problems = structural_check(data)
            if problems:
                errors.append(f'{rel}: {"; ".join(problems)}')
        if not isinstance(data.get('skill'), str) or not data.get('skill'):
            errors.append(f'{rel}: `skill` must be a non-empty string')

    if errors:
        print('ERRORS:')
        for e in errors:
            print(' -', e)
        print('\nEval case validation FAILED')
        return 1

    print(f'All {len(cases)} eval case files validated OK.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
