from typing import List, Dict, Any
from collections import deque
from sports_signal_bot.consistency_ledgers.contracts import (
    TribunalMeshPathRecord,
    TribunalMeshRouteOutcome,
    TribunalMeshEdgeRecord,
    TribunalMeshNodeRecord,
    DisputeTribunalMeshRecord,
    MeshPressureState,
)
from sports_signal_bot.consistency_ledgers.utils import generate_id


def enumerate_tribunal_mesh_paths(
    mesh: DisputeTribunalMeshRecord,
    start_node_ref: str,
    target_node_ref: str,
    edges: Dict[str, TribunalMeshEdgeRecord],
) -> List[List[str]]:
    """Simple BFS to find paths (sequences of edge IDs) between two nodes."""
    paths = []
    queue = deque([[start_node_ref]])
    edge_map = {}  # source_node -> List[edge_id]

    for edge_id in mesh.edge_refs:
        if edge_id in edges:
            edge = edges[edge_id]
            if edge.source_node_ref not in edge_map:
                edge_map[edge.source_node_ref] = []
            edge_map[edge.source_node_ref].append(edge_id)

    while queue:
        path = queue.popleft()
        current_node = path[-1]

        if current_node == target_node_ref and len(path) > 1:
            # Reconstruct edge path
            edge_path = []
            for i in range(len(path) - 1):
                src = path[i]
                dst = path[i + 1]
                for e_id in edge_map.get(src, []):
                    if edges[e_id].target_node_ref == dst:
                        edge_path.append(e_id)
                        break
            if edge_path:
                paths.append(edge_path)
            continue

        for next_edge_id in edge_map.get(current_node, []):
            next_node = edges[next_edge_id].target_node_ref
            if next_node not in path:
                queue.append(path + [next_node])

    return paths


def score_tribunal_mesh_paths(
    paths: List[List[str]],
    edges: Dict[str, TribunalMeshEdgeRecord],
    nodes: Dict[str, TribunalMeshNodeRecord],
) -> List[Dict[str, Any]]:
    """Scores paths based on currentness, caveat transfer, and node backlog."""
    scored_paths = []

    for path in paths:
        score = 100
        outcome = TribunalMeshRouteOutcome.BOUNDED_TRIBUNAL_ROUTE
        warnings = []

        for edge_id in path:
            edge = edges[edge_id]
            if edge.edge_status != "edge_current":
                score -= 20
                if outcome == TribunalMeshRouteOutcome.BOUNDED_TRIBUNAL_ROUTE:
                    outcome = TribunalMeshRouteOutcome.CAVEATED_TRIBUNAL_ROUTE
                warnings.append(f"Edge {edge_id} is not current.")
            if "no_safe" in edge.caveat_transfer_policy:
                outcome = TribunalMeshRouteOutcome.NO_SAFE_TRIBUNAL_ROUTE
                warnings.append(f"Edge {edge_id} involves no_safe conditions.")
                break  # NO_SAFE takes precedence

            target_node = nodes.get(edge.target_node_ref)

            if target_node and target_node.backlog_state in ["high", "critical"]:
                score -= 30
                if outcome in [
                    TribunalMeshRouteOutcome.BOUNDED_TRIBUNAL_ROUTE,
                    TribunalMeshRouteOutcome.CAVEATED_TRIBUNAL_ROUTE,
                ]:
                    outcome = TribunalMeshRouteOutcome.REVIEW_ONLY_TRIBUNAL_ROUTE
                warnings.append(f"Target node {target_node.node_id} has high backlog.")

        scored_paths.append(
            {"path": path, "score": score, "outcome": outcome, "warnings": warnings}
        )

    return sorted(scored_paths, key=lambda x: x["score"], reverse=True)


def apply_tribunal_mesh_constraints(
    scored_paths: List[Dict[str, Any]], pressure_state: MeshPressureState
) -> List[Dict[str, Any]]:
    """Applies global mesh pressure to further downgrade routes if necessary."""
    for p in scored_paths:
        if pressure_state == MeshPressureState.REVIEW_ONLY_BIAS:
            if p["outcome"] in [
                TribunalMeshRouteOutcome.BOUNDED_TRIBUNAL_ROUTE,
                TribunalMeshRouteOutcome.CAVEATED_TRIBUNAL_ROUTE,
            ]:
                p["outcome"] = TribunalMeshRouteOutcome.REVIEW_ONLY_TRIBUNAL_ROUTE
                p["warnings"].append(
                    "Downgraded to review_only due to mesh pressure bias."
                )
        elif pressure_state == MeshPressureState.SUPPRESS_NONCRITICAL_TRIBUNAL_PATHS:
            if p["outcome"] != TribunalMeshRouteOutcome.NO_SAFE_TRIBUNAL_ROUTE:
                p["outcome"] = TribunalMeshRouteOutcome.BLOCKED_TRIBUNAL_ROUTE
                p["warnings"].append(
                    "Blocked due to critical mesh pressure suppression."
                )
    return scored_paths


def select_tribunal_mesh_path(
    scored_paths: List[Dict[str, Any]], mesh_id: str
) -> TribunalMeshPathRecord:
    """Selects the best path or returns a blocked record if none exist."""
    if not scored_paths:
        return TribunalMeshPathRecord(
            path_id=generate_id("trib_path"),
            mesh_id=mesh_id,
            edge_sequence=[],
            outcome=TribunalMeshRouteOutcome.BLOCKED_TRIBUNAL_ROUTE,
            warnings=["No viable paths found."],
        )

    best_path = scored_paths[0]
    return TribunalMeshPathRecord(
        path_id=generate_id("trib_path"),
        mesh_id=mesh_id,
        edge_sequence=best_path["path"],
        outcome=best_path["outcome"],
        warnings=best_path["warnings"],
    )


def summarize_tribunal_mesh_route(record: TribunalMeshPathRecord) -> Dict[str, Any]:
    return {
        "path_id": record.path_id,
        "outcome": record.outcome.value,
        "edge_count": len(record.edge_sequence),
        "warnings": record.warnings,
    }
