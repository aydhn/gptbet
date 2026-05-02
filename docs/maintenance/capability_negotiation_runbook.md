---
owner: "@principal_assurance_engineer"
family: "runbook"
freshness_window: "90d"
---

# Capability Negotiation Runbook

## Task: Managing Capability Drift Alerts
**Symptom**: Monitoring alerts indicating a high rate of `federation_breaking_drift` or `cross-registry replay mismatch`.
**Action**:
1. Check the Capability Negotiation Manifest for recent drift records.
2. Identify which external verifier changed their profile.
3. If they dropped a required proof format, the automated system should have quarantined them. Verify quarantine status.
4. If a renegotiation is required, trigger it manually or communicate with the partner registry owner.

## Task: Running a Negotiation Pass
```bash
python -m sports_signal_bot.main capability-negotiation run-capability-negotiation-pass
```

## Task: Notarized Snapshots Missing Local Replay
**Symptom**: A notarized registry snapshot is imported, but the local replay validation fails.
**Action**:
- Remember: **Notarization strengthens snapshots, not authority.** A valid signature does not override local compatibility logic.
- Inspect the capability mismatch. It is likely the foreign registry snapshot relies on a spec version we do not support locally.
