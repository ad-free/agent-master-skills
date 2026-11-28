#!/usr/bin/env python3
"""Self-check for run_behavior.reap (Linux): python3 skills/dev-craft/eval/test_reap.py"""
import importlib.util
import os
import signal
import subprocess
import sys
import tempfile
import time

sys.modules.setdefault("yaml", type(sys)("yaml"))  # reap() needs no yaml; skip the dependency
spec = importlib.util.spec_from_file_location("rb", os.path.join(os.path.dirname(__file__), "run_behavior.py"))
rb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rb)


def escaped(cwd, secs):
    """A server the way agents leave one: setsid, so it is out of the claude process group."""
    p = subprocess.Popen(["bash", "-c", f"setsid sleep {secs} </dev/null >/dev/null 2>&1 & echo $!"], cwd=cwd,
                         stdout=subprocess.PIPE, text=True, start_new_session=True)
    pid = int(p.stdout.readline())
    p.wait()
    time.sleep(0.3)  # let it leave the group before we look
    return pid


with tempfile.TemporaryDirectory() as repo, tempfile.TemporaryDirectory() as other:
    inside, outside = escaped(repo, 311), escaped(other, 312)
    names_repo = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(314)", f"{repo}/x"], cwd="/",
                                  start_new_session=True).pid
    unrelated = subprocess.Popen(["sleep", "313"], cwd="/", start_new_session=True).pid
    time.sleep(0.3)
    try:
        assert rb.reap(repo) == []
        time.sleep(0.3)
        assert not rb.alive(inside), "server with cwd in repo survived"
        assert not rb.alive(names_repo), "process naming a repo path survived"
        assert rb.alive(outside) and rb.alive(unrelated), "an unrelated process was killed"
    finally:
        for pid in (inside, outside, names_repo, unrelated):
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
print("ok")
