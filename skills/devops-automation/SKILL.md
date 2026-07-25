---
name: devops-automation
description: Use when deciding deployment mechanics, rollback strategy, CI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/CD
  pipeline shape, or infrastructure-as-code choices. Do NOT use for "is this ready
  to deploy" (see quality-gates) or for writing the pipeline YAML itself (that's plain
  BUILD work once the strategy is decided).
metadata:
  origin: adapted from ECC and addyosmani${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/agent-skills
  version: 1
owner: noname.spyware@gmail.com
allowedTools:
- shell
- docker
- kubernetes
- terraform
- git

---

# devops-automation

## Relationship to existing skills

dev-craft's SHIP phase should invoke this skill for the deployment mechanics and rollback path, rather than deciding the strategy ad hoc per deploy. quality-gates runs before this — it validates the artifact; this skill defines how the validated artifact gets to production and back.

## Iron Law

**NO DEPLOY WITHOUT A TESTED ROLLBACK PATH.**

If you can't roll back in under 5 minutes with one command, the deploy strategy is incomplete — not just "risky," incomplete.

## Decision tree

1. **Where does this run?**
   - Kubernetes (EKS${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/self-managed) → ArgoCD (GitOps) + Argo Rollouts for progressive delivery. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/argocd-rollouts.md`
```bash
# EXAMPLE (do not run)
   - VMs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/bare metal → Terraform + systemd${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Docker Compose + SSH${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Ansible rollback. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/terraform-vm-deploy.md`
```
   - Serverless (Lambda${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Cloud Run${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Functions) → framework-native (SST, Serverless Framework, Terraform) with traffic shifting. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/serverless-deploy.md`

2. **How many environments, and what's the promotion path?**
   - Dev → Staging → Prod with manual gate → standard GitOps, promote via PR to environment branch or tag. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/promotion-strategy.md`
   - Preview env per PR → ephemeral namespaces${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/stacks, auto-cleanup on merge${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/close. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/preview-environments.md`

3. **What's the blast radius tolerance?**
   - Canary${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/blue-green required (payments, auth, critical path) → define traffic split, SLO burn-rate alert, automated rollback on SLO violation. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/progressive-delivery.md`
   - Rolling update acceptable (internal tools, batch) → define maxSurge${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/maxUnavailable and health check criteria. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/rolling-update.md`

4. **Secrets and config?**
   - External Secrets Operator + Vault${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Secrets Manager${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Parameter Store — never bake secrets into images or Git. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/secrets-management.md`

5. **Infrastructure as Code?**
   - Terraform${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/OpenTofu for cloud resources; Helm${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Kustomize for K8s manifests. State in remote backend with locking. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/iac-best-practices.md`

## Output

A deployment strategy doc: environment topology, promotion triggers, rollback command (tested in staging), secret injection method, and the CI${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/CD pipeline skeleton — handed to dev-craft's SHIP phase.