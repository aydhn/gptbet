from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Trace Router Federation Contracts
# ---------------------------------------------------------------------------

class TraceRouterFederationWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str

class TraceFederationLinkRecord(BaseModel):
    link_id: str
    source_router_ref: str
    target_router_ref: str
    status: str

class FederatedTraceNodeRecord(BaseModel):
    node_id: str
    trace_router_ref: str
    trace_router_family: str
    supported_trace_families: List[str]
    currentness_state: str
    caveat_state: str
    sovereignty_state: str
    node_status: str
    warnings: List[str] = Field(default_factory=list)

class TraceFederationCurrentnessRecord(BaseModel):
    currentness_id: str
    status: str
    timestamp: str

class TraceFederationLineageRecord(BaseModel):
    lineage_id: str
    path: List[str]

class TraceFederationCaveatRecord(BaseModel):
    caveat_id: str
    description: str

class TraceFederationScopeRecord(BaseModel):
    scope_id: str
    boundaries: List[str]

class TraceFederationDecisionRecord(BaseModel):
    decision_id: str
    decision_type: str
    rationale: str

class TraceFederationHealthRecord(BaseModel):
    health_id: str
    status: str
    details: Dict[str, Any]

class TraceRouterFederationManifestRecord(BaseModel):
    manifest_id: str
    generated_at: str
    federation_ref: str
    contents: Dict[str, Any]

class TraceRouterFederationRecord(BaseModel):
    trace_router_federation_id: str
    federation_family: str
    member_trace_router_refs: List[str]
    active_link_refs: List[str]
    currentness_policy_ref: str
    lineage_policy_ref: str
    scope_policy_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

# ---------------------------------------------------------------------------
# Proof Freshness Council Contracts
# ---------------------------------------------------------------------------

class ProofFreshnessCouncilWarningRecord(BaseModel):
    warning_id: str
    message: str

class ProofFreshnessInputRecord(BaseModel):
    input_id: str
    proof_ref: str

class ProofFreshnessEvidenceRecord(BaseModel):
    evidence_id: str
    data: Dict[str, Any]

class ProofFreshnessVoteRecord(BaseModel):
    vote_id: str
    voter_ref: str
    vote: str

class ProofFreshnessDecisionRecord(BaseModel):
    decision_id: str
    decision_type: str

class ProofFreshnessCapRecord(BaseModel):
    cap_id: str
    limit: str

class ProofFreshnessDecayRecord(BaseModel):
    decay_id: str
    band: str

class ProofFreshnessBacklogRecord(BaseModel):
    backlog_id: str
    items: List[str]

class ProofFreshnessHealthRecord(BaseModel):
    health_id: str
    status: str

class ProofFreshnessCouncilManifestRecord(BaseModel):
    manifest_id: str
    council_ref: str

class ProofFreshnessCaseRecord(BaseModel):
    proof_freshness_case_id: str
    case_family: str
    input_proof_refs: List[str]
    input_catalog_refs: List[str]
    input_atlas_refs: List[str]
    input_trace_refs: List[str]
    decision_needed: str
    escalation_state: str
    case_status: str
    warnings: List[str] = Field(default_factory=list)

class ProofFreshnessCouncilRecord(BaseModel):
    proof_freshness_council_id: str
    council_family: str
    governed_proof_refs: List[str]
    participant_refs: List[str]
    quorum_policy_ref: str
    precedence_policy_ref: str
    backlog_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

# ---------------------------------------------------------------------------
# Observatory Exchange Board Contracts
# ---------------------------------------------------------------------------

class ObservatoryExchangeBoardWarningRecord(BaseModel):
    warning_id: str
    message: str

class ObservatoryExchangeInputRecord(BaseModel):
    input_id: str
    exchange_ref: str

class ObservatoryExchangeEvidenceRecord(BaseModel):
    evidence_id: str
    data: Dict[str, Any]

class ObservatoryExchangeVoteRecord(BaseModel):
    vote_id: str
    voter_ref: str
    vote: str

class ObservatoryExchangeDecisionRecord(BaseModel):
    decision_id: str
    decision_type: str

class ObservatoryExchangeCapRecord(BaseModel):
    cap_id: str
    limit: str

class ObservatoryExchangeBacklogRecord(BaseModel):
    backlog_id: str
    items: List[str]

class ObservatoryExchangeHealthRecord(BaseModel):
    health_id: str
    status: str

class ObservatoryExchangeBoardManifestRecord(BaseModel):
    manifest_id: str
    board_ref: str

class ObservatoryExchangeCaseRecord(BaseModel):
    observatory_exchange_case_id: str
    case_family: str
    input_exchange_refs: List[str]
    input_snapshot_refs: List[str]
    input_signal_refs: List[str]
    input_alert_refs: List[str]
    input_mesh_refs: List[str]
    decision_needed: str
    escalation_state: str
    case_status: str
    warnings: List[str] = Field(default_factory=list)

class ObservatoryExchangeBoardRecord(BaseModel):
    observatory_exchange_board_id: str
    board_family: str
    governed_exchange_refs: List[str]
    participant_refs: List[str]
    quorum_policy_ref: str
    precedence_policy_ref: str
    backlog_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

# ---------------------------------------------------------------------------
# Sovereign Governance Context Assembler Contracts
# ---------------------------------------------------------------------------

class GovernanceContextAssemblerWarningRecord(BaseModel):
    warning_id: str
    message: str

class ContextSectionRecord(BaseModel):
    section_id: str
    family: str
    content: str

class ContextEvidenceLinkRecord(BaseModel):
    link_id: str
    evidence_ref: str

class ContextAudienceRecord(BaseModel):
    audience_id: str
    profile: str

class ContextFreshnessRecord(BaseModel):
    freshness_id: str
    status: str

class ContextCaveatRecord(BaseModel):
    caveat_id: str
    description: str

class ContextVerificationRecord(BaseModel):
    verification_id: str
    status: str

class ContextAssemblerHealthRecord(BaseModel):
    health_id: str
    status: str

class GovernanceContextAssemblerManifestRecord(BaseModel):
    manifest_id: str
    assembler_ref: str

class ContextAssemblyInputRecord(BaseModel):
    input_id: str
    input_family: str
    source_ref: str
    currentness_state: str
    caveat_state: str
    sovereignty_state: str
    no_safe_visibility_state: str
    warnings: List[str] = Field(default_factory=list)

class ContextBundleRecord(BaseModel):
    context_bundle_id: str
    bundle_family: str
    target_audience: str
    included_section_refs: List[str]
    included_evidence_refs: List[str]
    included_trace_refs: List[str]
    currentness_state: str
    bundle_status: str
    warnings: List[str] = Field(default_factory=list)

class SovereignGovernanceContextAssemblerRecord(BaseModel):
    context_assembler_id: str
    assembler_family: str
    input_refs: List[str]
    bundle_refs: List[str]
    section_refs: List[str]
    verification_refs: List[str]
    audience_profile_refs: List[str]
    health_status: str
    warnings: List[str] = Field(default_factory=list)

# Route Model
class FederatedTraceRouteRecord(BaseModel):
    route_id: str
    source_trace_router_refs: List[str]
    selected_route_refs: List[str]
    route_currentness_refs: List[str]
    preserved_caveat_refs: List[str]
    no_safe_visibility_state: str
    sovereignty_warning_refs: List[str]
    output_scope: str
    warnings: List[str] = Field(default_factory=list)
