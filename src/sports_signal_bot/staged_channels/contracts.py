import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ChannelFamily(str, Enum):
    STABLE_REFERENCE = "stable_reference_channel"
    SHADOW_CANDIDATE = "shadow_candidate_channel"
    CANDIDATE_EVAL = "candidate_eval_channel"
    LIVE_LIKE_SAFE = "live_like_safe_channel"
    ROLLBACK_SHADOW = "rollback_shadow_channel"
    RETIRED_CANDIDATE = "retired_candidate_channel"
    BLOCKED_CANDIDATE = "blocked_candidate_channel"

class StageStatus(str, Enum):
    CANDIDATE_QUEUED_FOR_SHADOW = "candidate_queued_for_shadow"
    RUNNING_IN_SHADOW = "running_in_shadow"
    SHADOW_VERIFIED = "shadow_verified"
    PENDING_CANDIDATE_EVAL = "pending_candidate_eval"
    RUNNING_CANDIDATE_EVAL = "running_candidate_eval"
    CANDIDATE_EVAL_VERIFIED = "candidate_eval_verified"
    PENDING_LIVE_LIKE_SAFE = "pending_live_like_safe"
    RUNNING_LIVE_LIKE_SAFE = "running_live_like_safe"
    LIVE_LIKE_SAFE_VERIFIED = "live_like_safe_verified"
    ROLLOUT_HOLD = "rollout_hold"
    ROLLBACK_TO_SHADOW = "rollback_to_shadow"
    ROLLOUT_RETIRED = "rollout_retired"
    ROLLOUT_BLOCKED = "rollout_blocked"
    ROLLOUT_READY_FOR_NEXT_PROMOTION_STEP = "rollout_ready_for_next_promotion_step"

class RolloutDecisionType(str, Enum):
    PROGRESS_TO_NEXT_STAGE = "progress_to_next_stage"
    HOLD_IN_CURRENT_STAGE = "hold_in_current_stage"
    ROLLBACK_TO_SHADOW = "rollback_to_shadow"
    RETIRE_CANDIDATE = "retire_candidate"
    BLOCK_CANDIDATE = "block_candidate"
    QUEUE_FOR_REVIEW = "queue_for_review"
    READY_FOR_FUTURE_RELEASE_STEP = "ready_for_future_release_step"
    SUPERSEDE_WITH_BETTER_CANDIDATE = "supersede_with_better_candidate"

class CandidateChannelRecord(BaseModel):
    channel_id: str
    channel_name: str
    channel_family: ChannelFamily
    safety_level: str
    comparison_mode: str
    allowed_candidate_families: List[str] = Field(default_factory=list)
    progression_policy: str
    capacity_limits: Dict[str, int] = Field(default_factory=dict)
    active_assignments: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class RolloutStageRecord(BaseModel):
    stage_id: str
    candidate_release_id: str
    current_channel: str
    stage_status: StageStatus
    entered_at: datetime.datetime
    required_evaluations: List[str] = Field(default_factory=list)
    stage_exit_criteria: Dict[str, Any] = Field(default_factory=dict)
    blockers: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class CandidateFleetRecord(BaseModel):
    fleet_id: str
    description: str
    members: List[str] = Field(default_factory=list)
    fleet_policy: str

class RolloutWaveRecord(BaseModel):
    wave_id: str
    included_candidates: List[str] = Field(default_factory=list)
    target_channel: str
    start_time: datetime.datetime
    evaluation_window_hours: int
    capacity_budget: Dict[str, int] = Field(default_factory=dict)
    safety_notes: List[str] = Field(default_factory=list)

class RolloutDecisionRecord(BaseModel):
    decision_id: str
    candidate_release_id: str
    decision_type: RolloutDecisionType
    reason: str
    timestamp: datetime.datetime
    metrics: Dict[str, Any] = Field(default_factory=dict)

class FleetConflictRecord(BaseModel):
    conflict_id: str
    involved_candidates: List[str]
    conflict_type: str
    severity: str
    description: str

class NextStepReadinessRecord(BaseModel):
    candidate_release_id: str
    readiness_level: str  # e.g., not_ready_for_release_step, shadow_only_candidate, candidate_eval_ready, live_like_safe_ready, release_step_consideration_ready
    notes: List[str] = Field(default_factory=list)
