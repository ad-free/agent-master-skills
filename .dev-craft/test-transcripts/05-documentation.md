# Test Transcript: Documentation Generation (05-documentation.md)

## Input
After mr-pr-review completes, human asked: "Generate documentation for this feature?"

## Expected Flow

### 1. Human Prompt
```
Agent: "Run mr-pr-review for peer review"
Human: "y"
...mr-pr-review completes...
Agent: "Review complete. Generate documentation? [y/n/m/s]"
Human: "y"
```

### 2. Documentation Type Selection
```
> "What documentation to generate?
> 1. ADR — Architecture decision record
> 2. Runbook — Operational procedure
> 3. User Guide — Feature walkthrough
> 4. Changelog Entry — This release
> 5. Onboarding — New dev setup
> 6. API Reference — From OpenAPI
> 7. Custom — Describe
> 
> Reply: 1, 2, 4"
```

### 3. Documentation Generation

#### ADR (adr-template.md)
```markdown
# ADR-004: JWT Authentication with Refresh Tokens

## Status
Accepted

## Context
Need stateless auth for SPA + mobile. Session-based auth doesn't scale.

## Decision
Use JWT access tokens (15min) + refresh tokens (7d) with rotation.

## Alternatives Considered
| Alternative | Why Rejected |
|-------------|--------------|
| Session cookies | Doesn't scale, CSRF risk |
| OAuth2 only | Overkill for internal app |
| Long-lived JWT | Token theft = long exposure |

## Consequences
### Positive
- Stateless, scales horizontally
- Short access token limits exposure
- Refresh rotation detects theft

### Negative
- More complex than sessions
- Need secure refresh storage
- Token revocation requires blocklist

### Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Refresh token theft | Medium | High | Rotation + short access TTL |
| Blocklist grows | Low | Medium | Periodic cleanup |

## Related
- ADR-001: JWT format
- ADR-002: Refresh rotation
- Issue #123

## Implementation Notes
- Access: 15min, RS256
- Refresh: 7d, rotating, httpOnly cookie
```

#### Runbook (runbook-template.md)
```markdown
# Runbook: Deploy Auth Service

## Prerequisites
- Access: Deploy role, AWS CLI, kubectl
- Tools: kubectl, helm, aws-cli
- Dependencies: PostgreSQL, Redis healthy

## Procedure

### Step 1: Build & Push Image
```bash
docker build -t auth:v1.2.0 .
docker push registry/auth:v1.2.0
```
**Verify:** Image in registry
**Rollback if:** Build fails

### Step 2: Deploy to Staging
```bash
helm upgrade auth ./helm/auth -n staging --set image.tag=v1.2.0
```
**Verify:** `kubectl get pods -n staging -l app=auth`
**Rollback if:** Pods not Ready in 5min

### Step 3: Deploy to Production
```bash
helm upgrade auth ./helm/auth -n prod --set image.tag=v1.2.0
```
**Verify:** Health checks, metrics
**Rollback if:** Error rate > 1%

## Verification
- [ ] Health check: `GET /health`
- [ ] Metrics: Grafana dashboard
- [ ] Logs: `kubectl logs -n prod -l app=auth`

## Rollback
```bash
helm rollback auth -n prod
```
**RTO:** 5 min | **RPO:** 0

## Links
- Dashboard: https://grafana/org/auth
- Logs: https://logs/org/auth
- ADR: ADR-004
- Repo: https://github.com/org/auth
```

#### Changelog (changelog-template.md)
```markdown
## [v1.2.0] - 2026-07-28

### Added
- JWT authentication with refresh tokens — #123
- Password reset flow with email — #124
- Email verification on register — #125

### Changed
- Login now returns access + refresh tokens — #123

### Fixed
- Login 500 on missing user now returns 401 — #126

### Security
- SQL injection fix in login endpoint — #127
```

### 4. State Update
```json
{
  "documentation": {
    "generated": ["ADR-004", "runbook-deploy-auth", "CHANGELOG.md"],
    "pending": ["user-guide-auth"],
    "prUrl": "https://github.com/org/repo/pull/123"
  }
}
```

### 5. Next: learn
```
Agent: "Documentation generated. Capture learnings? [y/n]"
Human: "y"
→ learn skill invoked
```