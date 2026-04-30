import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AdoptionStatus(str, Enum):
    ADOPTION_CANDIDATE_IDENTIFIED = "adoption_candidate_identified"
    PENDING_ACTIVATION_COUNCIL = "pending_activation_council"
    PENDING_FINAL_APPROVAL = "pending_final_approval"
    STABLE_POINTER_ADVANCE_READY = "stable_pointer_advance_ready"
    STABLE_POINTER_ADVANCED = "stable_pointer_advanced"
    PENDING_POST_ACTIVATION_VERIFICATION = "pending_post_activation_verification"
    POST_ACTIVATION_VERIFIED = "post_activation_verified"
    POST_ACTIVATION_WARNING = "post_activation_warning"
    ROLLBACK_REQUIRED = "rollback_required"
    ROLLBACK_EXECUTED = "rollback_executed"
    ROLLBACK_FAILED = "rollback_failed"
    ADOPTION_COMPLETED = "adoption_completed"
    ADOPTION_HOLD = "adoption_hold"
    ADOPTION_BLOCKED = "adoption_blocked"
    ADOPTION_REJECTED = "adoption_rejected"
    ADOPTION_SUPERSEDED = "adoption_superseded"

class ActivationDecisionType(str, Enum):
    APPROVE_ACTIVATION = "approve_activation"
    HOLD_ACTIVATION = "hold_activation"
    REJECT_ACTIVATION = "reject_activation"
    REQUIRE_MORE_EVIDENCE = "require_more_evidence"
    REQUIRE_MORE_GATES = "require_more_gates"
    REQUIRE_NARROWER_SCOPE = "require_narrower_scope"
    EXECUTE_LIMITED_STABLE_ADVANCEMENT = "execute_limited_stable_advancement"
    ROLLBACK_TO_PREVIOUS_STABLE = "rollback_to_previous_stable"
    KEEP_CURRENT_STABLE = "keep_current_stable"
    SUPERSEDE_ADOPTION_CANDIDATE = "supersede_adoption_candidate"
    APPROVE_LIMITED_ADVANCEMENT_ONLY = "approve_limited_advancement_only"
    ROLLBACK_REQUIRED_PREEMPTIVELY = "rollback_required_preemptively"
    REQUIRE_MORE_CONSTRAINTS = "require_more_constraints"

class AdvancementMode(str, Enum):
    FAMILY_SCOPED_POINTER_ADVANCE = "family_scoped_pointer_advance"
    MARKET_SCOPED_POINTER_ADVANCE = "market_scoped_pointer_advance"
    NARROW_BUNDLE_POINTER_ADVANCE = "narrow_bundle_pointer_advance"
    ADVISORY_SHADOW_REFERENCE_ONLY = "advisory_shadow_reference_only"
    BLOCKED_NO_ADVANCE = "blocked_no_advance"

class VerificationWindow(str, Enum):
    IMMEDIATE_VERIFICATION = "immediate_verification"
    EARLY_WINDOW_VERIFICATION = "early_window_verification"
    EXTENDED_WINDOW_VERIFICATION = "extended_window_verification"

class VerificationOutcomeType(str, Enum):
    VERIFIED_CLEAN = "verified_clean"
    VERIFIED_WITH_WARNINGS = "verified_with_warnings"
    DEGRADED_BUT_TOLERABLE = "degraded_but_tolerable"
    ROLLBACK_RECOMMENDED = "rollback_recommended"
    ROLLBACK_REQUIRED = "rollback_required"
    INVALID_ACTIVATION_STATE = "invalid_activation_state"

class RollbackType(str, Enum):
    ROLLBACK_TO_PREVIOUS_STABLE = "rollback_to_previous_stable"
    ROLLBACK_FAMILY_SCOPE_ONLY = "rollback_family_scope_only"
    ROLLBACK_BUNDLE_SCOPE_ONLY = "rollback_bundle_scope_only"
    ROLLBACK_DUE_TO_VERIFICATION_FAILURE = "rollback_due_to_verification_failure"
    ROLLBACK_DUE_TO_BLOCKER_DISCOVERED_POST_ACTIVATION = "rollback_due_to_blocker_discovered_post_activation"

class StableAdoptionRecord(BaseModel):
    adoption_id: str
    handoff_id: str
    candidate_release_id: str
    activation_bridge_id: str
    target_component_family: str
    adoption_scope: str
    current_status: AdoptionStatus
    proposed_stable_pointer_target: str
    previous_stable_pointer_ref: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    warnings: List[str] = Field(default_factory=list)

class ActivationCouncilRecord(BaseModel):
    council_id: str
    adoption_id: str
    lenses: Dict[str, Any] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

class ActivationDecisionRecord(BaseModel):
    activation_decision_id: str
    adoption_id: str
    decision_type: ActivationDecisionType
    decision_status: str
    council_ref: str
    blocker_refs: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)
    approval_status: str
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    warnings: List[str] = Field(default_factory=list)

class StablePointerAdvanceRecord(BaseModel):
    advance_id: str
    adoption_id: str
    old_stable_pointer_ref: str
    new_stable_pointer_ref: str
    advancement_mode: AdvancementMode
    limited_scope_notes: List[str] = Field(default_factory=list)
    performed_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    rollback_target_ref: str
    warnings: List[str] = Field(default_factory=list)

class PostActivationVerificationRecord(BaseModel):
    verification_id: str
    adoption_id: str
    window: VerificationWindow
    checks: List[str] = Field(default_factory=list)
    overall_outcome: VerificationOutcomeType
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

class PostActivationCheckRecord(BaseModel):
    check_id: str
    verification_id: str
    check_type: str
    passed: bool
    details: str

class AdoptionRollbackRecord(BaseModel):
    rollback_id: str
    adoption_id: str
    rollback_type: RollbackType
    target_snapshot_ref: str
    reason: str
    executed_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    warnings: List[str] = Field(default_factory=list)

class AdoptionLifecycleRecord(BaseModel):
    lifecycle_id: str
    adoption_id: str
    events: List[Dict[str, Any]] = Field(default_factory=list)

class AdoptionSummaryRecord(BaseModel):
    summary_id: str
    candidate_count: int = 0
    approve_count: int = 0
    hold_count: int = 0
    reject_count: int = 0
    pointer_advancements_count: int = 0
    post_activation_clean_count: int = 0
    post_activation_warning_count: int = 0
    post_activation_fail_count: int = 0
    rollback_count: int = 0
    blockers_distribution: Dict[str, int] = Field(default_factory=dict)
    rollback_readiness_coverage: float = 0.0

class AdoptionManifest(BaseModel):
    manifest_id: str
    adoptions: List[StableAdoptionRecord] = Field(default_factory=list)
    summary: AdoptionSummaryRecord
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

class ActivationConstraintRecord(BaseModel):
    constraint_id: str
    adoption_id: str
    constraint_type: str
    description: str

class AdoptionRiskReviewRecord(BaseModel):
    review_id: str
    adoption_id: str
    risk_level: str
    factors: List[str]

class StableReferenceSnapshotRecord(BaseModel):
    snapshot_id: str
    adoption_id: str
    stable_pointers: Dict[str, str] = Field(default_factory=dict)
    manifest_refs: List[str] = Field(default_factory=list)
    captured_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

class ActivationAuditRecord(BaseModel):
    audit_id: str
    adoption_id: str
    action: str
    details: Dict[str, Any]

class AdoptionBlockerRecord(BaseModel):
    blocker_id: str
    adoption_id: str
    blocker_family: str
    severity: str
    reversibility: str
    description: str

class AdoptionEvidenceMatrixRecord(BaseModel):
    evidence_matrix_id: str
    adoption_id: str
    citations: List[str] = Field(default_factory=list)
    explanations: Dict[str, str] = Field(default_factory=dict)

class RollbackReadinessRecord(BaseModel):
    readiness_id: str
    adoption_id: str
    is_ready: bool
    missing_criteria: List[str] = Field(default_factory=list)
    snapshot_ref: Optional[str] = None

class VerificationWindowRecord(BaseModel):
    window_id: str
    window_type: VerificationWindow
    start_time: datetime.datetime
    end_time: datetime.datetime

class VerificationOutcomeRecord(BaseModel):
    outcome_id: str
    verification_id: str
    outcome_type: VerificationOutcomeType
    notes: str

class VerificationRegressionRecord(BaseModel):
    regression_id: str
    verification_id: str
    metric: str
    degradation: float

class VerificationAlertRecord(BaseModel):
    alert_id: str
    verification_id: str
    alert_type: str
    message: str

class RollbackTriggerRecord(BaseModel):
    trigger_id: str
    adoption_id: str
    trigger_type: str

class RollbackExecutionPlanRecord(BaseModel):
    plan_id: str
    adoption_id: str
    steps: List[str]

class RollbackVerificationRecord(BaseModel):
    verification_id: str
    rollback_id: str
    is_successful: bool

class RollbackReasonRecord(BaseModel):
    reason_id: str
    rollback_id: str
    rationale: str

class ActivationChecklistItemRecord(BaseModel):
    item_id: str
    description: str
    is_checked: bool
    notes: str = ""

class ActivationChecklistResultRecord(BaseModel):
    checklist_id: str
    adoption_id: str
    items: List[ActivationChecklistItemRecord] = Field(default_factory=list)
    is_complete: bool

class ActivationChecklistFailureRecord(BaseModel):
    failure_id: str
    checklist_id: str
    reason: str
