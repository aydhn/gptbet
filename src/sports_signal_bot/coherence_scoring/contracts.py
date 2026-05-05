from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ContextAssemblerFederationRecord:
    context_federation_id: str
    federation_family: str
    member_context_assembler_refs: List[str] = field(default_factory=list)
    active_link_refs: List[str] = field(default_factory=list)
    currentness_policy_ref: str = "default"
    audience_policy_ref: str = "default"
    scope_policy_ref: str = "default"
    health_status: str = "initializing"
    warnings: List[str] = field(default_factory=list)

@dataclass
class FederatedContextNodeRecord:
    node_id: str
    context_assembler_ref: str
    assembler_family: str
    supported_bundle_families: List[str] = field(default_factory=list)
    currentness_state: str = "fresh"
    caveat_state: str = "clear"
    sovereignty_state: str = "passed"
    node_status: str = "active"
    warnings: List[str] = field(default_factory=list)

@dataclass
class ContextFederationLinkRecord:
    link_id: str
    status: str

@dataclass
class ContextFederationCurrentnessRecord:
    record_id: str

@dataclass
class ContextFederationAudienceRecord:
    record_id: str

@dataclass
class ContextFederationCaveatRecord:
    record_id: str

@dataclass
class ContextFederationScopeRecord:
    record_id: str

@dataclass
class ContextFederationDecisionRecord:
    record_id: str

@dataclass
class ContextFederationHealthRecord:
    record_id: str

@dataclass
class ContextAssemblerFederationManifestRecord:
    record_id: str

@dataclass
class ContextAssemblerFederationWarningRecord:
    record_id: str

@dataclass
class FreshnessDisputeChamberRecord:
    freshness_dispute_chamber_id: str
    chamber_family: str
    governed_freshness_refs: List[str] = field(default_factory=list)
    participant_refs: List[str] = field(default_factory=list)
    quorum_policy_ref: str = "default"
    precedence_policy_ref: str = "default"
    backlog_ref: str = "default"
    health_status: str = "active"
    warnings: List[str] = field(default_factory=list)

@dataclass
class FreshnessDisputeCaseRecord:
    freshness_dispute_case_id: str
    case_family: str
    input_proof_refs: List[str] = field(default_factory=list)
    input_signal_refs: List[str] = field(default_factory=list)
    input_context_refs: List[str] = field(default_factory=list)
    input_trace_refs: List[str] = field(default_factory=list)
    input_snapshot_refs: List[str] = field(default_factory=list)
    decision_needed: bool = True
    escalation_state: str = "none"
    case_status: str = "case_opened"
    warnings: List[str] = field(default_factory=list)

@dataclass
class FreshnessDisputeInputRecord:
    record_id: str

@dataclass
class FreshnessDisputeEvidenceRecord:
    record_id: str

@dataclass
class FreshnessDisputeReplayRecord:
    record_id: str

@dataclass
class FreshnessDisputeVoteRecord:
    record_id: str

@dataclass
class FreshnessDisputeDecisionRecord:
    record_id: str

@dataclass
class FreshnessDisputeCapRecord:
    record_id: str

@dataclass
class FreshnessDisputeDecayRecord:
    record_id: str

@dataclass
class FreshnessDisputeBacklogRecord:
    record_id: str

@dataclass
class FreshnessDisputeHealthRecord:
    record_id: str

@dataclass
class FreshnessDisputeChamberManifestRecord:
    record_id: str

@dataclass
class FreshnessDisputeChamberWarningRecord:
    record_id: str

@dataclass
class TraceEvidenceBrokerRecord:
    evidence_broker_id: str
    broker_family: str
    active_listing_refs: List[str] = field(default_factory=list)
    active_request_refs: List[str] = field(default_factory=list)
    active_match_refs: List[str] = field(default_factory=list)
    routing_policy_ref: str = "default"
    fairness_policy_ref: str = "default"
    ceiling_policy_ref: str = "default"
    health_status: str = "active"
    warnings: List[str] = field(default_factory=list)

@dataclass
class EvidenceBrokerListingRecord:
    listing_id: str
    listing_family: str
    source_ref: str
    source_family: str
    supported_trace_families: List[str] = field(default_factory=list)
    supported_audience_profiles: List[str] = field(default_factory=list)
    evidence_completeness: str = "full"
    currentness_state: str = "fresh"
    caveat_refs: List[str] = field(default_factory=list)
    listing_status: str = "listed_current"
    warnings: List[str] = field(default_factory=list)

@dataclass
class EvidenceBrokerRequestRecord:
    request_id: str
    status: str

@dataclass
class EvidenceBrokerMatchRecord:
    match_id: str
    outcome: str

@dataclass
class EvidenceBrokerConstraintRecord:
    record_id: str

@dataclass
class EvidenceBrokerRouteRecord:
    record_id: str

@dataclass
class EvidenceBrokerCeilingRecord:
    record_id: str

@dataclass
class EvidenceBrokerFairnessRecord:
    record_id: str

@dataclass
class EvidenceBrokerHealthRecord:
    record_id: str

@dataclass
class TraceEvidenceBrokerManifestRecord:
    record_id: str

@dataclass
class TraceEvidenceBrokerWarningRecord:
    record_id: str

@dataclass
class SovereignGovernanceCoherenceScorerRecord:
    coherence_scorer_id: str
    scorer_family: str
    input_refs: List[str] = field(default_factory=list)
    pass_refs: List[str] = field(default_factory=list)
    dimension_refs: List[str] = field(default_factory=list)
    penalty_refs: List[str] = field(default_factory=list)
    ceiling_refs: List[str] = field(default_factory=list)
    output_refs: List[str] = field(default_factory=list)
    current_state: str = "initialized"
    warnings: List[str] = field(default_factory=list)

@dataclass
class CoherenceInputRecord:
    coherence_input_id: str
    input_family: str
    source_ref: str
    currentness_state: str
    caveat_state: str
    sovereignty_state: str
    no_safe_visibility_state: str
    warnings: List[str] = field(default_factory=list)

@dataclass
class CoherencePassRecord:
    record_id: str
    pass_type: str
    status: str

@dataclass
class CoherenceDimensionRecord:
    record_id: str
    dimension_type: str

@dataclass
class CoherencePenaltyRecord:
    record_id: str
    penalty_family: str

@dataclass
class CoherenceCeilingRecord:
    record_id: str

@dataclass
class CoherenceOutputRecord:
    output_id: str
    band: str
    preserved_caveats: List[str] = field(default_factory=list)
    no_safe_visibility_preserved: bool = True

@dataclass
class CoherenceExplanationRecord:
    record_id: str

@dataclass
class CoherenceHealthRecord:
    record_id: str

@dataclass
class GovernanceCoherenceScorerManifestRecord:
    record_id: str

@dataclass
class GovernanceCoherenceScorerWarningRecord:
    record_id: str

@dataclass
class ContextFederationBundleRecord:
    bundle_id: str
    source_context_refs: List[str] = field(default_factory=list)
    selected_bundle_refs: List[str] = field(default_factory=list)
    bundle_currentness_refs: List[str] = field(default_factory=list)
    preserved_caveat_refs: List[str] = field(default_factory=list)
    no_safe_visibility_state: str = "preserved"
    sovereignty_warning_refs: List[str] = field(default_factory=list)
    output_scope: str = "bounded"
    warnings: List[str] = field(default_factory=list)
