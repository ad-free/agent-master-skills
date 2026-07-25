# Security Audit — [Project/Feature]

## Summary
- Dependency Deep Dive: [PASS / FLAGS]
- Data Classification: [PASS / FLAGS]
- Business Logic: [PASS / FLAGS]
- Infrastructure: [PASS / FLAGS]
- Compliance: [PASS / FLAGS]

## Findings

### Critical
| # | Category | Issue | Location | Reasoning |
|---|----------|-------|----------|-----------|
| 1 | Business Logic | IDOR | /:id | No ownership check, sequential IDs |

### High
| # | Category | Issue | Location | Reasoning |
|---|----------|-------|----------|-----------|
| 1 | Infrastructure | Root user | Dockerfile | Container runs as root, not appuser |

### Medium
| # | Category | Issue | Location | Acceptance |
|---|----------|-------|----------|------------|
| 1 | Dependency | Moment.js | package.json | Deprecated but not security-critical |

### Low
| # | Category | Issue | Location | Note |
|---|----------|-------|----------|------|
| 1 | Compliance | No GDPR export | — | Only if EU users expected |

## Verdict
[PASS / FLAGS / FAIL]
- PASS: No issues found
- FLAGS: Medium/Low issues with accepted risk
- FAIL: Critical/High issues must be fixed
