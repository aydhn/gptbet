# Governance Fabric Runbook

## Alert: Council Quorum Failure Spike
**Symptom:** High rate of `case_blocked` due to unmet quorums.
**Action:**
1. Check `participant_refs` availability.
2. Verify if the `quorum_policy_ref` is overly strict for the current tier conditions.
3. *Do not* manually override block states. Let the system fall back to safe local routes.

## Alert: Fabric Stale Signal Storm
**Symptom:** Fabric pressure outcome reads `suppress_noncritical_signal_paths` consistently.
**Action:**
1. Check external signal sources feeding the input segments.
2. Verify `freshness_decay` configurations in the channel rules.
3. Ensure suppression segments are correctly capturing and halting the stale flow.

## Alert: Audit Replay Mismatch Spike
**Symptom:** `replay_currentness_drifted` or `replay_baseline_shifted` outcomes are surging.
**Action:**
1. The external projections are drifting from local baseline reality.
2. Verify that the Controller is correctly applying caps (`ProjectionAuditDecisionRecord` final_status = `capped`).
3. Investigate the source of the audit packets for stale references.
