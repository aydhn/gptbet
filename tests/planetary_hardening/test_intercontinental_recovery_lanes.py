import pytest
from src.sports_signal_bot.planetary_hardening.recovery_lanes import (
    build_intercontinental_recovery_lane,
    verify_recovery_lane_source_and_target,
    evaluate_recovery_lane_lag
)
from src.sports_signal_bot.planetary_hardening.contracts import (
    RecoveryLaneSourceRecord,
    RecoveryLaneTargetRecord,
    RecoveryLaneLagRecord
)

def test_build_intercontinental_recovery_lane():
    lane = build_intercontinental_recovery_lane(
        "test_lane",
        RecoveryLaneSourceRecord(source_id="s1", is_fresh=True),
        RecoveryLaneTargetRecord(target_id="t1", is_ready=True)
    )
    assert lane.lane_family == "test_lane"
    assert lane.lane_status == "lane_review_only"

def test_verify_recovery_lane_fresh():
    lane = build_intercontinental_recovery_lane(
        "test_lane",
        RecoveryLaneSourceRecord(source_id="s1", is_fresh=True),
        RecoveryLaneTargetRecord(target_id="t1", is_ready=True)
    )
    lane = verify_recovery_lane_source_and_target(lane)
    assert lane.lane_status == "lane_verified"

def test_verify_recovery_lane_stale():
    lane = build_intercontinental_recovery_lane(
        "test_lane",
        RecoveryLaneSourceRecord(source_id="s1", is_fresh=False),
        RecoveryLaneTargetRecord(target_id="t1", is_ready=True)
    )
    lane = verify_recovery_lane_source_and_target(lane, reject_stale=True)
    assert lane.lane_status == "lane_caveated"

def test_evaluate_recovery_lane_lag():
    lane = build_intercontinental_recovery_lane(
        "test_lane",
        RecoveryLaneSourceRecord(source_id="s1", is_fresh=True),
        RecoveryLaneTargetRecord(target_id="t1", is_ready=True)
    )
    lane = evaluate_recovery_lane_lag(lane, RecoveryLaneLagRecord(lag_id="l1", duration_hours=5.0))
    assert lane.lane_status == "lane_caveated"
    assert len(lane.warnings) == 1
