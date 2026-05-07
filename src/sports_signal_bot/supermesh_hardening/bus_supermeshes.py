from typing import List
from .contracts import FederationBusSupermeshRecord, SupermeshNodeRecord, SupermeshEdgeRecord

def build_federation_bus_supermesh(mesh_id: str, family: str) -> FederationBusSupermeshRecord:
    return FederationBusSupermeshRecord(
        federation_bus_supermesh_id=mesh_id,
        supermesh_family=family,
        supermesh_status="supermesh_verified"
    )

def add_supermesh_node(mesh: FederationBusSupermeshRecord, node: SupermeshNodeRecord):
    mesh.node_refs.append(node.node_id)
    if node.is_ownerless and node.is_critical:
        mesh.supermesh_status = "supermesh_blocked"

def add_supermesh_edge(mesh: FederationBusSupermeshRecord, edge: SupermeshEdgeRecord):
    mesh.edge_refs.append(edge.edge_id)
    if edge.is_stale:
        mesh.supermesh_status = "supermesh_blocked"

def verify_federation_bus_supermesh(mesh: FederationBusSupermeshRecord) -> str:
    return mesh.supermesh_status

def summarize_federation_bus_supermesh(mesh: FederationBusSupermeshRecord) -> dict:
    return {
        "id": mesh.federation_bus_supermesh_id,
        "family": mesh.supermesh_family,
        "status": mesh.supermesh_status,
        "node_count": len(mesh.node_refs),
        "edge_count": len(mesh.edge_refs)
    }
