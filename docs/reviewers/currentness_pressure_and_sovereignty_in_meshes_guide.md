# Reviewer Guide: Currentness, Pressure, and Sovereignty in Meshes

## Mesh Path Guardrails

Reviewers must verify:
1. **Sovereignty Overrides:** If `sovereignty_deny` is triggered on a trust overlay edge, no mesh routing component should mask it.
2. **Currentness:** Paths operating on superseded or stale edges must produce `edge_superseded` or `edge_expired` and yield block or review-only mesh paths.
3. **Queue Pressure:** Hubs under `HIGH_PRESSURE` should see their preferred paths immediately transition to `degraded_fallback_path`.

The mesh model does not widen scope; it operates strictly inside existing bounding box limits.
