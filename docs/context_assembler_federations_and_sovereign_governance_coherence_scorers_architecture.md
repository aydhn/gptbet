# Context Assembler Federations and Sovereign Governance Coherence Scorers Architecture

## Why mature assurance surfaces need context federations and coherence scorers
As the governance assurance surface expands across regions and independent namespaces, simply collecting context is insufficient. We need bounded federations to align context outputs without establishing a central authority. The coherence scorers ensure that contradictions (e.g., between fresh proofs and stale signals) are detected, explicitly penalized, and reflected in non-authoritative coherence bands, ensuring safety boundaries are never overridden.

## Context Assembler Federation Model
Federates multiple context bundles, preserving the intersection of their caveats and reducing the overall output to the lowest common currentness state. It relies on the `FederatedContextNodeRecord` to evaluate each member.

## Freshness Dispute Chamber Model
Replaces simplistic "first in, wins" logic with formal dispute cases (`FreshnessDisputeCaseRecord`). It bounds freshness, enforces decay policies, and forces downgrade to `review_only` if sufficient `refresh_evidence` is not provided.

## Trace Evidence Broker Model
Routes requests to trace listings without expanding original scope. Bounded matching ensures that missing evidence or conflicting caveats naturally cap the route at a degraded level.

## Sovereign Governance Coherence Scorer Model
Aggregates the health of the previous structures. Evaluates multiple passes (Trace Integrity, Sovereignty Preservation, No-Safe Visibility) and assigns a final non-authoritative band (`strong_bounded_coherence`, `review_only_coherence`, etc.).

## Integration
- Integrates deeply with Phase 95's Context Assembly layer and Phase 94's Trace Routing structures.
- Future extension paths will scale these models to mesh topologies handling global cross-region disputes.
