from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime

class LinkStatus(str, Enum):
    link_current = "link_current"
    link_caveated = "link_caveated"
    link_review_only = "link_review_only"
    link_degraded = "link_degraded"
    link_blocked = "link_blocked"
    link_expired = "link_expired"
    link_superseded = "link_superseded"

class ConsistencyLedgerFederationRecord(BaseModel):
    consistency_federation_id: str
    federation_family: str
    member_consistency_ledger_refs: List[str] = Field(default_factory=list)
    active_link_refs: List[str] = Field(default_factory=list)
    currentness_policy_ref: str
    contradiction_policy_ref: str
    ceiling_policy_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

class FederatedConsistencyNodeRecord(BaseModel):
    node_id: str
    consistency_ledger_ref: str
    ledger_family: str
    supported_consistency_families: List[str] = Field(default_factory=list)
    currentness_state: str
    contradiction_state: str
    sovereignty_state: str
    node_status: str
    warnings: List[str] = Field(default_factory=list)

class ConsistencyFederationLinkRecord(BaseModel):
    link_id: str
    source_node_ref: str
    target_node_ref: str
    link_status: LinkStatus

class ConsistencyFederationCurrentnessRecord(BaseModel):
    currentness_id: str

class ConsistencyFederationContradictionRecord(BaseModel):
    contradiction_id: str

class ConsistencyFederationCeilingRecord(BaseModel):
    ceiling_id: str

class ConsistencyFederationNoSafeRecord(BaseModel):
    no_safe_id: str

class ConsistencyFederationDecisionRecord(BaseModel):
    decision_id: str

class ConsistencyFederationHealthRecord(BaseModel):
    health_id: str
    overall_health: str

class ConsistencyLedgerFederationManifestRecord(BaseModel):
    manifest_id: str
    federation_refs: List[str]

class ConsistencyLedgerFederationWarningRecord(BaseModel):
    warning_id: str
    warning_type: str
    details: str

class CaseStatus(str, Enum):
    case_opened = "case_opened"
    case_collecting_evidence = "case_collecting_evidence"
    case_replay_pending = "case_replay_pending"
    case_quorum_pending = "case_quorum_pending"
    case_decided = "case_decided"
    case_decided_with_caveats = "case_decided_with_caveats"
    case_review_only = "case_review_only"
    case_blocked = "case_blocked"
    case_superseded = "case_superseded"
    case_archived = "case_archived"

class RouteDecisionType(str, Enum):
    preserve_existing_route_caps = "preserve_existing_route_caps"
    downgrade_to_review_only_route = "downgrade_to_review_only_route"
    require_refresh_evidence = "require_refresh_evidence"
    require_trace_revalidation = "require_trace_revalidation"
    amplify_route_caveats = "amplify_route_caveats"
    preserve_no_safe_visibility = "preserve_no_safe_visibility"
    accept_bounded_route_with_caps = "accept_bounded_route_with_caps"
    block_due_to_unresolved_route_conflict = "block_due_to_unresolved_route_conflict"

class TribunalRouteCouncilRecord(BaseModel):
    tribunal_route_council_id: str
    council_family: str
    governed_mesh_refs: List[str] = Field(default_factory=list)
    participant_refs: List[str] = Field(default_factory=list)
    quorum_policy_ref: str
    precedence_policy_ref: str
    backlog_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

class TribunalRouteCaseRecord(BaseModel):
    tribunal_route_case_id: str
    case_family: str
    input_mesh_case_refs: List[str] = Field(default_factory=list)
    input_context_refs: List[str] = Field(default_factory=list)
    input_trace_refs: List[str] = Field(default_factory=list)
    input_proof_refs: List[str] = Field(default_factory=list)
    input_signal_refs: List[str] = Field(default_factory=list)
    decision_needed: bool = True
    escalation_state: str
    case_status: CaseStatus = CaseStatus.case_opened
    warnings: List[str] = Field(default_factory=list)

class TribunalRouteInputRecord(BaseModel):
    input_id: str

class TribunalRouteEvidenceRecord(BaseModel):
    evidence_id: str

class TribunalRouteVoteRecord(BaseModel):
    vote_id: str

class TribunalRouteDecisionRecord(BaseModel):
    decision_id: str
    decision_type: RouteDecisionType

class TribunalRouteCapRecord(BaseModel):
    cap_id: str

class TribunalRoutePrecedenceRecord(BaseModel):
    precedence_id: str

class TribunalRouteBacklogRecord(BaseModel):
    backlog_id: str

class TribunalRouteHealthRecord(BaseModel):
    health_id: str
    status: str

class TribunalRouteCouncilManifestRecord(BaseModel):
    manifest_id: str

class TribunalRouteCouncilWarningRecord(BaseModel):
    warning_id: str


class ExchangeStatus(str, Enum):
    prepared = "prepared"
    validated = "validated"
    exchanged_review_only = "exchanged_review_only"
    exchanged_bounded = "exchanged_bounded"
    exchanged_caveated = "exchanged_caveated"
    exchanged_degraded = "exchanged_degraded"
    exchanged_blocked = "exchanged_blocked"
    exchanged_expired = "exchanged_expired"
    exchanged_superseded = "exchanged_superseded"

class EvidenceClearingExchangeRecord(BaseModel):
    evidence_clearing_exchange_id: str
    source_clearer_refs: List[str] = Field(default_factory=list)
    target_clearer_refs: List[str] = Field(default_factory=list)
    exchange_packet_refs: List[str] = Field(default_factory=list)
    exchange_scope: str
    validity_window: str
    preserved_caveat_refs: List[str] = Field(default_factory=list)
    currentness_refs: List[str] = Field(default_factory=list)
    exchange_status: ExchangeStatus = ExchangeStatus.prepared
    warnings: List[str] = Field(default_factory=list)

class ClearingExchangePacketRecord(BaseModel):
    clearing_exchange_packet_id: str
    source_listing_refs: List[str] = Field(default_factory=list)
    source_request_refs: List[str] = Field(default_factory=list)
    source_trace_refs: List[str] = Field(default_factory=list)
    source_evidence_refs: List[str] = Field(default_factory=list)
    evidence_completeness: str
    currentness_refs: List[str] = Field(default_factory=list)
    caveat_refs: List[str] = Field(default_factory=list)
    scope_constraints: str
    warnings: List[str] = Field(default_factory=list)

class ClearingExchangeEnvelopeRecord(BaseModel):
    envelope_id: str

class ClearingExchangeScopeRecord(BaseModel):
    scope_id: str

class ClearingExchangeConstraintRecord(BaseModel):
    constraint_id: str

class ClearingExchangeVerificationRecord(BaseModel):
    verification_id: str

class ClearingExchangeRoutingRecord(BaseModel):
    routing_id: str
    route_outcome: str

class ClearingExchangeDecisionRecord(BaseModel):
    decision_id: str

class ClearingExchangeHealthRecord(BaseModel):
    health_id: str

class EvidenceClearingExchangeManifestRecord(BaseModel):
    manifest_id: str

class EvidenceClearingExchangeWarningRecord(BaseModel):
    warning_id: str

class SovereignGovernanceAssuranceSynthesizerRecord(BaseModel):
    assurance_synthesizer_id: str
    synthesizer_family: str
    input_refs: List[str] = Field(default_factory=list)
    pass_refs: List[str] = Field(default_factory=list)
    dimension_refs: List[str] = Field(default_factory=list)
    penalty_refs: List[str] = Field(default_factory=list)
    ceiling_refs: List[str] = Field(default_factory=list)
    output_refs: List[str] = Field(default_factory=list)
    current_state: str
    warnings: List[str] = Field(default_factory=list)

class AssuranceSynthesisInputRecord(BaseModel):
    assurance_input_id: str
    input_family: str
    source_ref: str
    currentness_state: str
    caveat_state: str
    sovereignty_state: str
    no_safe_visibility_state: str
    warnings: List[str] = Field(default_factory=list)

class AssuranceSynthesisPassRecord(BaseModel):
    pass_id: str
    pass_type: str
    outcome: str

class AssuranceSynthesisDimensionRecord(BaseModel):
    dimension_id: str
    dimension_type: str
    value: str

class AssuranceSynthesisPenaltyRecord(BaseModel):
    penalty_id: str
    penalty_family: str
    details: str

class AssuranceSynthesisCeilingRecord(BaseModel):
    ceiling_id: str

class AssuranceBand(str, Enum):
    critically_fragile_assurance = "critically_fragile_assurance"
    fragile_assurance = "fragile_assurance"
    review_only_assurance = "review_only_assurance"
    bounded_assurance_with_caveats = "bounded_assurance_with_caveats"
    stabilized_assurance_with_caps = "stabilized_assurance_with_caps"
    strong_bounded_assurance = "strong_bounded_assurance"

class AssuranceSynthesisOutputRecord(BaseModel):
    output_id: str
    band: AssuranceBand
    synthesizer_ref: str
    preserved_caveat_refs: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class AssuranceSynthesisExplanationRecord(BaseModel):
    explanation_id: str

class AssuranceSynthesisHealthRecord(BaseModel):
    health_id: str

class GovernanceAssuranceSynthesizerManifestRecord(BaseModel):
    manifest_id: str

class GovernanceAssuranceSynthesizerWarningRecord(BaseModel):
    warning_id: str
