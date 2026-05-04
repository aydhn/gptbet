from typing import List
from .contracts import (
    AssuranceExchangeMeshRecord,
    AssuranceMeshNodeRecord,
    AssuranceMeshEdgeRecord,
    AssuranceMeshHealthRecord,
    AssuranceMeshPathRecord,
    AssuranceMeshPressureRecord,
    AssuranceMeshPressureState,
    AssuranceMeshPathOutcome,
    AssuranceMeshEdgeStatus
)

def build_assurance_exchange_mesh(mesh_id: str, family: str) -> AssuranceExchangeMeshRecord:
    return AssuranceExchangeMeshRecord(
        assurance_mesh_id=mesh_id,
        mesh_family=family,
        routing_policy_ref="default_routing_policy",
        pressure_policy_ref="default_pressure_policy",
        degradation_policy_ref="default_degradation_policy",
        health_status="initializing"
    )

def add_assurance_mesh_node(mesh: AssuranceExchangeMeshRecord, node: AssuranceMeshNodeRecord) -> AssuranceExchangeMeshRecord:
    mesh.node_refs.append(node.node_id)
    return mesh

def add_assurance_mesh_edge(mesh: AssuranceExchangeMeshRecord, edge: AssuranceMeshEdgeRecord) -> AssuranceExchangeMeshRecord:
    mesh.edge_refs.append(edge.edge_id)
    return mesh

def validate_assurance_mesh_edge(edge: AssuranceMeshEdgeRecord) -> bool:
    return edge.edge_status not in [AssuranceMeshEdgeStatus.edge_blocked, AssuranceMeshEdgeStatus.edge_expired, AssuranceMeshEdgeStatus.edge_superseded]

def summarize_assurance_mesh_health(mesh: AssuranceExchangeMeshRecord, edges: List[AssuranceMeshEdgeRecord]) -> AssuranceMeshHealthRecord:
    valid_edges = [e for e in edges if validate_assurance_mesh_edge(e)]
    is_healthy = len(valid_edges) == len(edges) and len(edges) > 0
    return AssuranceMeshHealthRecord(
        is_healthy=is_healthy,
        score=len(valid_edges) / len(edges) if edges else 0.0,
        health_issues=["Some edges are invalid"] if not is_healthy else []
    )

def enumerate_assurance_mesh_paths(mesh: AssuranceExchangeMeshRecord, edges: List[AssuranceMeshEdgeRecord]) -> List[AssuranceMeshPathRecord]:
    # Placeholder for path enumeration
    paths = []
    if edges:
        paths.append(AssuranceMeshPathRecord(
            path_id=f"path_{mesh.assurance_mesh_id}_1",
            node_sequence=[edges[0].source_node_ref, edges[0].target_node_ref],
            edge_sequence=[edges[0].edge_id],
            outcome=AssuranceMeshPathOutcome.bounded_assurance_path
        ))
    return paths

def compute_assurance_mesh_pressure(mesh: AssuranceExchangeMeshRecord, edges: List[AssuranceMeshEdgeRecord]) -> AssuranceMeshPressureRecord:
    stale_edges = len([e for e in edges if e.currentness_state != "current"])
    backpressured = len([e for e in edges if e.edge_status == AssuranceMeshEdgeStatus.edge_backpressured])

    total = len(edges) if edges else 1

    return AssuranceMeshPressureRecord(
        pressure_state=AssuranceMeshPressureState.low if backpressured == 0 else AssuranceMeshPressureState.moderate,
        stale_packet_density=stale_edges / total,
        backpressured_edge_ratio=backpressured / total,
        degraded_node_ratio=0.0,
        narrative_refresh_backlog=0,
        alert_density=0.0,
        no_safe_visibility_burden=0.0,
        audience_projection_mismatch=0.0,
        caveat_heavy_packet_ratio=0.0
    )

def downgrade_assurance_paths_due_to_pressure(paths: List[AssuranceMeshPathRecord], pressure: AssuranceMeshPressureRecord) -> List[AssuranceMeshPathRecord]:
    if pressure.pressure_state in [AssuranceMeshPressureState.high, AssuranceMeshPressureState.critical]:
        for path in paths:
            if path.outcome == AssuranceMeshPathOutcome.bounded_assurance_path:
                path.outcome = AssuranceMeshPathOutcome.review_only_assurance_path
    return paths
