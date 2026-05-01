# Notarization and External Review Guide

## Understanding the Difference

- **Notarization**: The act of an external provider attesting to the existence and integrity of a specific digest at a specific time. It does *not* validate the contents or correctness of the data behind the digest, only that it was registered.
- **External Review**: The act of an independent auditor or verification exchange analyzing an exported packet (containing redacted data and proofs) and returning findings regarding its validity, accuracy, or compliance.
- **Witness Reputation**: The score assigned to an external responder based on their historical performance (e.g., accuracy of findings, timely responses).

## Operational Workflow

1. **Exporting Requests**: The system automatically generates `ExternalAuditRequestRecord` packets for eligible challenges or verification needs. These are processed by adapters (e.g., written to files or submitted via APIs).
2. **Ingesting Responses**: When an external party provides a response, it is imported as an `ExternalAuditResponseRecord`.
3. **Quarantine and Verification**: All imported responses enter a 'quarantine' or 'pending_verification' state. The system validates the schema, checks the responder's reputation, and evaluates the trust level.
4. **Local Action Mapping**: Findings are mapped to local actions. For example, a 'critical' finding from a trusted auditor might trigger an 'anomaly_case', while a response from an unknown source remains quarantined.

## Notarization Hooks
Notarization requests are triggered for critical decisions and checkpoints. Ensure that the `configs/external_audit_exchange/notarization.yaml` file lists the required families.

## Commands
Use `python -m sports_signal_bot.main run-external-audit-exchange-pass` to process requests, responses, and notarizations.
