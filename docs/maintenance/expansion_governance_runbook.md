---
owner: Maintenance
family: Runbook
freshness_window_days: 30
---

# Expansion Governance Runbook

## Resolving Global Pauses
1. Inspect the `expansion_governance_manifest_*.json` in `artifacts/`.
2. Identify the fired trigger (e.g., `critical_verification_regression_cluster`).
3. Resolve underlying root cause (rollback specific bad cohorts).
4. Unpause via operator override (not implemented in CLI yet, requires explicit API/script call).

## Budget Saturation
If budgets are exhausted, wait for current waves to complete and stabilize, which will release budget back to the pool.
