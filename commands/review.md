---
name: review
description: Code review pipeline — lint → typecheck → test → security → quality
triggers:
  - "review this"
  - "code review"
  - "check my changes"
  - "pre-merge review"
---

# /review — Code Review Pipeline

## When to Use
- Before committing/merging changes
- After implementing a feature
- Reviewing a PR/MR
- Quality gate before deployment

## Workflow

### 1. Structure Check
```
skill("code-review-and-quality")  # 8-axis review with confidence filtering
```

### 2. Deterministic Gates
```
skill("verification-before-completion")  # Structure → Deterministic → Security → Convention → LLM Judge
```

### 3. Security Audit
```
skill("secops-and-vulnerability-scanner")  # SAST, dependencies, secrets
```

### 4. Performance Check (if applicable)
```
skill("performance-profiler-and-tuner")  # If performance-sensitive changes
```

### 5. Verification
```
skill("verification-before-completion")  # Fresh evidence: lint, typecheck, tests
```

## Output
- Review report with findings by severity
- List of blocking vs. non-blocking issues
- Recommendations for fixes

## Completion
**DONE** — All gates green, no blocking issues
**DONE_WITH_CONCERNS** — Minor issues found: [list], non-blocking
**BLOCKED** — Blocking issues: [list], must fix before merge
**NEEDS_CONTEXT** — Need clarification on [specific change/requirement]