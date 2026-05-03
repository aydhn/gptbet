from datetime import datetime
from sports_signal_bot.remediation_lanes.contracts import (
    RemediationLaneRecord,
    BoundedExecutionTokenFamily,
    LoopClosureOutcome
)
from sports_signal_bot.remediation_lanes.tokens import (
    build_bounded_execution_token,
    validate_execution_token_scope
)
from sports_signal_bot.remediation_lanes.closure import build_loop_closure_packet

def test_token_creation_and_validation():
    lane = RemediationLaneRecord(
        lane_id="lane-123",
        lane_family="containment_lane",
        incident_family="sync_lag",
        scoped_playbook_ref="pb-123"
    )

    token = build_bounded_execution_token(
        token_id="tok-123",
        token_family=BoundedExecutionTokenFamily.staged_execution_token,
        lane_ref=lane.lane_id,
        allowed_step_families=["restart"],
        allowed_scope={"region": "eu-west"},
        approval_ref="appr-123",
        valid_from=datetime.now(),
        valid_until=datetime.now()
    )

    assert token.bound_lane_ref == "lane-123"
    assert validate_execution_token_scope(token, {"region": "eu-west"}) == True
    assert validate_execution_token_scope(token, {"region": "us-east"}) == False

def test_loop_closure():
    lane = RemediationLaneRecord(
        lane_id="lane-123",
        lane_family="containment_lane",
        incident_family="sync_lag",
        scoped_playbook_ref="pb-123"
    )

    closure = build_loop_closure_packet(lane, ["ev-1"], LoopClosureOutcome.closed_clean)
    assert closure.outcome == LoopClosureOutcome.closed_clean
