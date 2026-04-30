from typing import List, Dict, Any, Tuple
import uuid
from .contracts import (
    CrossCohortConflictRecord, CrossFamilyInteractionRecord, ConflictSeverity,
    InteractionNodeRecord, InteractionEdgeRecord, ExpansionInteractionGraphRecord
)

def detect_cross_cohort_conflicts(active_cohorts: List[Dict[str, Any]]) -> List[CrossCohortConflictRecord]:
    """Detects conflicts between multiple active cohorts (e.g. concurrent growth in same family)."""
    conflicts = []

    # Example logic: group by family
    family_map = {}
    for c in active_cohorts:
        fam = c.get('cohort_family')
        if fam:
            family_map.setdefault(fam, []).append(c['cohort_id'])

    for fam, c_ids in family_map.items():
        if len(c_ids) > 1:
            severity = ConflictSeverity.MEDIUM if len(c_ids) == 2 else ConflictSeverity.HIGH
            if len(c_ids) >= 4:
                severity = ConflictSeverity.CRITICAL

            conflicts.append(CrossCohortConflictRecord(
                conflict_id=f"conf_{uuid.uuid4().hex[:8]}",
                conflict_family="same_family_concurrent_growth_conflict",
                involved_cohorts=c_ids,
                severity=severity,
                description=f"Multiple cohorts ({len(c_ids)}) active simultaneously in family '{fam}'."
            ))

    # Mocking alias vs reconciliation
    alias_cohorts = [c['cohort_id'] for c in active_cohorts if c.get('target_component_family') == 'alias_memory']
    recon_cohorts = [c['cohort_id'] for c in active_cohorts if c.get('target_component_family') == 'reconciliation']

    if alias_cohorts and recon_cohorts:
        conflicts.append(CrossCohortConflictRecord(
            conflict_id=f"conf_{uuid.uuid4().hex[:8]}",
            conflict_family="alias_memory_and_reconciliation_scope_conflict",
            involved_cohorts=alias_cohorts + recon_cohorts,
            severity=ConflictSeverity.HIGH,
            description="Concurrent changes to alias memory and reconciliation logic detected."
        ))

    return conflicts

def detect_cross_family_interactions(active_families: List[str]) -> List[CrossFamilyInteractionRecord]:
    """Detects potentially unsafe interactions between component families currently undergoing rollout."""
    interactions = []

    # Example hardcoded interaction rules
    if "provider_priority" in active_families and "reconciliation_strategy" in active_families:
        interactions.append(CrossFamilyInteractionRecord(
            interaction_id=f"int_{uuid.uuid4().hex[:8]}",
            involved_families=["provider_priority", "reconciliation_strategy"],
            interaction_type="provider_and_reconciliation_compound_conflict",
            severity=ConflictSeverity.CRITICAL
        ))

    if "decision_thresholds" in active_families and "dynamic_weighting" in active_families:
         interactions.append(CrossFamilyInteractionRecord(
            interaction_id=f"int_{uuid.uuid4().hex[:8]}",
            involved_families=["decision_thresholds", "dynamic_weighting"],
            interaction_type="threshold_and_weighting_interaction_conflict",
            severity=ConflictSeverity.HIGH
        ))

    return interactions

def classify_conflict_severity(conflicts: List[CrossCohortConflictRecord]) -> ConflictSeverity:
    """Returns the highest severity among a list of conflicts."""
    if not conflicts:
        return ConflictSeverity.LOW

    severities = [c.severity for c in conflicts]
    if ConflictSeverity.CRITICAL in severities: return ConflictSeverity.CRITICAL
    if ConflictSeverity.HIGH in severities: return ConflictSeverity.HIGH
    if ConflictSeverity.MEDIUM in severities: return ConflictSeverity.MEDIUM
    return ConflictSeverity.LOW

def summarize_conflict_clusters(conflicts: List[CrossCohortConflictRecord]) -> Dict[str, int]:
    """Summarizes conflicts by family type."""
    summary = {}
    for c in conflicts:
        summary[c.conflict_family] = summary.get(c.conflict_family, 0) + 1
    return summary

def block_unsafe_multiwave_progression(conflicts: List[CrossCohortConflictRecord]) -> Tuple[bool, str]:
    """Evaluates if current conflicts should block new waves."""
    critical_count = sum(1 for c in conflicts if c.severity == ConflictSeverity.CRITICAL)
    if critical_count > 0:
        return True, f"Blocked due to {critical_count} CRITICAL conflicts."

    high_count = sum(1 for c in conflicts if c.severity == ConflictSeverity.HIGH)
    if high_count > 1:
        return True, f"Blocked due to {high_count} HIGH severity conflicts."

    return False, "Progression safe from conflict perspective."

def build_expansion_interaction_graph(cohorts: List[Dict[str, Any]], waves: List[Dict[str, Any]]) -> ExpansionInteractionGraphRecord:
    """Builds a formal graph of interactions between cohorts, waves, and families."""
    nodes = []
    edges = []

    family_nodes = set()

    # Add nodes
    for c in cohorts:
        nodes.append(InteractionNodeRecord(node_id=c['cohort_id'], node_type="cohort", name=c.get('name', c['cohort_id'])))
        fam = c.get('cohort_family')
        if fam:
            family_nodes.add(fam)
            edges.append(InteractionEdgeRecord(
                edge_id=f"edge_{uuid.uuid4().hex[:8]}",
                source_node_id=c['cohort_id'],
                target_node_id=f"fam_{fam}",
                edge_type="belongs_to_family"
            ))

    for w in waves:
        nodes.append(InteractionNodeRecord(node_id=w['wave_id'], node_type="wave", name=w.get('name', w['wave_id'])))
        for c_id in w.get('included_cohorts', []):
             edges.append(InteractionEdgeRecord(
                edge_id=f"edge_{uuid.uuid4().hex[:8]}",
                source_node_id=w['wave_id'],
                target_node_id=c_id,
                edge_type="includes_cohort"
            ))

    for f in family_nodes:
        nodes.append(InteractionNodeRecord(node_id=f"fam_{f}", node_type="family", name=f))

    return ExpansionInteractionGraphRecord(
        graph_id=f"graph_{uuid.uuid4().hex[:8]}",
        nodes=nodes,
        edges=edges
    )

def trace_shared_risk_paths(graph: ExpansionInteractionGraphRecord) -> List[str]:
    """Analyzes graph to find high-risk shared dependencies (e.g. multiple waves hitting same family)."""
    paths = []
    family_incoming = {}

    for edge in graph.edges:
        if edge.target_node_id.startswith("fam_"):
            family_incoming[edge.target_node_id] = family_incoming.get(edge.target_node_id, 0) + 1

    for fam, count in family_incoming.items():
        if count > 2:
            paths.append(f"High risk path: Family {fam} has {count} dependent active cohorts.")

    return paths

def detect_high_centrality_risk_nodes(graph: ExpansionInteractionGraphRecord) -> List[str]:
    """Finds nodes that represent centralization risk (single points of failure/contention)."""
    counts = {}
    for edge in graph.edges:
        counts[edge.target_node_id] = counts.get(edge.target_node_id, 0) + 1

    risky_nodes = [node_id for node_id, degree in counts.items() if degree > 3]
    return risky_nodes
