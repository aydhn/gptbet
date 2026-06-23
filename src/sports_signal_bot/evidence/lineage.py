from typing import List, Dict, Any
from collections import deque
from sports_signal_bot.evidence.contracts import (
    EvidenceLineageNode,
    EvidenceLineageEdge,
    EvidenceGraphRecord,
)


def build_evidence_graph(graph_id: str) -> EvidenceGraphRecord:
    return EvidenceGraphRecord(graph_id=graph_id, nodes=[], edges=[])


def add_lineage_node(
    graph: EvidenceGraphRecord,
    node_id: str,
    node_type: str,
    payload_summary: Dict[str, Any],
    schema_version: str = "1.0",
):
    for node in graph.nodes:
        if node.node_id == node_id:
            return
    graph.nodes.append(
        EvidenceLineageNode(
            node_id=node_id,
            node_type=node_type,
            payload_summary=payload_summary,
            schema_version=schema_version,
        )
    )


def add_lineage_edge(
    graph: EvidenceGraphRecord,
    source_id: str,
    target_id: str,
    relation_type: str,
):
    for edge in graph.edges:
        if (
            edge.source_node_id == source_id
            and edge.target_node_id == target_id
            and edge.relation_type == relation_type
        ):
            return
    graph.edges.append(
        EvidenceLineageEdge(
            source_node_id=source_id,
            target_node_id=target_id,
            relation_type=relation_type,
        )
    )


def trace_decision_backwards(
    graph: EvidenceGraphRecord,
    start_node_id: str,
) -> List[EvidenceLineageNode]:
    # Basic BFS/DFS for traceability
    visited = set()
    queue = deque([start_node_id])
    trace = []

    node_map = {n.node_id: n for n in graph.nodes}

    while queue:
        current_id = queue.popleft()
        if current_id not in visited:
            visited.add(current_id)
            if current_id in node_map:
                trace.append(node_map[current_id])

            # Find sources (where current_id is the target)
            for edge in graph.edges:
                if edge.target_node_id == current_id:
                    queue.append(edge.source_node_id)

    return trace
