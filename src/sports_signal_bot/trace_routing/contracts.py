from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TraceRouterFamily(str, Enum):
    GOVERNANCE_TRACE_ROUTER = "governance_trace_router"
    REPLAY_LINEAGE_TRACE_ROUTER = "replay_lineage_trace_router"
    DEBT_SETTLEMENT_TRACE_ROUTER = "debt_settlement_trace_router"
    SOVEREIGNTY_WARNING_TRACE_ROUTER = "sovereignty_warning_trace_router"
    NO_SAFE_VISIBILITY_TRACE_ROUTER = "no_safe_visibility_trace_router"
    ASSURANCE_SNAPSHOT_TRACE_ROUTER = "assurance_snapshot_trace_router"
    NARRATIVE_TRACE_ROUTER = "narrative_trace_router"

class NodeFamily(str, Enum):
    PROOF_NODE = "proof_node"
    DASHBOARD_SNAPSHOT_NODE = "dashboard_snapshot_node"
    NARRATIVE_SECTION_NODE = "narrative_section_node"
    REPLAY_SIGNAL_NODE = "replay_signal_node"
    DEBT_ENTRY_NODE = "debt_entry_node"
    SETTLEMENT_PLAN_NODE = "settlement_plan_node"
    COUNCIL_DECISION_NODE = "council_decision_node"
    OBSERVATORY_SNAPSHOT_NODE = "observatory_snapshot_node"
    SOVEREIGNTY_WARNING_NODE = "sovereignty_warning_node"
    NO_SAFE_VISIBILITY_NODE = "no_safe_visibility_node"

class EdgeRelationshipFamily(str, Enum):
    DERIVES_FROM = "derives_from"
    CAPPED_BY = "capped_by"
    CAVEATED_BY = "caveated_by"
    REFRESHED_BY = "refreshed_by"
    REPLAYED_BY = "replayed_by"
    BLOCKED_BY = "blocked_by"
    SETTLED_BY = "settled_by"
    SUPERSEDED_BY = "superseded_by"
    SUPPORTS_NARRATIVE = "supports_narrative"
    PRESERVES_NO_SAFE_VISIBILITY = "preserves_no_safe_visibility"
    WARNED_BY = "warned_by"
    OBSERVED_BY = "observed_by"

class TraceRouteOutcome(str, Enum):
    BOUNDED_TRACE_ROUTE = "bounded_trace_route"
    REVIEW_ONLY_TRACE_ROUTE = "review_only_trace_route"
    CAVEATED_TRACE_ROUTE = "caveated_trace_route"
    DEGRADED_TRACE_ROUTE = "degraded_trace_route"
    BLOCKED_TRACE_ROUTE = "blocked_trace_route"
    NO_SAFE_TRACE_ROUTE = "no_safe_trace_route"

class TraceRouterHealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CAVEATED = "caveated"
    BLOCKED = "blocked"

class TraceRouterNodeRecord(BaseModel):
    node_id: str
    node_family: NodeFamily
    source_ref: str
    source_family: str
    currentness_state: str
    caveat_state: str
    node_status: str
    warnings: List[str] = Field(default_factory=list)

class TraceRouterEdgeRecord(BaseModel):
    edge_id: str
    source_node_ref: str
    target_node_ref: str
    relationship_family: EdgeRelationshipFamily
    freshness_state: str
    caveat_transfer_policy: str
    edge_status: str
    warnings: List[str] = Field(default_factory=list)

class SovereignGovernanceTraceRouterRecord(BaseModel):
    trace_router_id: str
    router_family: TraceRouterFamily
    node_refs: List[str] = Field(default_factory=list)
    edge_refs: List[str] = Field(default_factory=list)
    routing_policy_ref: str
    constraint_policy_ref: str
    drilldown_policy_ref: str
    health_status: TraceRouterHealthStatus
    warnings: List[str] = Field(default_factory=list)

class TracePacketRecord(BaseModel):
    trace_packet_id: str
    origin_ref: str
    traversed_node_refs: List[str] = Field(default_factory=list)
    traversed_edge_refs: List[str] = Field(default_factory=list)
    proof_refs: List[str] = Field(default_factory=list)
    caveat_refs: List[str] = Field(default_factory=list)
    freshness_refs: List[str] = Field(default_factory=list)
    no_safe_visibility_state: str
    output_scope: str
    warnings: List[str] = Field(default_factory=list)

class TraceRouteRecord(BaseModel):
    trace_route_id: str
    router_ref: str
    packet_ref: str
    outcome: TraceRouteOutcome
    warnings: List[str] = Field(default_factory=list)

class SovereignGovernanceTraceRouterManifestRecord(BaseModel):
    manifest_id: str
    router_refs: List[str] = Field(default_factory=list)
    route_refs: List[str] = Field(default_factory=list)

class SovereignGovernanceTraceRouterWarningRecord(BaseModel):
    warning_id: str
    router_ref: str
    message: str

class ProofFederationFamily(str, Enum):
    GOVERNANCE_PROOF_CATALOG_FEDERATION = "governance_proof_catalog_federation"
    REPLAY_PROOF_CATALOG_FEDERATION = "replay_proof_catalog_federation"
    DEBT_SETTLEMENT_PROOF_CATALOG_FEDERATION = "debt_settlement_proof_catalog_federation"
    NARRATIVE_INTEGRITY_PROOF_CATALOG_FEDERATION = "narrative_integrity_proof_catalog_federation"
    SOVEREIGNTY_PRESERVATION_PROOF_CATALOG_FEDERATION = "sovereignty_preservation_proof_catalog_federation"
    NO_SAFE_VISIBILITY_PROOF_CATALOG_FEDERATION = "no_safe_visibility_proof_catalog_federation"
    ASSURANCE_SNAPSHOT_PROOF_CATALOG_FEDERATION = "assurance_snapshot_proof_catalog_federation"

class FederationLinkStatus(str, Enum):
    LINK_CURRENT = "link_current"
    LINK_CAVEATED = "link_caveated"
    LINK_REVIEW_ONLY = "link_review_only"
    LINK_DEGRADED = "link_degraded"
    LINK_BLOCKED = "link_blocked"
    LINK_EXPIRED = "link_expired"
    LINK_SUPERSEDED = "link_superseded"

class FederatedProofOutput(str, Enum):
    FEDERATED_PROOF_CURRENT_WITH_CAPS = "federated_proof_current_with_caps"
    FEDERATED_PROOF_CAVEATED = "federated_proof_caveated"
    FEDERATED_PROOF_REVIEW_ONLY = "federated_proof_review_only"
    FEDERATED_PROOF_DEGRADED = "federated_proof_degraded"
    FEDERATED_PROOF_BLOCKED = "federated_proof_blocked"
    FEDERATED_PROOF_STALE = "federated_proof_stale"

class ProofCatalogFederationRecord(BaseModel):
    proof_federation_id: str
    federation_family: ProofFederationFamily
    member_proof_catalog_refs: List[str] = Field(default_factory=list)
    active_link_refs: List[str] = Field(default_factory=list)
    currentness_policy_ref: str
    lineage_policy_ref: str
    applicability_policy_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

class FederatedProofNodeRecord(BaseModel):
    node_id: str
    proof_catalog_ref: str
    proof_catalog_family: str
    supported_proof_classes: List[str] = Field(default_factory=list)
    currentness_state: str
    caveat_state: str
    sovereignty_state: str
    node_status: str
    warnings: List[str] = Field(default_factory=list)

class ProofFederationLinkRecord(BaseModel):
    link_id: str
    source_node_ref: str
    target_node_ref: str
    status: FederationLinkStatus

class ObservatorySignalExchangeFamily(str, Enum):
    INTERNAL_OBSERVATORY_SIGNAL_EXCHANGE = "internal_observatory_signal_exchange"
    REVIEW_ONLY_OBSERVATORY_SIGNAL_EXCHANGE = "review_only_observatory_signal_exchange"
    BOUNDED_OBSERVATORY_SIGNAL_EXCHANGE = "bounded_observatory_signal_exchange"
    SOVEREIGNTY_WARNING_SIGNAL_EXCHANGE = "sovereignty_warning_signal_exchange"
    NO_SAFE_VISIBILITY_SIGNAL_EXCHANGE = "no_safe_visibility_signal_exchange"
    DEGRADED_OBSERVATORY_SIGNAL_EXCHANGE = "degraded_observatory_signal_exchange"
    AUDIT_SUPPORT_SIGNAL_EXCHANGE = "audit_support_signal_exchange"

class ExchangeStatus(str, Enum):
    PREPARED = "prepared"
    VALIDATED = "validated"
    EXCHANGED_REVIEW_ONLY = "exchanged_review_only"
    EXCHANGED_BOUNDED = "exchanged_bounded"
    EXCHANGED_CAVEATED = "exchanged_caveated"
    EXCHANGED_DEGRADED = "exchanged_degraded"
    EXCHANGED_BLOCKED = "exchanged_blocked"
    EXCHANGED_EXPIRED = "exchanged_expired"
    EXCHANGED_SUPERSEDED = "exchanged_superseded"

class ObservatorySignalExchangeRecord(BaseModel):
    observatory_signal_exchange_id: str
    source_observatory_refs: List[str] = Field(default_factory=list)
    source_snapshot_refs: List[str] = Field(default_factory=list)
    target_scope_refs: List[str] = Field(default_factory=list)
    exchange_scope: str
    included_signal_refs: List[str] = Field(default_factory=list)
    preserved_caveat_refs: List[str] = Field(default_factory=list)
    currentness_refs: List[str] = Field(default_factory=list)
    exchange_status: ExchangeStatus
    warnings: List[str] = Field(default_factory=list)

class ObservatorySignalPacketRecord(BaseModel):
    signal_packet_id: str
    source_observatory_ref: str
    source_snapshot_ref: str
    included_signal_refs: List[str] = Field(default_factory=list)
    included_anomaly_refs: List[str] = Field(default_factory=list)
    included_alert_refs: List[str] = Field(default_factory=list)
    currentness_refs: List[str] = Field(default_factory=list)
    caveat_refs: List[str] = Field(default_factory=list)
    scope_constraints: str
    warnings: List[str] = Field(default_factory=list)

class CouncilFamily(str, Enum):
    FRESHNESS_INTEGRITY_COUNCIL = "freshness_integrity_council"
    CAVEAT_INTEGRITY_COUNCIL = "caveat_integrity_council"
    SOVEREIGNTY_VISIBILITY_INTEGRITY_COUNCIL = "sovereignty_visibility_integrity_council"
    NO_SAFE_INTEGRITY_COUNCIL = "no_safe_integrity_council"
    NARRATIVE_TRACE_INTEGRITY_COUNCIL = "narrative_trace_integrity_council"
    REPLAY_AND_DEBT_INTEGRITY_COUNCIL = "replay_and_debt_integrity_council"
    EXECUTIVE_SUMMARY_INTEGRITY_COUNCIL = "executive_summary_integrity_council"

class CaseFamily(str, Enum):
    STALE_NARRATIVE_INTEGRITY_CASE = "stale_narrative_integrity_case"
    MISSING_CAVEAT_INTEGRITY_CASE = "missing_caveat_integrity_case"
    MISSING_NO_SAFE_INTEGRITY_CASE = "missing_no_safe_integrity_case"
    SOVEREIGNTY_SUMMARY_INTEGRITY_CASE = "sovereignty_summary_integrity_case"
    PROOF_TRACE_GAP_CASE = "proof_trace_gap_case"
    DASHBOARD_NARRATIVE_DRIFT_CASE = "dashboard_narrative_drift_case"
    EXECUTIVE_OVERCOMPRESSION_CASE = "executive_overcompression_case"
    CONFLICTING_INTEGRITY_CASE = "conflicting_integrity_case"

class CaseStatus(str, Enum):
    CASE_OPENED = "case_opened"
    CASE_COLLECTING_EVIDENCE = "case_collecting_evidence"
    CASE_QUORUM_PENDING = "case_quorum_pending"
    CASE_DECIDED = "case_decided"
    CASE_DECIDED_WITH_CAVEATS = "case_decided_with_caveats"
    CASE_REVIEW_ONLY = "case_review_only"
    CASE_BLOCKED = "case_blocked"
    CASE_SUPERSEDED = "case_superseded"
    CASE_ARCHIVED = "case_archived"

class IntegrityDecisionType(str, Enum):
    PRESERVE_EXISTING_CAPS = "preserve_existing_caps"
    AMPLIFY_NARRATIVE_CAVEATS = "amplify_narrative_caveats"
    DOWNGRADE_TO_REVIEW_ONLY_NARRATIVE = "downgrade_to_review_only_narrative"
    REQUIRE_DASHBOARD_REFRESH = "require_dashboard_refresh"
    REQUIRE_PROOF_TRACE_REFRESH = "require_proof_trace_refresh"
    REQUIRE_SIGNAL_REVALIDATION = "require_signal_revalidation"
    PRESERVE_NO_SAFE_VISIBILITY = "preserve_no_safe_visibility"
    ACCEPT_BOUNDED_NARRATIVE_WITH_CAPS = "accept_bounded_narrative_with_caps"
    BLOCK_DUE_TO_UNRESOLVED_INTEGRITY_CONFLICT = "block_due_to_unresolved_integrity_conflict"

class NarrativeIntegrityCouncilRecord(BaseModel):
    narrative_integrity_council_id: str
    council_family: CouncilFamily
    governed_narrative_refs: List[str] = Field(default_factory=list)
    participant_refs: List[str] = Field(default_factory=list)
    quorum_policy_ref: str
    precedence_policy_ref: str
    backlog_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

class NarrativeIntegrityCaseRecord(BaseModel):
    narrative_integrity_case_id: str
    case_family: CaseFamily
    input_narrative_refs: List[str] = Field(default_factory=list)
    input_dashboard_refs: List[str] = Field(default_factory=list)
    input_proof_refs: List[str] = Field(default_factory=list)
    input_atlas_refs: List[str] = Field(default_factory=list)
    input_signal_refs: List[str] = Field(default_factory=list)
    decision_needed: str
    escalation_state: str
    case_status: CaseStatus
    warnings: List[str] = Field(default_factory=list)

class NarrativeIntegrityDecisionRecord(BaseModel):
    decision_id: str
    case_ref: str
    decision_type: IntegrityDecisionType
    caps: List[str] = Field(default_factory=list)

class TraceRoutingSummary(BaseModel):
    proof_federation_counts_by_health: Dict[str, int] = Field(default_factory=dict)
    signal_exchange_counts: Dict[str, int] = Field(default_factory=dict)
    integrity_council_case_counts: Dict[str, int] = Field(default_factory=dict)
    trace_router_route_counts: Dict[str, int] = Field(default_factory=dict)
    trace_query_counts: Dict[str, int] = Field(default_factory=dict)
    narrative_integrity_counts: Dict[str, int] = Field(default_factory=dict)
    overall_health: str = "healthy"
