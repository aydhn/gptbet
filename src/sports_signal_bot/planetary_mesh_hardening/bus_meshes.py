from typing import List
from .contracts import PlanetaryBusMeshRecord, MeshStatus

def build_planetary_bus_mesh(mesh_id: str, family: str) -> PlanetaryBusMeshRecord:
    return PlanetaryBusMeshRecord(
        planetary_bus_mesh_id=mesh_id,
        mesh_family=family,
        node_refs=[],
        edge_refs=[],
        path_refs=[],
        lag_refs=[],
        packet_refs=[],
        continuity_refs=[],
        residue_refs=[],
        mesh_status=MeshStatus.MESH_REVIEW_ONLY,
        warnings=[]
    )

def add_bus_mesh_node(mesh: PlanetaryBusMeshRecord, node_id: str):
    mesh.node_refs.append(node_id)

def add_bus_mesh_edge(mesh: PlanetaryBusMeshRecord, edge_id: str):
    mesh.edge_refs.append(edge_id)

def verify_planetary_bus_mesh(mesh: PlanetaryBusMeshRecord):
    # Rule: stale packet strong transport support veremez
    if "stale" in mesh.packet_refs:
        mesh.mesh_status = MeshStatus.MESH_CAVEATED
        mesh.warnings.append("stale packet support rejected")
    else:
        mesh.mesh_status = MeshStatus.MESH_VERIFIED

    if "lagged" in mesh.edge_refs:
        mesh.mesh_status = MeshStatus.MESH_CAVEATED

def summarize_planetary_bus_mesh(mesh: PlanetaryBusMeshRecord) -> dict:
    return {
        "mesh_id": mesh.planetary_bus_mesh_id,
        "status": mesh.mesh_status.value
    }
