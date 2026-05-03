from sports_signal_bot.remediation_lanes.contracts import LaneEligibilityRecord, LaneEligibilityResult

def compute_lane_eligibility(lane_ref: str, is_reversible: bool, has_rollback: bool) -> LaneEligibilityRecord:
    if is_reversible and has_rollback:
        return LaneEligibilityRecord(
            lane_ref=lane_ref,
            eligibility_result=LaneEligibilityResult.token_issuable,
            confidence_score=0.9
        )
    return LaneEligibilityRecord(
        lane_ref=lane_ref,
        eligibility_result=LaneEligibilityResult.not_eligible,
        confidence_score=0.1
    )
