---
name: devops-automation
description: Use when deciding deployment mechanics, rollback strategy, CI/CD
  pipeline shape, or infrastructure-as-code choices. Do NOT use for "is this ready
  to deploy" (see quality-gates) or for writing the pipeline YAML itself (that's plain
  BUILD work once the strategy is decided).
metadata:
  origin: adapted from ECC and addyosmani/agent-skills
  version: 1

---

# devops-automation

## Relationship to existing skills

dev-craft's SHIP phase should invoke this skill for the deployment mechanics and rollback path, rather than deciding the strategy ad hoc per deploy. quality-gates runs before this — it validates the artifact; this skill defines how the validated artifact gets to production and back.

## Iron Law

**NO DEPLOY WITHOUT A TESTED ROLLBACK PATH.**

If you can't roll back in under 5 minutes with one command, the deploy strategy is incomplete — not just "risky," incomplete.

## Decision tree

1. **Where does this run?**
   - Kubernetes (EKS/self-managed) → ArgoCD (GitOps) + Argo Rollouts for progressive delivery. → `reference/argocd-rollouts.md`
```bash
# EXAMPLE (do not run)
   - VMs/bare metal → Terraform + systemd/Docker Compose + SSH/Ansible rollback. → `reference/terraform-vm-deploy.md`
```
   - Serverless (Lambda/Cloud Run/Functions) → framework-native (SST, Serverless Framework, Terraform) with traffic shifting. → `reference/serverless-deploy.md`

2. **How many environments, and what's the promotion path?**
   - Dev → Staging → Prod with manual gate → standard GitOps, promote via PR to environment branch or tag. → `reference/promotion-strategy.md`
   - Preview env per PR → ephemeral namespaces/stacks, auto-cleanup on merge/close. → `reference/preview-environments.md`

3. **What's the blast radius tolerance?**
   - Canary/blue-green required (payments, auth, critical path) → define traffic split, SLO burn-rate alert, automated rollback on SLO violation. → `reference/progressive-delivery.md`
   - Rolling update acceptable (internal tools, batch) → define maxSurge/maxUnavailable and health check criteria. → `reference/rolling-update.md`

4. **Secrets and config?**
   - External Secrets Operator + Vault/Secrets Manager/Parameter Store — never bake secrets into images or Git. → `reference/secrets-management.md`

5. **Infrastructure as Code?**
   - Terraform/OpenTofu for cloud resources; Helm/Kustomize for K8s manifests. State in remote backend with locking. → `reference/iac-best-practices.md`

## Output

A deployment strategy doc: environment topology, promotion triggers, rollback command (tested in staging), secret injection method, and the CI/CD pipeline skeleton — handed to dev-craft's SHIP phase.