from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class CatalogEntryRecord(BaseModel):
    entry_id: str
    entry_family: str
    target_ref: str
    display_name: str
    capability_summary: Dict[str, Any] = Field(default_factory=dict)
    claim_family_summary: List[str] = Field(default_factory=list)
    proof_family_summary: List[str] = Field(default_factory=list)
    spec_family_summary: List[str] = Field(default_factory=list)
    trust_notes: List[str] = Field(default_factory=list)
    availability_status: str
    freshness: float
    warnings: List[str] = Field(default_factory=list)

class AssuranceRegistryCatalogRecord(BaseModel):
    catalog_id: str
    catalog_name: str
    catalog_family: str
    owner_registry_ref: str
    published_entries: List[CatalogEntryRecord] = Field(default_factory=list)
    supported_query_families: List[str] = Field(default_factory=list)
    trust_profile: str
    freshness_state: str
    active_status: str
    warnings: List[str] = Field(default_factory=list)

class CatalogIndexRecord(BaseModel):
    catalogs: List[str] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class DiscoveryQueryRecord(BaseModel):
    query_id: str
    query_family: str
    target_criteria: Dict[str, Any] = Field(default_factory=dict)

class DiscoveryResultRecord(BaseModel):
    result_id: str
    query_id: str
    status: str
    matched_entries: List[CatalogEntryRecord] = Field(default_factory=list)

class DiscoveryTrustRecord(BaseModel):
    trust_band: str
    score: float
    drivers: List[str] = Field(default_factory=list)

class CatalogTrustScoreRecord(BaseModel):
    catalog_id: str
    score: float
    components: Dict[str, float] = Field(default_factory=dict)

class VerifierProtocolProfileRecord(BaseModel):
    protocol_profile_id: str
    profile_name: str
    supported_request_families: List[str] = Field(default_factory=list)
    supported_response_families: List[str] = Field(default_factory=list)
    supported_negotiation_modes: List[str] = Field(default_factory=list)
    supported_proof_formats: List[str] = Field(default_factory=list)
    supported_redaction_profiles: List[str] = Field(default_factory=list)
    supported_replay_modes: List[str] = Field(default_factory=list)
    trust_constraints: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)

class ProtocolNegotiationTemplateRecord(BaseModel):
    template_id: str
    offered_profile: VerifierProtocolProfileRecord

class PortableProofCatalogRecord(BaseModel):
    proof_family: str
    carried_claim_families: List[str] = Field(default_factory=list)
    compatible_spec_families: List[str] = Field(default_factory=list)
    supported_replay_modes: List[str] = Field(default_factory=list)
    notarization_availability: bool = False

class ProofAvailabilityRecord(BaseModel):
    state: str
    proof_ref: str

class RetrievalHintRecord(BaseModel):
    hint_type: str
    instructions: str

class DirectoryNodeRecord(BaseModel):
    node_id: str
    node_type: str
    name: str

class DirectoryLinkRecord(BaseModel):
    source_id: str
    target_id: str
    relationship: str

class DirectoryTrustBoundaryRecord(BaseModel):
    boundary_id: str
    nodes: List[str] = Field(default_factory=list)

class DirectoryDiscoveryHintRecord(BaseModel):
    hint: str

class EcosystemDirectoryRecord(BaseModel):
    directory_id: str
    catalogs: List[DirectoryNodeRecord] = Field(default_factory=list)
    registries: List[DirectoryNodeRecord] = Field(default_factory=list)
    verifier_nodes: List[DirectoryNodeRecord] = Field(default_factory=list)
    supported_trust_domains: List[str] = Field(default_factory=list)
    protocol_profile_families: List[str] = Field(default_factory=list)
    ecosystem_discovery_health: str = "unknown"
    recommended_negotiation_paths: List[str] = Field(default_factory=list)
    restricted_zones: List[str] = Field(default_factory=list)
    quarantine_sources: List[str] = Field(default_factory=list)

class DiscoveryPolicyRecord(BaseModel):
    allowed_source_catalogs: List[str] = Field(default_factory=list)
    trusted_discovery_families: List[str] = Field(default_factory=list)
    hidden_artifact_families: List[str] = Field(default_factory=list)

class DiscoveryDecisionRecord(BaseModel):
    decision: str
    reason: str

class CatalogWarningRecord(BaseModel):
    catalog_id: str
    warning: str

class DiscoveryAuditRecord(BaseModel):
    audit_id: str
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CatalogFreshnessRecord(BaseModel):
    catalog_id: str
    freshness_score: float
    last_verified: datetime

class DiscoveryCoverageRecord(BaseModel):
    registry_coverage: str = "sparse"
    verifier_profile_coverage: str = "sparse"
    spec_bundle_coverage: str = "sparse"

class EcosystemDiscoveryManifest(BaseModel):
    manifest_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    directory_ref: str
    catalogs: List[str] = Field(default_factory=list)
    coverage: DiscoveryCoverageRecord = Field(default_factory=DiscoveryCoverageRecord)

class CatalogOwnerRecord(BaseModel):
    owner_id: str

class CatalogScopeRecord(BaseModel):
    scope_id: str

class CatalogCapabilitySummaryRecord(BaseModel):
    capabilities: List[str] = Field(default_factory=list)

class CatalogVisibilityRecord(BaseModel):
    visibility: str

class CatalogSupersessionRecord(BaseModel):
    superseded_by: str

class PortableProofProfileRecord(BaseModel):
    profile_id: str

class ProofSupportMatrixRecord(BaseModel):
    support_matrix: Dict[str, Any] = Field(default_factory=dict)

class ProofVisibilityRecord(BaseModel):
    visibility: str

class ProofRetrievalPolicyRecord(BaseModel):
    policy: str

class AllowedCatalogRuleRecord(BaseModel):
    rule_id: str

class DiscoverySuppressionRuleRecord(BaseModel):
    rule_id: str

class DiscoveryTrustPolicyRecord(BaseModel):
    policy_id: str

class RestrictedArtifactRuleRecord(BaseModel):
    rule_id: str

class ProtocolDimensionRecord(BaseModel):
    dimension_name: str
    support_level: str

class ProtocolGapRecord(BaseModel):
    gap_id: str

class ProtocolCompatibilityDecisionRecord(BaseModel):
    decision: str

class ProtocolCaveatRecord(BaseModel):
    caveat: str

class PortableSpecCatalogEntryRecord(BaseModel):
    spec_family: str
    supported_versions: List[str] = Field(default_factory=list)
    semantic_tags: List[str] = Field(default_factory=list)

class SpecCapabilitySummaryRecord(BaseModel):
    capabilities: List[str] = Field(default_factory=list)

class SpecNegotiationHintRecord(BaseModel):
    hint: str

class SpecPortabilityVisibilityRecord(BaseModel):
    visibility: str

class ProofMarketplaceStyleRecord(BaseModel):
    listing_id: str

class ListingRankRecord(BaseModel):
    rank: int

class DiscoverySelectionRecord(BaseModel):
    selection_id: str

class RetrievalComplexityRecord(BaseModel):
    complexity_score: float

class CatalogMatchReasonRecord(BaseModel):
    reason: str

class DiscoveryQuarantineRecord(BaseModel):
    quarantine_id: str
    target_ref: str

class DiscoveryQuarantineReasonRecord(BaseModel):
    reason: str

class QuarantinedCatalogEntryRecord(BaseModel):
    entry_id: str

class DiscoverabilityPolicyRecord(BaseModel):
    policy_id: str

class ListingVisibilityPolicyRecord(BaseModel):
    policy_id: str

class FederationExposureRuleRecord(BaseModel):
    rule_id: str
