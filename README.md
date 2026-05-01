# Sports Signal Bot

A local-first, verifiable sports forecasting framework with an independently verifiable transparency layer.

## Transparency & Verification Architecture

Phase 56 introduces an append-only transparency log and independent verification mesh to ensure that all critical governance events (like decision proofs, multi-signer approvals, overrides, and policy promotions) are not only stored but cryptographically verifiable.

### Core Concepts

- **Append-Only Transparency Logs**: Immutable records of governance events mapped through Merkle trees. Hashes build a verifiable chain.
- **Inclusion & Consistency Proofs**: Verifiers can challenge the logs to provide proofs of inclusion (an event exists in the log) or consistency (a new checkpoint properly extends a previous one).
- **Verification Mirrors**: Independent read-only replicas that sync with the source transparency logs and flag divergence. Mirrors act as verifiers, not source-of-truth.
- **Trust Gossip**: Cross-plane signals that broadcast summaries of important state changes (like signed checkpoints or revoked trust). These trigger verification; they are not blindly trusted.
- **Independently Verifiable Governance**: Governance decisions are no longer just files on disk; they are mathematically linked via proofs, allowing a third party (or future public network) to audit without trusting local mutations.

## Getting Started

```bash
# Setup
python -m pip install -e .[dev]
cp .env.example .env

# Run transparency simulation
python -m sports_signal_bot.main transparency run-transparency-pass
python -m sports_signal_bot.main transparency verify-inclusion-proof
python -m sports_signal_bot.main transparency verify-transparency-mirrors
```


### Phase 58: External Audit Exchange Readiness
This phase implements the `external_audit_exchange` module, transitioning the system to be "exchange-ready" for external audits, notarization, and independent verification.
- **External Audit Exchange Layer**: Pluggable adapters for exporting safe, redacted verification packets and ingesting external responses.
- **Notarization Hooks**: Interfaces for notarizing critical state digests and verifying receipts.
- **Witness Reputation Engine**: Explainable scoring and adjustments for external responders.
- **Challenge Triage**: Priority-based routing and clustering for challenge resolution.
- **Fail-Safe Ingestion**: External findings are never blindly trusted; they follow a quarantine-first, local-verification required flow.
- **Readiness Scoring**: Metrics to evaluate the system's preparedness for public audit exchanges.

Commands to interact with this layer:
- `python -m sports_signal_bot.main run-external-audit-exchange-pass`
- `python -m sports_signal_bot.main list-external-audit-exchange-strategies`

## Phase 59: Public Verification Gateway
Phase 59 adds a controlled external gateway for securely publishing governance artifacts and intaking external challenges.
- **Why publication is redaction-governed**: It ensures verifiability without overexposure of sensitive internals.
- **Why challenge intake is review-only**: It prevents external state mutation while still accepting valuable public scrutiny.
Use `python -m sports_signal_bot.main run-public-verification-gateway-pass` to run the lifecycle.

### Verifier Portal Experience (Phase 60)
The **Verifier Portal Experience** introduces a structured, read-only experience layer designed to safely expose governance, adjudication, and decision traces to third-party consumers.
- **Why Read-Only**: The portal prevents state mutation from external actors. All active inputs must flow through strict Challenge Intake APIs to ensure proper validation and adjudication.
- **Packets & Profiles**: Artifacts are scoped to specific audience profiles (e.g., `public`, `verifier`, `auditor`). A single raw record is rendered differently for each audience:
    - **Public Packets**: Stripped of internal details, heavily redacted, only surfacing the minimal safe summary.
    - **Verifier Packets**: Includes deeper proof references, notarization receipts, and detailed caveats.
    - **Auditor Packets**: Full summary transparency to support rigorous oversight.
- **Challenge APIs**: A quarantine-first strategy controls the intake of external claims or issues.

#### Example Commands
```bash
python -m sports_signal_bot.main verifier-portal run-verifier-portal-pass
python -m sports_signal_bot.main verifier-portal preview-verifier-views
python -m sports_signal_bot.main verifier-portal preview-verification-packets
python -m sports_signal_bot.main verifier-portal preview-challenge-api-submissions
```
