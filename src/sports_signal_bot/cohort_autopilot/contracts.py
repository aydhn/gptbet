from pydantic import BaseModel, Field
from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime

class CohortStatus(str, Enum):
    COHORT_PLANNED = "cohort_planned"
    COHORT_PENDING_ACTIVATION = "cohort_pending_activation"
    COHORT_ACTIVE = "cohort_active"
    COHORT_VERIFYING = "cohort_verifying"
    COHORT_VERIFIED_CLEAN = "cohort_verified_clean"
    COHORT_VERIFIED_WITH_WARNINGS = "cohort_verified_with_warnings"
    COHORT_PAUSED = "cohort_paused"
    COHORT_SHRUNK = "cohort_shrunk"
    COHORT_GROWTH_READY = "cohort_growth_ready"
    COHORT_GROWTH_BLOCKED = "cohort_growth_blocked"
    COHORT_ROLLBACK_REQUIRED = "cohort_rollback_required"
    COHORT_ROLLBACK_EXECUTED = "cohort_rollback_executed"
    COHORT_RETIRED = "cohort_retired"
    COHORT_SUPERSEDED = "cohort_superseded"

class ActivationLevel(str, Enum):
    LEVEL_0_REFERENCE_ONLY = "level_0_reference_only"
    LEVEL_1_NARROW_ACTIVATION = "level_1_narrow_activation"
    LEVEL_2_SMALL_COHORT = "level_2_small_cohort"
    LEVEL_3_MEDIUM_COHORT = "level_3_medium_cohort"
    LEVEL_4_FULL_FAMILY_SCOPE_PLACEHOLDER = "level_4_full_family_scope_placeholder"
    LEVEL_HOLD = "level_hold"
    LEVEL_ROLLBACK = "level_rollback"

class AutopilotAction(str, Enum):
    PROGRESS_COHORT = "progress_cohort"
    HOLD_COHORT = "hold_cohort"
    PAUSE_COHORT = "pause_cohort"
    SHRINK_COHORT_SCOPE = "shrink_cohort_scope"
    ROLLBACK_COHORT = "rollback_cohort"
    KEEP_CURRENT_LEVEL = "keep_current_level"
    QUEUE_FOR_MANUAL_REVIEW = "queue_for_manual_review"
    REQUIRE_MORE_VERIFICATION = "require_more_verification"
    BLOCK_GROWTH = "block_growth"
    RETIRE_COHORT = "retire_cohort"

class GrowthEligibilityStatus(str, Enum):
    ELIGIBLE_FOR_GROWTH = "eligible_for_growth"
    ELIGIBLE_BUT_REVIEW_PREFERRED = "eligible_but_review_preferred"
    GROWTH_BLOCKED = "growth_blocked"
    HOLD_REQUIRED = "hold_required"
    ROLLBACK_PREFERRED = "rollback_preferred"

class VerificationWindowType(str, Enum):
    IMMEDIATE_WINDOW = "immediate_window"
    SHORT_WINDOW = "short_window"
    MEDIUM_WINDOW = "medium_window"
    STABILITY_WINDOW = "stability_window"

class WindowOutcome(str, Enum):
    VERIFIED_CLEAN = "verified_clean"
    VERIFIED_WARNING = "verified_warning"
    REGRESSION_DETECTED = "regression_detected"
    ROLLBACK_REQUIRED = "rollback_required"

class AdoptionCohortRecord(BaseModel):
    cohort_id: str
    adoption_id: str
    cohort_family: str
    scope: Dict[str, Any]
    target_component_family: str
    current_status: CohortStatus = CohortStatus.COHORT_PLANNED
    activation_level: ActivationLevel = ActivationLevel.LEVEL_0_REFERENCE_ONLY
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class CohortMembershipRecord(BaseModel):
    cohort_id: str
    member_id: str
    member_type: str
    added_at: datetime = Field(default_factory=datetime.utcnow)

class CohortScopeRecord(BaseModel):
    cohort_id: str
    scope_definition: Dict[str, Any]

class CohortActivationRecord(BaseModel):
    cohort_id: str
    activation_level: ActivationLevel
    activated_at: datetime = Field(default_factory=datetime.utcnow)

class CohortVerificationWindowRecord(BaseModel):
    cohort_id: str
    window_type: VerificationWindowType
    started_at: datetime
    ends_at: datetime
    is_completed: bool = False

class CohortHealthRecord(BaseModel):
    cohort_id: str
    health_score: float
    health_issues: List[str] = Field(default_factory=list)
    measured_at: datetime = Field(default_factory=datetime.utcnow)

class AutopilotDecisionRecord(BaseModel):
    autopilot_decision_id: str
    cohort_id: str
    current_activation_level: ActivationLevel
    proposed_action: AutopilotAction
    proposed_next_level: Optional[ActivationLevel] = None
    decision_status: str
    heuristic_breakdown: Dict[str, Any]
    blockers: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class CohortDecisionRecord(BaseModel):
    cohort_id: str
    decision_id: str
    decision_type: str
    rationale: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CohortRollbackRecord(BaseModel):
    cohort_id: str
    rollback_id: str
    rollback_level: ActivationLevel
    reason: str
    executed_at: datetime = Field(default_factory=datetime.utcnow)

class CohortGrowthRecord(BaseModel):
    cohort_id: str
    previous_level: ActivationLevel
    new_level: ActivationLevel
    grown_at: datetime = Field(default_factory=datetime.utcnow)

class CohortShrinkRecord(BaseModel):
    cohort_id: str
    original_scope: Dict[str, Any]
    new_scope: Dict[str, Any]
    reason: str
    shrunk_at: datetime = Field(default_factory=datetime.utcnow)

class CohortPauseRecord(BaseModel):
    cohort_id: str
    reason: str
    paused_at: datetime = Field(default_factory=datetime.utcnow)

class AdoptionAutopilotManifest(BaseModel):
    manifest_id: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    active_cohorts: int = 0
    decisions_made: List[AutopilotDecisionRecord] = Field(default_factory=list)

class CohortSummaryRecord(BaseModel):
    cohort_id: str
    current_level: ActivationLevel
    status: CohortStatus
    health_score: float

class CohortCapacityRecord(BaseModel):
    max_cohorts: int
    current_active_cohorts: int

class CohortEvidenceRecord(BaseModel):
    evidence_id: str
    cohort_id: str
    evidence_type: str
    payload: Dict[str, Any]
    collected_at: datetime = Field(default_factory=datetime.utcnow)

class CohortWarningRecord(BaseModel):
    cohort_id: str
    warning_message: str
    severity: str
    reported_at: datetime = Field(default_factory=datetime.utcnow)

class PartitionSliceRecord(BaseModel):
    slice_id: str
    scope_slice: Dict[str, Any]

class SegmentAllocationRecord(BaseModel):
    segment_id: str
    allocation_ratio: float

class RolloutPartitionPlanRecord(BaseModel):
    plan_id: str
    cohort_id: str
    slices: List[PartitionSliceRecord]

class AutopilotHeuristicRecord(BaseModel):
    heuristic_id: str
    components: Dict[str, float]
    total_score: float

class GrowthEligibilityRecord(BaseModel):
    cohort_id: str
    status: GrowthEligibilityStatus
    reasons: List[str]

class VerificationSignalRecord(BaseModel):
    signal_id: str
    cohort_id: str
    signal_type: str
    is_positive: bool

class CohortProgressionRecord(BaseModel):
    progression_id: str
    cohort_id: str
    from_level: ActivationLevel
    to_level: ActivationLevel

class AutopilotBlockerRecord(BaseModel):
    blocker_id: str
    cohort_id: str
    blocker_type: str
    description: str

class AutopilotAuditRecord(BaseModel):
    audit_id: str
    action_performed: str
    cohort_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ProgressionConstraintRecord(BaseModel):
    constraint_id: str
    description: str
    is_met: bool

class CohortRegressionRecord(BaseModel):
    regression_id: str
    cohort_id: str
    regression_metric: str
    magnitude: float

class GrowthRecommendationRecord(BaseModel):
    recommendation_id: str
    cohort_id: str
    recommended_action: AutopilotAction

class PauseReasonRecord(BaseModel):
    reason_id: str
    description: str

class ShrinkReasonRecord(BaseModel):
    reason_id: str
    description: str

class VerificationWindowPolicyRecord(BaseModel):
    policy_id: str
    window_type: VerificationWindowType
    duration_hours: int

class WindowOutcomeRecord(BaseModel):
    outcome_id: str
    cohort_id: str
    window_type: VerificationWindowType
    outcome: WindowOutcome

class WindowRegressionSummaryRecord(BaseModel):
    summary_id: str
    cohort_id: str
    window_type: VerificationWindowType
    regression_count: int

class WindowStabilityScoreRecord(BaseModel):
    score_id: str
    cohort_id: str
    window_type: VerificationWindowType
    score: float

class CohortLadderRuleRecord(BaseModel):
    rule_id: str
    from_level: ActivationLevel
    to_level: ActivationLevel
    requirements: List[str]

class GrowthStepRecord(BaseModel):
    step_id: str
    from_level: ActivationLevel
    to_level: ActivationLevel

class GrowthWindowRequirementRecord(BaseModel):
    requirement_id: str
    min_clean_windows: int

class CohortFleetRecord(BaseModel):
    fleet_id: str
    active_cohort_ids: List[str]

class FleetRiskBudgetRecord(BaseModel):
    budget_id: str
    max_risk_score: float
    current_risk_score: float

class FleetGrowthQuotaRecord(BaseModel):
    quota_id: str
    max_growing_cohorts: int
    current_growing_cohorts: int

class FleetAutopilotPressureRecord(BaseModel):
    pressure_id: str
    pressure_level: str

class GrowthApprovalRequirementRecord(BaseModel):
    requirement_id: str
    requires_approval: bool

class CouncilGrowthConstraintRecord(BaseModel):
    constraint_id: str
    description: str
