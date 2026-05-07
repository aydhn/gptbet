import uuid
from typing import List
from src.sports_signal_bot.planetary_hardening.contracts import (
    IntercontinentalRecoveryLaneRecord,
    RecoveryLaneSourceRecord,
    RecoveryLaneTargetRecord,
    RecoveryLaneStageRecord,
    RecoveryLaneCheckpointRecord,
    RecoveryLaneLagRecord,
    RecoveryLaneRollbackRecord,
    IntercontinentalRecoveryWarningRecord
)

def build_intercontinental_recovery_lane(lane_family: str, source: RecoveryLaneSourceRecord, target: RecoveryLaneTargetRecord) -> IntercontinentalRecoveryLaneRecord:
    return IntercontinentalRecoveryLaneRecord(
        intercontinental_recovery_lane_id=f"irl_{uuid.uuid4().hex[:8]}",
        lane_family=lane_family,
        source_ref=source,
        target_ref=target,
        lane_status="lane_review_only"
    )

def verify_recovery_lane_source_and_target(lane: IntercontinentalRecoveryLaneRecord, reject_stale: bool = True) -> IntercontinentalRecoveryLaneRecord:
    warnings = []
    if not lane.source_ref.is_fresh:
        warnings.append(IntercontinentalRecoveryWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="Stale source."))
        if reject_stale:
            lane.lane_status = "lane_caveated"

    if not lane.target_ref.is_ready:
        warnings.append(IntercontinentalRecoveryWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="Target not ready."))
        lane.lane_status = "lane_gapped" if lane.lane_status != "lane_caveated" else lane.lane_status

    if not warnings:
        lane.lane_status = "lane_verified"

    lane.warnings.extend(warnings)
    return lane

def evaluate_recovery_lane_lag(lane: IntercontinentalRecoveryLaneRecord, lag: RecoveryLaneLagRecord) -> IntercontinentalRecoveryLaneRecord:
    lane.lag_refs.append(lag)
    if lag.duration_hours > 4: # Configurable threshold in real app
        lane.warnings.append(IntercontinentalRecoveryWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="High lag detected."))
        lane.lane_status = "lane_caveated"
    return lane

def verify_recovery_lane_checkpoint(lane: IntercontinentalRecoveryLaneRecord, checkpoint: RecoveryLaneCheckpointRecord) -> IntercontinentalRecoveryLaneRecord:
    lane.checkpoint_refs.append(checkpoint)
    return lane

def summarize_intercontinental_recovery_lane(lane: IntercontinentalRecoveryLaneRecord) -> dict:
    return {
        "id": lane.intercontinental_recovery_lane_id,
        "family": lane.lane_family,
        "status": lane.lane_status,
        "warnings": [w.message for w in lane.warnings],
        "is_source_fresh": lane.source_ref.is_fresh,
        "is_target_ready": lane.target_ref.is_ready
    }
