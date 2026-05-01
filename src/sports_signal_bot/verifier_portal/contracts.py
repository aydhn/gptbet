import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class VerifierPortalRecord(BaseModel):
    portal_id: str
    portal_family: str
    enabled_profiles: List[str] = Field(default_factory=list)
    available_views: List[str] = Field(default_factory=list)
    supported_feed_families: List[str] = Field(default_factory=list)
    challenge_api_enabled: bool = False
    notarized_disclosure_enabled: bool = False
    access_mode: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)


class PortalViewRecord(BaseModel):
    view_id: str
    view_name: str
    description: str


class PortalSessionRecord(BaseModel):
    session_id: str
    profile: str
    started_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class PortalAudienceProfileRecord(BaseModel):
    profile_id: str
    visible_view_families: List[str] = Field(default_factory=list)
    proof_depth: str
    challenge_submission_rights: bool = False
    feed_access_level: str
    notarization_visibility: bool = False
    anomaly_detail_depth: str
    signer_metadata_masking_level: str


class VerificationViewPacketRecord(BaseModel):
    packet_id: str
    packet_family: str
    audience_profile: str
    view_name: str
    source_bundle_refs: List[str] = Field(default_factory=list)
    proof_refs: List[str] = Field(default_factory=list)
    redaction_profile: str
    freshness: str
    supersession_status: str
    warnings: List[str] = Field(default_factory=list)
    content: Dict[str, Any] = Field(default_factory=dict)


class DashboardFeedRecord(BaseModel):
    feed_id: str
    feed_family: str
    content: List[Dict[str, Any]] = Field(default_factory=list)
    freshness: str
    generated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class FeedSubscriptionRecord(BaseModel):
    subscription_id: str
    feed_family: str
    subscriber_profile: str


class FeedDeliveryRecord(BaseModel):
    delivery_id: str
    feed_id: str
    delivered_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    status: str


class ChallengeAPIRecord(BaseModel):
    api_id: str
    enabled: bool
    allowed_issue_taxonomy: List[str] = Field(default_factory=list)


class ChallengeSubmissionRecord(BaseModel):
    submission_id: str
    issue_type: str
    details: str
    submitted_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    status: str = "received"
    trust_class: str = "unknown"
    quarantined: bool = False


class ChallengeSubmissionResponseRecord(BaseModel):
    response_id: str
    submission_id: str
    status: str
    message: str
    received_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class DisclosureDeliveryRecord(BaseModel):
    delivery_id: str
    bundle_id: str
    delivery_mode: str
    delivered_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class NotarizedDisclosureRecord(BaseModel):
    disclosure_id: str
    bundle_ref: str
    notary_receipt: Dict[str, Any] = Field(default_factory=dict)
    visible_to: List[str] = Field(default_factory=list)


class PortalAccessDecisionRecord(BaseModel):
    decision_id: str
    profile: str
    resource_type: str
    resource_id: str
    decision: str
    reason: str


class PortalUsageAuditRecord(BaseModel):
    audit_id: str
    action: str
    profile: str
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    details: Dict[str, Any] = Field(default_factory=dict)


class PortalWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str


class PortalQueryRecord(BaseModel):
    query_id: str
    query_type: str
    params: Dict[str, Any] = Field(default_factory=dict)
    profile: str


class PortalResultRecord(BaseModel):
    result_id: str
    query_id: str
    data: Dict[str, Any] = Field(default_factory=dict)


class PortalExportRecord(BaseModel):
    export_id: str
    export_type: str
    format: str
    data: Dict[str, Any] = Field(default_factory=dict)


class VerifierExperienceManifest(BaseModel):
    manifest_id: str
    portal_id: str
    generated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    summary: Dict[str, Any] = Field(default_factory=dict)


class QueryConstraintRecord(BaseModel):
    allowed_fields: List[str]
    max_limit: int

class QueryResultProfileRecord(BaseModel):
    profile: str
    redacted_fields: List[str]

class QuerySafetyDecisionRecord(BaseModel):
    safe: bool
    reason: str

class AccessClassRecord(BaseModel):
    class_id: str
    description: str

class AccessScopeRecord(BaseModel):
    scope_id: str
    allowed_resources: List[str]

class AccessRestrictionRecord(BaseModel):
    restriction_id: str
    blocked_resources: List[str]

class AccessAuditRecord(BaseModel):
    audit_id: str
    action: str

class PublicNotarizationLabelRecord(BaseModel):
    label_id: str
    verified: bool

class NotarizedDeliverySummaryRecord(BaseModel):
    delivery_id: str
    summary: str

class NotarizationVisibilityRuleRecord(BaseModel):
    rule_id: str
    visible_profiles: List[str]

class FeedFamilyRecord(BaseModel):
    family_id: str

class FeedSchemaRecord(BaseModel):
    schema_id: str

class FeedFreshnessRecord(BaseModel):
    freshness: str

class FeedCaveatRecord(BaseModel):
    caveats: List[str]

class FeedPublicationWindowRecord(BaseModel):
    window_id: str

class FeedEligibilityRecord(BaseModel):
    eligible: bool

class FeedDeliveryPolicyRecord(BaseModel):
    policy_id: str

class FeedStalenessRecord(BaseModel):
    stale: bool

class FeedConsumerProfileRecord(BaseModel):
    profile_id: str

class ChallengeAPISchemaRecord(BaseModel):
    schema_id: str

class ChallengeSubmissionWindowRecord(BaseModel):
    window_id: str

class SubmissionRatePolicyRecord(BaseModel):
    limit: int

class SubmissionValidationRecord(BaseModel):
    valid: bool

class PublicationSupersessionRecord(BaseModel):
    superseded: bool

class PublicationRetractionRecord(BaseModel):
    retracted: bool

class TombstonePublicationRecord(BaseModel):
    tombstone_id: str
