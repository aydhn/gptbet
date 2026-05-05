from typing import List, Dict, Any
from sports_signal_bot.consistency_ledgers.contracts import (
    TribunalMeshNodeRecord,
    TribunalNodeFamily,
    DisputeTribunalMeshRecord
)
from sports_signal_bot.consistency_ledgers.utils import generate_id

def add_tribunal_mesh_node(
    mesh: DisputeTribunalMeshRecord,
    family: TribunalNodeFamily,
    hosted_tribunals: List[str],
    supported_cases: List[str]
) -> TribunalMeshNodeRecord:
    node = TribunalMeshNodeRecord(
        node_id=generate_id("trib_node"),
        node_family=family,
        hosted_tribunal_refs=hosted_tribunals,
        supported_case_families=supported_cases,
        currentness_state="current",
        backlog_state="low",
        node_status="active",
        warnings=[]
    )
    mesh.node_refs.append(node.node_id)
    return node
