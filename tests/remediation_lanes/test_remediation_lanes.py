import pytest
from datetime import datetime, timezone
from sports_signal_bot.remediation_lanes.contracts import (
    RemediationLaneRecord, LaneFamily, RollbackBindingRecord, ReviewAwareExecutionRecord
)
from sports_signal_bot.remediation_lanes.lanes import compute_lane_eligibility
from sports_signal_bot.remediation_lanes.tokens import build_bounded_execution_token, validate_execution_token_scope

def test_lane_eligibility_blocked_without_rehearsal():
    lane = RemediationLaneRecord(
        lane_id="test_1",
        lane_family=LaneFamily.containment_lane,
        incident_family="lag",
        scoped_playbook_ref="ref",
        allowed_step_families=[],
        forbidden_step_families=[],
        rollback_binding=RollbackBindingRecord(rollback_playbook_ref="", rollback_scope="", rollback_checkpoints=[]),
        observability_refs=[]
    )
    review = ReviewAwareExecutionRecord(lane_id="test_1", approval_ref="app1", unresolved_caveats=0, reviewer_restrictions=[], eligibility_downgraded=False)

    result = compute_lane_eligibility(lane, review)
    assert result.outcome.value == "blocked_by_safety"
    assert "rollback_not_verified_in_rehearsal" in result.blockers

def test_token_scope_validation():
    lane = RemediationLaneRecord(
        lane_id="test_2",
        lane_family=LaneFamily.reroute_lane,
        incident_family="route_issue",
        scoped_playbook_ref="ref",
        allowed_step_families=["reroute"],
        forbidden_step_families=[],
        rollback_binding=RollbackBindingRecord(rollback_playbook_ref="r", rollback_scope="s", rollback_checkpoints=[], is_verified_in_rehearsal=True),
        observability_refs=[]
    )
    review = ReviewAwareExecutionRecord(lane_id="test_2", approval_ref="app1", unresolved_caveats=0, reviewer_restrictions=[], eligibility_downgraded=False)

    token = build_bounded_execution_token(lane, review, 1800)

    assert validate_execution_token_scope(token, "route_issue", "reroute") is True
    assert validate_execution_token_scope(token, "wrong_scope", "reroute") is False
    assert validate_execution_token_scope(token, "route_issue", "drop_db") is False
