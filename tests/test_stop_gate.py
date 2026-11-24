import hashlib
import json
import os
import re
import subprocess

HOOK = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools", "hooks", "stop-gate.sh")


def repo(tmp_path, gate=None):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    if gate is not None:
        (tmp_path / "AGENTS.md").write_text(f"# Project\n\nGate: `{gate}`\n")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-qm", "init", "--allow-empty"], check=True)
    return tmp_path


def env(path):
    return {**os.environ, "AGENT_GATE_TRUST": str(path.parent / f"trust-{path.name}"),
            "AGENT_GATE_LOG": str(path.parent / f"log-{path.name}.jsonl")}


def trust(path):
    # --trust itself needs a terminal and a yes; tests write the same entry it would write.
    gate = None
    for f in ("AGENTS.md", "CLAUDE.md"):
        p = path / f
        m = p.exists() and re.search(r"^Gate: `(.*)`\s*$", p.read_text(), re.M)
        if m:
            gate = m.group(1)
            break
    if gate is None:
        return
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=path, capture_output=True,
                         text=True).stdout.strip()
    with open(env(path)["AGENT_GATE_TRUST"], "a") as fh:
        fh.write(f"{top}\t{hashlib.sha1(gate.encode()).hexdigest()}\n")


def run(path, active=False, trusted=True):
    if trusted:
        trust(path)
    p = subprocess.run(["bash", HOOK], input=json.dumps({"cwd": str(path), "stop_hook_active": active}),
                       capture_output=True, text=True, env=env(path))
    return p.returncode, p.stderr


def set_gate(path, gate):
    (path / "AGENTS.md").write_text(f"# Project\n\nGate: `{gate}`\n")


def test_no_gate_line_allows_stop(tmp_path):
    r = repo(tmp_path)
    (r / "a.py").write_text("x = 1\n")
    assert run(r, trusted=False)[0] == 0


def test_untrusted_gate_never_runs(tmp_path):
    log = tmp_path.parent / f"ran-{tmp_path.name}.log"
    r = repo(tmp_path, gate=f"echo x >> {log}; false")
    (r / "a.py").write_text("x = 1\n")
    assert run(r, trusted=False)[0] == 0
    assert not log.exists()


def test_edited_gate_line_voids_trust(tmp_path):
    r = repo(tmp_path, gate="true")
    trust(r)
    set_gate(r, "false")
    (r / "a.py").write_text("x = 1\n")
    assert run(r, trusted=False)[0] == 0


def test_clean_tree_skips_gate(tmp_path):
    r = repo(tmp_path, gate="false")
    assert run(r)[0] == 0


def test_failing_gate_blocks_with_output(tmp_path):
    r = repo(tmp_path, gate="echo boom-detail; false")
    (r / "a.py").write_text("x = 1\n")
    code, err = run(r)
    assert code == 2
    assert "Gate failed" in err and "boom-detail" in err


def test_changed_tree_reruns_gate(tmp_path):
    r = repo(tmp_path, gate="true")
    (r / "a.py").write_text("x = 1\n")
    assert run(r)[0] == 0
    set_gate(r, "false")
    assert run(r)[0] == 2


def test_cache_skips_rerun_when_tree_unchanged(tmp_path):
    log = tmp_path.parent / f"ran-{tmp_path.name}.log"
    r = repo(tmp_path, gate=f"echo x >> {log}")
    (r / "a.py").write_text("x = 1\n")
    assert run(r)[0] == 0
    assert run(r)[0] == 0
    assert log.read_text().count("x") == 1


def test_repeat_stop_without_changes_is_allowed(tmp_path):
    r = repo(tmp_path, gate="false")
    (r / "a.py").write_text("x = 1\n")
    assert run(r)[0] == 2
    assert run(r, active=True)[0] == 0


def test_question_turn_after_failure_does_not_rerun(tmp_path):
    log = tmp_path.parent / f"ran-{tmp_path.name}.log"
    r = repo(tmp_path, gate=f"echo x >> {log}; false")
    (r / "a.py").write_text("x = 1\n")
    assert run(r)[0] == 2
    assert run(r, active=False)[0] == 0
    assert log.read_text().count("x") == 1


def test_files_written_by_gate_do_not_loop(tmp_path):
    r = repo(tmp_path, gate="date +%s%N > out.txt; false")
    (r / "a.py").write_text("x = 1\n")
    assert run(r)[0] == 2
    assert run(r, active=True)[0] == 0


def test_blocks_are_capped(tmp_path):
    r = repo(tmp_path, gate="false")
    codes = []
    for i in range(4):
        (r / "a.py").write_text(f"x = {i}\n")
        codes.append(run(r, active=i > 0)[0])
    assert codes == [2, 2, 2, 0]


def test_trust_requires_a_terminal(tmp_path):
    r = repo(tmp_path, gate="true")
    p = subprocess.run(["bash", HOOK, "--trust"], cwd=r, env=env(r), input="y\n", capture_output=True, text=True)
    assert p.returncode == 1
    assert not os.path.exists(env(r)["AGENT_GATE_TRUST"])


def test_trust_is_per_repo(tmp_path):
    gate = f"echo x >> {tmp_path}/ran-b.log"
    a = repo(tmp_path / "a", gate=gate)
    b = repo(tmp_path / "b", gate=gate)  # same command, different repo: trust must not carry over
    trust(a)
    with open(env(a)["AGENT_GATE_TRUST"]) as fh:  # give repo b the same trust file as a
        entries = fh.read()
    open(env(b)["AGENT_GATE_TRUST"], "w").write(entries)
    (b / "a.py").write_text("x = 1\n")
    assert run(b, trusted=False)[0] == 0
    assert not (tmp_path / "ran-b.log").exists()


def test_repeat_stop_after_new_edit_still_blocks(tmp_path):
    r = repo(tmp_path, gate="false")
    (r / "a.py").write_text("x = 1\n")
    assert run(r)[0] == 2
    (r / "a.py").write_text("x = 2\n")  # edit inside a still-untracked file must count as a change
    assert run(r, active=True)[0] == 2


def test_claude_md_gate_is_read(tmp_path):
    r = repo(tmp_path)
    (r / "CLAUDE.md").write_text("Gate: `false`\n")
    assert run(r)[0] == 2


def test_outcomes_logged_only_when_log_exists(tmp_path):
    log = tmp_path.parent / f"log-{tmp_path.name}.jsonl"
    r = repo(tmp_path, gate="false")
    (r / "a.py").write_text("x = 1\n")
    run(r)
    assert not log.exists()
    log.write_text("")
    (r / "a.py").write_text("x = 2\n")
    run(r)
    set_gate(r, "true")
    run(r)
    rows = [json.loads(line) for line in log.read_text().splitlines()]
    assert [x["target"] for x in rows] == ["fail", "pass"]
    assert all(x["tool"] == "stop-gate" and x["cwd"] == str(r) for x in rows)


def test_untrusted_message_not_shown_on_clean_tree(tmp_path):
    r = repo(tmp_path, gate="true")
    p = subprocess.run(["bash", HOOK], input=json.dumps({"cwd": str(r)}), capture_output=True, text=True, env=env(r))
    assert p.returncode == 0 and p.stdout == ""
