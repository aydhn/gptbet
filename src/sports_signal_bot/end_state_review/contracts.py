from enum import Enum
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field

# --- FEDERATION LINK STATUS TAXONOMY ---
class FederationLinkStatus(str, Enum):
    link_current = "link_current"
    link_caveated = "link_caveated"
    link_review_only = "link_review_only"
    link_degraded = "link_degraded"
    link_blocked = "link_blocked"
    link_expired = "link_expired"
    link_superseded = "link_superseded"

# --- FEDERATED ASSURANCE OUTPUT TAXONOMY ---
class FederatedAssuranceOutput(str, Enum):
    federated_assurance_current_with_caps = "federated_assurance_current_with_caps"
    federated_assurance_caveated = "federated_assurance_caveated"
    federated_assurance_review_only = "federated_assurance_review_only"
    federated_assurance_degraded = "federated_assurance_degraded"
    federated_assurance_blocked = "federated_assurance_blocked"
    federated_assurance_stale = "federated_assurance_stale"

# --- FEDERATED ASSURANCE AGREEMENT MODEL ---
class AssuranceFederationAgreementBand(str, Enum):
    no_agreement = "no_agreement"
    weak_agreement = "weak_agreement"
    bounded_agreement = "bounded_agreement"
    strong_agreement_with_caveats = "strong_agreement_with_caveats"
    stable_agreement = "stable_agreement"

# --- EDGE STATUS TAXONOMY ---
class ClosureMeshEdgeStatus(str, Enum):
    edge_current = "edge_current"
    edge_caveated = "edge_caveated"
    edge_review_only = "edge_review_only"
    edge_degraded = "edge_degraded"
    edge_backpressured = "edge_backpressured"
    edge_blocked = "edge_blocked"
    edge_expired = "edge_expired"
    edge_superseded = "edge_superseded"

# --- CLOSURE MESH CASE ROUTING MODEL ---
class ClosureRouteOutcome(str, Enum):
    bounded_closure_route = "bounded_closure_route"
    review_only_closure_route = "review_only_closure_route"
    caveated_closure_route = "caveated_closure_route"
    degraded_closure_route = "degraded_closure_route"
    replay_required_closure_route = "replay_required_closure_route"
    blocked_closure_route = "blocked_closure_route"
    no_safe_closure_route = "no_safe_closure_route"

# --- EXCHANGE STATUS TAXONOMY ---
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

# --- ASSURANCE EXCHANGE ROUTE MODEL ---
class AssuranceExchangeRouteOutcome(str, Enum):
    routed_bounded_assurance_exchange = "routed_bounded_assurance_exchange"
    routed_review_only_assurance_exchange = "routed_review_only_assurance_exchange"
    routed_caveated_assurance_exchange = "routed_caveated_assurance_exchange"
    routed_degraded_assurance_exchange = "routed_degraded_assurance_exchange"
    revalidation_required_assurance_exchange = "revalidation_required_assurance_exchange"
    blocked_assurance_exchange_route = "blocked_assurance_exchange_route"
    no_safe_assurance_exchange_route = "no_safe_assurance_exchange_route"

# --- END-STATE REVIEW BANDS ---
class EndStateReviewBand(str, Enum):
    critically_fragile_review = "critically_fragile_review"
    fragile_review = "fragile_review"
    review_only_end_state = "review_only_end_state"
    bounded_end_state_with_caveats = "bounded_end_state_with_caveats"
    stabilized_end_state_with_caps = "stabilized_end_state_with_caps"
    mature_bounded_end_state = "mature_bounded_end_state"

# --- ASSURANCE SYNTHESIZER FEDERATION CONTRACTS ---
@dataclass
class FederatedAssuranceNodeRecord:
    node_id: str
    assurance_synthesizer_ref: str
    synthesizer_family: str
    supported_scope_refs: List[str]
    currentness_state: str
    penalty_state: str
    sovereignty_state: str
    node_status: str
    warnings: List[str] = field(default_factory=list)

@dataclass
class AssuranceSynthesizerFederationRecord:
    assurance_federation_id: str
    federation_family: str
    member_assurance_synthesizer_refs: List[str]
    active_link_refs: List[str]
    currentness_policy_ref: str
    ceiling_policy_ref: str
    agreement_policy_ref: str
    health_status: str
    warnings: List[str] = field(default_factory=list)

@dataclass
class AssuranceFederationLinkRecord:
    link_id: str
    source_ref: str
    target_ref: str
    status: FederationLinkStatus

@dataclass
class AssuranceFederationCurrentnessRecord:
    currentness_id: str
    status: str

@dataclass
class AssuranceFederationPenaltyRecord:
    penalty_id: str
    reason: str

@dataclass
class AssuranceFederationCeilingRecord:
    ceiling_id: str
    cap: str

@dataclass
class AssuranceFederationAgreementRecord:
    agreement_id: str
    band: AssuranceFederationAgreementBand

@dataclass
class AssuranceFederationDecisionRecord:
    decision_id: str
    outcome: FederatedAssuranceOutput

@dataclass
class AssuranceFederationHealthRecord:
    health_id: str
    status: str

@dataclass
class AssuranceSynthesizerFederationManifestRecord:
    manifest_id: str
    timestamp: str

@dataclass
class AssuranceSynthesizerFederationWarningRecord:
    warning_id: str
    message: str


# --- COUNCIL CLOSURE MESH CONTRACTS ---
@dataclass
class ClosureMeshNodeRecord:
    node_id: str
    node_family: str
    hosted_council_refs: List[str]
    supported_case_families: List[str]
    currentness_state: str
    closure_state: str
    node_status: str
    warnings: List[str] = field(default_factory=list)

@dataclass
class ClosureMeshEdgeRecord:
    edge_id: str
    source_node_ref: str
    target_node_ref: str
    supported_case_families: List[str]
    supported_scope_classes: List[str]
    caveat_transfer_policy: str
    currentness_state: str
    edge_status: ClosureMeshEdgeStatus
    warnings: List[str] = field(default_factory=list)

@dataclass
class CouncilClosureMeshRecord:
    closure_mesh_id: str
    mesh_family: str
    node_refs: List[str]
    edge_refs: List[str]
    case_refs: List[str]
    checkpoint_refs: List[str]
    routing_policy_ref: str
    closure_policy_ref: str
    pressure_policy_ref: str
    health_status: str
    warnings: List[str] = field(default_factory=list)

@dataclass
class ClosureMeshPathRecord:
    path_id: str
    outcome: ClosureRouteOutcome

@dataclass
class ClosureMeshCaseRecord:
    case_id: str

@dataclass
class ClosureMeshCheckpointRecord:
    checkpoint_id: str
    family: str

@dataclass
class ClosureMeshResidueRecord:
    residue_id: str
    family: str

@dataclass
class ClosureMeshDecisionRecord:
    decision_id: str

@dataclass
class ClosureMeshPressureRecord:
    pressure_id: str

@dataclass
class ClosureMeshHealthRecord:
    health_id: str
    status: str

@dataclass
class CouncilClosureMeshManifestRecord:
    manifest_id: str

@dataclass
class CouncilClosureMeshWarningRecord:
    warning_id: str


# --- EVIDENCE ASSURANCE EXCHANGE CONTRACTS ---
@dataclass
class AssuranceExchangePacketRecord:
    assurance_exchange_packet_id: str
    source_listing_refs: List[str]
    source_request_refs: List[str]
    source_trace_refs: List[str]
    source_evidence_refs: List[str]
    source_assurance_refs: List[str]
    evidence_completeness: str
    currentness_refs: List[str]
    caveat_refs: List[str]
    scope_constraints: List[str]
    warnings: List[str] = field(default_factory=list)

@dataclass
class EvidenceAssuranceExchangeRecord:
    evidence_assurance_exchange_id: str
    source_exchange_refs: List[str]
    target_exchange_refs: List[str]
    assurance_packet_refs: List[str]
    exchange_scope: str
    validity_window: str
    preserved_caveat_refs: List[str]
    currentness_refs: List[str]
    exchange_status: ExchangeStatus
    warnings: List[str] = field(default_factory=list)

@dataclass
class AssuranceExchangeEnvelopeRecord:
    envelope_id: str

@dataclass
class AssuranceExchangeScopeRecord:
    scope_id: str

@dataclass
class AssuranceExchangeConstraintRecord:
    constraint_id: str

@dataclass
class AssuranceExchangeVerificationRecord:
    verification_id: str

@dataclass
class AssuranceExchangeRoutingRecord:
    routing_id: str
    outcome: AssuranceExchangeRouteOutcome

@dataclass
class AssuranceExchangeDecisionRecord:
    decision_id: str

@dataclass
class AssuranceExchangeHealthRecord:
    health_id: str
    status: str

@dataclass
class EvidenceAssuranceExchangeManifestRecord:
    manifest_id: str

@dataclass
class EvidenceAssuranceExchangeWarningRecord:
    warning_id: str


# --- SOVEREIGN GOVERNANCE END-STATE REVIEW COMPILER CONTRACTS ---
@dataclass
class EndStateReviewInputRecord:
    review_input_id: str
    input_family: str
    source_ref: str
    currentness_state: str
    caveat_state: str
    sovereignty_state: str
    no_safe_visibility_state: str
    warnings: List[str] = field(default_factory=list)

@dataclass
class SovereignGovernanceEndStateReviewCompilerRecord:
    end_state_review_compiler_id: str
    compiler_family: str
    input_refs: List[str]
    pass_refs: List[str]
    dimension_refs: List[str]
    penalty_refs: List[str]
    ceiling_refs: List[str]
    output_refs: List[str]
    closure_refs: List[str]
    current_state: str
    warnings: List[str] = field(default_factory=list)

@dataclass
class EndStateReviewPassRecord:
    pass_id: str
    family: str

@dataclass
class EndStateReviewDimensionRecord:
    dimension_id: str

@dataclass
class EndStateReviewPenaltyRecord:
    penalty_id: str
    family: str

@dataclass
class EndStateReviewCeilingRecord:
    ceiling_id: str

@dataclass
class EndStateReviewOutputRecord:
    output_id: str
    band: EndStateReviewBand
    caveats: List[str] = field(default_factory=list)

@dataclass
class EndStateReviewExplanationRecord:
    explanation_id: str

@dataclass
class EndStateReviewClosureRecord:
    closure_id: str

@dataclass
class EndStateReviewHealthRecord:
    health_id: str
    status: str

@dataclass
class GovernanceEndStateReviewManifestRecord:
    manifest_id: str

@dataclass
class GovernanceEndStateReviewWarningRecord:
    warning_id: str
