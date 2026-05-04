# Phase 82: Overlay Exchange Mesh & Route Governance

Phase 82 extends the system from simply forming trust overlay exchanges to actively managing their topologies as bounded "overlay meshes", while applying multi-tier governance to any derived routing hints, evaluating signals via consortium layers, and managing sovereign baselines through strict registries.

## Overlay Exchange Mesh

Overlay exchange meshes represent the topologies of trust propagation. Rather than functioning as open network paths, they transport scoped, caveated, and lineage-preserving projections. The propagation logic ensures that boundaries (like "review_only") and caveats are strictly preserved and decays applicability across edges to prevent excessive unearned confidence.

## Multi-Tier Route Governance

When an overlay projection or mesh route acts as a recommendation, it is passed through a Multi-Tier Route Governance layer. This explicit pipeline categorizes rules into ranks (e.g., local scope > sovereignty guard > treaty scope), ensuring that a lower-tier signal or convenience path can never override an upper-tier constraint (like a local deny).

## Benchmark Signal Consortiums

Multiple signal sources are gathered into Consortium Layers. These layers explicitly govern provenance, corroboration, freshness, and suppression. If a consortium cluster suffers from stale data, unverified provenance, or internal conflicts, it is suppressed—it cannot be used to strengthen a route governance hint.

## Sovereign Resilience Baseline Registries

Resilience baselines are maintained inside formal Registries tracking their currentness, applicability, and supersession state. A baseline registry ensures that only valid, non-stale baselines are utilized to provide governance hints. If a baseline is superseded, its successor is linked and hints generated from the obsolete version are immediately downgraded or caveated.

## Integration
Phase 82 is integrated with previous phases:
- **Trust Exchange Scale (Phase 81):** Overlay meshes provide the structured paths for scalable trust exchanges.
- **Ecosystem Resilience (Phase 80):** Multi-tier route governance explicitly includes resilience pressure tiers.
- **Federation Ecosystem (Phase 79):** Hub mesh and federation ecosystems provide the context for consortium signals.
- **Registry Conformance (Phase 78):** Route governance tier inputs utilize registry conformance evidence.

## Important Commands
```bash
python -m sports_signal_bot.main overlay-mesh-governance run-overlay-mesh-governance-pass
python -m sports_signal_bot.main overlay-mesh-governance preview-overlay-meshes
python -m sports_signal_bot.main overlay-mesh-governance preview-route-tier-decisions
python -m sports_signal_bot.main overlay-mesh-governance preview-signal-consortiums
python -m sports_signal_bot.main overlay-mesh-governance preview-baseline-registries
python -m sports_signal_bot.main overlay-mesh-governance preview-overlay-mesh-governance-health
python -m sports_signal_bot.main overlay-mesh-governance list-overlay-mesh-governance-strategies
```

## Guardrails
- **Caveat Preservation:** Overlay mesh propagation inherently preserves caveats. Dropping caveats halts propagation.
- **Tier Precedence:** Lower-tier hints (e.g., quality improvements) can never override upper-tier blocks (e.g., sovereignty limits).
- **Consortium Suppression:** Stale or conflicting consortium signals cannot strengthen governance hints.
- **Stale Currentness:** A baseline registry pointer that is stale or superseded is explicitly downgraded from strong support to a review-only or caveated status.
