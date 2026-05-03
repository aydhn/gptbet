from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from enum import Enum


class RemediationLaneStatus(str, Enum):
    lane_defined = "lane_defined"
    lane_review_prepared = "lane_review_prepared"
    lane_awaiting_approval = "lane_awaiting_approval"
    lane_approved_for_rehearsal = "lane_approved_for_rehearsal"
    lane_rehearsal_verified = "lane_rehearsal_verified"
    lane_token_issuable = "lane_token_issuable"
    lane_token_issued = "lane_token_issued"
    lane_ready_for_staged_execution = "lane_ready_for_staged_execution"
    lane_execution_window_open = "lane_execution_window_open"
    lane_closed_loop_verifying = "lane_closed_loop_verifying"
    lane_completed_verified = "lane_completed_verified"
    lane_blocked = "lane_blocked"
    lane_expired = "lane_expired"
    lane_superseded = "lane_superseded"
    lane_archived = "lane_archived"


class BoundedExecutionTokenFamily(str, Enum):
    rehearsal_execution_token = "rehearsal_execution_token"
    staged_execution_token = "staged_execution_token"
    review_only_execution_token = "review_only_execution_token"
    federated_adaptation_token = "federated_adaptation_token"
    read_only_observation_token = "read_only_observation_token"
    rollback_only_token = "rollback_only_token"


class LoopClosureOutcome(str, Enum):
    closed_clean = "closed_clean"
    closed_with_caveats = "closed_with_caveats"
    closure_incomplete = "closure_incomplete"
    closure_failed = "closure_failed"
    rollback_recommended = "rollback_recommended"
    review_required_after_closure = "review_required_after_closure"


class LaneEligibilityResult(str, Enum):
    not_eligible = "not_eligible"
    review_only_eligible = "review_only_eligible"
    rehearsal_only_eligible = "rehearsal_only_eligible"
    staged_execution_eligible = "staged_execution_eligible"
    token_issuable = "token_issuable"
    blocked_by_safety = "blocked_by_safety"
    stale_eligibility = "stale_eligibility"


class RemediationLaneRecord(BaseModel):
    lane_id: str
    lane_family: str
    incident_family: str
    scoped_playbook_ref: str
    readiness_ref: Optional[str] = None
    current_status: RemediationLaneStatus = RemediationLaneStatus.lane_defined
    allowed_step_families: List[str] = Field(default_factory=list)
    forbidden_step_families: List[str] = Field(default_factory=list)
    rollback_ref: Optional[str] = None
    observability_ref: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class LaneDefinitionRecord(BaseModel):
    lane_id: str
    definition_id: str

class LaneEligibilityRecord(BaseModel):
    lane_ref: str
    eligibility_result: LaneEligibilityResult
    confidence_score: float = 0.0

class LaneExecutionWindowRecord(BaseModel):
    lane_ref: str
    window_id: str

class LaneScopeRecord(BaseModel):
    lane_ref: str
    scope_id: str

class LaneRiskBandRecord(BaseModel):
    lane_ref: str
    risk_band: str

class BoundedExecutionTokenRecord(BaseModel):
    token_id: str
    token_family: BoundedExecutionTokenFamily
    bound_lane_ref: str
    allowed_step_families: List[str] = Field(default_factory=list)
    allowed_scope: Dict[str, Any] = Field(default_factory=dict)
    issued_from_approval_ref: Optional[str] = None
    valid_from: datetime
    valid_until: datetime
    max_execution_window: int = 3600
    required_guards: List[str] = Field(default_factory=list)
    status: str = "issued"
    warnings: List[str] = Field(default_factory=list)

class ExecutionTokenConstraintRecord(BaseModel):
    token_ref: str
    constraint_id: str

class ExecutionTokenValidationRecord(BaseModel):
    token_ref: str
    is_valid: bool

class ReviewAwareExecutionRecord(BaseModel):
    execution_id: str

class ClosedLoopReadinessGateRecord(BaseModel):
    gate_id: str
    lane_ref: str
    required_checkpoints: List[str] = Field(default_factory=list)
    required_observability_signals: List[str] = Field(default_factory=list)
    required_rollback_checks: List[str] = Field(default_factory=list)
    required_review_state: str = ""
    gate_status: str = "pending"
    blocking_reasons: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class LoopClosureRecord(BaseModel):
    closure_id: str
    lane_ref: str
    outcome: LoopClosureOutcome
    evidence_refs: List[str] = Field(default_factory=list)
    verified_at: datetime = Field(default_factory=datetime.utcnow)

class LoopClosureEvidenceRecord(BaseModel):
    evidence_id: str
    closure_ref: str

class LoopClosureDecisionRecord(BaseModel):
    decision_id: str
    closure_ref: str

class FederatedPlaybookCatalogRecordV2(BaseModel):
    catalog_id: str
    listings: List[Dict[str, Any]] = Field(default_factory=list)

class PlaybookCatalogLaneEntryRecord(BaseModel):
    entry_id: str
    catalog_ref: str

class PlaybookExchangeListingRecord(BaseModel):
    listing_id: str
    catalog_ref: str

class LaneApprovalBindingRecord(BaseModel):
    binding_id: str
    lane_ref: str

class LaneCheckpointRecord(BaseModel):
    checkpoint_id: str
    lane_ref: str

class LaneStopConditionRecord(BaseModel):
    condition_id: str
    lane_ref: str

class LaneRollbackBindingRecord(BaseModel):
    binding_id: str
    lane_ref: str

class LaneAuditRecord(BaseModel):
    audit_id: str
    lane_ref: str

class RecoveryLaneManifest(BaseModel):
    manifest_id: str
    lanes: List[RemediationLaneRecord] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class LaneWarningRecord(BaseModel):
    warning_id: str
    lane_ref: str

class ReviewStateBindingRecord(BaseModel):
    binding_id: str

class ReviewRestrictionProjectionRecord(BaseModel):
    projection_id: str

class ReviewChangeImpactRecord(BaseModel):
    impact_id: str

class ReviewExecutionEligibilityRecord(BaseModel):
    eligibility_id: str

class RollbackBindingRecord(BaseModel):
    binding_id: str

class RollbackLaneCompatibilityRecord(BaseModel):
    compatibility_id: str

class RollbackReadinessProjectionRecord(BaseModel):
    projection_id: str

class PlaybookExchangeCatalogRecord(BaseModel):
    catalog_id: str

class PlaybookCatalogIndexRecord(BaseModel):
    index_id: str

class PlaybookListingRecord(BaseModel):
    listing_id: str

class PlaybookListingVisibilityRecord(BaseModel):
    visibility_id: str

class PlaybookListingTrustRecord(BaseModel):
    trust_id: str

class LaneAutomationCandidateRecord(BaseModel):
    candidate_id: str

class TokenTemplateRecord(BaseModel):
    template_id: str

class FutureAutomationEnvelopeRecord(BaseModel):
    envelope_id: str

class AutomationPreparationGateRecord(BaseModel):
    gate_id: str

class AutomationPreparationDecisionRecord(BaseModel):
    decision_id: str
