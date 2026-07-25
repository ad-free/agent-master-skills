---
name: observability-engineering
description: Use when deciding what to log, measure, trace, and alert on for a service — the observability contract. Do NOT use for "is this service secure" (see bug-hunting) or "is this hardened" (see dev-craft HARDEN, which invokes this skill). Do NOT use for implementing the instrumentation itself (that's BUILD work once the contract is decided).
metadata:
  origin: adapted from ECC and addyosmani${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/agent-skills
  version: 1
---

# observability-engineering

## Relationship to existing skills

dev-craft's HARDEN phase should invoke this skill to define the observability contract (logs${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/SLOs) for the thing it just built, rather than adding logging${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/monitoring as an afterthought. bug-hunting covers attack surface; this covers visibility into behavior — they're separate concerns.

## Iron Law

**NO ALERT WITHOUT AN OWNER AND A RUNBOOK LINK.**

Every alert must name a human who responds and a runbook URL they open first. Alerts without owners are noise, not signal.

## Decision tree

1. **What are the user-facing outcomes?**
   - Latency target → **SLO**: p99 < X ms. Error budget = 1 - SLO. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/slo-design.md`
   - Availability target → **SLO**: success rate > Y%. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/slo-design.md`
   - Throughput target → **SLO**: requests${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/sec > Z. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/slo-design.md`

2. **How do we know when the SLO is burning?**
   - Multi-window, multi-burn-rate alerts (fast: 2% budget in 1h; slow: 10% in 6h). No static thresholds. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/burn-rate-alerting.md`
   - Alert routes to on-call with runbook link. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/alert-routing.md`

3. **What do we log?**
   - Structured JSON with correlation IDs (trace_id, span_id) on every request. Log at the boundary (request in, response out), not inside every function. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/structured-logging.md`
   - No PII, no secrets in logs. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/log-sanitization.md`

4. **What metrics do we emit?**
   - RED (Rate, Errors, Duration) for every endpoint — auto-instrumented where possible (OpenTelemetry). → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/red-metrics.md`
   - USE (Utilization, Saturation, Errors) for resources (CPU, memory, disk, network, DB connections). → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/use-metrics.md`
   - Business metrics (orders placed, signups, payment failures) as counters with labels for slicing. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/business-metrics.md`

5. **How do we trace?**
   - OpenTelemetry everywhere — auto-instrumentation for framework, manual spans for business logic boundaries. → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/opentelemetry-instrumentation.md`
   - Sample rate: 100% for errors, configurable for success (head${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/tail sampling). → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/trace-sampling.md`

6. **Where does it go?**
   - Logs → Loki${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/CloudWatch
   - Metrics → Prometheus${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Mimir or managed (Grafana Cloud, Datadog)
   - Traces → Tempo${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/Zipkin or managed
   - Dashboards → Grafana (code-defined, not click-ops). → `reference${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/dashboard-as-code.md`

## Output

An observability contract doc per service: SLOs with error budgets, alert rules with owners${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/runbook links, log${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}${PROJECT_ROOT}/trace schema, and dashboard definitions — handed to dev-craft HARDEN.