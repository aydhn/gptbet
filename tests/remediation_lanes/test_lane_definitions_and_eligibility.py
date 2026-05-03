from sports_signal_bot.remediation_lanes.eligibility import compute_lane_eligibility
from sports_signal_bot.remediation_lanes.contracts import LaneEligibilityResult

def test_eligibility():
    eligibility = compute_lane_eligibility("lane-1", True, True)
    assert eligibility.eligibility_result == LaneEligibilityResult.token_issuable
