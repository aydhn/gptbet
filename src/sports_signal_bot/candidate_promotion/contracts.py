from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ..simulation.contracts import RiskLevel
from ..tournaments.contracts import ShortlistTier

class CandidateState(str, Enum):
    SHORTLISTED = "shortlisted"
    CANDIDATE_CREATED = "candidate_created"
    PENDING_STAGE_VALIDATION = "pending_stage_validation"
    SIMULATION_VERIFIED = "simulation_verified"
    PENDING_QUALITY_GATES = "pending_quality_gates"
    QUALITY_GATES_PASSED = "quality_gates_passed"
    PENDING_REVIEW = "pending_review"
    PENDING_APPROVAL = "pending_approval"
    CANDIDATE_READY = "candidate_ready"
    CANDIDATE_HOLD = "candidate_hold"
    CANDIDATE_REVISE = "candidate_revise"
    CANDIDATE_KILLED = "candidate_killed"
    CANDIDATE_SUPERSEDED = "candidate_superseded"
    CANDIDATE_EXPIRED = "candidate_expired"
    CANDIDATE_PROMOTE_RECOMMENDED = "candidate_promote_recommended"
    CANDIDATE_PROMOTE_BLOCKED = "candidate_promote_blocked"

class CandidateLane(str, Enum):
    FAST_SAFE_CANDIDATE_LANE = "fast_safe_candidate_lane"
    STANDARD_CANDIDATE_LANE = "standard_candidate_lane"
    HIGH_RISK_REVIEW_LANE = "high_risk_review_lane"
    REVISE_AND_RETRY_LANE = "revise_and_retry_lane"
    BLOCKED_CANDIDATE_LANE = "blocked_candidate_lane"
    KILL_LANE = "kill_lane"

class CandidateReadinessBand(str, Enum):
    NOT_READY = "not_ready"
    CONDITIONALLY_READY = "conditionally_ready"
    REVIEW_READY = "review_ready"
    APPROVAL_READY = "approval_ready"
    RELEASE_CANDIDATE_READY = "release_candidate_ready"
    BLOCKED_NOT_READY = "blocked_not_ready"

class FinalDecisionAction(str, Enum):
    PROMOTE_CANDIDATE_LANE = "promote_candidate_lane"
    HOLD_CANDIDATE = "hold_candidate"
    REVISE_CANDIDATE = "revise_candidate"
    KILL_CANDIDATE = "kill_candidate"
    SUPERSEDE_CANDIDATE = "supersede_candidate"
    BLOCK_PROMOTION = "block_promotion"
    REQUEST_MORE_EVIDENCE = "request_more_evidence"
    REQUEST_ADDITIONAL_SIMULATION = "request_additional_simulation"
    REQUEST_NARROWER_SCOPE = "request_narrower_scope"

class KillReason(str, Enum):
    KILL_DUE_TO_SAFETY = "kill_due_to_safety"
    KILL_DUE_TO_FAILED_GATES = "kill_due_to_failed_gates"
    KILL_DUE_TO_INCONCLUSIVE_BENEFIT = "kill_due_to_inconclusive_benefit"
    KILL_DUE_TO_BETTER_SUCCESSOR = "kill_due_to_better_successor"
    NOT_KILLED = "not_killed"

class HoldReason(str, Enum):
    HOLD_DUE_TO_MISSING_APPROVAL = "hold_due_to_missing_approval"
    HOLD_DUE_TO_GATE_BACKLOG = "hold_due_to_gate_backlog"
    NOT_HELD = "not_held"

class ReviseReason(str, Enum):
    REVISE_DUE_TO_SCOPE_TOO_BROAD = "revise_due_to_scope_too_broad"
    REVISE_DUE_TO_LOW_SUPPORT = "revise_due_to_low_support"
    REVISE_DUE_TO_CONFLICTING_EVIDENCE = "revise_due_to_conflicting_evidence"
    REVISE_DUE_TO_SIMULATION_UNFAIRNESS = "revise_due_to_simulation_unfairness"
    NOT_REVISED = "not_revised"

class CandidateWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str

class CandidateReleaseRecord(BaseModel):
    candidate_release_id: str
    suggestion_id: str
    patch_id: str
    tournament_ref: str
    target_component_family: str
    scope: Dict[str, Any]
    risk_level: RiskLevel
    support_strength: float
    confidence_band: str
    current_state: CandidateState = CandidateState.CANDIDATE_CREATED
    lane: Optional[CandidateLane] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[CandidateWarningRecord] = Field(default_factory=list)

class CandidateBundleRecord(BaseModel):
    candidate_bundle_id: str
    included_candidate_ids: List[str]
    target_family: str
    patch_payloads: List[Dict[str, Any]]
    simulation_refs: List[str]
    evidence_refs: List[str]
    gate_requirements: List[str]
    approval_requirements: List[str]
    release_notes_summary: str
    bundle_status: str
    warnings: List[CandidateWarningRecord] = Field(default_factory=list)

class CandidateStateRecord(BaseModel):
    state_id: str
    candidate_id: str
    current_state: CandidateState
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ValidationStageDefinition(BaseModel):
    stage_id: str
    stage_name: str
    required_for_family: List[str]

class StageCheckRecord(BaseModel):
    check_id: str
    description: str
    passed: bool

class CandidateValidationStageRecord(BaseModel):
    validation_id: str
    candidate_id: str
    stage_id: str
    passed: bool
    checks: List[StageCheckRecord] = Field(default_factory=list)

class CandidateGateResultRecord(BaseModel):
    gate_result_id: str
    candidate_id: str
    passed: bool
    failures: List[str]

class CandidateReadinessRecord(BaseModel):
    readiness_id: str
    candidate_id: str
    readiness_band: CandidateReadinessBand
    missing_requirements: List[str]

class CandidatePromotionDecisionRecord(BaseModel):
    decision_id: str
    candidate_id: str
    action: FinalDecisionAction
    rationale: str
    lane: CandidateLane

class CandidateKillDecisionRecord(BaseModel):
    decision_id: str
    candidate_id: str
    reason: KillReason
    rationale: str

class CandidateLifecycleRecord(BaseModel):
    lifecycle_id: str
    candidate_id: str
    transitions: List[Dict[str, Any]]

class CandidateSummaryRecord(BaseModel):
    candidate_id: str
    final_state: CandidateState
    action: FinalDecisionAction

class CandidateManifest(BaseModel):
    manifest_id: str
    candidates: List[CandidateReleaseRecord]
    decisions: List[CandidatePromotionDecisionRecord]
    readiness: List[CandidateReadinessRecord]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CandidateStageTransitionRecord(BaseModel):
    transition_id: str
    from_state: CandidateState
    to_state: CandidateState

class CandidateDependencyRecord(BaseModel):
    dependency_id: str
    candidate_id: str
    depends_on_candidate_id: str

class CandidateEvidenceRecord(BaseModel):
    evidence_id: str
    candidate_id: str
    citations: List[str]

class CandidateReleasePlanRecord(BaseModel):
    plan_id: str
    candidate_id: str
    target_channel: str

class CandidateReviewOutcomeRecord(BaseModel):
    review_id: str
    candidate_id: str
    approved: bool
    reviewer: str

class StageFailureRecord(BaseModel):
    failure_id: str
    candidate_id: str
    stage_id: str
    reason: str

class StagePassRecord(BaseModel):
    pass_id: str
    candidate_id: str
    stage_id: str

class StageBypassRecord(BaseModel):
    bypass_id: str
    candidate_id: str
    stage_id: str
    reason: str

class CandidateConflictRecord(BaseModel):
    conflict_id: str
    candidate_id_1: str
    candidate_id_2: str

class CandidateSupersessionRecord(BaseModel):
    supersession_id: str
    superseded_candidate_id: str
    superseding_candidate_id: str

class CandidatePrerequisiteRecord(BaseModel):
    prerequisite_id: str
    candidate_id: str
    required_candidate_id: str

class CandidateReleasePackageRecord(BaseModel):
    package_id: str
    candidate_id: str
    payload: Dict[str, Any]
    target_channels: List[str]

class CandidatePromotionDraftRecord(BaseModel):
    draft_id: str
    candidate_id: str

class CandidateCanaryPrepRecord(BaseModel):
    prep_id: str
    candidate_id: str
