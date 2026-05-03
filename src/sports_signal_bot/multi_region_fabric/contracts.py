from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class MultiRegionExecutionFabricRecord(BaseModel):
    fabric_id: str
    region_refs: List[str]
    cluster_refs: List[str]
    shard_refs: List[str]
    treaty_refs: List[str]
    sovereignty_policy_refs: List[str]
    active_status: str
    warnings: List[str] = Field(default_factory=list)

class RegionRecord(BaseModel):
    region_id: str
    region_family: str
    description: str

class RegionBoundaryRecord(BaseModel):
    boundary_id: str
    region_id: str
    restricted_families: List[str]

class RegionAffinityRecord(BaseModel):
    affinity_id: str
    affinity_type: str
    target_region: Optional[str] = None

class BrokerShardRecord(BaseModel):
    shard_id: str
    shard_family: str
    owning_region_ref: str
    owning_cluster_ref: str
    token_family_scope: List[str]
    approval_domain_scope: List[str]
    failover_candidates: List[str]
    current_status: str
    warnings: List[str] = Field(default_factory=list)

class ShardOwnershipPolicyRecord(BaseModel):
    policy_id: str
    shard_family: str
    rules: Dict[str, Any]

class ShardRoutingRecord(BaseModel):
    routing_id: str
    request_id: str
    routed_shard_id: str
    decision: str

class CrossClusterRecoveryTreatyRecord(BaseModel):
    treaty_id: str
    treaty_family: str
    treaty_parties: List[str]
    allowed_lane_families: List[str]
    forbidden_lane_families: List[str]
    delegation_rules: Dict[str, Any]
    token_acceptance_rules: Dict[str, Any]
    replay_requirements: Dict[str, Any]
    rollback_visibility_rules: Dict[str, Any]
    expiry: datetime
    warnings: List[str] = Field(default_factory=list)

class TreatyPartyRecord(BaseModel):
    party_id: str
    cluster_ref: str
    region_ref: str

class TreatyScopeRecord(BaseModel):
    scope_id: str
    treaty_id: str
    allowed_actions: List[str]

class TreatyConstraintRecord(BaseModel):
    constraint_id: str
    treaty_id: str
    constraint_type: str

class TreatyDecisionRecord(BaseModel):
    decision_id: str
    treaty_id: str
    outcome: str
    reasoning: str

class SovereigntyPolicyRecord(BaseModel):
    sovereignty_policy_id: str
    domain_ref: str
    local_execution_only_families: List[str]
    cross_region_review_requirements: List[str]
    approval_translation_rules: Dict[str, Any]
    token_nonportability_rules: Dict[str, Any]
    observability_export_limits: Dict[str, Any]
    failover_constraints: Dict[str, Any]
    warnings: List[str] = Field(default_factory=list)

class SovereigntyBoundaryRecord(BaseModel):
    boundary_id: str
    policy_id: str
    enforced_rules: List[str]

class SovereigntyDelegationRecord(BaseModel):
    delegation_id: str
    policy_id: str
    delegated_to: str
    allowed_actions: List[str]

class RegionFailoverRecord(BaseModel):
    failover_id: str
    source_region: str
    target_region: str
    status: str
    reason: str

class RegionTransferRecord(BaseModel):
    transfer_id: str
    source_region: str
    target_region: str
    status: str

class CrossRegionAdmissionRecord(BaseModel):
    admission_id: str
    lane_id: str
    source_region: str
    target_region: str
    outcome: str
    reasoning: str

class CrossRegionContentionRecord(BaseModel):
    contention_id: str
    contention_family: str
    regions_involved: List[str]
    outcome: str

class RecoveryTreatyManifest(BaseModel):
    manifest_id: str
    treaty_id: str
    snapshot_hash: str
    timestamp: datetime

class SovereigntyWarningRecord(BaseModel):
    warning_id: str
    policy_id: str
    issue: str

class RegionAuditRecord(BaseModel):
    audit_id: str
    region_id: str
    findings: List[str]

# More specific records as requested
class ShardRoutingDecisionRecord(BaseModel):
    decision_id: str
    shard_id: str
    outcome: str
    reasoning: str

class ShardRoutingConstraintRecord(BaseModel):
    constraint_id: str
    rule: str

class ShardBackpressureRecord(BaseModel):
    shard_id: str
    pressure_level: float

class ShardFallbackRecord(BaseModel):
    shard_id: str
    fallback_shard_id: str

class SovereigntyRuleRecord(BaseModel):
    rule_id: str
    rule_type: str

class SovereigntyConflictRecord(BaseModel):
    conflict_id: str
    description: str

class SovereigntyExceptionRecord(BaseModel):
    exception_id: str
    policy_id: str

class SovereigntyDecisionRecord(BaseModel):
    decision_id: str
    outcome: str

class TokenPortabilityRecord(BaseModel):
    token_id: str
    is_portable: bool
    allowed_regions: List[str]

class TokenReissuanceRecord(BaseModel):
    original_token_id: str
    new_token_id: str
    target_region: str

class RegionTokenConstraintRecord(BaseModel):
    region_id: str
    constraints: List[str]

class PortabilityDecisionRecord(BaseModel):
    decision_id: str
    outcome: str

class RegionSnapshotRecord(BaseModel):
    snapshot_id: str
    region_id: str
    timestamp: datetime
    hash_ref: str

class TreatySnapshotRecord(BaseModel):
    snapshot_id: str
    treaty_id: str
    timestamp: datetime

class ShardOwnershipSnapshotRecord(BaseModel):
    snapshot_id: str
    shard_id: str
    owner: str
    timestamp: datetime

class SnapshotTransferRecord(BaseModel):
    transfer_id: str
    snapshot_id: str
    target_region: str

class RegionalListingVisibilityRecord(BaseModel):
    listing_id: str
    region_id: str
    visibility: str

class TreatyListingAllowanceRecord(BaseModel):
    treaty_id: str
    listing_id: str

class SovereignListingRestrictionRecord(BaseModel):
    policy_id: str
    listing_id: str

class RegionRuntimeFitRecord(BaseModel):
    region_id: str
    is_fit: bool
