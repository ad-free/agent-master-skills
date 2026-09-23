import subprocess
import sys
import os
import re

HERE = os.path.dirname(os.path.dirname(__file__))


def run(cmd):
    proc = subprocess.run(cmd, shell=False, cwd=HERE, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def test_validate_agents():
    py = sys.executable
    code, out = run([py, "tools/validate_agents.py"])
    assert code == 0, out


def test_validate_dev_craft_state_good():
    py = sys.executable
    sample = os.path.join(HERE, "tests", "fixtures", "project_with_dev_craft")
    code, out = run([py, "tools/validate_dev_craft_state.py", sample])
    assert code == 0, out


def test_validate_eval_cases():
    py = sys.executable
    code, out = run([py, "tools/validate_eval_cases.py"])
    assert code == 0, out


def test_eval_harness_ci():
    py = sys.executable
    code, out = run([py, "tools/eval_harness.py", "ci"])
    assert code == 0, out
    # Harness must run to completion with every check passing.
    # Parse the Total line instead of hardcoding a count so adding
    # eval cases doesn't break the test (regression: "3/3" fossil).
    assert "[FAIL" not in out, out
    m = re.search(r"Total: (\d+)/(\d+) checks passed", out)
    assert m, out
    passed, total = int(m.group(1)), int(m.group(2))
    assert total > 0, out
    assert passed == total, out
