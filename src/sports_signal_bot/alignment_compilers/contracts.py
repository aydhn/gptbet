from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import datetime

# --- Coherence Scorer Federation ---
@dataclass
class CoherenceFederationWarningRecord:
    warning_type: str
    message: str
    severity: str

@dataclass
class CoherenceFederationCurrentnessRecord:
    state: str
    last_updated: str
    caveat_refs: List[str] = field(default_factory=list)

@dataclass
class CoherenceFederationPenaltyRecord:
    penalty_type: str
    applied_to: str
    reason: str

@dataclass
class CoherenceFederationCeilingRecord:
    ceiling_band: str
    reason: str

@dataclass
class CoherenceFederationAgreementRecord:
    agreement_band: str
    score: float

@dataclass
class CoherenceFederationDecisionRecord:
    decision: str
    caps: List[str]

@dataclass
class CoherenceFederationHealthRecord:
    status: str
    metrics: Dict[str, Any]

@dataclass
class CoherenceFederationLinkRecord:
    link_id: str
    source_ref: str
    target_ref: str
    status: str

@dataclass
class FederatedCoherenceNodeRecord:
    node_id: str
    coherence_scorer_ref: str
    scorer_family: str
    supported_scope_refs: List[str]
    currentness_state: str
    penalty_state: str
    sovereignty_state: str
    node_status: str
    warnings: List[CoherenceFederationWarningRecord] = field(default_factory=list)

@dataclass
class CoherenceScorerFederationRecord:
    coherence_federation_id: str
    federation_family: str
    member_scorer_refs: List[str]
    active_link_refs: List[str]
    currentness_policy_ref: str
    ceiling_policy_ref: str
    agreement_policy_ref: str
    health_status: str
    warnings: List[CoherenceFederationWarningRecord] = field(default_factory=list)
    nodes: List[FederatedCoherenceNodeRecord] = field(default_factory=list)

@dataclass
class CoherenceScorerFederationManifestRecord:
    federation_refs: List[str]
    generated_at: str

# --- Context Dispute Tribunal ---

@dataclass
class ContextDisputeTribunalWarningRecord:
    warning_type: str
    message: str

@dataclass
class TribunalClaimRecord:
    claim_id: str
    claim_type: str
    description: str

@dataclass
class TribunalEvidenceRecord:
    evidence_id: str
    source_ref: str
    completeness: str

@dataclass
class TribunalReplayRecord:
    replay_id: str
    result: str

@dataclass
class TribunalPanelRecord:
    panel_id: str
    panel_family: str
    findings: List[str]

@dataclass
class TribunalVoteRecord:
    vote_id: str
    voter_ref: str
    decision: str

@dataclass
class TribunalDecisionRecord:
    decision_type: str
    caps: List[str]
    refresh_requirements: List[str]

@dataclass
class TribunalCapRecord:
    cap_id: str
    cap_type: str
    target_ref: str

@dataclass
class TribunalBacklogRecord:
    pending_cases: int
    oldest_case_age_minutes: int

@dataclass
class TribunalHealthRecord:
    status: str
    resolution_rate: float

@dataclass
class ContextDisputeCaseRecord:
    context_dispute_case_id: str
    case_family: str
    input_context_refs: List[str]
    input_trace_refs: List[str]
    input_proof_refs: List[str]
    input_dashboard_refs: List[str]
    input_narrative_refs: List[str]
    input_signal_refs: List[str]
    decision_needed: str
    escalation_state: str
    case_status: str
    decision: Optional[TribunalDecisionRecord] = None
    warnings: List[ContextDisputeTribunalWarningRecord] = field(default_factory=list)

@dataclass
class ContextDisputeTribunalRecord:
    context_dispute_tribunal_id: str
    tribunal_family: str
    governed_context_refs: List[str]
    participant_refs: List[str]
    quorum_policy_ref: str
    precedence_policy_ref: str
    backlog_ref: str
    health_status: str
    warnings: List[ContextDisputeTribunalWarningRecord] = field(default_factory=list)
    cases: List[ContextDisputeCaseRecord] = field(default_factory=list)

@dataclass
class ContextDisputeTribunalManifestRecord:
    tribunal_refs: List[str]
    generated_at: str

# --- Trace Evidence Broker Exchange ---

@dataclass
class EvidenceBrokerExchangeWarningRecord:
    warning_type: str
    message: str

@dataclass
class BrokerExchangeScopeRecord:
    audience_refs: List[str]
    constraints: List[str]

@dataclass
class BrokerExchangeConstraintRecord:
    constraint_type: str
    value: str

@dataclass
class BrokerExchangeVerificationRecord:
    verified: bool
    details: str

@dataclass
class BrokerExchangeRoutingRecord:
    route_status: str
    selected_route_ref: str

@dataclass
class BrokerExchangeMatchRecord:
    match_status: str
    score: float

@dataclass
class BrokerExchangeHealthRecord:
    status: str
    metrics: Dict[str, Any]

@dataclass
class BrokerExchangePacketRecord:
    broker_exchange_packet_id: str
    source_listing_refs: List[str]
    source_request_refs: List[str]
    source_trace_refs: List[str]
    source_evidence_refs: List[str]
    evidence_completeness: str
    currentness_refs: List[str]
    caveat_refs: List[str]
    scope_constraints: List[str]
    warnings: List[EvidenceBrokerExchangeWarningRecord] = field(default_factory=list)

@dataclass
class EvidenceBrokerExchangeRecord:
    broker_exchange_id: str
    source_broker_refs: List[str]
    target_broker_refs: List[str]
    exchange_packet_refs: List[str]
    exchange_scope: BrokerExchangeScopeRecord
    validity_window: str
    preserved_caveat_refs: List[str]
    currentness_refs: List[str]
    exchange_status: str
    warnings: List[EvidenceBrokerExchangeWarningRecord] = field(default_factory=list)

@dataclass
class EvidenceBrokerExchangeManifestRecord:
    exchange_refs: List[str]
    generated_at: str

# --- Sovereign Governance Alignment Compiler ---

@dataclass
class GovernanceAlignmentCompilerWarningRecord:
    warning_type: str
    message: str

@dataclass
class AlignmentInputRecord:
    alignment_input_id: str
    input_family: str
    source_ref: str
    currentness_state: str
    caveat_state: str
    sovereignty_state: str
    no_safe_visibility_state: str
    warnings: List[GovernanceAlignmentCompilerWarningRecord] = field(default_factory=list)

@dataclass
class AlignmentPassRecord:
    pass_id: str
    pass_type: str
    result: str

@dataclass
class AlignmentDimensionRecord:
    dimension_type: str
    score: float

@dataclass
class AlignmentPenaltyRecord:
    penalty_family: str
    severity: str
    reason: str

@dataclass
class AlignmentCeilingRecord:
    ceiling_band: str
    reason: str

@dataclass
class AlignmentOutputRecord:
    output_id: str
    alignment_band: str
    preserved_caveats: List[str]
    no_safe_recovery_hints: List[str]

@dataclass
class AlignmentExplanationRecord:
    explanation_id: str
    details: str

@dataclass
class AlignmentHealthRecord:
    status: str
    metrics: Dict[str, Any]

@dataclass
class SovereignGovernanceAlignmentCompilerRecord:
    alignment_compiler_id: str
    compiler_family: str
    input_refs: List[str]
    pass_refs: List[str]
    dimension_refs: List[str]
    penalty_refs: List[str]
    ceiling_refs: List[str]
    output_refs: List[str]
    current_state: str
    warnings: List[GovernanceAlignmentCompilerWarningRecord] = field(default_factory=list)

@dataclass
class GovernanceAlignmentCompilerManifestRecord:
    compiler_refs: List[str]
    generated_at: str
