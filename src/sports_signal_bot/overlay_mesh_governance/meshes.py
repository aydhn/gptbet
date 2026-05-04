from typing import List, Dict, Any, Optional
from datetime import datetime
from sports_signal_bot.overlay_mesh_governance.contracts import (
    OverlayExchangeMeshRecord,
    OverlayMeshNodeRecord,
    OverlayMeshEdgeRecord,
    OverlayMeshHealthRecord,
    OverlayMeshWarningRecord,
    OverlayMeshCaveatRecord,
    OverlayMeshConstraintRecord,
    OverlayMeshCurrentnessRecord
)

def build_overlay_exchange_mesh(
    mesh_id: str,
    mesh_family: str,
    propagation_policy_ref: str,
    currentness_policy_ref: str,
    degradation_policy_ref: str
) -> OverlayExchangeMeshRecord:
    return OverlayExchangeMeshRecord(
        overlay_mesh_id=mesh_id,
        mesh_family=mesh_family,
        node_refs=[],
        edge_refs=[],
        propagation_policy_ref=propagation_policy_ref,
        currentness_policy_ref=currentness_policy_ref,
        degradation_policy_ref=degradation_policy_ref,
        health_status=OverlayMeshHealthRecord(status="healthy", details={})
    )

def add_overlay_mesh_node(mesh: OverlayExchangeMeshRecord, node: OverlayMeshNodeRecord) -> OverlayExchangeMeshRecord:
    if node.node_id not in mesh.node_refs:
        mesh.node_refs.append(node.node_id)
    return mesh

def add_overlay_mesh_edge(mesh: OverlayExchangeMeshRecord, edge: OverlayMeshEdgeRecord) -> OverlayExchangeMeshRecord:
    if edge.edge_id not in mesh.edge_refs:
        mesh.edge_refs.append(edge.edge_id)
    return mesh

def validate_overlay_mesh_edge(edge: OverlayMeshEdgeRecord) -> bool:
    if edge.edge_status in ["edge_expired", "edge_superseded", "edge_blocked"]:
        return False
    if edge.currentness_state.currentness_state in ["stale", "expired"]:
        return False
    return True

def summarize_overlay_mesh_health(mesh: OverlayExchangeMeshRecord) -> OverlayMeshHealthRecord:
    # A real implementation would check all nodes and edges
    if mesh.warnings:
        mesh.health_status.status = "degraded"
        mesh.health_status.details["warnings_count"] = str(len(mesh.warnings))
    else:
        mesh.health_status.status = "healthy"
    return mesh.health_status
