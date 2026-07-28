# Test Transcript: New Feature Pipeline (01-new-feature.md)

## Input
User: "Build a REST API for user authentication with JWT tokens, including login, register, password reset, and email verification."

## Expected Flow

### 1. agent-router → planner
```
User request received
→ agent-router routes to planner (vague feature request)
→ planner invokes product-thinking
```

### 2. product-thinking (4 rounds)
```
Round 1: Domain & Problem
→ Domain: SaaS auth system
→ Users: App users
→ Problem: Secure authentication with email verification

Round 2: Scope Triangulation
→ Modules: Auth, User, Email
→ Boundaries: No admin panel, no OAuth2 yet

Round 3: Feature Extraction
→ Login, Register, Password Reset, Email Verification, Token Refresh

Round 4: Priority & Sequencing
→ G1: Login, Register, JWT
→ G2: Password Reset, Email Verification
→ G3: Token Refresh, Rate Limiting
```
**Output:** PRODUCT.md

### 3. planning-and-task-breakdown
```
Input: PRODUCT.md
→ Dependency map: Auth → User → Email
→ Vertical slices:
  Slice 1: User model + Register API
  Slice 2: Login + JWT issuance
  Slice 3: Password Reset flow
  Slice 4: Email Verification flow
→ Tasks with acceptance criteria
```
**Output:** PLAN.md, requirements.md

### 4. grilling (adversarial review)
```
Risks identified:
R-01: JWT secret rotation breaks sessions (High) → Graceful rotation overlap
R-02: Email enumeration via register/login (Medium) → Uniform error messages
R-03: Weak password policy (Medium) → Enforce strength + breach check
R-04: No rate limiting on auth endpoints (High) → Add rate limiter
```
**Output:** risk-register.md

### 5. dev-craft Pipeline with Gates

#### Gate 1: REQUIREMENTS-EXTRACTION → DESIGN
```
GATE 1 — REQUIREMENTS-EXTRACTION COMPLETE
──────────────────────────────────────────
Requirements extracted: 12
P1/G1 traced: 8 / 8
Gaps: 0 (P1/G1: 0, G2/G3: 2)
Deferred: none
Next phase: DESIGN (spec + ADRs + task breakdown)

Proceed to DESIGN? [y/n/m/s]
```
→ Human: `y`

#### Gate 2: DESIGN → BUILD
```
GATE 2 — DESIGN APPROVED
────────────────────────
Spec: JWT auth with refresh tokens
ADRs: 3 written (ADR-001: JWT, ADR-002: Refresh, ADR-003: Rate limit)
Slices: 4 defined
Build order: 3 modules / 12 slices
Estimated effort: 3 days
Next phase: BUILD (TDD per slice)

Proceed to BUILD? [y/n/m/s]
```
→ Human: `y`

#### Gate 3: TEST → REVIEW
```
GATE 3 — TEST SUITES PASS
──────────────────────────
Suites run: 4 (BE: 2, FE: 2)
Tests passed: 47 / 47
Contract conformance: PASS
Coverage: 87% (threshold: 80%)
Flaky tests: 0 (quarantined: 0)
Next phase: REVIEW (7-axis audit + lint gate)

Proceed to REVIEW? [y/n/m/s]
```
→ Human: `y`

#### Gate 4: REVIEW → HARDEN
```
GATE 4 — REVIEW COMPLETE
────────────────────────
Findings: Critical 0 | High 2 | Medium 3 | Low 1
Critical/High resolved: Y
P1/G1 requirements verified: 8 / 8
Lint gate: PASS
Next phase: HARDEN (cross-cutting security + observability)

Proceed to HARDEN? [y/n/m/s]
```
→ Human: `y`

#### Gate 5: HARDEN → SHIP
```
GATE 5 — HARDEN COMPLETE
────────────────────────
Critical/High findings: 2 (resolved: 2)
Risk register: 4 risks (2 accepted, 2 mitigated)
Observability: instrumented (metrics, traces, logs)
Cross-slice audit: PASS
BE↔FE contract: PASS
Next phase: SHIP (automated release via ship skill)

Proceed to SHIP? [y/n/m/s]
```
→ Human: `y`

#### Gate 6: SHIP → mr-pr-review
```
GATE 6 — SHIP COMPLETE / PR CREATED
───────────────────────────────────
PR: https://github.com/org/repo/pull/123
Version: v1.2.0
Branch: feat/auth-jwt
Tests: 47 passed
Coverage: 87%
Lint/Typecheck: PASS
Next: mr-pr-review (peer review on GitHub)

Proceed to mr-pr-review? [y/n/m/s]
```
→ Human: `y`

#### Gate 7: mr-pr-review → documentation
```
GATE 7 — PEER REVIEW COMPLETE
─────────────────────────────
PR: https://github.com/org/repo/pull/123
Review verdict: APPROVE
Reviewers: 2 (approvals: 2)
Security review: PASS
Performance review: PASS
Docs required: YES
Next: documentation-engineering (local markdown generation)

Proceed to documentation? [y/n/m/s]
```
→ Human: `y`

### 6. documentation-engineering
```
Type selection:
1. ADR — Architecture decision record
2. Runbook — Operational procedure
3. User Guide — Feature walkthrough
4. Changelog Entry — This release
5. Onboarding — New dev setup
6. API Reference — From OpenAPI
7. Custom
Reply: 1, 2, 4
```
→ Generates: ADR-004, runbook-deploy-auth, CHANGELOG.md entry

### 7. learn (capture learnings)
```
learn-051: JWT secret rotation requires overlapping validity window (2x TTL)
learn-052: Rate limit auth endpoints at edge, not just app layer
learn-053: Uniform error messages prevent email enumeration
```

### 8. retro (weekly)
```
Action items:
- Add rate limit middleware to shared library
- Document JWT rotation procedure
- Pair on email service integration
```

---

## Checkpoints to Verify
- [ ] Human asked at Gate 1 (REQUIREMENTS-EXTRACTION → DESIGN)
- [ ] Human asked at Gate 2 (DESIGN → BUILD)
- [ ] Human asked at Gate 3 (TEST → REVIEW)
- [ ] Human asked at Gate 4 (REVIEW → HARDEN)
- [ ] Human asked at Gate 5 (HARDEN → SHIP)
- [ ] Human asked at Gate 6 (SHIP → mr-pr-review)
- [ ] Human asked at Gate 7 (mr-pr-review → documentation)
- [ ] Out-of-scope detection at each gate
- [ ] State.json updated at each phase
- [ ] Per-slice BUILD gates triggered
- [ ] mr-pr-review NOT auto-run (human invoked)
- [ ] Documentation type selected by human
- [ ] Learnings captured via `learn` skill