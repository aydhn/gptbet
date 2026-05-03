from .contracts import (
    RemediationLaneRecord, LaneEligibilityRecord, LaneEligibilityOutcome,
    ReviewAwareExecutionRecord, LaneStatus, LaneLedgerEntry
)

def compute_lane_eligibility(lane: RemediationLaneRecord, review_state: ReviewAwareExecutionRecord) -> LaneEligibilityRecord:
    blockers = []

    if not lane.rollback_binding.is_verified_in_rehearsal:
        blockers.append("rollback_not_verified_in_rehearsal")

    if review_state.unresolved_caveats > 0:
        blockers.append(f"unresolved_review_caveats:{review_state.unresolved_caveats}")

    if review_state.eligibility_downgraded:
        outcome = LaneEligibilityOutcome.review_only_eligible
    elif blockers:
        outcome = LaneEligibilityOutcome.blocked_by_safety
    else:
        outcome = LaneEligibilityOutcome.token_issuable

    return LaneEligibilityRecord(
        lane_id=lane.lane_id,
        outcome=outcome,
        confidence_score=0.9 if not blockers else 0.4,
        is_reversible=True,
        has_explicit_rollback=True,
        has_strong_rehearsal_evidence=lane.rollback_binding.is_verified_in_rehearsal,
        blockers=blockers
    )

def project_review_restrictions_into_lane(lane_id: str, approval_ref: str, caveats: int, restrictions: list) -> ReviewAwareExecutionRecord:
    return ReviewAwareExecutionRecord(
        lane_id=lane_id,
        approval_ref=approval_ref,
        unresolved_caveats=caveats,
        reviewer_restrictions=restrictions,
        eligibility_downgraded=(caveats > 0 or "read_only" in restrictions)
    )

def append_lane_lifecycle_entry(ledger: list, lane_id: str, action: str, details: str):
    ledger.append(LaneLedgerEntry(lane_id=lane_id, action=action, details=details))
