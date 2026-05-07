from .contracts import ReleaseGatingMeshRecord, GatingMeshGateRecord

def build_release_gating_mesh(mesh_id: str, family: str) -> ReleaseGatingMeshRecord:
    return ReleaseGatingMeshRecord(
        release_gating_mesh_id=mesh_id,
        mesh_family=family,
        mesh_status="mesh_verified"
    )

def add_gating_mesh_gate(mesh: ReleaseGatingMeshRecord, gate: GatingMeshGateRecord):
    mesh.gate_refs.append(gate.gate_id)

def evaluate_release_blockers(mesh: ReleaseGatingMeshRecord):
    pass

def resolve_release_gating_mesh(mesh: ReleaseGatingMeshRecord):
    pass

def summarize_release_gating_mesh(mesh: ReleaseGatingMeshRecord) -> dict:
    return {"id": mesh.release_gating_mesh_id, "status": mesh.mesh_status}
