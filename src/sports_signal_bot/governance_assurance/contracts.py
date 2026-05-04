from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

# --- COUNCIL ENUMS ---
class CouncilFamily(str, Enum):
    SYNTHESIS_BAND_REVIEW = "synthesis_band_review_council"
    DEBT_CEILING_REVIEW = "debt_ceiling_review_council"
    REPLAY_QUALITY_REVIEW = "replay_quality_review_council"
    SOVEREIGNTY_PRESERVATION_REVIEW = "sovereignty_preservation_review_council"
    NO_SAFE_VISIBILITY_REVIEW = "no_safe_visibility_review_council"
    RESTORATION_CAP_REVIEW = "restoration_cap_review_council"
    ASSURANCE_SUMMARY_REVIEW = "assurance_summary_review_council"

class CaseFamily(str, Enum):
    SYNTHESIZED_BAND_CONFLICT = "synthesized_band_conflict_case"
    DEBT_PENALTY_DISPUTE = "debt_penalty_dispute_case"
    REPLAY_QUALITY_MISMATCH = "replay_quality_mismatch_case"
    SOVEREIGNTY_CAP = "sovereignty_cap_case"
    NO_SAFE_VISIBILITY = "no_safe_visibility_case"
    RESTORATION_OVERCLAIM = "restoration_overclaim_case"
    DASHBOARD_PROJECTION = "dashboard_projection_case"

class CaseStatus(str, Enum):
    OPENED = "case_opened"
    COLLECTING_EVIDENCE = "case_collecting_evidence"
    QUORUM_PENDING = "case_quorum_pending"
    DECIDED = "case_decided"
    DECIDED_WITH_CAVEATS = "case_decided_with_caveats"
    REVIEW_ONLY = "case_review_only"
    BLOCKED = "case_blocked"
    SUPERSEDED = "case_superseded"
    ARCHIVED = "case_archived"

class CouncilDecisionType(str, Enum):
    PRESERVE_EXISTING_CAP = "preserve_existing_cap"
    DOWNGRADE_TO_REVIEW_ONLY = "downgrade_to_review_only_synthesis"
    AMPLIFY_CAVEATS = "amplify_caveats"
    REQUIRE_REPLAY_REVALIDATION = "require_replay_revalidation"
    REQUIRE_DEBT_REASSESSMENT = "require_debt_reassessment"
    REQUIRE_PORTFOLIO_REBALANCE = "require_portfolio_rebalance"
    PRESERVE_NO_SAFE_VISIBILITY = "preserve_no_safe_visibility"
    ACCEPT_BOUNDED_SCORE_WITH_CAPS = "accept_bounded_score_with_caps"
    BLOCK_DUE_TO_UNRESOLVED_CONFLICT = "block_due_to_unresolved_conflict"

# --- MARKETPLACE ENUMS ---
class ReplayMarketplaceFamily(str, Enum):
    INTERNAL_REPLAY = "internal_replay_marketplace"
    REVIEW_ONLY_REPLAY = "review_only_replay_marketplace"
    BOUNDED_REPLAY = "bounded_replay_marketplace"
    SUCCESSOR_SUPPORT = "successor_support_marketplace"
    EXCEPTION_SUPPORT = "exception_support_marketplace"
    DEGRADED_REPLAY = "degraded_replay_marketplace"
    AUDIT_SUPPORT = "audit_support_marketplace"

class ListingStatus(str, Enum):
    LISTED_CURRENT = "listed_current"
    LISTED_CAVEATED = "listed_caveated"
    LISTED_REVIEW_ONLY = "listed_review_only"
    LISTED_BACKPRESSURED = "listed_backpressured"
    LISTED_DEGRADED = "listed_degraded"
    LISTED_MATCHED = "listed_matched"
    LISTED_EXPIRED = "listed_expired"
    LISTED_SUPERSEDED = "listed_superseded"
    LISTED_BLOCKED = "listed_blocked"

class MatchOutcome(str, Enum):
    MATCHED_BOUNDED = "matched_bounded_replay"
    MATCHED_REVIEW_ONLY = "matched_review_only_replay"
    MATCHED_CAVEATED = "matched_caveated_replay"
    MATCHED_DEGRADED = "matched_degraded_replay"
    REPLAY_REVALIDATION_REQUIRED = "replay_revalidation_required"
    MATCH_BLOCKED = "match_blocked"
    NO_SAFE_MARKET_MATCH = "no_safe_market_match"

# --- PLANNER ENUMS ---
class PlannerFamily(str, Enum):
    REPLAY_RECONCILIATION = "replay_reconciliation_planner"
    SUCCESSOR_RESOLUTION = "successor_resolution_planner"
    LINEAGE_REPAIR = "lineage_repair_planner"
    APPLICABILITY_ALIGNMENT = "applicability_alignment_planner"
    RESTORATION_CEILING_REDUCTION = "restoration_ceiling_reduction_planner"
    NO_SAFE_VISIBILITY_PRESERVATION = "no_safe_visibility_preservation_planner"
    MIXED_DEBT_REDUCTION = "mixed_debt_reduction_planner"

class PlanStatus(str, Enum):
    BUILT = "plan_built"
    REVIEW_ONLY = "plan_review_only"
    READY_FOR_BOUNDED_PROGRESS = "plan_ready_for_bounded_progress"
    REPLAY_REQUIRED = "plan_replay_required"
    SUCCESSOR_REQUIRED = "plan_successor_required"
    BLOCKED = "plan_blocked"
    IN_PROGRESS = "plan_in_progress"
    CAVEATED = "plan_caveated"
    COMPLETED_BOUNDED = "plan_completed_bounded"
    SUPERSEDED = "plan_superseded"

class SettlementStepFamily(str, Enum):
    REPLAY_RECONCILE = "replay_reconcile_step"
    SUCCESSOR_RESOLVE = "successor_resolve_step"
    LINEAGE_REPAIR = "lineage_repair_step"
    APPLICABILITY_RECHECK = "applicability_recheck_step"
    EVIDENCE_REFRESH = "evidence_refresh_step"
    CAVEAT_REPROJECTION = "caveat_reprojection_step"
    NO_SAFE_VISIBILITY_CHECKPOINT = "no_safe_visibility_checkpoint_step"
    SETTLEMENT_VALIDATION = "settlement_validation_step"

class ProgressState(str, Enum):
    NOT_STARTED = "not_started"
    REPLAY_IN_PROGRESS = "replay_in_progress"
    SUCCESSOR_RESOLUTION_IN_PROGRESS = "successor_resolution_in_progress"
    PARTIAL_SETTLEMENT = "partial_settlement"
    CAVEATED_PROGRESS = "caveated_progress"
    BLOCKED_PROGRESS = "blocked_progress"
    BOUNDED_PROGRESS_VERIFIED = "bounded_progress_verified"
    SETTLEMENT_REPLAYED = "settlement_replayed"
    SETTLEMENT_CLOSED_WITH_CAPS = "settlement_closed_with_caps"

# --- DASHBOARD ENUMS ---
class DashboardFamily(str, Enum):
    OPERATOR_ASSURANCE = "operator_assurance_dashboard"
    REVIEWER_ASSURANCE = "reviewer_assurance_dashboard"
    EXECUTIVE_SUMMARY = "executive_summary_dashboard"
    SOVEREIGNTY_PRESERVATION = "sovereignty_preservation_dashboard"
    REPLAY_AND_DEBT = "replay_and_debt_dashboard"
    STABILIZATION_PORTFOLIO = "stabilization_portfolio_dashboard"
    NO_SAFE_VISIBILITY = "no_safe_visibility_dashboard"

class PanelFamily(str, Enum):
    FEDERATED_HEALTH = "federated_health_panel"
    REPLAY_MARKET = "replay_market_panel"
    DEBT_LEDGER = "debt_ledger_panel"
    SETTLEMENT_PLANNER = "settlement_planner_panel"
    SUCCESSOR_CONVERGENCE = "successor_convergence_panel"
    NO_SAFE_VISIBILITY = "no_safe_visibility_panel"
    SOVEREIGNTY_CAP = "sovereignty_cap_panel"
    RESTORATION_CEILING = "restoration_ceiling_panel"
    LINEAGE_INTEGRITY = "lineage_integrity_panel"
    CURRENTNESS_AND_STALENESS = "currentness_and_staleness_panel"

class SnapshotState(str, Enum):
    CURRENT = "snapshot_current"
    CAVEATED = "snapshot_caveated"
    STALE = "snapshot_stale"
    REVIEW_ONLY = "snapshot_review_only"
    DEGRADED = "snapshot_degraded"
    BLOCKED = "snapshot_blocked"

# --- CONTRACT RECORDS ---

class SynthesisCouncilWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str

class ResilienceSynthesisCouncilRecord(BaseModel):
    synthesis_council_id: str
    council_family: CouncilFamily
    governed_synthesis_refs: List[str]
    participant_refs: List[str]
    quorum_policy_ref: str
    precedence_policy_ref: str
    backlog_ref: str
    health_status: str
    warnings: List[SynthesisCouncilWarningRecord] = Field(default_factory=list)

class SynthesisCouncilInputRecord(BaseModel):
    input_id: str
    source_ref: str

class SynthesisCouncilEvidenceRecord(BaseModel):
    evidence_id: str
    description: str

class SynthesisCouncilVoteRecord(BaseModel):
    vote_id: str
    voter_ref: str
    decision: str

class SynthesisCouncilCapRecord(BaseModel):
    cap_id: str
    cap_type: str
    reason: str

class SynthesisCouncilCaveatRecord(BaseModel):
    caveat_id: str
    caveat_type: str
    description: str

class SynthesisCouncilDecisionRecord(BaseModel):
    decision_id: str
    decision_type: CouncilDecisionType
    cap_refs: List[str]
    caveat_refs: List[str]
    explanation: str

class SynthesisCouncilCaseRecord(BaseModel):
    synthesis_case_id: str
    case_family: CaseFamily
    input_synthesis_refs: List[str]
    input_compiler_refs: List[str]
    input_debt_refs: List[str]
    input_replay_refs: List[str]
    input_portfolio_refs: List[str]
    decision_needed: str
    escalation_state: str
    case_status: CaseStatus
    decision: Optional[SynthesisCouncilDecisionRecord] = None
    warnings: List[SynthesisCouncilWarningRecord] = Field(default_factory=list)

class SynthesisCouncilBacklogRecord(BaseModel):
    backlog_id: str
    pending_case_refs: List[str]

class SynthesisCouncilHealthRecord(BaseModel):
    council_ref: str
    health_band: str
    active_cases: int

class ResilienceSynthesisCouncilManifestRecord(BaseModel):
    manifest_id: str
    council_refs: List[str]
    timestamp: str

class ReplayExchangeMarketplaceWarningRecord(BaseModel):
    warning_id: str
    message: str

class ReplayMarketListingRecord(BaseModel):
    listing_id: str
    listing_family: str
    source_fabric_ref: str
    replay_family: str
    scope_class: str
    evidence_completeness: str
    fidelity_band: str
    caveat_refs: List[str]
    currentness_state: str
    listing_status: ListingStatus
    warnings: List[str] = Field(default_factory=list)

class ReplayMarketOfferRecord(BaseModel):
    offer_id: str
    listing_ref: str
    available_capacity: int
    supported_fidelity: str
    supported_scope_classes: List[str]
    replay_evidence_profile: str
    price_like_priority_score: int
    offer_status: str
    warnings: List[str] = Field(default_factory=list)

class ReplayMarketRequestRecord(BaseModel):
    request_id: str
    target_lineage_ref: str
    requested_replay_family: str
    required_fidelity: str
    required_evidence_refs: List[str]
    required_scope_class: str
    request_priority: int
    request_status: str
    warnings: List[str] = Field(default_factory=list)

class ReplayMarketMatchRecord(BaseModel):
    match_id: str
    request_ref: str
    offer_ref: str
    match_outcome: MatchOutcome
    caveat_refs: List[str] = Field(default_factory=list)
    revalidation_required: bool = False

class ReplayMarketConstraintRecord(BaseModel):
    constraint_id: str
    description: str

class ReplayMarketFairnessRecord(BaseModel):
    fairness_id: str
    fairness_score: int
    aging_factor: float

class ReplayMarketPressureRecord(BaseModel):
    pressure_id: str
    backlog_pressure: int

class ReplayMarketClearingHintRecord(BaseModel):
    hint_id: str
    suggestion: str

class ReplayMarketHealthRecord(BaseModel):
    marketplace_ref: str
    status: str

class ReplayExchangeMarketplaceManifestRecord(BaseModel):
    manifest_id: str
    marketplace_refs: List[str]
    timestamp: str

class ReplayExchangeMarketplaceRecord(BaseModel):
    replay_marketplace_id: str
    marketplace_family: ReplayMarketplaceFamily
    active_listing_refs: List[str]
    active_offer_refs: List[str]
    active_request_refs: List[str]
    active_match_refs: List[str]
    matching_policy_ref: str
    fairness_policy_ref: str
    health_status: str
    warnings: List[ReplayExchangeMarketplaceWarningRecord] = Field(default_factory=list)

class DebtSettlementPlannerWarningRecord(BaseModel):
    warning_id: str
    message: str

class SettlementStepRecord(BaseModel):
    step_id: str
    step_family: SettlementStepFamily
    description: str

class DebtSettlementPlanRecord(BaseModel):
    settlement_plan_id: str
    source_debt_refs: List[str]
    settlement_goal: str
    step_refs: List[str]
    bounded_effect_summary: str
    replay_requirements: List[str]
    successor_requirements: List[str]
    plan_status: PlanStatus
    warnings: List[str] = Field(default_factory=list)

class SettlementCandidateRecord(BaseModel):
    candidate_id: str
    debt_ref: str
    severity: str

class SettlementSequenceRecord(BaseModel):
    sequence_id: str
    ordered_step_refs: List[str]

class SettlementRiskRecord(BaseModel):
    risk_id: str
    description: str

class SettlementBoundRecord(BaseModel):
    bound_id: str
    ceiling_cap: str

class SettlementProgressRecord(BaseModel):
    progress_id: str
    plan_ref: str
    state: ProgressState

class SettlementPlannerHealthRecord(BaseModel):
    planner_ref: str
    status: str

class DebtSettlementPlannerManifestRecord(BaseModel):
    manifest_id: str
    planner_refs: List[str]
    timestamp: str

class ConvergenceDebtSettlementPlannerRecord(BaseModel):
    settlement_planner_id: str
    planner_family: PlannerFamily
    input_debt_ledger_refs: List[str]
    active_plan_refs: List[str]
    ranking_policy_ref: str
    sequencing_policy_ref: str
    boundedness_policy_ref: str
    health_status: str
    warnings: List[DebtSettlementPlannerWarningRecord] = Field(default_factory=list)

class GovernanceAssuranceDashboardWarningRecord(BaseModel):
    warning_id: str
    message: str

class DashboardPanelRecord(BaseModel):
    panel_id: str
    panel_family: PanelFamily
    metric_refs: List[str]

class DashboardViewRecord(BaseModel):
    view_id: str
    view_family: DashboardFamily
    intended_audience: str
    included_panel_refs: List[str]
    visibility_policy_ref: str
    refresh_policy_ref: str
    currentness_state: str
    warnings: List[str] = Field(default_factory=list)

class DashboardMetricRecord(BaseModel):
    metric_id: str
    metric_type: str
    value: str

class DashboardAlertRibbonRecord(BaseModel):
    alert_id: str
    severity: str
    message: str

class DashboardDrilldownRecord(BaseModel):
    drilldown_id: str
    target_ref: str

class DashboardAudienceProfileRecord(BaseModel):
    profile_id: str
    role: str

class DashboardSnapshotRecord(BaseModel):
    snapshot_id: str
    view_ref: str
    state: SnapshotState
    timestamp: str

class DashboardHealthRecord(BaseModel):
    dashboard_ref: str
    status: str

class GovernanceAssuranceDashboardManifestRecord(BaseModel):
    manifest_id: str
    dashboard_refs: List[str]
    timestamp: str

class SovereignGovernanceAssuranceDashboardRecord(BaseModel):
    dashboard_id: str
    dashboard_family: DashboardFamily
    view_refs: List[str]
    panel_refs: List[str]
    audience_profile_refs: List[str]
    snapshot_refs: List[str]
    alert_refs: List[str]
    health_status: str
    warnings: List[GovernanceAssuranceDashboardWarningRecord] = Field(default_factory=list)
