# Coherence Scorer Federations & Sovereign Governance Alignment Compilers Architecture

## Purpose
This architecture defines the mechanisms for federating coherence scorers, adjudicating context disputes via tribunals, facilitating bounded evidence exchange via brokers, and ultimately compiling sovereign governance alignment outputs. It bridges the gap between raw coherence scores and aggregated, explainable governance alignment without introducing centralized authority or overriding local sovereignty.

## Why Mature Assurance Surfaces Need Dispute Tribunals and Alignment Compilers
As assurance surfaces expand across contexts, simple raw coherence scores are insufficient. Competing or conflicting context bundles require structured dispute resolution (tribunals). Exchanging trace evidence across boundaries requires strict bounding (broker exchanges). Finally, compiling these disparate signals into a unified but non-authoritative alignment view ensures that executives and auditors see a cohesive picture that still retains critical nuances like staleness, missing evidence, and sovereignty caveats.

## Core Components

### Coherence Scorer Federation
Combines multiple coherence scores while preserving penalties, caps, and currentness. A stale member strictly degrades the federation's overall currentness and agreement band.

### Context Dispute Tribunal
Handles conflicts between context bundles (e.g., stale vs. refresh cases). Employs quorums and panels to reach decisions (e.g., applying caps or requiring refresh), ensuring that unresolved conflicts degrade context to `review_only`.

### Evidence Broker Exchange
Facilitates the sharing of evidence between domains. It strictly enforces boundaries, preventing scope widening. Incomplete evidence or stale requests force the exchange route to be degraded or caveated.

### Sovereign Governance Alignment Compiler
The capstone component that takes inputs from federations, tribunals, and exchanges. It runs specific alignment passes (e.g., `no_safe_visibility_pass`, `sovereignty_preservation_pass`) and applies penalties to derive a final alignment band (e.g., `strong_bounded_alignment` or `review_only_alignment`).

## Key Principles
1. **Federated Coherence Does Not Imply Authority**: The combined output of a federation is advisory and non-authoritative.
2. **Tribunals Cannot Override Sovereignty**: Decisions from tribunals respect local `deny` signals.
3. **Broker Exchanges Remain Bounded**: Evidence shared between brokers must retain its original caveats and audience scope.
4. **Currentness and Evidence Sufficiency Rule**: Stale inputs or missing evidence critically cap the final alignment band, often dropping it to `review_only_alignment`.
5. **No-Safe Visibility is Load-Bearing**: If no-safe hints are hidden or obscured during any step (federation, tribunal, exchange, or compilation), the alignment is severely penalized.

## Integration Path
These components integrate heavily with Phase 96 (Coherence Scoring) by acting as a consumer of individual coherence scores and context assemblies. The alignment compiler outputs then feed into assurance dashboards and narrative compilers (Phase 91/92). Future phases will expand on federation networks and alignment compiler exchanges at scale.
