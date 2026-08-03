---
name: devops-automation
description: |
  CI/CD pipeline design, IaC best practices (Terraform/Kubernetes), security-by-default
  configurations, automated rollback strategies, and deployment validation gates. Use when
  deciding deployment mechanics, rollback strategy, CI/CD pipeline shape, or
  infrastructure-as-code choices. Do NOT use for "is this ready to deploy" (see
  verification-before-completion) or for writing the pipeline YAML itself (that's plain BUILD work
  once the strategy is decided).
model: deepseek-v4-flash-free
version: 2.0.0
preamble-tier: 3
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - AskUserQuestion
  - Task
triggers:
  - "deploy"
  - "ci/cd"
  - "infrastructure"
  - "devops"
  - "pipeline"
  - "terraform"
  - "kubernetes"
  - "rollback strategy"
  - "iac"
metadata:
  origin: agent-master-skills
  preferred-model: deepseek-v4-flash-free
  version: 2.0.0
  domain: devops
  integrates-with: [verification-before-completion, dev-craft, verification-before-completion, security-audit]
---

TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# devops-automation

## Relationship to existing skills

- `dev-craft` — dev-craft's SHIP phase invokes this skill for deployment mechanics and rollback path, rather than deciding the strategy ad hoc per deploy
- `verification-before-completion` — runs before this skill; it validates the artifact; this skill defines how the validated artifact gets to production and back
- `security-audit` — security-by-default configurations in this skill complement the security audit
- `verification-before-completion` — runs after deployment to confirm the release succeeded

## When to Use

- Deciding deployment mechanics or strategy
- Setting up CI/CD pipelines
- Defining IaC for cloud resources
- Planning rollback strategies
- Configuring secrets management
- Setting up progressive delivery (canary, blue-green)
- Infrastructure-as-code decisions (Terraform, Kubernetes)

**When NOT to use:** "Is this ready to deploy?" (see `verification-before-completion`), writing pipeline YAML itself (that's BUILD work once the strategy is decided), or trivial config changes.

## The Iron Law

**NO DEPLOY WITHOUT A TESTED ROLLBACK PATH.**

If you can't roll back in under 5 minutes with one command, the deploy strategy is incomplete — not just "risky," incomplete.

## Workflow

### Phase 1: ASSESS — Determine deployment topology

1. **Where does this run?**
   - Kubernetes (EKS/self-managed) → ArgoCD (GitOps) + Argo Rollouts for progressive delivery
   - VMs/bare metal → Terraform + systemd/Docker Compose + SSH/Ansible rollback
   - Serverless (Lambda/Cloud Run/Functions) → framework-native (SST, Serverless Framework, Terraform) with traffic shifting

2. **How many environments, and what's the promotion path?**
   - Dev → Staging → Prod with manual gate → standard GitOps, promote via PR to environment branch or tag
   - Preview env per PR → ephemeral namespaces/stacks, auto-cleanup on merge/close

3. **What's the blast radius tolerance?**
   - Canary/blue-green required (payments, auth, critical path) → define traffic split, SLO burn-rate alert, automated rollback on SLO violation
   - Rolling update acceptable (internal tools, batch) → define maxSurge/maxUnavailable and health check criteria

**Exit criterion:** Deployment topology documented, environment map defined, promotion path clear.

### Phase 2: SECURE — Apply security-by-default configurations

1. **Least privilege:**
   - IAM roles scoped to minimum required permissions
   - Service accounts per workload, not shared
   - No wildcard permissions in policies

2. **Secrets management:**
   - External Secrets Operator + Vault/Secrets Manager/Parameter Store
   - Never bake secrets into images or Git
   - Rotate secrets automatically

3. **Network security:**
   - Network policies restrict pod-to-pod communication
   - Ingress controllers with TLS termination
   - No exposed admin ports in production

4. **Container security:**
   - Run as non-root
   - Read-only filesystem where possible
   - No privileged containers
   - Scan images for CVEs before deployment

**Exit criterion:** Security checklist passed, secrets configured, least privilege verified.

### Phase 3: BUILD — Define IaC and pipeline

1. **Terraform/OpenTofu for cloud resources:**
   - State in remote backend with locking (S3 + DynamoDB, or Terraform Cloud)
   - Module structure: one module per logical component
   - Variable validation with `variable {}` blocks and `validation {}` rules
   - Output only what downstream consumers need
   - `terraform plan` in CI, never apply from local

2. **Kubernetes manifests:**
   - Helm charts or Kustomize overlays
   - Namespace per environment (dev/staging/prod)
   - Resource requests and limits on every workload
   - PodDisruptionBudgets for critical services
   - HorizontalPodAutoscaler for stateless services

3. **CI/CD pipeline skeleton:**
   ```yaml
   stages:
     - validate     # lint, typecheck, test
     - build        # container image build
     - scan         # security scan (SAST, DAST, image scan)
     - deploy-staging  # deploy to staging
     - smoke-test   # automated smoke tests against staging
     - promote      # manual or automated promotion to prod
     - deploy-prod  # deploy to production
     - verify       # post-deploy health checks
   ```

**Exit criterion:** IaC code committed, pipeline skeleton defined, `terraform plan` succeeds.

### Phase 4: ROLLBACK — Define automated rollback strategy

1. **Rollback triggers:**
   - Health check failure after deploy
   - SLO burn-rate alert triggered
   - Error rate spike > threshold
   - Manual rollback command

2. **Rollback methods by platform:**
   - Kubernetes: `kubectl rollout undo deployment/<name>` or Argo Rollouts abort
   - Terraform: `terraform apply` with previous state (keep last 3 state files)
   - Serverless: traffic shift back to previous version
   - Blue-green: switch traffic back to green

3. **Rollback validation:**
   - Run smoke tests against the rolled-back version
   - Verify data integrity (no partial migrations)
   - Confirm monitoring dashboards return to baseline

4. **Rollback testing:**
   - Test rollback in staging at least once per sprint
   - Document rollback commands and expected time
   - Time-box: rollback must complete in under 5 minutes

**Exit criterion:** Rollback strategy documented, commands tested in staging, time-box verified.

### Phase 5: VALIDATE — CI/CD validation gates

1. **Pre-deploy gates:**
   - All tests pass (unit, integration, e2e)
   - Lint and typecheck clean
   - Security scan passed (no Critical/High findings)
   - `terraform plan` shows expected changes only
   - Image scan passed (no Critical CVEs)

2. **Post-deploy gates:**
   - Health checks pass (all endpoints responding)
   - Smoke tests pass (critical user journeys)
   - Metrics baseline established (latency, error rate, throughput)
   - No alerts firing within 5 minutes of deploy

3. **Progressive delivery gates (canary/blue-green):**
   - Traffic split configured correctly
   - SLO burn-rate within threshold for canary duration
   - Automated rollback triggered if SLO violation detected
   - Manual approval gate before full rollout (if manual gate configured)

**Exit criterion:** All validation gates pass, deployment verified, rollback path tested.

## Output Contract

A deployment strategy doc containing: environment topology, promotion triggers, rollback command (tested in staging), secret injection method, IaC module structure, CI/CD pipeline skeleton, security configurations, and validation gate definitions — handed to `dev-craft`'s SHIP phase.

## Quality Gates

- [ ] Deployment topology documented (K8s, VM, or serverless)
- [ ] Promotion path defined (Dev → Staging → Prod)
- [ ] Rollback strategy documented and tested in staging
- [ ] Secrets management configured (no secrets in Git or images)
- [ ] Least privilege IAM roles defined
- [ ] Terraform state in remote backend with locking
- [ ] K8s manifests have resource requests/limits
- [ ] CI/CD pipeline has pre-deploy and post-deploy gates
- [ ] Security scan configured (SAST, DAST, image scan)
- [ ] Progressive delivery configured for critical paths (canary/blue-green)
- [ ] Rollback time-box verified (< 5 minutes)
- [ ] All validation gates pass in staging

## Error Handling

| Failure Mode | Response |
|--------------|----------|
| Terraform plan shows unexpected changes | Stop, review diff, fix IaC before proceeding |
| Rollback takes longer than 5 minutes | Redesign rollback strategy, simplify deployment |
| Secrets exposed in logs or images | Rotate secrets immediately, fix CI pipeline |
| Security scan finds Critical/High CVEs | Block deploy, remediate or accept with documented risk |
| Post-deploy health checks fail | Trigger automated rollback, investigate before re-deploying |
| SLO burn-rate exceeded during canary | Auto-rollback canary, fix before full rollout |

## References

- `references/argocd-rollouts.md` — ArgoCD + Argo Rollouts progressive delivery configuration
- `references/terraform-vm-deploy.md` — Terraform + VM deployment with SSH/Ansible rollback
- `references/serverless-deploy.md` — Serverless deployment with traffic shifting
- `references/promotion-strategy.md` — Dev → Staging → Prod promotion strategies
- `references/preview-environments.md` — Ephemeral preview environments per PR
- `references/progressive-delivery.md` — Canary/blue-green with SLO burn-rate alerts
- `references/rolling-update.md` — Rolling update configuration with health checks
- `references/secrets-management.md` — External Secrets Operator + Vault/Secrets Manager setup
- `references/iac-best-practices.md` — Terraform/OpenTofu best practices and state management