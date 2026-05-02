# Assurance Exchange Runbook

- **Stale Snapshots**: If `sync_state` shows stale mirrors, verify connectivity.
- **Quarantine Surges**: A spike in quarantines means a partner registry updated their schema or policy without coordinating translation rules. Update `translations.yaml`.
