from typing import List, Optional
from .contracts import (
    GrowthEligibilityRecord, GrowthEligibilityStatus,
    CohortProgressionRecord, ActivationLevel, GrowthRecommendationRecord, AutopilotAction
)

def compute_growth_eligibility(cohort_id: str, blockers: List[str], stability_score: float) -> GrowthEligibilityRecord:
    if blockers:
        return GrowthEligibilityRecord(
            cohort_id=cohort_id,
            status=GrowthEligibilityStatus.GROWTH_BLOCKED,
            reasons=blockers
        )

    if stability_score >= 0.9:
        return GrowthEligibilityRecord(
            cohort_id=cohort_id,
            status=GrowthEligibilityStatus.ELIGIBLE_FOR_GROWTH,
            reasons=["High stability score and no blockers."]
        )

    return GrowthEligibilityRecord(
        cohort_id=cohort_id,
        status=GrowthEligibilityStatus.ELIGIBLE_BUT_REVIEW_PREFERRED,
        reasons=["Marginal stability score, review recommended."]
    )

def collect_growth_blockers(cohort_id: str, active_disputes: bool, stale_verification: bool) -> List[str]:
    blockers = []
    if active_disputes:
        blockers.append("Active unresolved critical disputes.")
    if stale_verification:
        blockers.append("Stale verification window.")
    return blockers

def explain_growth_decision(eligibility: GrowthEligibilityRecord) -> str:
    return f"Status: {eligibility.status.value}. Reasons: {', '.join(eligibility.reasons)}"

def require_manual_review_for_growth(cohort_id: str) -> bool:
    return False

def progress_cohort(cohort_id: str, from_level: ActivationLevel, to_level: ActivationLevel) -> CohortProgressionRecord:
    return CohortProgressionRecord(
        progression_id=f"prog_{cohort_id}",
        cohort_id=cohort_id,
        from_level=from_level,
        to_level=to_level
    )
