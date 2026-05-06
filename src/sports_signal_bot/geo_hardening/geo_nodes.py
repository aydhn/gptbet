from typing import Dict, Any

def verify_geo_node_freshness(node: dict, current_time: int) -> bool:
    if node.get("last_seen", 0) < current_time - 60:
        return False
    return True

def compute_geo_edge_lag(source_time: int, target_time: int) -> int:
    return abs(source_time - target_time)

def detect_geo_mesh_gaps(nodes: list, edges: list) -> list:
    connected = set()
    for e in edges:
        connected.add(e.get("source"))
        connected.add(e.get("target"))

    gaps = []
    for n in nodes:
        if n.get("id") not in connected:
            gaps.append(n.get("id"))
    return gaps

def summarize_geo_mesh_edges(edges: list) -> Dict[str, Any]:
    return {"total": len(edges), "active": sum(1 for e in edges if e.get("status") == "active")}
