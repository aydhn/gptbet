from datetime import datetime, timezone
from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class LaneFamily(str, Enum):
    containment_lane = "containment_lane"
    replay_recovery_lane = "replay_recovery_lane"
    reroute_lane = "reroute_lane"
    overlay_repair_lane = "overlay_repair_lane"
    supersession_repair_lane = "supersession_repair_lane"
    freshness_repair_lane = "freshness_repair_lane"
    quarantine_reentry_lane = "quarantine_reentry_lane"
    relay_stabilization_lane = "relay_stabilization_lane"
    degraded_mode_exit_lane = "degraded_mode_exit_lane"
    review_only_investigation_lane = "review_only_investigation_lane"

class LaneStatus(str, Enum):
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
    lane_archived = "lane_archived"

class TokenFamily(str, Enum):
    rehearsal_execution_token = "rehearsal_execution_token"
    staged_execution_token = "staged_execution_token"
    review_only_execution_token = "review_only_execution_token"
    federated_adaptation_token = "federated_adaptation_token"
    read_only_observation_token = "read_only_observation_token"
    rollback_only_token = "rollback_only_token"

class LaneEligibilityOutcome(str, Enum):
    not_eligible = "not_eligible"
    review_only_eligible = "review_only_eligible"
    rehearsal_only_eligible = "rehearsal_only_eligible"
    staged_execution_eligible = "staged_execution_eligible"
    token_issuable = "token_issuable"
    blocked_by_safety = "blocked_by_safety"

class ClosureOutcome(str, Enum):
    closed_clean = "closed_clean"
    closed_with_caveats = "closed_with_caveats"
    closure_incomplete = "closure_incomplete"
    closure_failed = "closure_failed"
    rollback_recommended = "rollback_recommended"
    review_required_after_closure = "review_required_after_closure"

class RollbackBindingRecord(BaseModel):
    rollback_playbook_ref: str
    rollback_scope: str
    rollback_checkpoints: List[str]
    is_verified_in_rehearsal: bool = False

class RemediationLaneRecord(BaseModel):
    lane_id: str
    lane_family: LaneFamily
    incident_family: str
    scoped_playbook_ref: str
    readiness_ref: Optional[str] = None
    current_status: LaneStatus = LaneStatus.lane_defined
    allowed_step_families: List[str]
    forbidden_step_families: List[str]
    rollback_binding: RollbackBindingRecord
    observability_refs: List[str]
    warnings: List[str] = Field(default_factory=list)

class LaneEligibilityRecord(BaseModel):
    lane_id: str
    outcome: LaneEligibilityOutcome
    confidence_score: float
    is_reversible: bool
    has_explicit_rollback: bool
    has_strong_rehearsal_evidence: bool
    blockers: List[str]

class ReviewAwareExecutionRecord(BaseModel):
    lane_id: str
    approval_ref: str
    unresolved_caveats: int
    reviewer_restrictions: List[str]
    eligibility_downgraded: bool

class BoundedExecutionTokenRecord(BaseModel):
    token_id: str
    token_family: TokenFamily
    bound_lane_ref: str
    allowed_step_families: List[str]
    allowed_scope: str
    issued_from_approval_ref: str
    valid_from: datetime
    valid_until: datetime
    max_execution_window_seconds: int
    required_guards: List[str]
    status: str = "active"
    warnings: List[str] = Field(default_factory=list)

class ClosedLoopReadinessGateRecord(BaseModel):
    gate_id: str
    lane_ref: str
    required_checkpoints: List[str]
    required_observability_signals: List[str]
    required_rollback_checks: List[str]
    gate_status: str
    blocking_reasons: List[str]

class LaneCheckpointRecord(BaseModel):
    checkpoint_id: str
    lane_ref: str
    checkpoint_family: str
    observed_at: datetime
    is_aligned_with_expectation: bool

class LaneStopConditionRecord(BaseModel):
    condition_id: str
    lane_ref: str
    condition_family: str
    triggered: bool
    details: str

class LoopClosureRecord(BaseModel):
    closure_id: str
    lane_ref: str
    outcome: ClosureOutcome
    checkpoints_met: int
    total_checkpoints: int
    stop_conditions_triggered: int
    rollback_used: bool
    evidence_refs: List[str]
    warnings: List[str]

class PlaybookListingRecord(BaseModel):
    listing_id: str
    listing_family: str
    playbook_ref: str
    trust_domain: str
    supported_lane_families: List[LaneFamily]
    required_guards: List[str]
    has_rehearsal_evidence: bool
    portability_profile: str

class PlaybookExchangeCatalogRecord(BaseModel):
    catalog_id: str
    published_at: datetime
    listings: List[PlaybookListingRecord]
    catalog_health: str

class LaneAutomationCandidateRecord(BaseModel):
    candidate_id: str
    lane_family: LaneFamily
    scoped_playbook_ref: str
    successful_closures: int
    caveat_ratio: float
    is_approved_candidate: bool
    envelope_ref: Optional[str] = None
    reasons: List[str]

class LaneLedgerEntry(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    lane_id: str
    action: str
    details: str

class RemediationLanesManifest(BaseModel):
    manifest_id: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    active_lanes: List[RemediationLaneRecord]
    active_tokens: List[BoundedExecutionTokenRecord]
    readiness_gates: List[ClosedLoopReadinessGateRecord]
    closures: List[LoopClosureRecord]
    catalogs: List[PlaybookExchangeCatalogRecord]
    automation_candidates: List[LaneAutomationCandidateRecord]
    ledger: List[LaneLedgerEntry]
    summary: Dict[str, Any]
