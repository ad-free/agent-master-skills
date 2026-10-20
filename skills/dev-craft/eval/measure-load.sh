#!/usr/bin/env bash
# Usage: eval/measure-load.sh [skill_dir]   (default: the skill dir containing this script)
# Sums lines of the files the SKILL.md read-now table loads per scenario. Missing files count 0 and are listed.
D="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
R=references
BASE="SKILL.md"
STD="$R/workflow.md $R/build-protocol.md $R/clean-code-defaults.md $R/idioms/README.md $R/verify.md $R/red-flags.md $R/review.md"
declare -A S
S["Trivial edit"]="$BASE"
S["Standard bug fix"]="$BASE $STD $R/idioms/python.md $R/checklists/bugs.md $R/checklists/testing.md"
S["Standard FE-only feature"]="$BASE $STD $R/challenge.md $R/frontend-design.md $R/checklists/ui.md $R/ui-patterns/hrm.md $R/idioms/react-typescript.md"
S["Standard schema change (risk flag)"]="$BASE $STD $R/challenge.md $R/data-modeling.md $R/idioms/postgres.md $R/test-agent.md $R/checklists/testing.md"
S["Large full-stack feature"]="$BASE $STD $R/challenge.md $R/fullstack.md $R/phases-large.md $R/phase-templates.md $R/codebase-map-template.md $R/harden-checks.md $R/lint-rules.md $R/test-agent.md $R/checklists/bugs.md $R/checklists/security.md $R/checklists/testing.md $R/idioms/python.md $R/idioms/fastapi.md $R/idioms/react-typescript.md"
S["Large UI app"]="$BASE $STD $R/challenge.md $R/frontend-design.md $R/checklists/ui.md $R/ui-patterns/hrm.md $R/phases-large.md $R/phase-templates.md $R/codebase-map-template.md $R/harden-checks.md $R/lint-rules.md $R/test-agent.md $R/checklists/testing.md $R/idioms/react-typescript.md"
echo "| Scenario | Files | Lines |"; echo "|---|---|---|"
for k in "Trivial edit" "Standard bug fix" "Standard FE-only feature" "Standard schema change (risk flag)" "Large full-stack feature" "Large UI app"; do
  t=0; n=0; miss=""
  for f in ${S[$k]}; do if [ -f "$D/$f" ]; then t=$((t+$(wc -l < "$D/$f"))); n=$((n+1)); else miss="$miss $f"; fi; done
  echo "| $k | $n | $t |"; [ -n "$miss" ] && echo "<!-- missing:$miss -->"
done
