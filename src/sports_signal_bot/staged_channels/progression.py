import datetime
import uuid
from typing import Dict, Any, List
from sports_signal_bot.staged_channels.contracts import (
    RolloutStageRecord, StageStatus, CandidateChannelRecord,
    RolloutDecisionRecord, RolloutDecisionType, NextStepReadinessRecord
)

def build_rollout_decision(
    candidate_id: str,
    decision_type: RolloutDecisionType,
    reason: str,
    metrics: Dict[str, Any] = None
) -> RolloutDecisionRecord:
    return RolloutDecisionRecord(
        decision_id=str(uuid.uuid4()),
        candidate_release_id=candidate_id,
        decision_type=decision_type,
        reason=reason,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        metrics=metrics or {}
    )

def simulate_rollout_stage(candidate_id: str, current_stage: StageStatus) -> StageStatus:
    # A simple mock simulation advancing the stage
    transitions = {
        StageStatus.CANDIDATE_QUEUED_FOR_SHADOW: StageStatus.RUNNING_IN_SHADOW,
        StageStatus.RUNNING_IN_SHADOW: StageStatus.SHADOW_VERIFIED,
        StageStatus.SHADOW_VERIFIED: StageStatus.PENDING_CANDIDATE_EVAL,
        StageStatus.PENDING_CANDIDATE_EVAL: StageStatus.RUNNING_CANDIDATE_EVAL,
        StageStatus.RUNNING_CANDIDATE_EVAL: StageStatus.CANDIDATE_EVAL_VERIFIED,
        StageStatus.CANDIDATE_EVAL_VERIFIED: StageStatus.PENDING_LIVE_LIKE_SAFE,
        StageStatus.PENDING_LIVE_LIKE_SAFE: StageStatus.RUNNING_LIVE_LIKE_SAFE,
        StageStatus.RUNNING_LIVE_LIKE_SAFE: StageStatus.LIVE_LIKE_SAFE_VERIFIED,
        StageStatus.LIVE_LIKE_SAFE_VERIFIED: StageStatus.ROLLOUT_READY_FOR_NEXT_PROMOTION_STEP
    }
    return transitions.get(current_stage, current_stage)

def compute_next_step_readiness(stage: StageStatus, candidate_id: str) -> NextStepReadinessRecord:
    readiness = "not_ready_for_release_step"
    if stage == StageStatus.SHADOW_VERIFIED:
        readiness = "shadow_only_candidate"
    elif stage == StageStatus.CANDIDATE_EVAL_VERIFIED:
        readiness = "candidate_eval_ready"
    elif stage == StageStatus.LIVE_LIKE_SAFE_VERIFIED:
        readiness = "live_like_safe_ready"
    elif stage == StageStatus.ROLLOUT_READY_FOR_NEXT_PROMOTION_STEP:
        readiness = "release_step_consideration_ready"

    return NextStepReadinessRecord(
        candidate_release_id=candidate_id,
        readiness_level=readiness,
        notes=["Computed from stage " + stage.value]
    )

def compare_channel_behaviors(candidate_id: str, channel1_metrics: dict, channel2_metrics: dict) -> dict:
    return {
        "candidate_id": candidate_id,
        "diff_metrics": {}, # Placeholder
        "consistent": True
    }
