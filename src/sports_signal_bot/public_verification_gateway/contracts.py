from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from pydantic import BaseModel, Field

class PublicationWarningRecord(BaseModel):
    warning_code: str
    description: str
    severity: str
    mitigation_hint: Optional[str] = None

class DisclosureBundleRecord(BaseModel):
    disclosure_bundle_id: str
    bundle_family: str
    publication_profile: str
    source_refs: List[str]
    included_items: List[str]
    redaction_profile: str
    verification_refs: List[str]
    publishability_status: str
    created_at: datetime
    warnings: List[PublicationWarningRecord] = Field(default_factory=list)

class PublicationProfileRecord(BaseModel):
    profile_id: str
    profile_name: str
    audience_family: str
    redaction_level: str
    allowed_item_families: List[str]
    forbidden_field_families: List[str]
    proof_depth: str
    notarization_visibility: str
    challenge_intake_allowed: bool
    warnings: List[PublicationWarningRecord] = Field(default_factory=list)

class PublicationScopeRecord(BaseModel):
    scope_id: str
    target_audiences: List[str]
    allowed_families: List[str]
    time_window_hours: Optional[int] = None

class GatewayIndexEntryRecord(BaseModel):
    bundle_id: str
    family: str
    version: str
    publication_profile: str
    proof_coverage_summary: str
    notarization_summary: Optional[str] = None
    freshness: str
    supersession_status: str
    challenge_intake_endpoint_ref: Optional[str] = None
    signed_checkpoint_refs: Optional[List[str]] = None

class PublicationIndexRecord(BaseModel):
    index_id: str
    generated_at: datetime
    entries: List[GatewayIndexEntryRecord]

class GatewayChannelRecord(BaseModel):
    channel_id: str
    profile: str
    active: bool

class GatewayEndpointRecord(BaseModel):
    endpoint_id: str
    channel_id: str
    endpoint_type: str

class VerificationGatewayRecord(BaseModel):
    gateway_id: str
    channels: List[GatewayChannelRecord]
    endpoints: List[GatewayEndpointRecord]

class PublicPacketRecord(BaseModel):
    packet_id: str
    bundle_id: str
    metadata: Dict[str, Any]
    claimed_content: Dict[str, Any]
    independently_checkable: List[str]
    proof_refs: List[str]
    redaction_notice: str
    caveats: List[str]
    publication_time: datetime
    supersession_marker: Optional[str] = None
    challenge_instructions: Optional[str] = None

class ExternalVerifierPacketRecord(BaseModel):
    packet_id: str
    base_packet: PublicPacketRecord
    deeper_inclusion_refs: List[str]
    broader_witness_summary: str
    richer_anomaly_context: Optional[str] = None
    audit_trail_linkage: List[str]
    exchange_request_correlation_ids: List[str]

class PublicDisclosureManifest(BaseModel):
    manifest_id: str
    generated_at: datetime
    index_ref: str
    total_bundles: int
    readiness_status: str

class PublicationRedactionRuleRecord(BaseModel):
    rule_id: str
    target_family: str
    fields_to_redact: List[str]
    masking_strategy: str

class DisclosureRedactionDecisionRecord(BaseModel):
    decision_id: str
    bundle_id: str
    applied_rules: List[str]
    redacted_fields_count: int

class RedactionPublicationRecord(BaseModel):
    record_id: str
    bundle_id: str
    redaction_decision_ref: str
    safe_to_publish: bool

class PublicationLeakCheckRecord(BaseModel):
    check_id: str
    bundle_id: str
    passed: bool
    detected_leaks: List[str]

class DisclosureCoverageRecord(BaseModel):
    coverage_id: str
    family: str
    coverage_score: float
    band: str
    gaps: List[str]

class PublicationDecisionRecord(BaseModel):
    decision_id: str
    bundle_id: str
    decision: str
    blockers: List[str]
    caveats: List[str]
    evaluated_at: datetime

class PublicChallengeIntakeRecord(BaseModel):
    intake_id: str
    envelope_id: str
    status: str
    trust_class: str
    received_at: datetime

class PublicChallengeEnvelopeRecord(BaseModel):
    envelope_id: str
    payload: Dict[str, Any]
    signature: Optional[str] = None

class ChallengeIntakeDecisionRecord(BaseModel):
    decision_id: str
    intake_id: str
    action: str
    reason: str

class IntakeQuarantineReasonRecord(BaseModel):
    reason_code: str
    description: str

class ChallengeIntakeQuarantineRecord(BaseModel):
    quarantine_id: str
    intake_id: str
    reasons: List[IntakeQuarantineReasonRecord]
    quarantined_at: datetime

class PublicVerificationSummaryRecord(BaseModel):
    summary_id: str
    generated_at: datetime
    metrics: Dict[str, Any]
    readiness_score: str

class DisclosureAuditRecord(BaseModel):
    audit_id: str
    bundle_id: str
    audited_by: str
    audit_time: datetime
    findings: List[str]

class PublicationDiscoveryRecord(BaseModel):
    discovery_id: str
    available_profiles: List[str]
    endpoints: List[str]

class PublicationAccessRuleRecord(BaseModel):
    rule_id: str
    profile_id: str
    allowed_audiences: List[str]

class ChallengeIntakeSchemaRecord(BaseModel):
    schema_id: str
    version: str
    required_fields: List[str]

class IntakeRateLimitRecord(BaseModel):
    limit_id: str
    trust_class: str
    max_requests_per_hour: int

class IntakeDedupRecord(BaseModel):
    dedup_id: str
    intake_id: str
    duplicate_of: Optional[str] = None

class IntakeTrustClassRecord(BaseModel):
    class_id: str
    description: str
    action_level: str

class IntakeSanitizationRecord(BaseModel):
    sanitization_id: str
    intake_id: str
    cleaned_fields: List[str]
    rejected_fields: List[str]

class VerifierProfileRecord(BaseModel):
    profile_id: str
    verifier_class: str
    trust_level: str

class VerifierCapabilityRecord(BaseModel):
    capability_id: str
    profile_id: str
    allowed_actions: List[str]

class VerifierAccessPolicyRecord(BaseModel):
    policy_id: str
    profile_id: str
    allowed_publication_profiles: List[str]

class ExternalVerifierOnrampRecord(BaseModel):
    onramp_id: str
    verifier_id: str
    profile_ref: str
    status: str

class PublicClaimRecord(BaseModel):
    claim_id: str
    description: str

class PublicCitationRecord(BaseModel):
    citation_id: str
    source: str
    description: str

class PublicCaveatRecord(BaseModel):
    caveat_id: str
    description: str

class PublicEvidencePacketRecord(BaseModel):
    packet_id: str
    claim: PublicClaimRecord
    citations: List[PublicCitationRecord]
    caveats: List[PublicCaveatRecord]

class PublicationQuarantineRecord(BaseModel):
    quarantine_id: str
    bundle_id: str
    reason: str
    quarantined_at: datetime

class DisclosureReviewQueueRecord(BaseModel):
    queue_id: str
    bundle_id: str
    status: str
    added_at: datetime
