---
name: observability-engineering
description: |
  Use when deciding what to log, measure, trace, and alert on for a service — the observability contract.
  Do NOT use for "is this service secure" (see bug-hunting) or "is this hardened" (see dev-craft HARDEN, which invokes this skill).
  Do NOT use for implementing the instrumentation itself (that's BUILD work once the contract is decided).
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
triggers:
  - "observability"
  - "monitoring"
  - "logging"
  - "telemetry"
  - "instrument"
metadata:
  origin: agent-master-skills
  preferred-model: nemotron-3-ultra-free
  version: 2.0.0
  domain: specialized-engineering
  integrates-with: [dev-craft, bug-hunting, verification-before-completion]
  source-enhancements: v2.0.0 Master Template alignment
---
TOKEN CEILING: ~2K tokens. If skill exceeds, extract sections to references/.

# observability-engineering

## Relationship to existing skills

dev-craft's HARDEN phase should invoke this skill to define the observability contract (logs/SLOs) for the thing it just built, rather than adding logging/monitoring as an afterthought. bug-hunting covers attack surface; this covers visibility into behavior — they're separate concerns.

## Iron Law

**NO ALERT WITHOUT AN OWNER AND A RUNBOOK LINK.**

Every alert must name a human who responds and a runbook URL they open first. Alerts without owners are noise, not signal.

## Decision tree

1. **What are the user-facing outcomes?**
   - Latency target → **SLO**: p99 < X ms. Error budget = 1 - SLO.
   - Availability target → **SLO**: success rate > Y%.
   - Throughput target → **SLO**: requests/sec > Z.

2. **How do we know when the SLO is burning?**
   - Multi-window, multi-burn-rate alerts (fast: 2% budget in 1h; slow: 10% in 6h). No static thresholds.
   - Alert routes to on-call with runbook link.

3. **What do we log?**
   - Structured JSON with correlation IDs (trace_id, span_id) on every request. Log at the boundary (request in, response out), not inside every function.
   - No PII, no secrets in logs.

4. **What metrics do we emit?**
   - RED (Rate, Errors, Duration) for every endpoint — auto-instrumented where possible (OpenTelemetry).
   - USE (Utilization, Saturation, Errors) for resources (CPU, memory, disk, network, DB connections).
   - Business metrics (orders placed, signups, payment failures) as counters with labels for slicing.

5. **How do we trace?**
   - OpenTelemetry everywhere — auto-instrumentation for framework, manual spans for business logic boundaries.
   - Sample rate: 100% for errors, configurable for success (head/tail sampling).

6. **Where does it go?**
   - Logs → Loki/CloudWatch
   - Metrics → Prometheus/Mimir or managed (Grafana Cloud, Datadog)
   - Traces → Tempo/Zipkin or managed
   - Dashboards → Grafana (code-defined, not click-ops).

## Output

An observability contract doc per service: SLOs with error budgets, alert rules with owners/runbook links, log/trace schema, and dashboard definitions — handed to dev-craft HARDEN.