#!/usr/bin/env python3
"""Lightweight eval harness runner.

Discovers eval test cases under `skills/**/eval/cases/*.yaml`, executes
deterministic checks (file existence, JSON-path assertions) against skill
state, and emits pass/fail results. Supports model-based grading and pass@k
metrics for reliability measurement.

Commands:
  eval_harness.py run --skill <name>           # run cases for one skill
  eval_harness.py run --skill <name> --trials 3  # run with pass@k trials
  eval_harness.py ci                           # run all cases, fail on regressions
  eval_harness.py ci --trials 3                # CI mode with pass@k
  eval_harness.py list                         # list discovered cases

Verification kinds supported in a case's `verification` block:
  files: [{path, mustExist}]                   # file presence checks
  assertions: [{type, path, expected}]         # equals | contains | not_contains | matches | not_empty
                                              #   (path applied to state.json)
  model-grading: [{prompt, expected_score}]    # LLM-as-judge grading (optional)

Grader Types:
  code     - Run a shell command; pass if exit code is 0
  grep     - Check if pattern exists in files
  llm      - Use LLM as judge (requires OPENAI_API_KEY or ANTHROPIC_API_KEY)

Metrics:
  pass@1      - First attempt success rate
  pass@3      - Success within 3 attempts (at least one success)
  pass^3      - All 3 consecutive trials succeed (stability test)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from glob import glob

try:
    import yaml
except Exception:
    yaml = None

ROOT = os.path.dirname(os.path.dirname(__file__))
CASES_GLOB = os.path.join(ROOT, "skills", "**", "eval", "cases", "*.yaml")


def discover_cases():
    return sorted(glob(CASES_GLOB, recursive=True))


def load_case(path):
    if yaml is None:
        raise RuntimeError("pyyaml is required to load eval cases")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_value(state, json_path):
    """Resolve a JSONPath-ish path like `$.state.topology` in state dict."""
    if not json_path or not json_path.startswith("$."):
        return None
    current = state
    for part in json_path[2:].split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def run_code_check(check):
    """Run a shell command check. Pass if exit code is 0."""
    cmd = check.get("command", "")
    cwd = check.get("cwd", ROOT)
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, timeout=60
        )
        ok = result.returncode == 0
    except Exception as e:
        ok = False
        result = None
    return (f"code check: {cmd}", ok)


def run_grep_check(check, path):
    """Grep for pattern in specified files."""
    pattern = check.get("pattern", "")
    files = check.get("files", [])
    matches = []
    for f in files:
        full_path = os.path.join(ROOT, f)
        if os.path.isfile(full_path):
            with open(full_path, encoding="utf-8") as fh:
                try:
                    content = fh.read()
                    if re.search(pattern, content):
                        matches.append(f)
                except Exception:
                    pass
    ok = len(matches) > 0
    return (f"grep check: {pattern} in {len(files)} files", ok)


def run_llm_judge(check):
    """Run LLM-as-judge grading."""
    prompt = check.get("prompt", "")
    expected_score = check.get("expected_score", 4)
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return (f"llm judge: [SKIP - no API key]", False)

    # Simple LLM judge via curl to OpenAI-compatible endpoint
    import urllib.request
    import urllib.error

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    endpoint = os.environ.get(
        "LLM_JUDGE_ENDPOINT", "https://api.openai.com/v1/chat/completions"
    )
    model = os.environ.get("LLM_JUDGE_MODEL", "gpt-4o-mini")

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.3,
    }

    try:
        req = urllib.request.Request(
            endpoint, json.dumps(payload).encode(), headers=headers
        )
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read())
        output = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        # Extract score from output (look for "Score: N" or "score: N")
        score_match = re.search(r"[Ss]core:\s*(\d+)", output)
        score = int(score_match.group(1)) if score_match else 0

        ok = score >= expected_score
        return (f"llm judge: score={score} (expected >= {expected_score})", ok)
    except Exception as e:
        return (f"llm judge: [ERROR - {e}]", False)


def run_case(path, trial=1):
    case = load_case(path)
    name = case.get("name", os.path.basename(path))
    verification = case.get("verification", {})
    results = []

    # File presence checks
    for fspec in verification.get("files", []):
        fpath = fspec.get("path", "")
        full = os.path.join(ROOT, fpath)
        exists = os.path.isfile(full)
        want = fspec.get("mustExist", True)
        results.append((f"file exists: {fpath}", exists == want))

    # Assertions against a state.json if the case provides one
    # under eval/state.json or eval/state/state.json
    state = {}
    eval_dir = os.path.dirname(os.path.dirname(path))
    state_path = None
    for candidate in ("state.json", os.path.join("state", "state.json")):
        candidate_path = os.path.join(eval_dir, candidate)
        if os.path.isfile(candidate_path):
            state_path = candidate_path
            break
    if state_path:
        with open(state_path, encoding="utf-8") as f:
            try:
                state = json.load(f)
            except Exception:
                state = {}
    for assertion in verification.get("assertions", []):
        atype = assertion.get("type")
        a_path = assertion.get("path", "")
        expected = assertion.get("expected")
        actual = get_value(state, a_path)
        if atype == "equals":
            ok = actual == expected
        elif atype == "contains":
            ok = expected in str(actual)
        elif atype == "not_contains":
            ok = expected not in str(actual)
        elif atype == "matches":
            ok = bool(re.search(str(expected), str(actual or "")))
        elif atype == "not_empty":
            ok = bool(actual)
        else:
            ok = False
        results.append((f"assertion[{atype}] {a_path} == {expected}", ok))

    # Code-based checks (deterministic)
    for check in verification.get("checks", []):
        ctype = check.get("type")
        if ctype == "command":
            results.append(run_code_check(check))
        elif ctype == "grep":
            results.append(run_grep_check(check, path))
        elif ctype == "llm":
            results.append(run_llm_judge(check))

    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    return f"{name} (trial {trial})" if trial > 1 else name, passed, total, results


def compute_pass_at_k(trial_results):
    """Compute pass@k and pass^k metrics from trial results.

    pass@k: at least one success in k attempts
    pass^k: all k trials succeed
    """
    if not trial_results:
        return {"pass@1": 0.0, "pass@3": 0.0, "pass^3": 0.0}

    k = len(trial_results)
    successes = [1 if p == t else 0 for _, p, t, _ in trial_results]

    pass_at_1 = successes[0] if successes else 0
    pass_at_k = 1 if any(successes) else 0
    pass_k_all = 1 if all(successes) else 0

    metrics = {
        "pass@1": pass_at_1,
        "pass@{}".format(k): pass_at_k,
        "pass^{}".format(k): pass_k_all,
        "trials": k,
    }
    return metrics


def run_all(trials=1):
    cases = discover_cases()
    if not cases:
        print("No eval cases found under skills/**/eval/cases/")
        return 0
    failures = []
    report = {"cases": [], "passed": 0, "total": 0, "trials": trials}

    for path in cases:
        case = load_case(path)
        # Check if this case should only run in CI or has pass@k requirements
        use_trials = trials if case.get("execution", {}).get("pass_at_k", False) else 1

        trial_results = []
        if use_trials == 1:
            trial_results.append(run_case(path))
        else:
            for t in range(1, use_trials + 1):
                trial_results.append(run_case(path, trial=t))

        # Use first trial for display
        name, passed, total, results = trial_results[0]

        case_report = {
            "name": name,
            "passed": passed,
            "total": total,
            "trials": len(trial_results),
        }

        if len(trial_results) > 1:
            metrics = compute_pass_at_k(trial_results)
            case_report["metrics"] = {k: v for k, v in metrics.items() if k != "trials"}
            status = "PASS" if passed == total else "FAIL"
        else:
            status = "PASS" if passed == total else "FAIL"

        report["cases"].append(case_report)
        report["passed"] += passed
        report["total"] += total
        print(f"[{status}] {name} ({passed}/{total})")
        for check, ok in results:
            if not ok:
                print(f"    - FAIL: {check}")
                failures.append(f"{name}: {check}")

    report["ok"] = report["passed"] == report["total"]
    with open(os.path.join(ROOT, "eval-results.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"\nTotal: {report['passed']}/{report['total']} checks passed")
    if trials > 1:
        print(f"Used {trials} trials for pass@k metrics")
    return 1 if failures else 0


def main():
    parser = argparse.ArgumentParser(description="Eval harness runner")
    parser.add_argument("command", choices=["ci", "list", "run"])
    parser.add_argument("--skill", default=None, help="Filter by skill name")
    parser.add_argument(
        "--trials", type=int, default=1, help="Number of trials for pass@k metrics"
    )
    parser.add_argument(
        "--model-grading", action="store_true", help="Enable LLM-as-judge grading"
    )
    args = parser.parse_args()

    if args.command == "list":
        for path in discover_cases():
            print(os.path.relpath(path, ROOT))
        return 0

    if args.skill:
        # Filter cases for specific skill
        cases = [p for p in discover_cases() if f"skills/{args.skill}/" in p]
        if not cases:
            print(f"No eval cases found for skill: {args.skill}")
            return 0
        failures = []
        for path in cases:
            name, passed, total, results = run_case(
                path
            )  # Fixed: was using undefined `cases` variable
            status = "PASS" if passed == total else "FAIL"
            print(f"[{status}] {name} ({passed}/{total})")
            for check, ok in results:
                if not ok:
                    print(f"    - FAIL: {check}")
                    failures.append(f"{name}: {check}")
        return 1 if failures else 0

    return run_all(trials=args.trials)


if __name__ == "__main__":
    sys.exit(main())
