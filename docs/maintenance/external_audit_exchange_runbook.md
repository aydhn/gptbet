# External Audit Exchange Runbook

## Routine Operations

1. **Run the Exchange Pass**
   Execute `python -m sports_signal_bot.main run-external-audit-exchange-pass` periodically to process pending requests, ingest responses, and update reputation/readiness.

2. **Review Triage Backlog**
   Use `preview-challenge-triage` to check if high-priority challenges are stuck or assigned to incorrect responder classes.

3. **Monitor Quarantined Inputs**
   If the quarantine rate spikes, investigate the source. It may indicate a malformed adapter configuration, a spam attack, or an issue with a specific external provider.

4. **Verify Notarization Coverage**
   Ensure critical checkpoints are successfully notarized. Use `preview-notarization-receipts`.

## Troubleshooting

- **Symptom: All external responses are quarantined.**
  - **Check**: The configured `default_external_audit_strategy`. If using `QuarantineHeavyExternalInputStrategy`, this is expected for unknown responders.
  - **Check**: Schema validation failures in the ingestor.

- **Symptom: Witness reputation is dropping rapidly.**
  - **Check**: Is the witness sending repeated false alarms or stale responses? Use `preview-witness-reputation` to inspect the signal breakdown.

- **Symptom: Notarization receipts failing verification.**
  - **Check**: Ensure the digest logic in `build_notarization_digest` matches what the notary provider expects and signs.
