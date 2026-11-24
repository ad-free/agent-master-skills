#!/usr/bin/env bash
# Claude Code Stop hook: run the project's gate before the agent may stop.
# The gate is the command on a line `Gate: `<cmd>`` in the project's AGENTS.md (or CLAUDE.md).
# Exit 2 blocks the stop and sends the failure tail to the agent; exit 0 lets it stop.
# Runs only when the working tree changed since the gate last ran, so question-only turns cost nothing.
# Trust: a repo's Gate line is code from that repo, so it runs only after the user approves that exact command
# for that repo, once, in a terminal inside it: `bash stop-gate.sh --trust`. Editing the Gate line voids the
# approval. Trust pins the command text, not the Makefile or scripts it calls.
# Needs: git, jq. Timeout: set it on the hook in settings.json (the gate may run tests).
set -u
trust="${AGENT_GATE_TRUST:-$HOME/.claude/agent-gate-trusted}"
log="${AGENT_GATE_LOG:-$HOME/.claude/usage-log.jsonl}"
max_blocks=3
# Outcome signal for /lessons: one line per real gate decision, only if the usage log already exists.
outcome() { [ -f "$log" ] && jq -nc --arg r "$1" --arg c "$top" \
  '{ts: (now|todate), tool: "stop-gate", target: $r, cwd: $c}' >>"$log"; return 0; }

read_gate() {
  local f g
  for f in AGENTS.md CLAUDE.md; do
    [ -f "$f" ] || continue
    g=$(sed -n 's/^Gate: `\(.*\)`[[:space:]]*$/\1/p' "$f" | head -1)
    [ -n "$g" ] && { printf '%s' "$g"; return; }
  done
}
key() { printf '%s\t%s' "$1" "$(printf '%s' "$2" | sha1sum | cut -d' ' -f1)"; }
# Status, tracked changes (binary-safe; staged-only diff in a repo with no commits) and untracked file contents.
fingerprint() {
  { git status --porcelain
    git diff HEAD --binary 2>/dev/null || git diff --cached --binary
    git ls-files -o --exclude-standard -z | xargs -0 -r sha1sum --; } | sha1sum | cut -d' ' -f1
}

if [ "${1:-}" = "--trust" ]; then
  # A terminal and an explicit yes: the agent's shell has no TTY, so it cannot approve its own gate.
  [ -t 0 ] || { echo "--trust must be run by you, in a terminal" >&2; exit 1; }
  top=$(git rev-parse --show-toplevel) && cd "$top" || exit 1
  gate=$(read_gate); [ -n "$gate" ] || { echo "No Gate: line in $top/AGENTS.md or CLAUDE.md" >&2; exit 1; }
  printf 'Run this at every agent stop in %s?\n  %s\n[y/N] ' "$top" "$gate"; read -r ok
  [ "$ok" = y ] || [ "$ok" = Y ] || { echo "Not trusted."; exit 1; }
  mkdir -p "$(dirname "$trust")"; key "$top" "$gate" >>"$trust"; echo >>"$trust"
  echo "Trusted for $top: $gate"; exit 0
fi

input=$(cat)
cwd=$(jq -r '.cwd // empty' <<<"$input")
cd "${cwd:-.}" 2>/dev/null || exit 0
top=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$top" || exit 0

gate=$(read_gate)
[ -n "$gate" ] || exit 0
[ -n "$(git status --porcelain)" ] || exit 0
if ! grep -qxF "$(key "$top" "$gate")" "$trust" 2>/dev/null; then
  outcome untrusted
  jq -nc --arg m "Stop gate not trusted for $top (Gate: $gate). If that command is safe, run in a terminal in the repo: bash $0 --trust" \
    '{systemMessage: $m}'
  exit 0
fi
state="$(git rev-parse --git-dir)/agent-gate"
fp=$(fingerprint)
# Unchanged since the gate last ran: passed -> nothing to do; failed -> the agent has already seen this failure.
[ "$(cat "$state.pass" 2>/dev/null)" = "$fp" ] && exit 0
[ "$(cat "$state.fail" 2>/dev/null)" = "$fp" ] && exit 0

out=$(bash -c "$gate" 2>&1); rc=$?
fp=$(fingerprint)  # after the run: files the gate itself writes must not look like new edits
if [ $rc -eq 0 ]; then
  printf '%s' "$fp" >"$state.pass"; rm -f "$state.fail" "$state.blocks"
  outcome pass
  exit 0
fi
printf '%s' "$fp" >"$state.fail"
outcome fail
n=$(( $(cat "$state.blocks" 2>/dev/null || echo 0) + 1 )); printf '%s' "$n" >"$state.blocks"
if [ "$n" -gt "$max_blocks" ]; then
  jq -nc --arg m "Stop gate still failing after $max_blocks blocks ($gate); letting the agent stop. Check its report." \
    '{systemMessage: $m}'
  exit 0
fi
{
  echo "Gate failed: $gate"
  printf '%s\n' "$out" | tail -n 40
  echo "Fix the cause (never weaken a test). If it cannot be fixed here, list it under Not verified and stop."
} >&2
exit 2
