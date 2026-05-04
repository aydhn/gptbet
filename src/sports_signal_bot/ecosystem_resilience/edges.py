from typing import List
from sports_signal_bot.ecosystem_resilience.contracts import MeshEdgeRecord, MeshEdgeStatus

def add_mesh_edge(
    edge_id: str,
    source_hub: str,
    target_hub: str,
    supported_exchange_scopes: List[str],
    sovereignty_constraints: List[str],
    status: MeshEdgeStatus = MeshEdgeStatus.EDGE_ACTIVE
) -> MeshEdgeRecord:
    return MeshEdgeRecord(
        edge_id=edge_id,
        source_hub_ref=source_hub,
        target_hub_ref=target_hub,
        supported_exchange_scopes=supported_exchange_scopes,
        supported_attestation_families=["baseline"],
        sovereignty_constraints=sovereignty_constraints,
        currentness_state="current",
        pressure_state="low",
        edge_status=status,
        warnings=[]
    )

def validate_mesh_edge(edge: MeshEdgeRecord) -> bool:
    if edge.edge_status in [MeshEdgeStatus.EDGE_BLOCKED, MeshEdgeStatus.EDGE_EXPIRED, MeshEdgeStatus.EDGE_SUPERSEDED]:
        return False
    return True
