# Sports Signal Bot

...

## Proof-Carrying Governance Architecture
The Phase 62 proof-carrying governance layer aims to elevate assurance by mandating that promotion envelopes carry verifiable, machine-checkable assurance claims, attestations, and their dependency graphs. Compliance passes alone are insufficient for higher-assurance promotion; immutable refs and replayability matter for true promotion trust.

See the following docs for more details:
- `docs/proof_carrying_governance_architecture.md`
- `docs/operators/assurance_claims_and_envelopes_guide.md`
- `docs/reviewers/attestations_and_replay_guide.md`
- `docs/reference/assurance_claim_taxonomy.md`
- `docs/maintenance/assurance_runbook.md`

To run the assurance pass:
`python -m sports_signal_bot.main assurance run-assurance-pass`

## Phase 63: Assurance Interoperability & Exchange
Adds cross-system assurance packages, notarized promotion envelopes, and quarantine-first federated registry evaluation rules.

### Phase 64: Capability Negotiation & Registry Notarization
Establishes a capability negotiation layer for external registries. Rather than blindly trusting imported assurance envelopes or federation profiles, registries can explicitly negotiate a safe, compatible subset of features (like supported claim families, proof formats, and replay modes). Includes portable spec bundles and snapshot notarization for auditable cross-system exchange.
