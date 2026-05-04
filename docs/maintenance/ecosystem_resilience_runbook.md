# Ecosystem Resilience Maintenance Runbook

## Resolving No Safe Mesh Path
If the system routinely yields `no_safe_mesh_path`:
1. Check Controller State: Ensure controllers aren't stuck in `degraded_state`.
2. Evaluate Pressure: Look at Hub queue sizes. If `high_pressure`, back pressure triggers `degraded_fallback_path`.
3. Check Sovereignty: Validate no new global deny constraints are blocking existing pathways.

## Addressing Stale Marketplace Signals
Stale signals are capped at a low score (e.g. `0.4`).
- Refresh the baseline catalog and ensure treaties are updating on-time.

## Validating Controller Recovery
When controllers recover, they transition from `degraded_state` to `recovery_monitoring_state`, eventually restoring `monitoring_normal`. Mesh routes will automatically recover their preference band during the next pass.
