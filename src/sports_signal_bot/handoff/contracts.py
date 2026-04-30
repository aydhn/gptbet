from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class HandoffStatus(str, Enum):
    HANDOFF_CANDIDATE_IDENTIFIED = "handoff_candidate_identified"
    PENDING_FINAL_READINESS_REVIEW = "pending_final_readiness_review"
    PENDING_COUNCIL_EVALUATION = "pending_council_evaluation"
    HANDOFF_READY = "handoff_ready"
    HANDOFF_HOLD = "handoff_hold"
    HANDOFF_REVISE = "handoff_revise"
    HANDOFF_REJECTED = "handoff_rejected"
    CANDIDATE_KILLED_BEFORE_HANDOFF = "candidate_killed_before_handoff"
    HANDOFF_SUPERSEDED = "handoff_superseded"
    HANDOFF_EXPIRED = "handoff_expired"
    HANDOFF_PACKAGE_EMITTED = "handoff_package_emitted"

class CouncilDecisionType(str, Enum):
    APPROVE_HANDOFF = "approve_handoff"
    HOLD_FOR_MORE_EVIDENCE = "hold_for_more_evidence"
    REQUIRE_ADDITIONAL_GATES = "require_additional_gates"
    REQUIRE_ADDITIONAL_SIMULATION = "require_additional_simulation"
    REQUIRE_ADDITIONAL_REVIEW = "require_additional_review"
    REJECT_HANDOFF = "reject_handoff"
    KILL_CANDIDATE_BEFORE_HANDOFF = "kill_candidate_before_handoff"
    SUPERSEDE_WITH_BETTER_HANDOFF_CANDIDATE = "supersede_with_better_handoff_candidate"
    NARROW_SCOPE_AND_RETRY = "narrow_scope_and_retry"
    READY_FOR_ACTIVATION_BRIDGE_ONLY = "ready_for_activation_bridge_only"

    # Internal council aggregated outcomes
    UNANIMOUS_APPROVE = "unanimous_approve"
    APPROVE_WITH_CAVEATS = "approve_with_caveats"
    MIXED_HOLD = "mixed_hold"

class HandoffKillReason(str, Enum):
    STALE_CANDIDATE_PACKAGE = "stale_candidate_package"
    UNRESOLVED_CRITICAL_BLOCKERS = "unresolved_critical_blockers"
    WEAK_EVIDENCE_AT_FINAL_STAGE = "weak_evidence_at_final_stage"
    SUPERSEDED_BY_NARROWER_SAFER_CANDIDATE = "superseded_by_narrower_safer_candidate"
    FAILED_FRESH_GATE_REQUIREMENTS = "failed_fresh_gate_requirements"
    CONTRADICTORY_COUNCIL_DIMENSIONS = "contradictory_council_dimensions"
    UNSTABLE_STAGE_HISTORY = "unstable_stage_history"
    INCOMPLETE_ROLLBACK_NOTES = "incomplete_rollback_notes"
    ACTIVATION_RISK_EXCEEDS_SCOPE_VALUE = "activation_risk_exceeds_scope_value"
    MISSING_FINAL_APPROVAL_WITH_EXPIRED_WINDOW = "missing_final_approval_with_expired_window"
    NOT_KILLED = "not_killed"

class AdoptionReadinessStatus(str, Enum):
    NOT_READY = "not_ready"
    BRIDGE_READY = "bridge_ready"
    ACTIVATION_REVIEW_READY = "activation_review_ready"
    BLOCKED_FOR_ACTIVATION = "blocked_for_activation"
    NEEDS_MORE_CONSTRAINTS = "needs_more_constraints"

class ReadinessBand(str, Enum):
    FAIL = "fail"
    WARN = "warn"
    PASS = "pass"
    BLOCKED = "blocked"

class HandoffCandidateRecord(BaseModel):
    handoff_candidate_id: str
    candidate_release_id: str
    candidate_bundle_id: Optional[str] = None
    target_component_family: str
    current_channel: str
    current_stage: str
    readiness_band: ReadinessBand = ReadinessBand.WARN
    warnings: List[str] = Field(default_factory=list)

class ReleaseHandoffRecord(BaseModel):
    handoff_id: str
    candidate_release_id: str
    candidate_bundle_id: Optional[str] = None
    target_component_family: str
    current_channel: str
    current_stage: str
    readiness_band: str
    handoff_status: HandoffStatus
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    warnings: List[str] = Field(default_factory=list)

class FinalReadinessCouncilRecord(BaseModel):
    council_id: str
    handoff_candidate_ids: List[str]
    evaluation_scope: str
    evaluation_window: Dict[str, Any]
    readiness_matrix: Dict[str, Any] = Field(default_factory=dict)
    blocker_summary: Dict[str, Any] = Field(default_factory=dict)
    recommended_outcomes: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    warnings: List[str] = Field(default_factory=list)

class CouncilDecisionRecord(BaseModel):
    decision_id: str
    handoff_id: str
    decision_type: CouncilDecisionType
    decision_status: str
    blocker_refs: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)
    required_followups: List[str] = Field(default_factory=list)
    approval_status: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    warnings: List[str] = Field(default_factory=list)

class HandoffBridgeRecord(BaseModel):
    bridge_id: str
    handoff_id: str
    candidate_package_refs: List[str] = Field(default_factory=list)
    council_decision_ref: str
    adoption_scope_hints: List[str] = Field(default_factory=list)

class ActivationPrerequisiteRecord(BaseModel):
    prerequisite_id: str
    description: str
    met: bool

class AdoptionReadinessRecord(BaseModel):
    adoption_id: str
    handoff_id: str
    status: AdoptionReadinessStatus
    blockers: List[str] = Field(default_factory=list)
    hints: List[str] = Field(default_factory=list)

class HandoffBlockerRecord(BaseModel):
    blocker_id: str
    handoff_id: str
    severity: str
    description: str

class HandoffPackageRecord(BaseModel):
    package_id: str
    handoff_id: str
    candidate_release_package_ref: str
    council_decision: Dict[str, Any] = Field(default_factory=dict)
    readiness_matrix: Dict[str, Any] = Field(default_factory=dict)
    evidence_bundle_refs: List[str] = Field(default_factory=list)
    simulation_refs: List[str] = Field(default_factory=list)
    gate_matrix: Dict[str, Any] = Field(default_factory=dict)
    approval_ledger_refs: List[str] = Field(default_factory=list)
    rollout_history: Dict[str, Any] = Field(default_factory=dict)
    rollback_notes: List[str] = Field(default_factory=list)
    activation_constraints: List[str] = Field(default_factory=list)
    adoption_readiness_hints: List[str] = Field(default_factory=list)
    post_handoff_verification_plan: str

class HandoffSummaryRecord(BaseModel):
    summary_id: str
    total_candidates_evaluated: int
    approve_count: int
    hold_count: int
    reject_count: int
    kill_count: int
    bridge_ready_count: int
    activation_blocker_count: int
    superseded_handoff_candidate_count: int
    top_blocker_families: List[str] = Field(default_factory=list)
    readiness_dimension_distribution: Dict[str, int] = Field(default_factory=dict)

class HandoffManifest(BaseModel):
    manifest_id: str
    packages: List[HandoffPackageRecord] = Field(default_factory=list)
    summary: Optional[HandoffSummaryRecord] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CouncilVoteLikeRecord(BaseModel):
    vote_id: str
    lens_name: str
    recommendation: CouncilDecisionType
    blockers: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
    refs: List[str] = Field(default_factory=list)

class HandoffEvidenceMatrixRecord(BaseModel):
    evidence_matrix_id: str
    handoff_id: str
    citations: List[str] = Field(default_factory=list)
    explanations: Dict[str, str] = Field(default_factory=dict)

class HandoffRiskReviewRecord(BaseModel):
    risk_review_id: str
    handoff_id: str
    risk_score: float
    high_risk_areas: List[str] = Field(default_factory=list)

class PreActivationCheckItemRecord(BaseModel):
    item_id: str
    description: str
    is_checked: bool
    notes: str = ""

class PreActivationChecklistResult(BaseModel):
    checklist_id: str
    handoff_id: str
    items: List[PreActivationCheckItemRecord] = Field(default_factory=list)
    is_complete: bool

class StableAdoptionHintRecord(BaseModel):
    hint_id: str
    handoff_id: str
    hint_text: str

class HandoffAuditRecord(BaseModel):
    audit_id: str
    handoff_id: str
    action: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str
    details: Dict[str, Any] = Field(default_factory=dict)

# Helper Models for Council Dimensions
class CouncilDimensionScoreRecord(BaseModel):
    dimension_name: str
    score: float
    band: ReadinessBand
    blockers: List[str] = Field(default_factory=list)
    caveats: List[str] = Field(default_factory=list)
    supporting_refs: List[str] = Field(default_factory=list)

class CouncilBlockerMatrixRecord(BaseModel):
    matrix_id: str
    handoff_id: str
    dimension: str
    blockers: List[str] = Field(default_factory=list)

class CouncilCaveatRecord(BaseModel):
    caveat_id: str
    handoff_id: str
    description: str

class CouncilRecommendationRecord(BaseModel):
    recommendation_id: str
    handoff_id: str
    recommendation: CouncilDecisionType
    rationale: str

# Activation Bridge
class ActivationBridgePackageRecord(BaseModel):
    bridge_package_id: str
    handoff_id: str
    candidate_package_refs: List[str] = Field(default_factory=list)
    council_decision_ref: str
    required_final_approvals: List[str] = Field(default_factory=list)
    required_post_handoff_checks: List[str] = Field(default_factory=list)
    adoption_scope_hints: List[str] = Field(default_factory=list)
    rollback_safety_notes: List[str] = Field(default_factory=list)
    activation_constraints: List[str] = Field(default_factory=list)
    do_not_activate_reasons: List[str] = Field(default_factory=list)

class BridgeConstraintRecord(BaseModel):
    constraint_id: str
    bridge_package_id: str
    constraint_type: str
    value: str

class BridgeApprovalRequirementRecord(BaseModel):
    approval_requirement_id: str
    bridge_package_id: str
    role: str

class BridgeRollbackNoteRecord(BaseModel):
    note_id: str
    bridge_package_id: str
    note: str

class BridgeTransferSummaryRecord(BaseModel):
    transfer_id: str
    bridge_package_id: str
    status: str

# Activation Blockers
class ActivationBlockerRecord(BaseModel):
    blocker_id: str
    handoff_id: str
    description: str

# Hold / Revise / Reject Model
class HandoffFollowupActionRecord(BaseModel):
    action_id: str
    handoff_id: str
    action_type: str
    description: str

class HandoffRevisionRequestRecord(BaseModel):
    request_id: str
    handoff_id: str
    requested_changes: List[str] = Field(default_factory=list)

class HandoffHoldReasonRecord(BaseModel):
    reason_id: str
    handoff_id: str
    reason: str
