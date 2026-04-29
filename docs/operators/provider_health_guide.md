---
title: Provider Health Guide
owner: Data Engineer
family: guide
freshness_window: 90
---

# Provider Health Guide

Monitoring provider health is crucial for maintaining data integrity. The health status governs how the Provider Abstraction Layer routes requests and triggers failovers.

## Status Classifications
1. **HEALTHY**: Operational. Failover rate is negligible.
2. **DEGRADED**: Minor issues or occasional latency. Still used, but backups may be primed.
3. **UNSTABLE**: High timeout or failover rate. A secondary provider may be promoted to primary.
4. **QUARANTINED**: Consistently failing. Hard-disabled until manual operator intervention.

## Actions
- Use `python -m sports_signal_bot.main preview-provider-health` to check the current status of all providers.
