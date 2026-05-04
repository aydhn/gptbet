from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

# --- Common ---
class WarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str

# --- Dashboard Exchanges ---
class AssuranceDashboardExchangeRecord(BaseModel):
    dashboard_exchange_id: str
    source_dashboard_refs: List[str]
    source_snapshot_refs: List[str]
    source_panel_refs: List[str]
    target_scope_refs: List[str]
    exchange_scope: str
    audience_profile_refs: List[str]
    preserved_caveat_refs: List[str]
    currentness_refs: List[str]
    exchange_status: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class DashboardExchangePacketRecord(BaseModel):
    dashboard_exchange_packet_id: str
    source_dashboard_ref: str
    source_snapshot_ref: str
    included_panel_refs: List[str]
    included_alert_refs: List[str]
    included_metric_refs: List[str]
    caveat_refs: List[str]
    currentness_refs: List[str]
    visibility_constraints: List[str]
    warnings: List[WarningRecord] = Field(default_factory=list)

class DashboardExchangeEnvelopeRecord(BaseModel):
    envelope_id: str

class DashboardExchangeScopeRecord(BaseModel):
    scope_id: str

class DashboardExchangeConstraintRecord(BaseModel):
    constraint_id: str

class DashboardExchangeVerificationRecord(BaseModel):
    verification_id: str

class DashboardExchangeAudienceRecord(BaseModel):
    audience_id: str

class DashboardExchangeProjectionRecord(BaseModel):
    projection_id: str

class DashboardExchangeHealthRecord(BaseModel):
    health_id: str
    status: str

class AssuranceDashboardExchangeManifestRecord(BaseModel):
    manifest_id: str
    dashboard_exchange_refs: List[str]

class AssuranceDashboardExchangeWarningRecord(WarningRecord):
    pass


# --- Federation Boards ---
class CouncilFederationBoardRecord(BaseModel):
    federation_board_id: str
    board_family: str
    member_council_refs: List[str]
    participant_refs: List[str]
    quorum_policy_ref: str
    precedence_policy_ref: str
    backlog_ref: str
    health_status: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class FederationBoardCaseRecord(BaseModel):
    federation_board_case_id: str
    case_family: str
    input_council_case_refs: List[str]
    input_synthesis_refs: List[str]
    input_dashboard_refs: List[str]
    input_debt_refs: List[str]
    input_replay_refs: List[str]
    decision_needed: str
    escalation_state: str
    case_status: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class FederationBoardMemberRecord(BaseModel):
    member_id: str

class FederationBoardInputRecord(BaseModel):
    input_id: str

class FederationBoardEvidenceRecord(BaseModel):
    evidence_id: str

class FederationBoardVoteRecord(BaseModel):
    vote_id: str

class FederationBoardDecisionRecord(BaseModel):
    decision_id: str
    decision_type: str

class FederationBoardCapRecord(BaseModel):
    cap_id: str

class FederationBoardBacklogRecord(BaseModel):
    backlog_id: str

class FederationBoardHealthRecord(BaseModel):
    health_id: str

class CouncilFederationBoardManifestRecord(BaseModel):
    manifest_id: str

class CouncilFederationBoardWarningRecord(WarningRecord):
    pass


# --- Replay Market Clearing ---
class ReplayMarketClearingLayerRecord(BaseModel):
    replay_clearing_layer_id: str
    clearing_family: str
    marketplace_refs: List[str]
    clearing_book_refs: List[str]
    active_offer_refs: List[str]
    active_request_refs: List[str]
    active_decision_refs: List[str]
    fairness_policy_ref: str
    health_status: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class ReplayClearingBookRecord(BaseModel):
    clearing_book_id: str
    replay_family: str
    scope_class: str
    compatible_offer_refs: List[str]
    compatible_request_refs: List[str]
    backlog_refs: List[str]
    pressure_state: str
    clearing_status: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class ReplayClearingOfferRecord(BaseModel):
    offer_id: str
    listing_ref: str
    available_capacity: float
    supported_fidelity: str
    supported_scope_classes: List[str]
    replay_evidence_profile: str
    priority_hint: int
    offer_currentness_state: str
    offer_status: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class ReplayClearingRequestRecord(BaseModel):
    request_id: str
    target_lineage_ref: str
    requested_replay_family: str
    required_fidelity: str
    required_evidence_refs: List[str]
    required_scope_class: str
    priority_band: int
    request_currentness_state: str
    request_status: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class ReplayClearingConstraintRecord(BaseModel):
    constraint_id: str

class ReplayClearingDecisionRecord(BaseModel):
    decision_id: str

class ReplayClearingCeilingRecord(BaseModel):
    ceiling_id: str

class ReplayClearingFairnessRecord(BaseModel):
    fairness_id: str

class ReplayClearingPressureRecord(BaseModel):
    pressure_id: str

class ReplayClearingHealthRecord(BaseModel):
    health_id: str

class ReplayMarketClearingManifestRecord(BaseModel):
    manifest_id: str

class ReplayMarketClearingWarningRecord(WarningRecord):
    pass


# --- Debt Settlement Planner V2 ---
class DebtSettlementPlannerRecordV2(BaseModel):
    settlement_planner_id: str
    planner_family: str
    source_debt_ledger_refs: List[str]
    source_marketplace_refs: List[str]
    source_compiler_refs: List[str]
    active_plan_refs: List[str]
    sequencing_policy_ref: str
    boundedness_policy_ref: str
    health_status: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class SettlementPlanRecordV2(BaseModel):
    settlement_plan_id: str
    source_debt_refs: List[str]
    source_replay_refs: List[str]
    source_successor_refs: List[str]
    settlement_goal: str
    step_refs: List[str]
    replay_requirements: List[str]
    successor_requirements: List[str]
    bounded_effect_summary: str
    plan_status: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class SettlementPlanStepRecordV2(BaseModel):
    step_id: str

class SettlementCandidateRecordV2(BaseModel):
    candidate_id: str

class SettlementSequenceRecordV2(BaseModel):
    sequence_id: str

class SettlementCheckpointRecordV2(BaseModel):
    checkpoint_id: str

class SettlementValidationRecordV2(BaseModel):
    validation_id: str

class SettlementCeilingImpactRecord(BaseModel):
    impact_id: str

class SettlementPlannerHealthRecordV2(BaseModel):
    health_id: str

class DebtSettlementPlannerManifestRecordV2(BaseModel):
    manifest_id: str

class DebtSettlementPlannerWarningRecordV2(WarningRecord):
    pass


# --- Sovereign Governance Assurance Dashboards V2 ---
class SovereignGovernanceAssuranceDashboardRecordV2(BaseModel):
    dashboard_id: str
    dashboard_family: str
    view_refs: List[str]
    panel_refs: List[str]
    snapshot_refs: List[str]
    alert_refs: List[str]
    narrative_section_refs: List[str]
    audience_profile_refs: List[str]
    health_status: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class DashboardViewRecordV2(BaseModel):
    view_id: str
    view_family: str
    intended_audience: str
    included_panel_refs: List[str]
    included_narrative_refs: List[str]
    visibility_policy_ref: str
    refresh_policy_ref: str
    currentness_state: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class DashboardPanelRecordV2(BaseModel):
    panel_id: str

class DashboardMetricRecordV2(BaseModel):
    metric_id: str

class DashboardAlertRibbonRecordV2(BaseModel):
    alert_id: str

class DashboardDrilldownRecordV2(BaseModel):
    drilldown_id: str

class DashboardAudienceProfileRecordV2(BaseModel):
    audience_id: str

class DashboardSnapshotRecordV2(BaseModel):
    snapshot_id: str
    status: str

class DashboardNarrativeSectionRecord(BaseModel):
    section_id: str

class DashboardHealthRecordV2(BaseModel):
    health_id: str

class GovernanceAssuranceDashboardManifestRecordV2(BaseModel):
    manifest_id: str

class GovernanceAssuranceDashboardWarningRecordV2(WarningRecord):
    pass


# --- Sovereign Governance Narrative Compilers ---
class SovereignGovernanceNarrativeCompilerRecord(BaseModel):
    narrative_compiler_id: str
    compiler_family: str
    input_refs: List[str]
    section_refs: List[str]
    verification_refs: List[str]
    audience_profile_refs: List[str]
    currentness_policy_ref: str
    health_status: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class NarrativeInputRecord(BaseModel):
    narrative_input_id: str
    input_family: str
    source_ref: str
    currentness_state: str
    caveat_state: str
    sovereignty_state: str
    no_safe_visibility_state: str
    warnings: List[WarningRecord] = Field(default_factory=list)

class NarrativeSectionRecord(BaseModel):
    section_id: str

class NarrativeCaveatRecord(BaseModel):
    caveat_id: str

class NarrativeCeilingRecord(BaseModel):
    ceiling_id: str

class NarrativeAudienceRecord(BaseModel):
    audience_id: str

class NarrativeVerificationRecord(BaseModel):
    verification_id: str

class NarrativeFreshnessRecord(BaseModel):
    freshness_id: str

class NarrativeOutputRecord(BaseModel):
    output_id: str
    output_status: str

class NarrativeCompilerHealthRecord(BaseModel):
    health_id: str

class GovernanceNarrativeCompilerManifestRecord(BaseModel):
    manifest_id: str

class GovernanceNarrativeCompilerWarningRecord(WarningRecord):
    pass

