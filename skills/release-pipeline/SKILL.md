---
name: release-pipeline
description: "Use when you need a full release pipeline: ship → land-and-deploy → canary → benchmark. Automates the entire release process with safety gates, canary deployments, and performance benchmarking."
model: big-pickle
version: 1.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
triggers:
  - "release"
  - "ship"
  - "deploy"
  - "canary"
  - "benchmark"
  - "pipeline"
metadata:
  origin: agent-master-skills
  preferred-model: big-pickle
---

# Release Pipeline

Full release pipeline: ship → land-and-deploy → canary → benchmark.

---

## 1. PIPELINE STAGES

### Stage 1: Ship (Pre-release)
1. Verify all tests pass
2. Run security scan
3. Update version
4. Update changelog
5. Create release commit
6. Push to remote

### Stage 2: Land and Deploy
1. Merge to main branch
2. Build production artifacts
3. Deploy to staging
4. Run smoke tests
5. Deploy to production

### Stage 3: Canary
1. Deploy canary (5% traffic)
2. Monitor error rates
3. Monitor performance metrics
4. Monitor user behavior
5. Promote or rollback

### Stage 4: Benchmark
1. Run performance benchmarks
2. Compare to baseline
3. Generate report
4. Alert on regressions

---

## 2. SHIP STAGE

### Pre-flight Checks
```bash
# Verify tests pass
npm test

# Run security scan
npx ecc-agentshield scan --path . --min-severity high

# Run linter
npm run lint

# Run typecheck
npm run typecheck
```

### Version Update
```bash
# Bump version
npm version patch  # or minor, major

# Or manually update package.json
jq '.version = "1.2.3"' package.json > tmp && mv tmp package.json
```

### Changelog Update
```bash
# Generate changelog from commits
git log --oneline --no-merges HEAD~10..HEAD > CHANGELOG.md

# Or use conventional-changelog
npx conventional-changelog -p angular -i CHANGELOG.md -s
```

### Release Commit
```bash
# Stage changes
git add package.json CHANGELOG.md

# Commit
git commit -m "release: v1.2.3"

# Tag
git tag v1.2.3

# Push
git push origin main --tags
```

---

## 3. LAND AND DEPLOY STAGE

### Merge to Main
```bash
# Create release branch
git checkout -b release/v1.2.3

# Push release branch
git push origin release/v1.2.3

# Create PR to main
gh pr create --base main --head release/v1.2.3 --title "Release v1.2.3"

# Merge PR
gh pr merge --merge
```

### Build Production Artifacts
```bash
# Build
npm run build

# Or for specific platforms
npm run build:linux
npm run build:macos
npm run build:windows
```

### Deploy to Staging
```bash
# Deploy to staging environment
./scripts/deploy.sh staging

# Or use specific deployment tool
npm run deploy:staging
```

### Smoke Tests
```bash
# Run smoke tests against staging
npm run test:smoke

# Or run specific smoke tests
npx playwright test --grep="smoke"
```

### Deploy to Production
```bash
# Deploy to production
./scripts/deploy.sh production

# Or use specific deployment tool
npm run deploy:production
```

---

## 4. CANARY STAGE

### Deploy Canary
```bash
# Deploy canary (5% traffic)
./scripts/canary.sh deploy --percent=5

# Or use specific canary tool
npm run canary:deploy -- --percent=5
```

### Monitor Metrics
```bash
# Monitor error rates
./scripts/canary.sh monitor --metric=errors --duration=300

# Monitor performance
./scripts/canary.sh monitor --metric=performance --duration=300

# Monitor user behavior
./scripts/canary.sh monitor --metric=behavior --duration=300
```

### Promote or Rollback
```bash
# If metrics are good, promote
./scripts/canary.sh promote

# If metrics are bad, rollback
./scripts/canary.sh rollback
```

---

## 5. BENCHMARK STAGE

### Run Benchmarks
```bash
# Run performance benchmarks
npm run benchmark

# Or run specific benchmarks
npm run benchmark:api
npm run benchmark:ui
npm run benchmark:load
```

### Compare to Baseline
```bash
# Load baseline
cat benchmarks/baseline.json

# Compare to current
npm run benchmark:compare -- --baseline=benchmarks/baseline.json

# Generate report
npm run benchmark:report
```

### Alert on Regressions
```bash
# Check for regressions
npm run benchmark:check -- --threshold=10

# If regressions found, alert
if [ $? -ne 0 ]; then
  echo "Performance regression detected!"
  # Send alert
fi
```

---

## 6. SAFETY GATES

### Gate 1: Pre-ship
- [ ] All tests pass
- [ ] Security scan passes (no critical/high)
- [ ] Lint passes
- [ ] Typecheck passes
- [ ] Build succeeds

### Gate 2: Pre-deploy
- [ ] Staging deployment succeeds
- [ ] Smoke tests pass
- [ ] No performance regressions

### Gate 3: Pre-promote
- [ ] Canary error rate < 1%
- [ ] Canary performance within baseline
- [ ] No user behavior anomalies

### Gate 4: Post-benchmark
- [ ] All benchmarks pass
- [ ] No regressions > 10%
- [ ] Report generated

---

## 7. ROLLBACK PROCEDURE

### Immediate Rollback
```bash
# Rollback canary
./scripts/canary.sh rollback

# Rollback production
./scripts/deploy.sh rollback

# Or use specific rollback tool
npm run deploy:rollback
```

### Post-mortem
```a]1. Document what went wrong
2. Update monitoring/alerting
3. Fix root cause
4. Re-run pipeline
```

---

## 8. CI/CD INTEGRATION

### GitHub Actions
```yaml
name: Release Pipeline
on:
  push:
    tags:
      - 'v*'

jobs:
  ship:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm test
      - run: npx ecc-agentshield scan --path . --min-severity high
      - run: npm run build
      - run: npm run deploy:staging
      - run: npm run test:smoke
      - run: npm run deploy:production

  canary:
    needs: ship
    runs-on: ubuntu-latest
    steps:
      - run: ./scripts/canary.sh deploy --percent=5
      - run: ./scripts/canary.sh monitor --duration=300
      - run: ./scripts/canary.sh promote

  benchmark:
    needs: canary
    runs-on: ubuntu-latest
    steps:
      - run: npm run benchmark
      - run: npm run benchmark:compare
      - run: npm run benchmark:report
```

---

## 9. MONITORING AND ALERTING

### Error Rate Monitoring
```bash
# Check error rate
ERROR_RATE=$(curl -s "https://metrics.example.com/error-rate" | jq '.rate')

if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
  echo "Error rate too high: $ERROR_RATE"
  # Send alert
fi
```

### Performance Monitoring
```bash
# Check response time
RESPONSE_TIME=$(curl -s "https://metrics.example.com/response-time" | jq '.p95')

if (( $(echo "$RESPONSE_TIME > 500" | bc -l) )); then
  echo "Response time too high: ${RESPONSE_TIME}ms"
  # Send alert
fi
```

---

## 10. BEST PRACTICES

### Do
- Run all safety gates
- Monitor canary metrics
- Benchmark before and after
- Document rollbacks
- Alert on regressions

### Don't
- Skip safety gates
- Promote canary without monitoring
- Ignore performance regressions
- Deploy without smoke tests
- Forget to update changelog

---

## 11. QUICK RELEASE

For a fast release:
```bash
# Quick ship
npm test && npm run lint && npm run typecheck && npm run build && git tag v1.2.3 && git push --tags

# Quick deploy
npm run deploy:production

# Quick canary
./scripts/canary.sh deploy --percent=5 && ./scripts/canary.sh monitor --duration=60 && ./scripts/canary.sh promote

# Quick benchmark
npm run benchmark && npm run benchmark:report
```
