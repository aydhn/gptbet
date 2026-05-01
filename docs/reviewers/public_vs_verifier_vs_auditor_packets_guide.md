# Public vs. Verifier vs. Auditor Packets Guide

## Packet Depth and Differentiation
The verification experience differentiates artifact visibility using specific packet profiles. This guide explains how to handle each tier during a review process.

### Public Packets (`public_viewer`)
- **Focus**: Safest proofs, lowest exposure.
- **Characteristics**: Extremely summarized, heavily redacted signer metadata, only critical summary information is provided.

### Verifier Packets (`registered_verifier`, `trusted_external_verifier`)
- **Focus**: Usable data for external validation.
- **Characteristics**: Deeper proof references, detailed caveats, access to challenge APIs and richer diagnostic views.

### Auditor Packets (`external_auditor`)
- **Focus**: Complete systemic review.
- **Characteristics**: Full access to anomaly context, exchange references, and complete proof traces.

## Review Responsibility
When reviewing portal updates, verify that information intended for Auditors does not leak into Verifier or Public profiles. Test profile boundaries rigorously.
