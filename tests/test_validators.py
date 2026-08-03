import subprocess
import sys
import os

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
    sample = os.path.join(HERE, 'tests', 'fixtures', 'project_with_dev_craft')
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
    assert "3/3 checks passed" in out
