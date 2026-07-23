---
name: devops-automation
description: Use when deciding HOW a change gets deployed — CI/CD pipeline shape, IaC approach, deployment strategy, rollback plan. Do NOT use for "is this change ready to deploy" (see quality-gates, verification-before-completion) — this skill assumes the change already passed those and decides deployment mechanics only.
metadata:
  origin: adapted from ECC
  version: 1
---

# devops-automation

## Relationship to existing skills

dev-craft's SHIP phase already produces "commit + rollback plan." This skill
is what SHIP should invoke to decide the actual rollback/deployment mechanics
in more complexity than a one-line plan — it does not replace SHIP's
responsibility to require a rollback plan exist, it supplies how to build one.

## Iron Law

**NO DEPLOY WITHOUT A TESTED ROLLBACK PATH.**

If you can't state how this deploy gets undone in under a sentence, and
haven't verified that path works, you're not ready to deploy — regardless of
how confident the change itself is.

## Decision tree

1. **Does this change require infrastructure changes, not just app code?**
   - Yes → Infrastructure as Code (Terraform/Pulumi/CloudFormation), changes
     go through the same review as application code, plan/diff reviewed
     before apply. → `reference/iac-patterns.md`
   - No → skip straight to deployment strategy.

2. **What's the blast radius if this deploy is bad?**
   - Low (internal tool, easy revert) → rolling deploy is fine.
   - Medium/high (customer-facing, hard to detect issues fast) →
     **canary** or **blue-green**, so bad deploys are caught on a subset of
     traffic before full rollout. → `reference/deployment-strategies.md`

3. **Secrets/config for this environment** — never inline, never in the
   pipeline definition file itself. → `reference/secrets-management.md`

4. **Pipeline itself** (GitHub Actions/GitLab CI/Jenkins) — the pipeline
   definition is code: it gets reviewed, and a failing pipeline blocks merge,
   it doesn't get bypassed. → `reference/cicd-pipelines.md`

## Output

A deployment plan: strategy chosen (rolling/canary/blue-green) and why,
rollback trigger condition, and where secrets/config live — attached to
dev-craft's SHIP output.
