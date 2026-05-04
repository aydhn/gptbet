from typing import List, Dict, Any
from .contracts import (
    SovereignGovernanceEvidenceAtlasRecord,
    EvidenceAtlasNodeRecord,
    EvidenceAtlasEdgeRecord,
    EvidenceAtlasHealthRecord,
    EvidenceAtlasViewRecord,
    EvidenceAtlasQueryRecord,
    EvidenceAtlasMatchRecord
)

def build_governance_evidence_atlas(atlas_id: str, family: str) -> SovereignGovernanceEvidenceAtlasRecord:
    return SovereignGovernanceEvidenceAtlasRecord(
        evidence_atlas_id=atlas_id,
        atlas_family=family,
        freshness_policy_ref="default_freshness_policy",
        health_status="initializing"
    )

def add_evidence_atlas_node(atlas: SovereignGovernanceEvidenceAtlasRecord, node: EvidenceAtlasNodeRecord) -> SovereignGovernanceEvidenceAtlasRecord:
    atlas.node_refs.append(node.atlas_node_id)
    return atlas

def add_evidence_atlas_edge(atlas: SovereignGovernanceEvidenceAtlasRecord, edge: EvidenceAtlasEdgeRecord) -> SovereignGovernanceEvidenceAtlasRecord:
    atlas.edge_refs.append(edge.atlas_edge_id)
    return atlas

def validate_evidence_atlas_integrity(atlas: SovereignGovernanceEvidenceAtlasRecord, nodes: List[EvidenceAtlasNodeRecord], edges: List[EvidenceAtlasEdgeRecord]) -> bool:
    node_ids = {n.atlas_node_id for n in nodes}
    for edge in edges:
        if edge.source_node_ref not in node_ids or edge.target_node_ref not in node_ids:
            return False
    return True

def summarize_evidence_atlas_health(atlas: SovereignGovernanceEvidenceAtlasRecord, nodes: List[EvidenceAtlasNodeRecord], edges: List[EvidenceAtlasEdgeRecord]) -> EvidenceAtlasHealthRecord:
    stale_nodes = len([n for n in nodes if n.currentness_state != "current"])
    stale_edges = len([e for e in edges if e.freshness_state != "fresh"])

    is_healthy = stale_nodes == 0 and stale_edges == 0
    score = 1.0 if is_healthy else max(0.0, 1.0 - (stale_nodes + stale_edges) * 0.1)

    return EvidenceAtlasHealthRecord(
        is_healthy=is_healthy,
        score=score,
        stale_node_count=stale_nodes,
        stale_edge_count=stale_edges
    )

def build_evidence_atlas_view(view_id: str, family: str, nodes: List[EvidenceAtlasNodeRecord]) -> EvidenceAtlasViewRecord:
    return EvidenceAtlasViewRecord(
        view_id=view_id,
        view_family=family,
        node_refs=[n.atlas_node_id for n in nodes]
    )

def execute_evidence_atlas_query(atlas: SovereignGovernanceEvidenceAtlasRecord, query_family: str, params: Dict[str, Any], nodes: List[EvidenceAtlasNodeRecord]) -> EvidenceAtlasQueryRecord:
    # Placeholder for actual query logic
    has_stale = any(n.currentness_state != "current" for n in nodes)
    has_caveats = any(n.caveat_state != "none" for n in nodes)

    return EvidenceAtlasQueryRecord(
        query_id=f"query_{query_family}_{len(params)}",
        query_family=query_family,
        query_params=params,
        results_caveated=has_caveats,
        results_stale=has_stale
    )

def summarize_atlas_query_result(query_result: EvidenceAtlasQueryRecord) -> str:
    parts = [f"Query {query_result.query_id} ({query_result.query_family})"]
    if query_result.results_stale:
        parts.append("WARNING: Results include stale data.")
    if query_result.results_caveated:
        parts.append("NOTE: Results are caveated.")
    return " - ".join(parts)

def preserve_caveats_in_atlas_results(nodes: List[EvidenceAtlasNodeRecord]) -> List[str]:
    caveats = []
    for node in nodes:
        if node.caveat_state and node.caveat_state != "none":
            caveats.append(f"Node {node.atlas_node_id}: {node.caveat_state}")
    return caveats

def enforce_phase92_currentness_caveat_scope_rules() -> str:
    return "Enforcing Phase 92 currentness, caveat, and scope rules."

def cap_phase92_outputs_due_to_staleness_or_evidence_gaps() -> str:
    return "Capping Phase 92 outputs due to staleness or evidence gaps."

def enforce_sovereignty_across_phase92() -> str:
    return "Enforcing sovereignty rules across Phase 92."
