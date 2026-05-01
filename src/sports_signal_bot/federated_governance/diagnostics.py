from typing import Dict, Any, List
from .contracts import ControlPlaneRecord, MeshTopologyRecord

def run_federated_diagnostics(planes: List[ControlPlaneRecord], topology: MeshTopologyRecord) -> Dict[str, Any]:
    return {
        "total_planes": len(planes),
        "suspended_planes": [p.plane_id for p in planes if not p.active_status],
        "topology_nodes": len(topology.nodes),
        "topology_edges": len(topology.edges)
    }
