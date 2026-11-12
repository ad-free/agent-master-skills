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


def test_validate_agents_rejects_ignored_fields(tmp_path):
    sys.path.insert(0, os.path.join(HERE, "tools"))
    from validate_agents import validate_file

    def check(front):
        p = tmp_path / "a.md"
        p.write_text(f"---\n{front}\n---\n\nbody\n")
        return validate_file(str(p))

    good = "name: rev\ndescription: d\ntools: Read, mcp__playwright__browser_navigate\nmodel: inherit\nmaxTurns: 5"
    assert check(good)[0], check(good)
    assert not check(good + "\nallowed-tools: [Read]")[0]
    assert not check(good + "\nmax-steps: 5")[0]
    assert not check(good.replace("name: rev", "name: Code Reviewer"))[0]
    assert not check(good.replace("tools: Read, mcp__playwright__browser_navigate\n", ""))[0]
    assert not check(good.replace("maxTurns: 5", "maxTurns: 0"))[0]


def test_validate_skills_rejects_ignored_fields(tmp_path):
    import shutil

    (tmp_path / "tools").mkdir()
    shutil.copy(os.path.join(HERE, "tools", "validate_skills.py"), tmp_path / "tools")
    skill = tmp_path / "skills" / "x"
    skill.mkdir(parents=True)

    def check(front):
        (skill / "SKILL.md").write_text(f"---\n{front}\n---\n\nbody\n")
        return run([sys.executable, str(tmp_path / "tools" / "validate_skills.py")])[0]

    good = "name: x\ndescription: Use when testing.\nmetadata:\n  version: 1.0.0"
    assert check(good) == 0
    assert check(good + "\ntriggers: [a]") != 0
    assert check(good + "\npreamble-tier: 3") != 0
    assert check("version: 1.0.0\n" + good.replace("metadata:\n  version: 1.0.0", "")) != 0
    assert check(good + "\n  preferred-model: big-pickle") != 0


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


def test_validate_skills():
    py = sys.executable
    code, out = run([py, "tools/validate_skills.py"])
    assert code == 0, out
