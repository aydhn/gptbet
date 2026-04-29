---
owner_role: lead_engineer
doc_family: reference
freshness_window_days: 180
last_reviewed: 2026-04-28
---

# KPI Reference

The following are the core KPIs managed by the central reporting registry:

## Operational Health
- **Slot Health Score**: Composite score evaluating the end-to-end success of a processing slot. (Higher is better)
- **Recovery Success Rate**: Percentage of automated recoveries successful without manual intervention. (Higher is better)

## Execution Reliability
- **Dispatch Delivery Success Rate**: Percentage of signals successfully dispatched to downstream sinks. (Higher is better)

## Release Governance
- **Release Promotion Stability**: Percentage of releases promoted without incident or rollback. (Higher is better)

## Decision Quality
- **Candidate to Approved Conversion Rate**: Ratio of approved signals vs generated candidate signals. (Neutral)

## Predictive Quality
- **Selected Subset Quality Index**: Lift of log-loss/brier score on the approved subset versus the global dataset. (Higher is better)

## Bankroll Risk
- **Bankroll Return %**: Percentage return on initial bankroll for the period. (Higher is better)
- **Max Drawdown %**: Maximum peak-to-trough drop in portfolio value during the period. (Lower is better)

## Deployment Readiness
- **Schema Compatibility Health**: Score representing the absence of breaking schema changes across integrations. (Higher is better)
