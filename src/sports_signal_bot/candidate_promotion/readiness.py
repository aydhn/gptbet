from typing import List, Dict, Any, Tuple
from .contracts import CandidateReadinessRecord, CandidateReadinessBand, CandidateReleaseRecord, CandidateValidationStageRecord

def compute_candidate_readiness(
    candidate: CandidateReleaseRecord,
    stage_results: List[CandidateValidationStageRecord],
    has_approvals: bool = False
) -> CandidateReadinessRecord:
    """Computes the readiness record for a candidate based on stage results and approvals."""
    failed_stages = [r.stage_id for r in stage_results if not r.passed]

    missing_requirements = failed_stages.copy()

    if candidate.risk_level in ["high", "critical"] and not has_approvals:
        missing_requirements.append("missing_approval")

    if len(missing_requirements) > 0:
        band = CandidateReadinessBand.BLOCKED_NOT_READY if "safety_validation" in failed_stages else CandidateReadinessBand.NOT_READY
    elif not has_approvals and candidate.risk_level in ["medium"]:
        band = CandidateReadinessBand.REVIEW_READY
    else:
        band = CandidateReadinessBand.RELEASE_CANDIDATE_READY

    return CandidateReadinessRecord(
        readiness_id=f"readiness_{candidate.candidate_release_id}",
        candidate_id=candidate.candidate_release_id,
        readiness_band=band,
        missing_requirements=missing_requirements
    )

def classify_readiness_band(readiness: CandidateReadinessRecord) -> str:
    """Classifies readiness into low, medium, high, gated, blocked."""
    if readiness.readiness_band == CandidateReadinessBand.BLOCKED_NOT_READY:
        return "blocked"
    if readiness.readiness_band == CandidateReadinessBand.NOT_READY:
        return "low"
    if readiness.readiness_band == CandidateReadinessBand.REVIEW_READY:
        return "medium"
    return "high"

def collect_readiness_blockers(readiness: CandidateReadinessRecord) -> List[str]:
    """Collects blockers."""
    return readiness.missing_requirements

def summarize_readiness_requirements(readiness: CandidateReadinessRecord) -> str:
    if not readiness.missing_requirements:
        return "All readiness requirements met."
    return f"Missing requirements: {', '.join(readiness.missing_requirements)}"
