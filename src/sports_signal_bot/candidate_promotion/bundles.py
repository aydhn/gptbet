from typing import List, Dict, Any, Tuple
from .contracts import CandidateReleaseRecord, CandidateBundleRecord
import uuid

def build_candidate_bundle(candidates: List[CandidateReleaseRecord], target_family: str) -> CandidateBundleRecord:
    """Builds a bundle from candidates of the same family."""
    included = [c.candidate_release_id for c in candidates if c.target_component_family == target_family]

    return CandidateBundleRecord(
        candidate_bundle_id=str(uuid.uuid4()),
        included_candidate_ids=included,
        target_family=target_family,
        patch_payloads=[],
        simulation_refs=[],
        evidence_refs=[],
        gate_requirements=[],
        approval_requirements=[],
        release_notes_summary="Bundle constructed.",
        bundle_status="created"
    )

def compute_bundle_risk(bundle: CandidateBundleRecord, candidates: List[CandidateReleaseRecord]) -> str:
    """Computes aggregated bundle risk."""
    risk_levels = []
    for c in candidates:
        if c.candidate_release_id in bundle.included_candidate_ids:
            risk_levels.append(c.risk_level)

    if "critical" in risk_levels:
        return "critical"
    if "high" in risk_levels:
        return "high"
    if "medium" in risk_levels:
        return "medium"
    return "low"
