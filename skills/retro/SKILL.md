---
name: retro
description: |
  Weekly engineering retrospective. Analyzes commit history, work patterns, and code quality metrics
  with persistent history and trend tracking. Team-aware: per-person contributions with praise and growth areas.
  Use when asked "weekly retro", "what did we ship", "engineering retrospective".
  Proactively suggest at end of work week or sprint.
model: deepseek-v4-flash-free
tools: Read, Write, Bash, Grep, Glob, AskUserQuestion
preamble-tier: 4
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
triggers:
  - "weekly retro"
  - "what did we ship"
  - "engineering retrospective"
  - "sprint retrospective"
metadata:
  origin: agent-master-skills
  source: gstack retro skill
  output: .dev-craft/retros/YYYY-MM-DD.md
  preferred-model: nemotron-3-ultra-free
  gbrain:
    schema: 1
    context_queries:
      - id: prior-retros
        kind: filesystem
        glob: "~/.dev-craft/retros/*.md"
        sort: mtime_desc
        limit: 5
        render_as: "## Prior Retros for This Project"
      - id: recent-timeline
        kind: filesystem
        glob: "~/.dev-craft/timeline.jsonl"
        tail: 30
        render_as: "## Recent Timeline Events"
      - id: recent-learnings
        kind: filesystem
        glob: "~/.dev-craft/learnings/learnings.jsonl"
        tail: 10
        render_as: "## Recent Learnings"
---

TOKEN CEILING: ~5K tokens. If skill exceeds, extract sections to references/.

# /retro — Weekly Engineering Retrospective

Generates a comprehensive engineering retrospective analyzing commit history, work patterns, and code quality metrics. Team-aware: identifies the user running the command, then analyzes every contributor with per-person praise and growth opportunities. Designed for a senior IC/CTO-level builder using AI agents as a force multiplier.

## User-Invocable Commands

- `/retro` — Generate retrospective for last 7 days (default)
- `/retro --since="2 weeks ago"` — Custom period
- `/retro --format=json` — Machine-readable output
- `/retro --no-gbrain` — Skip GBrain context loading

---

## Retrospective Sections

### 1. Summary Dashboard

| Metric | Current | Trend | Target |
|--------|---------|-------|--------|
| Slices completed | 3.2/week | ↗️ +0.5 | 4/week |
| PR cycle time | 4.2hrs | ↘️ -0.8 | <4hrs |
| Test flakiness | 2.1% | → | <1% |
| Security findings | 0 critical | → | 0 |
| Deploy frequency | 3/week | ↗️ +1 | 5/week |

### 2. Git Analysis (Last 7 Days)

```bash
# Commits by author
git log --since="7 days ago" --pretty=format:"%an" | sort | uniq -c | sort -rn

# Files changed most
git log --since="7 days ago" --name-only --pretty=format: | grep -v "^$" | sort | uniq -c | sort -rn | head -20

# Revert rate
git log --since="7 days ago" --grep="revert" --oneline | wc -l
```

**Output:**
- Top contributors (commits, lines, files)
- Hotspots (files changed most — potential tech debt)
- Revert rate (quality signal)
- Commit message quality (conventional commits %)

### 3. CI/CD Health

- Pipeline success rate
- Avg pipeline duration
- Flaky test count (tests failing >1x in 10 runs)
- Time to deploy (merge → production)

### 4. Code Quality Trends

- PR size (lines changed) — target <400
- Review throughput (PRs reviewed per person)
- Security findings (new this week)
- Test coverage delta

### 5. Per-Contributor Breakdown

For each author:

**Praise** (specific wins):
- "Refactored auth module — clean separation, good tests"
- "Caught 3 security issues in review this week"

**Growth** (actionable):
- "PR descriptions often missing context — use template"
- "CI pipeline knowledge — pair on DevOps tasks"

### 6. Learnings Captured

Auto-links to `learn` skill entries from this period:
- "Stripe webhook idempotency requires sorting by created timestamp"
- "React Query cache TTL must match backend TTL"

### 7. Action Items

| Action | Owner | Due | Success Criteria |
|--------|-------|-----|------------------|
| Add PR description template | @author | Next sprint | 100% PRs have context |
| Pair on CI/CD | @author1, @author2 | 2 weeks | Both can deploy independently |
| Fix flaky E2E suite | @author | This week | 0 flaky runs in CI |

---

## Output

Saves to `.dev-craft/retros/YYYY-MM-DD.md`

Also appends learnings to `.dev-craft/learnings/learnings.jsonl` via `learn` skill.

---

## Proactive Trigger

At end of work week (Friday) or sprint boundary, suggest:
> "It's Friday — want me to run the weekly retro? Takes ~2 minutes and captures learnings for next week."