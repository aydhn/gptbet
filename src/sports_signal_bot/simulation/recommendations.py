from .contracts import (
    SimulationComparisonRecord,
    SimulationRecommendationRecord,
    RecommendationType,
    MaterialityBand,
    ComparisonStatus
)
import uuid

def generate_recommendation(comparison: SimulationComparisonRecord) -> SimulationRecommendationRecord:
    status = comparison.status
    mat_band = comparison.materiality_band

    rec_type = RecommendationType.KEEP_ADVISORY_ONLY
    rationale = "Default fallback"

    if status == ComparisonStatus.IMPROVED:
        if mat_band in [MaterialityBand.LARGE, MaterialityBand.CRITICAL]:
            rec_type = RecommendationType.SAFE_FOR_REVIEW
            rationale = "Material improvement detected, requires review due to high impact."
        else:
            rec_type = RecommendationType.SAFE_FOR_CANDIDATE_RELEASE_PATH
            rationale = "Consistent improvement with safe materiality bounds."
    elif status == ComparisonStatus.DEGRADED:
        rec_type = RecommendationType.REJECT_PATCH
        rationale = "Simulation shows degraded performance."
    elif status == ComparisonStatus.MIXED:
        if mat_band in [MaterialityBand.LARGE, MaterialityBand.CRITICAL]:
            rec_type = RecommendationType.NARROW_SCOPE_AND_RETRY
            rationale = "Mixed results with high impact; narrow scope."
        else:
            rec_type = RecommendationType.REQUEST_MORE_DATA
            rationale = "Mixed results on small scale; need more data."
    elif status == ComparisonStatus.INVALID_SIMULATION:
        rec_type = RecommendationType.REJECT_PATCH
        rationale = "Simulation was invalid."

    return SimulationRecommendationRecord(
        recommendation_id=f"rec_{uuid.uuid4().hex[:8]}",
        comparison_id=comparison.comparison_id,
        recommendation=rec_type,
        required_gates=[],
        rationale=rationale,
        warnings=[]
    )
