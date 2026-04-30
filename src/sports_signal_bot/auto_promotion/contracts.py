from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class AutoDecisionType(str, Enum):
    auto_progress = "auto_progress"
    auto_hold = "auto_hold"
    auto_kill = "auto_kill"
    auto_defer = "auto_defer"
    review_required = "review_required"
    approval_required = "approval_required"
    blocked_by_safety = "blocked_by_safety"
    blocked_by_manual_override = "blocked_by_manual_override"
    blocked_by_capacity = "blocked_by_capacity"
    blocked_by_staleness = "blocked_by_staleness"
    blocked_by_conflict = "blocked_by_conflict"
    insufficient_evidence = "insufficient_evidence"

class EligibilityStatus(str, Enum):
    eligible_for_auto_progress = "eligible_for_auto_progress"
    eligible_but_review_preferred = "eligible_but_review_preferred"
    hold_required = "hold_required"
    kill_candidate = "kill_candidate"
    approval_required = "approval_required"
    blocked = "blocked"

class KillReasonCode(str, Enum):
    repeated_stage_regression = "repeated_stage_regression"
    critical_safety_violation = "critical_safety_violation"
    stale_or_invalid_simulation = "stale_or_invalid_simulation"
    failed_required_quality_gates = "failed_required_quality_gates"
    unresolved_critical_dispute = "unresolved_critical_dispute"
    broad_scope_high_risk_no_approval = "broad_scope_high_risk_no_approval"
    superseded_by_stronger_candidate = "superseded_by_stronger_candidate"
    repeated_hold_without_progress = "repeated_hold_without_progress"
    invalid_candidate_state = "invalid_candidate_state"
    contradictory_evidence_burden = "contradictory_evidence_burden"
    fleet_conflict_with_stronger_safer_candidate = "fleet_conflict_with_stronger_safer_candidate"
    candidate_expired_without_readiness = "candidate_expired_without_readiness"

class HoldReasonCode(str, Enum):
    missing_fresh_gate_results = "missing_fresh_gate_results"
    pending_approval = "pending_approval"
    pending_manual_review = "pending_manual_review"
    insufficient_simulation_coverage = "insufficient_simulation_coverage"
    fleet_capacity_pressure = "fleet_capacity_pressure"
    unresolved_noncritical_conflicts = "unresolved_noncritical_conflicts"
    stage_evidence_not_fresh = "stage_evidence_not_fresh"
    quality_gate_backlog = "quality_gate_backlog"
    narrow_scope_retry_recommended = "narrow_scope_retry_recommended"
    contradictory_noncritical_metrics = "contradictory_noncritical_metrics"

class CandidateInputRecord(BaseModel):
    candidate_release_id: str
    target_family: str
    current_stage: str
    risk_level: str
    scope_breadth: str
    manual_override: Optional[str] = None
    approval_status: str = "none"
    simulation_freshness_hours: float
    evidence_completeness: float
    readiness_score: float
    gate_cleanliness: float
    conflict_burden: int
    dispute_count: int
    repeated_holds: int

class ProgressionBlockerRecord(BaseModel):
    blocker_type: str
    reason: str
    severity: str

class HeuristicScoreRecord(BaseModel):
    composite_score: float
    components: Dict[str, float]

class AutoProgressionDecisionRecord(BaseModel):
    auto_progression_id: str
    candidate_release_id: str
    current_stage: str
    proposed_next_stage: Optional[str]
    decision_type: AutoDecisionType
    eligibility_status: EligibilityStatus
    heuristic_score: Optional[HeuristicScoreRecord] = None
    safety_clearance_status: bool
    approval_requirement_status: str
    blockers: List[ProgressionBlockerRecord] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    warnings: List[str] = Field(default_factory=list)

class AutoKillDecisionRecord(BaseModel):
    auto_kill_id: str
    candidate_release_id: str
    kill_reason_code: KillReasonCode
    current_stage: str
    supporting_failures: List[str]
    confidence_in_kill: float
    reversible: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    warnings: List[str] = Field(default_factory=list)

class AutoHoldDecisionRecord(BaseModel):
    auto_hold_id: str
    candidate_release_id: str
    hold_reason_code: HoldReasonCode
    current_stage: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProgressionQuotaRecord(BaseModel):
    max_progressions: int
    max_kills: int
    used_progressions: int = 0
    used_kills: int = 0

class AutoPromotionSummaryRecord(BaseModel):
    total_evaluated: int
    eligible_for_auto_progress_count: int
    auto_progress_count: int
    auto_hold_count: int
    auto_kill_count: int
    review_required_count: int
    safety_boundary_block_count: int
    quota_block_count: int
    fleet_suppression_count: int
    future_release_step_ready_count: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
