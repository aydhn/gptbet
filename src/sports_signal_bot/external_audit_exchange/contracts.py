import datetime
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field

class ExternalAuditRequestRecord(BaseModel):
    external_request_id: str
    request_family: str
    target_ref: str
    packet_ref: str
    target_scope: Dict[str, Any]
    redaction_profile: str
    requested_verification_type: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class ExternalAuditFindingRecord(BaseModel):
    finding_id: str
    finding_family: str
    severity: str
    target_ref: str
    description: str
    evidence_refs: List[str] = Field(default_factory=list)

class ExternalAuditResponseRecord(BaseModel):
    external_response_id: str
    request_id: str
    responder_family: str
    response_status: str
    findings: List[ExternalAuditFindingRecord] = Field(default_factory=list)
    attestation_refs: Optional[List[str]] = None
    notarization_refs: Optional[List[str]] = None
    trust_level_claimed: str
    verification_needed: bool = True
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class ExternalAuditExchangeRecord(BaseModel):
    exchange_id: str
    request: ExternalAuditRequestRecord
    response: Optional[ExternalAuditResponseRecord] = None
    status: str
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class AuditExchangeAdapterRecord(BaseModel):
    adapter_id: str
    adapter_family: str
    supported_request_families: List[str]
    capabilities: List[str]

class NotarizationRequestRecord(BaseModel):
    request_id: str
    digest: str
    notary_provider: str
    target_ref: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class NotarizationReceiptRecord(BaseModel):
    receipt_id: str
    request_id: str
    notary_provider: str
    receipt_payload: str
    notarized_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class NotarizationVerificationRecord(BaseModel):
    verification_id: str
    receipt_id: str
    status: str
    verified_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class ReputationSignalRecord(BaseModel):
    signal_id: str
    witness_id: str
    signal_type: str
    value: float
    context_ref: str
    recorded_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class ReputationAdjustmentRecord(BaseModel):
    adjustment_id: str
    witness_id: str
    adjustment_type: str
    score_delta: float
    reason: str
    applied_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class WitnessReputationRecord(BaseModel):
    witness_id: str
    reputation_score: float
    reputation_band: str
    signal_breakdown: Dict[str, float] = Field(default_factory=dict)
    freshness: str
    downgrade_flags: List[str] = Field(default_factory=list)
    upgrade_flags: List[str] = Field(default_factory=list)
    last_updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class ChallengeExchangePacketRecord(BaseModel):
    packet_id: str
    challenge_ref: str
    severity: str
    target_ref: str
    safe_payload: Dict[str, Any]
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class ExternalVerificationImportRecord(BaseModel):
    import_id: str
    external_response_id: str
    status: str
    local_actions: List[str] = Field(default_factory=list)

class ExternalVerificationDecisionRecord(BaseModel):
    decision_id: str
    import_id: str
    decision: str
    justification: str

class ExchangeReadinessRecord(BaseModel):
    readiness_id: str
    status: str
    dimensions: Dict[str, float]
    score: float
    generated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class ExternalAuditManifest(BaseModel):
    manifest_id: str
    exported_requests: int
    imported_responses: int
    quarantined_responses: int
    notarizations_verified: int
    notarizations_unverified: int
    reputation_distribution: Dict[str, int]
    generated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class ExchangeWarningRecord(BaseModel):
    warning_id: str
    warning_type: str
    context_ref: str
    message: str

class ExternalAuditAuditRecord(BaseModel):
    audit_id: str
    event_type: str
    target_ref: str
    details: Dict[str, Any]
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class ExternalProviderCapabilityRecord(BaseModel):
    provider_id: str
    capabilities: List[str]

class ExternalExchangeScopeRecord(BaseModel):
    scope_id: str
    allowed_families: List[str]
    denied_families: List[str]

class NotaryProviderRecord(BaseModel):
    provider_id: str
    name: str

class NotaryCapabilityRecord(BaseModel):
    provider_id: str
    supported_digests: List[str]

class NotaryTrustRecord(BaseModel):
    provider_id: str
    trust_level: str

class NotarizationDigestRecord(BaseModel):
    digest: str
    family: str
    target_ref: str

class ChallengeRoutingRecord(BaseModel):
    routing_id: str
    challenge_ref: str
    suggested_responder_class: str
    priority_score: float

class ChallengeTriageRecord(BaseModel):
    triage_id: str
    challenge_ref: str
    status: str
    priority: str
    assigned_responder_class: Optional[str] = None

class ChallengeClusterRecord(BaseModel):
    cluster_id: str
    challenge_refs: List[str]
    cluster_reason: str

class ChallengeResponderProfileRecord(BaseModel):
    profile_id: str
    responder_class: str
    reputation_required: float

class ChallengeMarketplaceReadinessRecord(BaseModel):
    readiness_id: str
    status: str
    metrics: Dict[str, float]

class ExternalVerifierProfileRecord(BaseModel):
    profile_id: str
    verifier_id: str
    trust_score: float

class FederatedAuditExchangeRecord(BaseModel):
    exchange_id: str
    local_exchange_ref: str
    federated_nodes_involved: List[str]

class ExternalResponseTrustEnvelopeRecord(BaseModel):
    envelope_id: str
    response_ref: str
    trust_assertions: List[str]
