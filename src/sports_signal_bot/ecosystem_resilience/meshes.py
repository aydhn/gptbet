from typing import List
from sports_signal_bot.ecosystem_resilience.contracts import (
    HubRoutingMeshRecord,
    MeshPressureOutcome,
    MeshEdgeRecord
)

def build_hub_routing_mesh(
    mesh_id: str,
    mesh_family: str,
    hub_refs: List[str],
    edge_refs: List[str],
    routing_policy_ref: str,
    pressure_state: MeshPressureOutcome = MeshPressureOutcome.LOW_PRESSURE,
    degradation_state: str = "healthy",
    health_status: str = "ok"
) -> HubRoutingMeshRecord:
    return HubRoutingMeshRecord(
        mesh_id=mesh_id,
        mesh_family=mesh_family,
        hub_refs=hub_refs,
        edge_refs=edge_refs,
        routing_policy_ref=routing_policy_ref,
        pressure_state=pressure_state,
        degradation_state=degradation_state,
        health_status=health_status,
        warnings=[]
    )

def compute_mesh_health(mesh: HubRoutingMeshRecord, edges: List[MeshEdgeRecord]) -> str:
    degraded_count = sum(1 for e in edges if e.edge_status in ["edge_degraded", "edge_blocked", "edge_expired"])
    if degraded_count > len(edges) / 2:
        return "critical"
    if degraded_count > 0:
        return "degraded"
    if mesh.pressure_state in [MeshPressureOutcome.HIGH_PRESSURE, MeshPressureOutcome.CRITICAL_PRESSURE]:
        return "pressured"
    return "healthy"

def summarize_mesh_state(mesh: HubRoutingMeshRecord) -> str:
    return f"Mesh {mesh.mesh_id} ({mesh.mesh_family}): Health={mesh.health_status}, Pressure={mesh.pressure_state.value}"
