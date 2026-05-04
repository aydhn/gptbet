import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class QuorumAttestationRecord(BaseModel):
    quorum_attestation_id: str
    source_council_case_ref: str
    council_ref: str
    attestation_family: str
    attested_decision_type: str
    quorum_summary: str
    supporting_vote_refs: List[str] = Field(default_factory=list)
    supporting_evidence_refs: List[str] = Field(default_factory=list)
    caveat_refs: List[str] = Field(default_factory=list)
    validity_window: str
    attestation_status: str
    warnings: List[str] = Field(default_factory=list)

class QuorumAttestationEnvelopeRecord(BaseModel):
    envelope_id: str
    attestation_ref: str
    source_scope_ref: str
    governed_tier_refs: List[str] = Field(default_factory=list)
    preserved_currentness_refs: List[str] = Field(default_factory=list)
    preserved_caveat_refs: List[str] = Field(default_factory=list)
    replay_support_refs: List[str] = Field(default_factory=list)
    integrity_refs: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class SignalRoutingBackplaneRecord(BaseModel):
    backplane_id: str
    backplane_family: str
    segment_refs: List[str] = Field(default_factory=list)
    channel_refs: List[str] = Field(default_factory=list)
    active_flow_refs: List[str] = Field(default_factory=list)
    capacity_refs: List[str] = Field(default_factory=list)
    backpressure_refs: List[str] = Field(default_factory=list)
    health_status: str
    warnings: List[str] = Field(default_factory=list)

class BackplaneChannelRecord(BaseModel):
    backplane_channel_id: str
    source_segment_ref: str
    target_segment_ref: str
    supported_signal_families: List[str] = Field(default_factory=list)
    supported_scope_classes: List[str] = Field(default_factory=list)
    backpressure_state: str
    freshness_state: str
    caveat_transfer_policy: str
    channel_status: str
    warnings: List[str] = Field(default_factory=list)

class BaselineFederationMeshRecord(BaseModel):
    baseline_mesh_id: str
    mesh_family: str
    node_refs: List[str] = Field(default_factory=list)
    edge_refs: List[str] = Field(default_factory=list)
    currentness_policy_ref: str
    applicability_policy_ref: str
    supersession_policy_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

class BaselineMeshEdgeRecord(BaseModel):
    edge_id: str
    source_baseline_node_ref: str
    target_baseline_node_ref: str
    supported_baseline_families: List[str] = Field(default_factory=list)
    applicability_constraints: str
    currentness_state: str
    drift_state: str
    edge_status: str
    warnings: List[str] = Field(default_factory=list)

class SovereignAuditDisputeRecord(BaseModel):
    dispute_id: str
    dispute_family: str
    source_projection_ref: str
    conflicting_projection_refs: List[str] = Field(default_factory=list)
    affected_scope_ref: str
    opened_reason: str
    evidence_set_refs: List[str] = Field(default_factory=list)
    mediation_session_ref: Optional[str] = None
    dispute_status: str
    warnings: List[str] = Field(default_factory=list)

class DisputeCaseRecord(BaseModel):
    dispute_case_id: str
    dispute_ref: str
    case_family: str
    input_claim_refs: List[str] = Field(default_factory=list)
    input_evidence_refs: List[str] = Field(default_factory=list)
    replay_requirement: str
    sovereignty_constraints: str
    mediation_needed: bool
    case_status: str
    warnings: List[str] = Field(default_factory=list)
