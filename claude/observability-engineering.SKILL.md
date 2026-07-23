---
name: observability-engineering
description: Use when deciding WHAT to instrument and alert on for a change — structured logging, metrics, tracing, SLOs. Do NOT use for general security hardening unrelated to visibility into system behavior (see bug-hunting for that); this skill is specifically about knowing what's happening in production, not preventing attacks.
metadata:
  origin: adapted from ECC
  version: 1
---

# observability-engineering

## Relationship to existing skills

dev-craft's HARDEN phase does cross-cutting security checks. This skill is a
separate, adjacent concern it should also invoke: not "is this safe from
attack" but "will we know if this breaks in production." Don't conflate the
two — a system can be secure and unobservable, or observable and insecure.

## Iron Law

**NO ALERT WITHOUT AN OWNER AND A RUNBOOK LINK.**

An alert that fires with no clear owner or no linked next-action trains
people to ignore alerts. Don't add one without both.

## Decision tree

1. **Is this change adding a new failure mode that wasn't visible before?**
   - Yes → add structured logging at the failure point (JSON, correlation ID
     threaded through, appropriate level — not everything at ERROR).
     → `reference/structured-logging.md`

2. **Does this change affect a metric someone already tracks, or need a new one?**
   - Use RED (Rate/Errors/Duration) for request-driven services, USE
     (Utilization/Saturation/Errors) for resources. Don't invent a third
     scheme without reason. → `reference/metrics-red-use.md`

3. **Does this change cross service boundaries?**
   - Yes → trace context (W3C Trace Context) must propagate through the new
     boundary, or the trace breaks silently at that hop.
     → `reference/distributed-tracing.md`

4. **Before adding an alert, check**: does this map to an SLO/error budget,
   or is it a vanity metric? Alerts not tied to user-facing impact are a
   common source of alert fatigue. → `reference/slo-alerting.md`

5. **Dashboard for this** — one dashboard answering "is this system healthy
   right now," not a wall of every metric available.
   → `reference/dashboard-design.md`

## Output

An observability plan for the change: what's logged, what metric/trace
changed, what alert (if any) was added and its owner+runbook — attached to
dev-craft's HARDEN output.
