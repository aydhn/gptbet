import pytest
from sports_signal_bot.continuity_verification_hardening.scheduler_proof_lanes import (
    build_scheduler_proof_lane,
    build_scheduler_proof_packet,
    verify_scheduler_proof_lane,
    replay_scheduler_proof_lane,
    summarize_scheduler_proof_lane
)
from sports_signal_bot.continuity_verification_hardening.contracts import (
    SchedulerProofLaneFamily,
    SchedulerProofLaneStatus
)

def test_build_scheduler_proof_lane():
    lane = build_scheduler_proof_lane("lane_test", SchedulerProofLaneFamily.planetary_coverage_proof_lane)
    assert lane.scheduler_proof_lane_id == "lane_test"
    assert lane.lane_family == SchedulerProofLaneFamily.planetary_coverage_proof_lane
    assert lane.lane_status == SchedulerProofLaneStatus.lane_gapped

def test_verify_scheduler_proof_lane():
    lane = build_scheduler_proof_lane("lane_test", SchedulerProofLaneFamily.planetary_coverage_proof_lane)
    packets = [
        build_scheduler_proof_packet("packet_1", is_stale=False)
    ]
    verified_lane = verify_scheduler_proof_lane(lane, packets)
    assert verified_lane.lane_status == SchedulerProofLaneStatus.lane_verified

def test_replay_scheduler_proof_lane():
    lane = build_scheduler_proof_lane("lane_test", SchedulerProofLaneFamily.planetary_coverage_proof_lane)
    result = replay_scheduler_proof_lane(lane)
    assert result["replay_successful"] is True
