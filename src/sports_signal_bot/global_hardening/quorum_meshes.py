from typing import List, Optional
from .contracts import (
    RegionalQuorumMeshRecord,
    QuorumMeshNodeRecord,
    QuorumMeshEdgeRecord,
    QuorumMeshPathRecord,
    RegionalQuorumMeshWarningRecord,
    QuorumMeshLagRecord,
    QuorumMeshResidueRecord,
)

def build_regional_quorum_mesh(mesh_id: str, family: str) -> RegionalQuorumMeshRecord:
    return RegionalQuorumMeshRecord(
        regional_quorum_mesh_id=mesh_id,
        mesh_family=family,
        mesh_status="mesh_verified"
    )

def add_quorum_mesh_node(mesh: RegionalQuorumMeshRecord, node: QuorumMeshNodeRecord) -> None:
    if node.status == "stale":
        mesh.warnings.append(RegionalQuorumMeshWarningRecord(warning_id=f"warn_{node.node_id}", message="stale regional support rejected"))
        mesh.mesh_status = "mesh_blocked"
    mesh.node_refs.append(node)

def add_quorum_mesh_edge(mesh: RegionalQuorumMeshRecord, edge: QuorumMeshEdgeRecord) -> None:
    mesh.edge_refs.append(edge)

def verify_quorum_mesh_path(mesh: RegionalQuorumMeshRecord, path: QuorumMeshPathRecord) -> None:
    mesh.path_refs.append(path)

def summarize_regional_quorum_mesh(mesh: RegionalQuorumMeshRecord) -> dict:
    return {
        "id": mesh.regional_quorum_mesh_id,
        "status": mesh.mesh_status,
        "nodes_count": len(mesh.node_refs),
        "warnings": len(mesh.warnings)
    }

def verify_quorum_mesh_node_freshness(node: QuorumMeshNodeRecord) -> bool:
    return node.status != "stale"

def detect_quorum_mesh_gaps(mesh: RegionalQuorumMeshRecord) -> List[str]:
    return [node.node_id for node in mesh.node_refs if node.status == "gapped"]
