import uuid
from .contracts import BaselineFederationMeshRecord, BaselineMeshEdgeRecord

def build_baseline_federation_mesh(family: str) -> BaselineFederationMeshRecord:
    return BaselineFederationMeshRecord(
        baseline_mesh_id=f"mesh_{uuid.uuid4()}",
        mesh_family=family,
        currentness_policy_ref="strict",
        applicability_policy_ref="strict",
        supersession_policy_ref="visible",
        health_status="healthy"
    )

def add_baseline_mesh_edge(mesh: BaselineFederationMeshRecord, source: str, target: str) -> BaselineMeshEdgeRecord:
    edge = BaselineMeshEdgeRecord(
        edge_id=f"edge_{uuid.uuid4()}",
        source_baseline_node_ref=source,
        target_baseline_node_ref=target,
        applicability_constraints="none",
        currentness_state="current",
        drift_state="none",
        edge_status="edge_current"
    )
    mesh.edge_refs.append(edge.edge_id)
    return edge

def project_baseline_across_mesh(edge: BaselineMeshEdgeRecord) -> str:
    if edge.currentness_state == "stale":
        return "projected_caveated_hint"
    if edge.drift_state != "none":
        return "projected_review_only_hint"
    return "projected_bounded_hint"

def summarize_baseline_mesh_health(mesh: BaselineFederationMeshRecord) -> dict:
    return {
        "id": mesh.baseline_mesh_id,
        "health": mesh.health_status,
        "edge_count": len(mesh.edge_refs)
    }
