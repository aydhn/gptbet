from .contracts import *

def build_recovery_quorum_mesh(mesh_id: str, family: RecoveryMeshFamily) -> RecoveryQuorumMeshRecord:
    return RecoveryQuorumMeshRecord(
        recovery_mesh_id=mesh_id,
        mesh_family=family
    )

def add_recovery_mesh_node(mesh: RecoveryQuorumMeshRecord, node: RecoveryMeshNodeRecord):
    mesh.node_refs.append(node)

def add_recovery_mesh_edge(mesh: RecoveryQuorumMeshRecord, edge: RecoveryMeshEdgeRecord):
    # Rule: degraded edge cannot produce clean bounded hint
    if edge.edge_status == RecoveryEdgeStatus.edge_degraded:
        mesh.warnings.append(f"Degraded edge {edge.edge_id} restricts mesh to caveated/review-only outputs.")
    mesh.edge_refs.append(edge)

def compute_recovery_mesh_pressure(mesh: RecoveryQuorumMeshRecord) -> RecoveryMeshPressureRecord:
    degraded_count = sum(1 for e in mesh.edge_refs if e.edge_status == RecoveryEdgeStatus.edge_degraded)
    ratio = degraded_count / max(1, len(mesh.edge_refs))

    pressure = RecoveryMeshPressureRecord(degraded_edge_ratio=ratio)
    if ratio > 0.5:
        pressure.pressure_state = RecoveryPressureState.critical
    elif ratio > 0.2:
        pressure.pressure_state = RecoveryPressureState.high
    else:
        pressure.pressure_state = RecoveryPressureState.low

    mesh.pressure = pressure
    return pressure
