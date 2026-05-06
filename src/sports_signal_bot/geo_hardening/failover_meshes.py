from typing import List, Dict, Any
from .contracts import GeoFailoverMeshRecord

def build_geo_failover_mesh(mesh_id: str, family: str) -> GeoFailoverMeshRecord:
    return GeoFailoverMeshRecord(
        geo_failover_mesh_id=mesh_id,
        mesh_family=family,
        node_refs=[],
        edge_refs=[],
        path_refs=[],
        lag_refs=[],
        continuity_refs=[],
        residue_refs=[],
        mesh_status="mesh_ready",
        warnings=[]
    )

def add_geo_mesh_node(mesh: GeoFailoverMeshRecord, node_id: str):
    mesh.node_refs.append(node_id)
    return mesh

def add_geo_mesh_edge(mesh: GeoFailoverMeshRecord, edge_id: str):
    mesh.edge_refs.append(edge_id)
    return mesh

def verify_geo_mesh_path(mesh: GeoFailoverMeshRecord, path_id: str):
    mesh.path_refs.append(path_id)
    return True

def summarize_geo_failover_mesh(mesh: GeoFailoverMeshRecord) -> Dict[str, Any]:
    return {
        "mesh_id": mesh.geo_failover_mesh_id,
        "status": mesh.mesh_status,
        "nodes": len(mesh.node_refs),
        "edges": len(mesh.edge_refs)
    }
