from typing import List
from sports_signal_bot.ecosystem_resilience.contracts import (
    FederationTrustOverlayRecord,
    HubRoutingMeshRecord,
    MeshPressureOutcome,
    ResilienceControllerState
)

def run_overlay_mesh_watchers(overlay: FederationTrustOverlayRecord, mesh: HubRoutingMeshRecord, controller_state: ResilienceControllerState) -> str:
    if controller_state == ResilienceControllerState.DEGRADED_STATE:
        return "downgrade_overlay"
    if mesh.pressure_state in [MeshPressureOutcome.CRITICAL_PRESSURE, MeshPressureOutcome.HIGH_PRESSURE]:
        return "suppress_mesh_route"
    return "ok"

def invalidate_federated_projections(overlay: FederationTrustOverlayRecord) -> FederationTrustOverlayRecord:
    overlay.final_overlay_band = "highly_fragile"
    overlay.warnings.append("Invalidated by watcher.")
    return overlay

def explain_overlay_mesh_watcher_outcome(outcome: str) -> str:
    return f"Watcher triggered outcome: {outcome}"

def summarize_watcher_pressure(pressure_count: int) -> str:
    return f"Active watcher invalidations: {pressure_count}"
