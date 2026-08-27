---
name: agent-shield
description: AgentShield security scanner integration. Scans agent configurations, hooks, MCP servers, permissions, and secrets for security vulnerabilities. Provides deterministic scanning with remediation plans. Ported from ECC/agentshield.
version: 1.0.0
triggers:
  - "security scan"
  - "agent shield"
  - "scan agents"
  - "scan hooks"
  - "scan mcp"
  - "scan secrets"
metadata:
  origin: agent-master-skills
  ports: ECC/agentshield
---

# AgentShield Security Scanner Integration

Scans agent configurations, hooks, MCP servers, permissions, and secrets for security vulnerabilities.

---

## 1. DETERMINISTIC SCANNER

### Run AgentShield
```bash
# Using packaged scanner
npx ecc-agentshield scan --path . --format text

# Using local development
npm run scan -- --path . --format text

# Output formats
npx ecc-agentshield scan --path . --format json
npx ecc-agentshield scan --path . --format markdown
npx ecc-agentshield scan --path . --format html
```

### Filter by Severity
```bash
# Only medium and above
npx ecc-agentshield scan --path . --min-severity medium

# Only high and critical
npx ecc-agentshield scan --path . --min-severity high
```

### Auto-fix Safe Issues
```bash
# Apply safe auto-fixes
npx ecc-agentshield scan --path . --fix
```

---

## 2. SCAN TARGETS

### Agent Configurations
- `.claude/` directory
- `AGENTS.md` files
- Agent prompt files
- Permission configurations

### Hooks
- SessionStart hooks
- SessionEnd hooks
- PreToolUse hooks
- PostToolUse hooks

### MCP Servers
- Server configurations
- Shell access
- Filesystem access
- Remote transport
- Unpinned `npx` commands

### Permissions
- Tool permissions
- File access permissions
- Network access permissions

### Secrets
- Hardcoded API keys
- Hardcoded passwords
- Hardcoded tokens
- Environment variable exposure

---

## 3. REVIEW CHECKLIST

### 1. Active Runtime Findings
- Hardcoded secrets
- Broad permissions
- Executable hooks
- MCP servers with shell, filesystem, remote transport, or unpinned `npx`
- Agent prompts that handle untrusted content without defenses

### 2. Lower-Confidence Inventory
- Docs examples
- Template examples
- Plugin manifests
- Project-local optional settings

### 3. Per-Finding Details
For each critical or high finding:
- File path
- Severity
- Runtime confidence
- Why it matters
- Exact remediation
- Whether it is safe to auto-fix

---

## 4. OUTPUT CONTRACT

### Security Report
```markdown
# Security Scan Report

## Grade
- **Grade:** A
- **Score:** 92/100

## Counts by Severity
- **Critical:** 0
- **High:** 1
- **Medium:** 3
- **Low:** 5

## Critical/High Findings

### [HIGH] Hardcoded API Key
- **File:** `.opencode-plugin/hooks/post-tool-use.js:42`
- **Severity:** HIGH
- **Confidence:** HIGH (runtime)
- **Why:** API key exposed in source code
- **Fix:** Move to environment variable
- **Auto-fixable:** Yes

### [MEDIUM] Broad File Access
- **File:** `.opencode-plugin/hooks/pre-tool-use.js:15`
- **Severity:** MEDIUM
- **Confidence:** MEDIUM (config)
- **Why:** Hook has access to entire filesystem
- **Fix:** Restrict to project directory only
- **Auto-fixable:** No

## Lower-Confidence Findings
- [List of lower-confidence findings]

## Remediation Order
1. Fix CRITICAL findings first
2. Address HIGH findings
3. Track MEDIUM/LOW as tech debt

## Commands Run
- `npx ecc-agentshield scan --path . --format markdown`
- Scan type: Local
```

---

## 5. CI INTEGRATION

### GitHub Actions
```yaml
- uses: affaan-m/agentshield@v1
  with:
    path: "."
    min-severity: "medium"
    fail-on-findings: true
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

npx ecc-agentshield scan --path . --min-severity high --format text
if [ $? -ne 0 ]; then
  echo "Security scan failed. Fix issues before committing."
  exit 1
fi
```

---

## 6. REMEDIATION PATTERNS

### Hardcoded Secrets
```javascript
// BAD
const API_KEY = "sk-1234567890abcdef";

// GOOD
const API_KEY = process.env.API_KEY;
```

### Broad Permissions
```javascript
// BAD
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]

// GOOD
allowed-tools: ["Read", "Grep", "Glob"]
```

### Executable Hooks
```javascript
// BAD
// Hook executes arbitrary code

// GOOD
// Hook validates input before executing
```

### MCP Server Configuration
```yaml
# BAD
mcp:
  - name: filesystem
    transport: shell
    command: "bash -c 'cat $FILE'"

# GOOD
mcp:
  - name: filesystem
    transport: stdio
    command: "node"
    args: ["fs-server.js"]
    env:
      ALLOWED_DIR: "./data"
```

---

## 7. INTEGRATION WITH VERIFICATION GATE

The verify-gate hook can include AgentShield scanning:

```javascript
// In hooks/verify-gate.js
const { execSync } = require('child_process');

// Run AgentShield scan
try {
  const output = execSync('npx ecc-agentshield scan --path . --format json --min-severity high', {
    encoding: 'utf-8',
  });
  
  const results = JSON.parse(output);
  
  if (results.critical > 0 || results.high > 0) {
    console.log('[verify-gate] ❌ SECURITY SCAN FAILED');
    console.log(`Critical: ${results.critical}`);
    console.log(`High: ${results.high}`);
    
    return {
      block: true,
      message: `Security scan failed: ${results.critical} critical, ${results.high} high findings.`
    };
  }
} catch (error) {
  console.log('[verify-gate] Security scan error:', error.message);
}
```

---

## 8. QUICK SCAN

For a fast security check:
```bash
# Quick scan for critical/high
npx ecc-agentshield scan --path . --min-severity high --format text

# Quick secrets check
grep -r "sk-\|api_key\|password\|secret\|token" --include="*.js" --include="*.ts" --include="*.json" .

# Quick permissions check
find . -name "*.json" -exec grep -l "Bash\|Write\|Edit" {} \;
```

---

## 9. BEST PRACTICES

### Do
- Run AgentShield before every commit
- Fix CRITICAL findings immediately
- Track HIGH findings in issue tracker
- Use environment variables for secrets
- Restrict permissions to minimum required

### Don't
- Commit secrets to source code
- Use broad permissions without justification
- Skip security scans
- Ignore HIGH findings
- Auto-fix without reviewing changes

---

## 10. TROUBLESHOOTING

### Scanner Not Found
```bash
# Install AgentShield
npm install -g ecc-agentshield

# Or use npx
npx ecc-agentshield scan --path .
```

### False Positives
```bash
# Check if finding is in example/template
grep -r "example\|template\|sample" <file>

# Check if finding is in test file
grep -r "test\|spec\|mock" <file>
```

### Scanner Timeout
```bash
# Increase timeout
npx ecc-agentshield scan --path . --timeout 60000

# Scan specific directory
npx ecc-agentshield scan --path .opencode-plugin
```
