from typing import List
from .contracts import SupermeshNodeRecord, SupermeshEdgeRecord, SupermeshLagRecord

def verify_supermesh_node_freshness(node: SupermeshNodeRecord) -> bool:
    # A node is considered fresh if it's not explicitly stale in its details,
    # and has an owner if critical.
    if node.is_critical and node.is_ownerless:
        return False
    return not node.details.get("stale", False)

def compute_supermesh_edge_lag(edge: SupermeshEdgeRecord) -> float:
    return float(edge.details.get("lag", 0.0))

def detect_supermesh_gaps(nodes: List[SupermeshNodeRecord], edges: List[SupermeshEdgeRecord]) -> List[str]:
    gaps = []
    for node in nodes:
        if node.is_critical and node.is_ownerless:
            gaps.append(f"Gap: Ownerless critical node {node.node_id}")
    for edge in edges:
        if edge.is_stale:
            gaps.append(f"Gap: Stale edge {edge.edge_id}")
    return gaps

def summarize_supermesh_edges(edges: List[SupermeshEdgeRecord]) -> dict:
    return {
        "total_edges": len(edges),
        "stale_edges": sum(1 for e in edges if e.is_stale),
        "fallback_edges": sum(1 for e in edges if e.is_fallback)
    }
