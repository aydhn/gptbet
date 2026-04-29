---
title: Provider Failover Runbook
owner: Data Engineer
family: runbook
freshness_window: 90
---

# Provider Failover Runbook

This runbook outlines steps for dealing with sustained provider failovers.

## Scenario: Primary Provider Timeout
1. The Abstraction Layer intercepts the timeout and flags the provider.
2. The `ProviderFailoverEngine` evaluates the failover sequence defined in `configs/providers/failover.yaml`.
3. The fallback provider is invoked. If successful, lineage is recorded showing the failover chain.
4. **Operator Task**: Check `provider_health_summary.json` to see if the timeout is an anomaly or a persistent issue requiring quarantine.

## Scenario: Unacceptable Quality Score
1. A payload is fetched but lacks required fields (Completeness Score < Threshold).
2. The payload is rejected, and a failover to a cached or secondary provider is triggered.
3. **Operator Task**: Investigate schema changes on the primary provider's end.
