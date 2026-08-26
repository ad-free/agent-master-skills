---
name: review-subagents
description: |
  Use when conducting parallel specialized code review subagents for security,
  style, issues/debug, and performance. Each subagent focuses on one domain.
  Use when you need comprehensive code review that covers multiple quality
  dimensions in parallel, with specialized prompts for each review type.
  Integrates with review-orchestrator and verification-before-completion.
model: gpt-5-nano
version: 1.0.0
preamble-tier: 4
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Task
triggers:
  - "review code"
  - "run review subagents"
  - "parallel review"
  - "security review subagent"
  - "style review subagent"
  - "debug review subagent"
  - "performance review subagent"
metadata:
  origin: agent-master-skills
  preferred-model: gpt-5-nano
  version: 1.0.0
  domain: quality-safety
  integrates-with: [review-orchestrator, code-review-and-quality, verification-before-completion, bug-hunting, cost-optimizer]
---

# Review Subagents

## Overview

Parallel specialized code review subagents that each focus on one quality dimension. This skill is invoked by `review-orchestrator` to spawn focused reviewers that return compressed findings. Each subagent works independently with isolated context.

## Subagent Types

### 1. Security Reviewer
**Model:** `big-pickle` (for files >500 LOC) or `gpt-5-nano` (for files <500 LOC)
**Focus:** OWASP Top 10, secrets, injection, authz, crypto

```markdown
# Security Reviewer Subagent

## Focus Areas
1. Secrets/credentials in code (hardcoded keys, tokens, passwords)
2. Injection vulnerabilities (SQL, NoSQL, command injection, XSS)
3. AuthZ bypasses (IDOR, missing access checks, privilege escalation)
4. Cryptography misuse (weak algorithms, hardcoded keys, improper use)
5. Path traversal (file inclusion, directory traversal)
6. Deserialization (unsafe deserialization, object injection)
7. Dependency vulnerabilities (known CVEs)
8. SSRF and network security issues

## Output Format (JSON)
{
  "findings": [
    {
      "file": "src/auth.ts",
      "line": 42,
      "severity": "CRITICAL|HIGH|MEDIUM|LOW|INFO",
      "category": "secrets|injection|authz|crypto|path|deserialization|dependency|ssrf",
      "message": "Description of the issue",
      "fix": "Suggested fix or mitigation"
    }
  ],
  "summary": "Total: X findings (Y critical, Z high)"
}

## Instructions
- Only report actual vulnerabilities, not style issues
- Include exact file path and line number
- Provide actionable fix guidance
- Flag false positives with confidence level
- Never modify code — only report findings
```

### 2. Style Reviewer
**Model:** `gpt-5-nano` (cheapest, pattern-based)
**Focus:** Code style, naming, imports, formatting, language idioms

```markdown
# Style Reviewer Subagent

## Focus Areas
1. Naming conventions (variables, functions, classes, files)
2. Import organization and unused imports
3. Code formatting consistency
4. Language-specific idioms and best practices
5. Code complexity (cyclomatic complexity, cognitive complexity)
6. Comment quality (explain why, not what)
7. File structure and module organization
8. Dead code and unreachable branches

## Output Format (JSON)
{
  "findings": [
    {
      "file": "src/utils.ts",
      "line": 15,
      "severity": "LOW|MEDIUM|HIGH",
      "category": "naming|imports|formatting|idiom|complexity|comments|structure|dead-code",
      "message": "Description of the style issue",
      "fix": "Suggested fix"
    }
  ],
  "summary": "Total: X findings across Y files"
}

## Instructions
- Follow existing project conventions (check for eslint, prettier, editorconfig)
- Language-specific rules (TypeScript: strict null checks, Go: error handling, Python: PEP 8, etc.)
- No security or bug findings — focus on style only
- Use language-rules plugin patterns where available
```

### 3. Issues/Debug Reviewer
**Model:** big-pickle (or debugger agent)
**Focus:** Logic bugs, edge cases, null handling, error paths

```markdown
# Issues/Debug Reviewer Subagent

## Focus Areas
1. Logic errors (incorrect algorithms, boundary conditions)
2. Null pointer / undefined dereference risks
3. Error handling gaps (unhandled errors, swallowed exceptions)
4. Edge case coverage (empty inputs, max values, invalid states)
5. Off-by-one errors and index issues
6. Race conditions and concurrency bugs
7. Resource leaks (unclosed files, connections, memory)
8. Test coverage gaps for identified paths

## Output Format (JSON)
{
  "findings": [
    {
      "file": "src/payment.ts",
      "line": 87,
      "severity": "HIGH|MEDIUM|LOW|INFO",
      "category": "logic|null|error|edge-case|bounds|concurrency|resource|testing",
      "message": "Description of the potential issue",
      "fix": "Suggested fix or test case"
    }
  ],
  "summary": "Total: X findings; Y potentially breaking"
}

## Instructions
- Focus on correctness and robustness, not style
- Trace data flow and execution paths
- Consider null/undefined/empty/invalid inputs
- Check error handling completeness
- Suggest failing test cases where applicable
```

### 4. Performance Reviewer
**Model:** gpt-5-nano
**Focus:** Algorithmic complexity, resource usage, bottlenecks

```markdown
# Performance Reviewer Subagent

## Focus Areas
1. Algorithmic complexity (O(n) → O(n²) issues, missing indexes)
2. Memory leaks and excessive allocations
3. Database query issues (N+1 queries, missing indexes, full scans)
4. Network request patterns (blocking calls, missing caching, retries)
5. Bundle size and import bloat
6. Unnecessary re-renders (frontend)
7. Blocking operations in async contexts
8. Resource pooling and connection management

## Output Format (JSON)
{
  "findings": [
    {
      "file": "src/search.ts",
      "line": 23,
      "severity": "HIGH|MEDIUM|LOW|INFO",
      "category": "algorithm|memory|database|network|bundle|rendering|blocking|resource",
      "message": "Description of the performance issue",
      "fix": "Suggested optimization"
    }
  ],
  "summary": "Total: X findings; Y high-impact"
}

## Instructions
- Look for patterns, not micro-optimizations
- Identify systemic issues over local optimizations
- Consider both runtime and build-time performance
- Suggest measurable improvements where possible
```

## Orchestration Pattern

### Invocation via review-orchestrator
```markdown
When reviewing a codebase, the review-orchestrator skill:

1. Determines which subagents to spawn based on:
   - Project size (>10 files → full review)
   - Languages present (JS/TS → style, Python → style)
   - Domain (web app → security, API → security)
   - History (recent bugs → debug reviewer)

2. Spawns subagents in parallel via `dispatching-parallel-agents`:
   [security-reviewer] + [style-reviewer] + [issues-debug-reviewer] + [performance-reviewer]

3. Each subagent returns findings.json to:
   `.dev-craft/review-findings/<subagent-name>.json`

4. review-orchestrator aggregates findings and passes to:
   - `code-review-and-quality` for 8-axis scoring
   - `verification-before-completion` Gate 3 (Security) and Gate 5 (LLM-Judge)
```

## Shared Instructions for All Subagents

1. **Scope**: Only review the files in the specified diff/changed-files
2. **Format**: Return JSON only — no prose
3. **Evidence**: Include file path, line number, severity, message, and fix
4. **Brevity**: Each finding must fit one paragraph
5. **Actionable**: Every finding must have a fix suggestion
6. **No code changes**: Only report, never modify files

## Integration Points

- **review-orchestrator**: Spawns and aggregates subagent outputs
- **code-review-and-quality**: Uses findings as input for 8-axis scoring
- **verification-before-completion**: Gate 3 (Security) consumes security findings; Gate 5 (LLM-Judge) consumes all findings for final assessment
- **bug-hunting**: Security reviewer uses bug-hunting methodology
- **debugging-and-error-recovery**: Debug reviewer uses investigation methodology
- **secops-and-vulnerability-scanner**: Security reviewer leverages scanning patterns

## Best Practices

1. **Parallelize by default** — all 4 subagents run simultaneously (4x speedup vs sequential)
2. **Dedupe findings** — orchestrator removes duplicate findings across reviewers
3. **Severity priority** — CRITICAL → HIGH → MEDIUM → LOW ordering
4. **False positive tracking** — each subagent reports confidence level
5. **Incremental review** — only review changed files, not entire codebase
6. **Caching** — findings cached per-commit to avoid re-reviewing same code
7. **Cost-aware model routing** — security/debug use `big-pickle` for complex code; style/perf use `gpt-5-nano` for pattern matching; see `cost-optimizer` skill

## Configuration

```yaml
# .dev-craft/review-config.yaml
subagents:
  enabled:
    - security
    - style
    - issues-debug
    - performance  # only for files > 500 LOC

  models:
    security: big-pickle        # higher reasoning for vulnerabilities
    style: gpt-5-nano           # cheap, pattern-based
    issues-debug: big-pickle    # higher reasoning for logic bugs
    performance: gpt-5-nano     # pattern-based optimization detection

  severity_threshold: HIGH  # minimum severity to block merge
  findings_dir: ".dev-craft/review-findings"
```
