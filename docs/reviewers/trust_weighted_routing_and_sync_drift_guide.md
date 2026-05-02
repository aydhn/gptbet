---
owner: ecosystem_sync_team
family: reviewer_guide
freshness_window_days: 90
---

# Trust-Weighted Routing & Sync Drift Guide

This guide is for reviewers analyzing routing recommendations and sync lag.

## Routing Weights
Routing recommendations are based on a combination of trust, freshness, capability fit, and penalty reductions. Ensure that `trust_first` or `balanced` policies are used for critical paths.

## Sync Drift
Sync drift occurs when the routing cache outpaces or falls behind the continuous sync pipeline. A high drift index triggers reroute recommendations.

## Supersession Audits
Reviewers should check supersession propagation to ensure stale entries are tombstoned correctly.
