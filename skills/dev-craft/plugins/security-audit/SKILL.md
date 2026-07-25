---
owner: noname.spyware@gmail.com
allowedTools:
- file
- http

---

## Extended Checks (Beyond HARDEN Built-ins)

### 1. Dependency Deep Dive

The agent reads every dependency file and reasons about risk based on training knowledge:

```
Read: package.json, requirements.txt, go.mod, Cargo.toml, pom.xml, Gemfile

For each dependency, reason about:
- Known CVEs from training data (Log4j, Spring4Shell, etc.)
- Package maintenance status (last release date per agent knowledge)
- Deprecation status (Express < 4.18, jQuery < 3.5, Moment.js, etc.)
- Supply chain risk (is the package widely used? Maintained by a team or individual?)
- License compatibility (GPL in MIT project? AGPL for internal tools?)
```

**Output:**
```
DEPENDENCY DEEP DIVE:
- High risk: [package]@[version] — [reasoning]
- Medium risk: [package]@[version] — [reasoning]
- Low risk: [package]@[version] — [note]
- Clean: remaining [N] packages
```

### 2. Data Classification Audit

The agent traces every data type through the system to verify proper handling:

```
Read all models, schemas, types, and the code that handles each data class:

PII (personally identifiable information):
├── Where does PII enter the system? (registration, profiles, forms)
├── Where is it stored? (DB columns, cache, logs)
├── Where is it transmitted? (API responses, third-party integrations)
└── Is it properly protected? (encrypted at rest, stripped from logs, not in URLs)

Credentials (passwords, tokens, keys):
├── Are passwords hashed before storage? (bcrypt${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/argon2, not MD5${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/SHA1)
├── Are API keys stored encrypted? (not plaintext in DB)
├── Are session tokens in httpOnly cookies? (not accessible from JS)
└── Are JWTs signed and verified? (not just base64-decoded)

Payment${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Financial data:
├── Is payment data handled by a PCI-compliant processor? (Stripe, etc.)
├── Is the app itself storing raw card data? (should never happen)
└── Are payment webhooks signature-verified?
```

### 3. Business Logic Abuse Analysis

The agent reads the application logic to find flaws that automated tools cannot detect:

```
Read: route handlers, business logic services, state machines

Check for logic flaws:
├── Can a user perform an action multiple times when they should only do it once?
│   (double-spend, double-refund, double-vote)
├── Can a user skip required steps in a multi-step process?
│   (skip payment in checkout, skip verification in registration)
├── Can a user manipulate prices or quantities in their favor?
│   (negative numbers, fractional quantities, price modification in request)
├── Can a user access resources by changing sequential IDs?
│   (IDOR: ${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/1, ${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/2 — does it check ownership?)
├── Can a user escalate privileges by modifying their role${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/permissions?
│   (mass assignment: User.update(req.body) allows setting role=admin)
└── Can a user bypass feature flags or A${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/B tests to access unreleased features?
```

### 4. Infrastructure & Deployment Security

The agent reads deployment configs to find runtime vulnerabilities:

```
Read: Dockerfile, docker-compose.yml, nginx.conf, CI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/CD configs, Terraform

Container security:
├── Non-root user in Dockerfile? (USER appuser, not root)
├── No secrets in image layers? (ARG${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/ENV for secrets → use build args or secrets mount)
├── Minimal base image? (alpine or distroless, not full OS)
├── No unnecessary packages installed?
└── HEALTHCHECK defined?

Network security:
├── Only necessary ports exposed? (not 0.0.0.0:5432 for dev DB)
├── CORS whitelisted origins? (not * with credentials: true)
├── TLS enforced? (HTTP → HTTPS redirect)
└── Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options?

CI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/CD security:
├── Secrets from CI environment, not in repo?
├── Branch protection on main? (no direct pushes, PR reviews required)
├── Supply chain verification? (lock files committed, integrity checks)
└── Deployments require human approval for production?
```

### 5. Compliance Surface Check

The agent reads code patterns relevant to common compliance frameworks:

```
GDPR (if handling EU user data):
├── User data export endpoint? (right to access)
├── User data deletion endpoint? (right to be forgotten)
├── Consent recorded and stored? (opt-in, not pre-checked)
├── Data retention policy documented? (auto-delete after X days)
└── Data processing records maintained?

SOC2 / Enterprise readiness:
├── Audit logging for sensitive actions? (who did what, when)
├── Access controls with principle of least privilege?
├── Change management process? (migrations, feature flags)
└── Incident response procedures documented?

OWASP ASVS (Application Security Verification Standard):
├── Level 1: All automated checks in HARDEN pass
├── Level 2: Agent has verified auth, session, access control patterns
└── Level 3: Agent has verified architecture-level security (logged with reasoning)
```

---

## Report Format

```markdown
# Security Audit — [Project${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Feature]

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
| 1 | Business Logic | IDOR | ${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/:id | No ownership check, sequential IDs |

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
- FLAGS: Medium${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Low issues with accepted risk
- FAIL: Critical${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/High issues must be fixed
```

---

## Optional Tool Accelerators

If the development environment happens to have these tools, they can speed up specific checks. The agent always performs the check by reading code — tools only make it faster:

| Check | Tool | What it speeds up |
|-------|------|--------------------|
| Secrets | `trufflehog`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`gitleaks` | Scanning all files instead of agent reading one by one |
| SAST | `semgrep`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`gosec` | Finding ALL injection patterns instead of tracing each manually |
| Dependencies | `npm audit`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`pip-audit` | Checking ALL known CVEs instead of agent reasoning from training data |
| Container | `dockle`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`trivy` | Dockerfile best practices instead of agent reading each line |
| IaC | `tfsec`${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/`checkov` | Infrastructure-as-code scanning instead of agent reading templates |

**Rule:** The agent performs the check regardless. If a tool is available, run it and use the output to accelerate the review. If not, the agent reads the relevant files directly.