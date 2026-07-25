---
owner: noname.spyware@gmail.com
allowedTools:
- file
- http

---

---
name: dependency-audit
description: Use when dependency vulnerability scanning, license compliance, and supply chain security.
metadata:
  origin: agent-master-skills---

# Dependency Audit Plugin

## Overview

Scans project dependencies for known vulnerabilities, license compliance issues, and supply chain risks.

## When to Use

- Before adding any new dependency
- Regular maintenance (weekly scheduled)
- After a security advisory is published
- Before production deployment

## Scan Order

1. **Vulnerability scan** — `npm audit`, `pip-audit`, `cargo audit`, etc.
2. **License compliance** — Check all licenses against approved list
3. **Deprecated packages** — Flag unmaintained packages (>1 year since update)
4. **Supply chain** — Check lock file integrity, signature verification
5. **Bundle size** — Flag oversized dependencies

## Integration

Registered in `state.json`:
```json
{
  "plugins": ["dependency-audit"],
  "pluginConfig": {
    "dependency-audit": {
      "failOnCritical": true,
      "allowedLicenses": ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "Unlicense"]
    }
  }
}
```