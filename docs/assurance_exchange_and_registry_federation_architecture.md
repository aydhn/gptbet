# Assurance Exchange and Registry Federation Architecture

This module implements the cross-system assurance exchange and federated registry layer for the Sports Signal Bot. It allows proof-carrying assurance packages, promotion envelopes, and verifiable claims to be exchanged across trust domains without blindly trusting external systems.

Key concepts:
- **Registry Federation**: Linked registries share data via exports/imports but retain their own local policy evaluation (replay).
- **Assurance Exchange Packets**: Bound packages of claims, proofs, and attestations.
- **Claim Translation**: When families differ across domains, they are explicitly translated with recorded semantic loss limits.
- **Cross-System Replay**: All imported packages are re-run against local policy context.
- **Notarized Promotion Envelopes**: Envelopes that carry multi-signer digests suitable for public exchange.
- **Quarantine First**: If translation or replay fails, packages fall back to a quarantine state requiring review.
