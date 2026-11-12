# Automated Scanning Accelerators (optional)

Agent reasoning first; these tools accelerate Phases 2–3 when available. (Folded from `secops-and-vulnerability-scanner`.)

## SAST per language

| Language | Tool |
|----------|------|
| Python | `bandit` |
| JS/TS | eslint security plugin |
| Multi-language | `semgrep` |

## Dependency audit

`npm audit`, `pip-audit`, `cargo audit`, `safety check`, dependabot.
Check: known CVEs (record CVE IDs), license compatibility, abandoned packages (>2y stale), transitive risks. Prioritize critical/high.

## Secrets detection

`trufflehog`, `gitleaks`, plus `git log -p` for history. Cover source, git history, CI/CD configs, docs.
**Never auto-rewrite git history** for leaked secrets — report location, recommend `git filter-repo` or BFG, rotate the secret.

## Compliance mapping

Map findings to OWASP Top 10 / CWE; summarize against SOC 2, PCI-DSS, GDPR where relevant. Output: dependency report (CVE + remediation), secrets report (location + severity), prioritized remediation plan.
