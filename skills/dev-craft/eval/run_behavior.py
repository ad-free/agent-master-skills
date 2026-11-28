#!/usr/bin/env python3
"""Run one behavior eval case headless, on a fresh git copy of its fixture.

Usage: uv run --no-project --with pyyaml python skills/dev-craft/eval/run_behavior.py \
         <case.yaml> <skill_dir> <label> [--run N] [--budget USD] [--model sonnet] [--out DIR]

The agent is told to follow the skill files in <skill_dir> (so a branch and master copy can be compared); the
Skill tool and all hooks are off for the run. Not sandboxed: the agent runs with bypassPermissions, your real
$HOME, network and MCP servers, so only run cases and skill copies you have read. Writes <out>/<case>/<label>-<N>/ with repo/, events.jsonl,
report.md, tools.txt (every tool call, with subagent types), tests.txt (case tests re-run after) and meta.json
(cost, turns, duration). Grading against the case rubric is done by reading those files (POLICY.md).
"""
import argparse
import json
import os
import shutil
import signal
import subprocess
import sys

import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def sh(cmd, cwd, **kw):
    return subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case")
    ap.add_argument("skill_dir")
    ap.add_argument("label")
    ap.add_argument("--run", type=int, default=1)
    ap.add_argument("--budget", default="2.5")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--out", default=os.environ.get("EVAL_OUT", "/tmp/dev-craft-evals"))
    a = ap.parse_args()

    case = yaml.safe_load(open(a.case))
    name = os.path.splitext(os.path.basename(a.case))[0]
    skill_dir = os.path.abspath(a.skill_dir)
    run_dir = os.path.join(a.out, name, f"{a.label}-{a.run}")
    repo = os.path.join(run_dir, "repo")
    if os.path.exists(run_dir):
        sys.exit(f"{run_dir} exists; pick another --run or --out")
    shutil.copytree(os.path.join(ROOT, case["setup"]["fixture"]), repo,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"],
                ["git", "-c", "user.name=eval", "-c", "user.email=eval@local", "commit", "-qm", "fixture"]):
        sh(cmd, repo, check=True)

    prompt = (f"Follow the dev-craft skill for this task. Read {skill_dir}/SKILL.md first, then the files under "
              f"{skill_dir}/references/ that it tells you to read. Other skills it names are at "
              f"{os.path.dirname(skill_dir)}/<name>/SKILL.md; use those copies, not ~/.claude/skills. The Skill "
              f"tool is disabled; read those files instead. {case['input'].get('mode', '')}.\n\nTask: {case['input']['prompt']}")
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--model", a.model,
           "--max-budget-usd", str(a.budget), "--disallowedTools", "Skill", "--permission-mode",
           "bypassPermissions", "--settings", json.dumps({"disableAllHooks": True}), "--no-session-persistence"]
    timeout = case.get("execution", {}).get("timeout", 1800)
    # Own process group, killed at the end: servers the agent started must not outlive the run.
    proc = subprocess.Popen(cmd, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        out, err = proc.communicate()
        err = "timeout " + (err or "")
    finally:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    open(os.path.join(run_dir, "events.jsonl"), "w").write(out)

    result, tools = {}, []
    for line in out.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "result":
            result = ev
        for block in (ev.get("message") or {}).get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                inp = block.get("input") or {}
                where = "sub" if ev.get("parent_tool_use_id") else "main"
                tools.append(f"{where}\t{block.get('name')}\t{inp.get('subagent_type', '')}")
    open(os.path.join(run_dir, "report.md"), "w").write(result.get("result", "") or f"(no result) {err[-2000:]}")
    open(os.path.join(run_dir, "tools.txt"), "w").write("\n".join(tools) + "\n")
    t = sh(case["setup"].get("tests", "true"), repo)
    open(os.path.join(run_dir, "tests.txt"), "w").write(f"exit={t.returncode}\n{(t.stdout + t.stderr)[-3000:]}")
    meta = {k: result.get(k) for k in ("total_cost_usd", "num_turns", "duration_ms", "is_error", "subtype")}
    meta.update(case=name, label=a.label, run=a.run, model=a.model, skill_dir=skill_dir, tests_exit=t.returncode)
    json.dump(meta, open(os.path.join(run_dir, "meta.json"), "w"), indent=1)
    print(json.dumps(meta))


if __name__ == "__main__":
    main()
