from typing import List, Dict, Any
from .contracts import TournamentEvidenceRecord, CandidateComparisonRecord
import uuid

def attach_evidence_to_tournament_candidate(
    candidate_id: str,
    simulation_run_id: str,
    citations: List[str]
) -> TournamentEvidenceRecord:
    """Attaches an evidence bundle reference to a candidate."""
    return TournamentEvidenceRecord(
        evidence_id=str(uuid.uuid4()),
        candidate_id=candidate_id,
        simulation_bundle_ref=f"bundle_for_run_{simulation_run_id}",
        citations=citations
    )

def build_tournament_claims(
    comparison: CandidateComparisonRecord
) -> List[str]:
    """Builds textual claims based on comparison metrics."""
    claims = []
    for metric in comparison.metrics:
        claims.append(f"Metric {metric.metric_name} changed by {metric.value} (direction: {metric.direction.value})")
    return claims

def explain_dominance_with_citations(
    dominating_id: str,
    dominated_id: str,
    dominating_metrics: List[str],
    evidence_map: Dict[str, TournamentEvidenceRecord]
) -> str:
    """Explains dominance referencing evidence."""
    dom_ev = evidence_map.get(dominating_id)
    dom_ref = dom_ev.simulation_bundle_ref if dom_ev else "unknown"
    return f"Candidate {dominating_id} dominates {dominated_id} on {dominating_metrics}. Evidence: {dom_ref}"

def build_shortlist_explanation_packet(
    candidate_id: str,
    evidence: TournamentEvidenceRecord,
    profile: str = "reviewer_standard"
) -> Dict[str, Any]:
    """Builds an explanation packet tailored to the audience profile."""
    packet = {
        "candidate_id": candidate_id,
        "bundle_ref": evidence.simulation_bundle_ref
    }
    if profile == "auditor_full":
        packet["citations"] = evidence.citations
        packet["full_trace"] = True
    else:
        packet["summary"] = f"Supported by {len(evidence.citations)} citations."
    return packet
