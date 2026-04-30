from typing import List, Dict, Any, Tuple
from .contracts import (
    CandidateReleaseRecord,
    CandidateReadinessRecord,
    CandidateReadinessBand,
    FinalDecisionAction,
    CandidatePromotionDecisionRecord,
    CandidateKillDecisionRecord,
    KillReason,
    CandidateLane
)

def build_promote_or_kill_decision(
    candidate: CandidateReleaseRecord,
    readiness: CandidateReadinessRecord,
    lane: CandidateLane
) -> Tuple[FinalDecisionAction, str]:
    """Builds a promote or kill decision based on candidate state."""

    if readiness.readiness_band == CandidateReadinessBand.BLOCKED_NOT_READY:
        if "safety_validation" in readiness.missing_requirements:
            return FinalDecisionAction.KILL_CANDIDATE, "Candidate failed safety validation and is blocked."
        return FinalDecisionAction.REVISE_CANDIDATE, "Candidate has blockages that might be revised."

    if readiness.readiness_band == CandidateReadinessBand.RELEASE_CANDIDATE_READY:
        return FinalDecisionAction.PROMOTE_CANDIDATE_LANE, "Candidate is ready and has passed all gates."

    if readiness.readiness_band in [CandidateReadinessBand.REVIEW_READY, CandidateReadinessBand.CONDITIONALLY_READY]:
        return FinalDecisionAction.HOLD_CANDIDATE, "Candidate held for review/approvals."

    return FinalDecisionAction.REVISE_CANDIDATE, "Candidate not ready. Requires revision."

def classify_candidate_outcome(decision: FinalDecisionAction) -> str:
    """Classifies outcome as positive, negative, or neutral."""
    if decision == FinalDecisionAction.PROMOTE_CANDIDATE_LANE:
        return "positive"
    if decision in [FinalDecisionAction.KILL_CANDIDATE, FinalDecisionAction.BLOCK_PROMOTION]:
        return "negative"
    return "neutral"

def explain_candidate_decision(candidate: CandidateReleaseRecord, decision: FinalDecisionAction, rationale: str) -> str:
    """Explains candidate decision."""
    return f"Decision for {candidate.candidate_release_id}: {decision.value} - {rationale}"

def detect_revision_needed(decision: FinalDecisionAction) -> bool:
    """Returns True if revision is needed."""
    return decision in [FinalDecisionAction.REVISE_CANDIDATE, FinalDecisionAction.REQUEST_NARROWER_SCOPE]

def detect_superseded_candidate(candidate_id: str, active_candidates: List[CandidateReleaseRecord]) -> bool:
    """Returns true if a candidate is superseded. Placeholder logic."""
    return False
