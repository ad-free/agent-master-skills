---
name: review-orchestrator
description: |
  Use when orchestrating parallel code review subagents (security, style,
  issues/debug, performance). Spawns subagents, aggregates findings, deduplicates,
  and feeds results into code-review-and-quality and verification-before-completion.
  Single entry point for comprehensive code review.
model: big-pickle
version: 1.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Task
triggers:
  - "orchestrate review"
  - "run full review"
  - "comprehensive code review"
  - "parallel review"
  - "aggregate review findings"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
  version: 1.0.0
  domain: quality-safety
  integrates-with: [review-subagents, code-review-and-quality, verification-before-completion, dispatching-parallel-agents, bug-hunting]
---

# Review Orchestrator

## Overview

Single entry point for comprehensive code review. Orchestrates multiple specialized `review-subagents` in parallel, aggregates their findings, deduplicates, and passes results to verification gates. Implements the parallel review pattern proven in oh-my-pi and similar systems.

## Workflow

### Step 1: Determine Review Scope
```bash
# Get changed files from git
git diff --name-only HEAD~1
git diff --name-only --cached

# Filter to relevant source files
find . -name "*.ts" -o -name "*.tsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" | head -50
```

### Step 2: Select Subagents
Based on project characteristics:

| Trigger | Subagents |
|---------|-----------|
| All changes | style + issues-debug |
| New API endpoints | + security |
| DB schema changes | + performance |
| >10 files changed | + performance |
| Web app (HTML/CSS/JS) | + security + style |
| Recent production bug | + debug-focused reviewer |

### Step 3: Spawn Subagents in Parallel
Uses `dispatching-parallel-agents` pattern:

```yaml
# Each subagent gets:
# - Isolated context (only changed files)
# - Specialized prompt (see review-subagents SKILL.md)
# - Output format: JSON findings
#
# Tasks:
#   Task("security-reviewer", changed_files=["src/auth.ts", ...])
#   Task("style-reviewer", changed_files=["src/utils.ts", ...])
#   Task("issues-debug-reviewer", changed_files=["src/payment.ts", ...])
#   Task("performance-reviewer", changed_files=["src/search.ts", ...])
```

### Step 4: Collect and Aggregate Findings

Each subagent writes to `.dev-craft/review-findings/<name>.json`:

```json
// security-reviewer.json
{
  "findings": [
    {
      "file": "src/auth.ts",
      "line": 42,
      "severity": "CRITICAL",
      "category": "secrets",
      "message": "Hardcoded JWT secret key",
      "fix": "Move to environment variable: process.env.JWT_SECRET",
      "confidence": "HIGH"
    }
  ],
  "summary": "2 critical, 1 high, 3 medium"
}
```

Orchestrator aggregates all findings into:
`.dev-craft/review-findings/aggregated.json`

### Step 5: Deduplicate and Prioritize

```python
# Deduplication logic:
# 1. Group findings by (file, line, category)
# 2. If multiple subagents flag same location, keep highest severity
# 3. Merge duplicate messages (fuzzy match > 85%)
# 4. Sort by severity: CRITICAL → HIGH → MEDIUM → LOW → INFO
```

### Step 6: Generate Review Report

```markdown
# Code Review Report

## Summary
- **Security**: 2 CRITICAL, 1 HIGH
- **Style**: 5 MEDIUM, 3 LOW  
- **Issues/Debug**: 1 HIGH, 3 MEDIUM
- **Performance**: 0 HIGH, 2 MEDIUM

## Blockers (CRITICAL/HIGH)
| File | Line | Severity | Category | Finding |
|------|------|----------|----------|---------|
| src/auth.ts | 42 | CRITICAL | secrets | Hardcoded JWT secret |

## Recommendations
1. Fix CRITICAL issues before merge
2. Address HIGH issues in same PR or follow-up
3. Track MEDIUM/LOW as tech debt
```

## Integration with dev-craft REVIEW Phase

### Phase 7 REVIEW (Modified)
```diff
# OLD (single skill):
review:
  - code-review-and-quality (8-axis, single pass)

# NEW (orchestrated subagents):
review:
  - review-orchestrator (spawns review-subagents in parallel)
  - code-review-and-quality (uses subagent findings for 8-axis scoring)
  - verification-before-completion (gates consume findings)
```

## Integration with verification-before-completion

| Gate | Consumes |
|------|----------|
| Gate 3 (Security) | `security-reviewer.json` findings |
| Gate 5 (Convention) | `style-reviewer.json` findings |
| Gate 5 (LLM-Judge) | All aggregated findings |

```bash
# verification-before-completion checks:
# Gate 3: Any CRITICAL security finding → BLOCK
# Gate 5: All HIGH severity findings addressed → PASS
```

## Configuration

```yaml
# .dev-craft/review-config.yaml
orchestrator:
  findings_dir: ".dev-craft/review-findings"
  max_files_per_subagent: 50
  timeout_seconds: 120

  subagents:
    - security
    - style
    - issues-debug
    - performance

  severity_blocks:
    critical: true    # CRITICAL always blocks
    high: true        # HIGH blocks unless waived
    medium: false     # Track but don't block
    low: false

  auto_assign_models:
    security: big-pickle
    style: gpt-5-nano
    issues-debug: big-pickle
    performance: gpt-5-nano
```

## Commands

```bash
# Run full review on staged changes
review-orchestrator run

# Run on specific files
review-orchestrator run --files src/auth.ts,src/payment.ts

# Run with specific subagents
review-orchestrator run --subagents security,issues-debug

# View aggregated report
review-orchestrator report

# Clear findings
review-orchestrator clean
```

## Benefits Over Single-Reviewer Pattern

| Aspect | Single Reviewer | Orchestrated Subagents |
|--------|----------------|----------------------|
| Coverage | 1 perspective, 8 axes | 4 perspectives, parallel |
| Speed | Sequential | Parallel (2-4x faster) |
| Focus | Generalist | Specialist in domain |
| Context | Full codebase | Changed files only |
| Output | Single report | Structured JSON findings |
| Integration | Manual synthesis | Automated gating |
| False positives | Higher (generalist) | Lower (specialist) |
| **Cost** | 1x model call (big-pickle) | Optimized: gpt-5-nano for style/perf, big-pickle only for security/debug |

## Example: Oh-My-Pi Pattern Adaptation

```python
# From oh-my-pi's successful pattern:
#
# Task → [Security Reviewer (8s)] → findings
# Task → [Style Reviewer (3s)]    → findings
# Task → [Debug Reviewer (6s)]    → findings
# Task → [Perf Reviewer (4s)]     → findings
#                        ↓
#                Aggregator + Deduper
#                        ↓
#            code-review-and-quality (score)
#            verification-before-completion (gate)
#
# Total time: ~8s (parallel) vs ~21s (sequential)
# Total cost: ~$0.02 (4 parallel calls: 2x gpt-5-nano + 2x big-pickle) vs ~$0.06 (single big-pickle pass)
```

## Cost Optimization

| Optimization | Detail |
|-------------|--------|
| **Model routing** | Style/perf reviewers use `gpt-5-nano` (cheapest); security/debug use `big-pickle` only for >500 LOC |
| **Incremental review** | Only review changed files (diff), not entire codebase |
| **Result caching** | Findings cached per-commit SHA; skip re-review on same commit |
| **Parallel execution** | 4 subagents run simultaneously; wall-clock time is max(individual times), not sum |
| **JSON output** | Compressed findings only — no full code context in output |
| **See also** | `cost-optimizer` skill for model selection thresholds and budget tracking |

## Two-Axis Review Integration

The review-orchestrator can also run the two-axis review pattern (Standards + Spec) from `skills/two-axis-review/`:

### Standards Axis
Runs as a parallel sub-agent checking:
- Documented coding standards (CODING_STANDARDS.md, CONTRIBUTING.md)
- Fowler code smells baseline (Mysterious Name, Duplicated Code, Feature Envy, etc.)
- Repo-specific conventions

### Spec Axis
Runs as a parallel sub-agent checking:
- Requirements from originating issue/spec
- Scope creep (behaviour not asked for)
- Implementation correctness

### Aggregated Report
```markdown
# Two-Axis Review Report

## Standards
- 3 findings (worst: Shotgun Surgery in auth.ts)

## Spec
- 2 findings (worst: Missing requirement §2.3)

## Combined
- CRITICAL: 0
- HIGH: 2
- MEDIUM: 3
- LOW: 1
```

## References

- `skills/review-subagents/` — Individual subagent definitions
- `skills/code-review-and-quality/` — 8-axis scoring (consumes findings)
- `skills/verification-before-completion/` — Gate integration
- `skills/dispatching-parallel-agents/` — Parallel execution pattern
- `skills/bug-hunting/` — Security reviewer methodology
- `skills/debugging-and-error-recovery/` — Debug reviewer methodology
- `skills/two-axis-review/` — Standards + Spec review (mattpocock port)
