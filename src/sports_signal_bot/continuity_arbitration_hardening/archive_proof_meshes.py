import uuid
from typing import List, Dict, Any
from datetime import datetime, timezone
from .contracts import (
    ArchiveProofMeshRecord,
    ProofMeshNodeRecord,
    ProofMeshReplayRecord,
    ProofMeshLineageRecord
)

def build_archive_proof_mesh(mesh_family: str, nodes: List[ProofMeshNodeRecord], replays: List[ProofMeshReplayRecord]) -> ArchiveProofMeshRecord:
    all_replays_successful = all(r.replay_successful for r in replays) if replays else False
    status = "mesh_verified"
    warnings = []

    if not all_replays_successful:
        status = "mesh_broken"
        warnings.append("Replay support missing or failed.")

    return ArchiveProofMeshRecord(
        archive_proof_mesh_id=str(uuid.uuid4()),
        mesh_family=mesh_family,
        node_refs=[n.node_id for n in nodes],
        edge_refs=[],
        path_refs=[],
        hash_refs=[],
        lineage_refs=[],
        replay_refs=[r.replay_id for r in replays],
        residue_refs=[],
        mesh_status=status,
        warnings=warnings
    )

def add_archive_proof_node(node_family: str) -> ProofMeshNodeRecord:
    return ProofMeshNodeRecord(
        node_id=str(uuid.uuid4()),
        node_family=node_family
    )

def summarize_archive_proof_mesh(mesh: ArchiveProofMeshRecord) -> Dict[str, Any]:
    return {
        "mesh_id": mesh.archive_proof_mesh_id,
        "status": mesh.mesh_status,
        "node_count": len(mesh.node_refs),
        "replay_count": len(mesh.replay_refs),
        "warnings": mesh.warnings
    }
