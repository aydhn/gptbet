# Operator Guide: Overlays, Meshes, Signals, and Controllers

## Trust Overlays
Overlays are generated per pipeline pass. Operators can observe the `TrustOverlayBand` (e.g. `bounded_reliable`). Check penalties if scores are suppressed.

## Hub Routing Meshes
Mesh outcomes provide guidance on exchange topology. If a path returns `degraded_fallback_path` or `blocked_path`, it implies edge health degradation, likely triggered by a resilience controller.

## Marketplace Signals
Operators can use `BaselineMarketplaceSignalRecord` to check corroboration hints. Suppressed signals mean data is stale or irrelevantly caveated.

## Ecosystem Controllers
Controllers maintain states like `MONITORING_NORMAL` or `DEGRADED_STATE`. When degraded, visibility is strictly suppressed.

## CLI Commands
- `preview-trust-overlays`
- `preview-hub-routing-meshes`
- `preview-marketplace-signals`
- `preview-resilience-controllers`
