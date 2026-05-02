from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime

# --- Enums ---

class SubscriptionFamily(str, Enum):
    REGISTRY_CATALOG = "registry_catalog_subscription"
    VERIFIER_CATALOG = "verifier_catalog_subscription"
    PORTABLE_SPEC = "portable_spec_subscription"
    PORTABLE_PROOF = "portable_proof_subscription"
    PROTOCOL_PROFILE = "protocol_profile_subscription"
    NOTARIZED_SNAPSHOT = "notarized_snapshot_subscription"
    SUPERSESSION_MAP = "supersession_map_subscription"
    TRUST_METADATA = "trust_metadata_subscription"
    QUARANTINE_FEED = "quarantine_feed_subscription"
    DIRECTORY = "directory_subscription"

class SyncMode(str, Enum):
    MANUAL = "manual_pull"
    SCHEDULED = "scheduled_pull"
    INCREMENTAL = "incremental_snapshot_pull"
    FULL_REFRESH = "full_refresh_pull"
    REVIEW_QUARANTINE = "review_quarantine_pull"
    OVERLAY_REFRESH = "overlay_refresh_only"
    METADATA_ONLY = "metadata_only_pull"

class SubscriptionStatus(str, Enum):
    CREATED = "subscription_created"
    AWAITING_FIRST_SYNC = "awaiting_first_sync"
    ACTIVE_SYNCING = "active_syncing"
    ACTIVE_STALE = "active_stale"
    DEGRADED = "degraded"
    QUARANTINED = "quarantined_source"
    PAUSED = "sync_paused"
    BLOCKED = "sync_blocked"
    RETIRED = "retired"
    SUPERSEDED = "superseded"

class OverlayFamily(str, Enum):
    TRUST = "trust_overlay"
    FRESHNESS = "freshness_overlay"
    FEDERATION = "federation_overlay"
    QUARANTINE = "quarantine_overlay"
    NOTARIZATION = "notarization_overlay"
    SUPERSESSION = "supersession_overlay"
    NEGOTIATED_PROFILE = "negotiated_profile_overlay"

class OverlayMergeOutcome(str, Enum):
    CLEAN = "merged_clean"
    WITH_CAVEATS = "merged_with_caveats"
    CONFLICT_RETAINED = "conflict_retained"
    REVIEW_ONLY = "downgrade_to_review_only"
    QUARANTINED = "quarantine_overlay_entry"
    REPLACED = "superseded_replaced"
    STALE_VISIBLE = "stale_overlay_visible_not_current"

class RoutingStatus(str, Enum):
    SELECTED = "route_selected"
    SELECTED_WITH_CAVEATS = "route_selected_with_caveats"
    REVIEW_ONLY = "review_only_route"
    QUARANTINE_ONLY = "quarantine_only_route"
    NO_SAFE_ROUTE = "no_safe_route"
    STALE_AVAILABLE = "stale_route_available"
    DEGRADED = "degraded_route_selected"
    REROUTE_REQUIRED = "reroute_required"

class RoutingDecisionType(str, Enum):
    PREFER_TRUSTED = "prefer_trusted_current"
    PREFER_FRESH_REVIEW = "prefer_fresh_but_review_only"
    PREFER_NOTARIZED = "prefer_notarized_snapshot_with_replay"
    PREFER_QUARANTINE = "prefer_quarantine_path"
    SUPPRESS = "suppress_source"
    RETRY_LATER = "retry_after_sync"

class DriftOutcome(str, Enum):
    NO_DRIFT = "no_material_drift"
    REROUTE_REC = "reroute_recommended"
    REROUTE_REQ = "reroute_required"
    ROUTE_QUARANTINED = "route_quarantined"
    POLICY_UPDATE_NEEDED = "subscription_policy_update_needed"


# --- Core Models ---

class SyncWarningRecord(BaseModel):
    warning_id: str
    message: str
    timestamp: datetime

class RefreshWindowRecord(BaseModel):
    interval_seconds: int

class RetryPolicyRecord(BaseModel):
    max_attempts: int
    backoff_factor: float

class SourceSuppressionRuleRecord(BaseModel):
    threshold_seconds: int
    suppress: bool

class SyncAdmissionRuleRecord(BaseModel):
    require_signature: bool

class OverlayAllowanceRuleRecord(BaseModel):
    allow_downgrade: bool

class SubscriptionPolicyRecord(BaseModel):
    refresh_interval_hints: RefreshWindowRecord
    freshness_thresholds: Dict[str, int]
    allowed_target_families: List[SubscriptionFamily]
    trust_downgrade_triggers: List[str]
    stale_source_suppression_rules: SourceSuppressionRuleRecord
    sync_retry_policy: RetryPolicyRecord
    supersession_required_families: List[SubscriptionFamily]
    quarantine_on_mismatch_rules: Dict[str, Any]
    source_visibility_restrictions: List[str]
    overlay_merge_allowances: OverlayAllowanceRuleRecord

class DiscoverySubscriptionRecord(BaseModel):
    subscription_id: str
    subscription_family: SubscriptionFamily
    target_catalog_ref: str
    target_scope: Dict[str, Any]
    subscribed_families: List[SubscriptionFamily]
    refresh_policy: SubscriptionPolicyRecord
    trust_policy_ref: str
    sync_mode: SyncMode
    current_status: SubscriptionStatus
    last_success_at: Optional[datetime] = None
    warnings: List[SyncWarningRecord] = Field(default_factory=list)

class SubscriptionTargetRecord(BaseModel):
    target_id: str
    uri: str
    capabilities: List[str]

class SubscriptionEventRecord(BaseModel):
    event_id: str
    event_family: str
    subscription_id: str
    timestamp: datetime
    details: Dict[str, Any]

class OverlayLineageRecord(BaseModel):
    source_ref: str
    provenance_hash: str
    timestamp: datetime

class OverlayConflictRecord(BaseModel):
    conflict_type: str
    refs: List[str]
    description: str

class OverlayTrustDiffRecord(BaseModel):
    base_trust: float
    source_trust: float
    diff: float

class OverlayFreshnessDiffRecord(BaseModel):
    base_timestamp: datetime
    source_timestamp: datetime
    lag_seconds: int

class OverlaySourceRecord(BaseModel):
    source_id: str
    source_family: OverlayFamily

class CatalogOverlayRecord(BaseModel):
    overlay_id: str
    overlay_family: OverlayFamily
    base_catalog_ref: str
    source_catalog_refs: List[str]
    merged_entry_refs: List[str]
    overlay_policy_ref: str
    lineage_refs: List[OverlayLineageRecord]
    freshness_state: str
    trust_state: str
    warnings: List[SyncWarningRecord] = Field(default_factory=list)

class OverlayMergeDecisionRecord(BaseModel):
    decision_id: str
    overlay_id: str
    outcome: OverlayMergeOutcome
    conflicts: List[OverlayConflictRecord] = Field(default_factory=list)

class RoutingWeightComponentRecord(BaseModel):
    component_name: str
    weight: float

class RoutingScoreBreakdownRecord(BaseModel):
    base_score: float
    components: List[RoutingWeightComponentRecord]
    total_score: float

class RoutingPenaltyRecord(BaseModel):
    penalty_name: str
    deduction: float

class RoutingCandidateRecord(BaseModel):
    candidate_ref: str
    score_breakdown: RoutingScoreBreakdownRecord
    penalties: List[RoutingPenaltyRecord] = Field(default_factory=list)

class EcosystemRoutingRecord(BaseModel):
    routing_id: str
    query_ref: str
    candidate_refs: List[RoutingCandidateRecord]
    selected_route_refs: List[str]
    weighting_profile: str
    trust_weight_summary: float
    freshness_weight_summary: float
    compatibility_weight_summary: float
    routing_status: RoutingStatus
    warnings: List[SyncWarningRecord] = Field(default_factory=list)

class RoutingWeightRecord(BaseModel):
    weight_id: str
    value: float

class RoutingDecisionRecord(BaseModel):
    decision_id: str
    routing_id: str
    decision_type: RoutingDecisionType
    rationale: str

class SyncPlanRecord(BaseModel):
    plan_id: str
    subscriptions_to_sync: List[str]
    sync_mode: SyncMode
    timestamp: datetime

class SourceSyncCheckpointRecord(BaseModel):
    source_ref: str
    last_seen_digest: str
    timestamp: datetime

class LocalSyncCheckpointRecord(BaseModel):
    local_ref: str
    last_synced_digest: str
    timestamp: datetime

class SyncCheckpointRecord(BaseModel):
    checkpoint_id: str
    source: SourceSyncCheckpointRecord
    local: LocalSyncCheckpointRecord

class SyncLagRecord(BaseModel):
    lag_id: str
    subscription_id: str
    lag_seconds: int
    is_stale: bool

class SyncConflictRecord(BaseModel):
    conflict_id: str
    description: str

class SyncHealthRecord(BaseModel):
    health_id: str
    status: str
    stale_count: int

class SyncStalenessRecord(BaseModel):
    staleness_id: str
    is_stale: bool

class SupersessionPropagationRecord(BaseModel):
    propagation_id: str
    superseded_ref: str
    new_ref: str
    timestamp: datetime

class CatalogOverlayManifest(BaseModel):
    manifest_id: str
    overlays: List[CatalogOverlayRecord]
    timestamp: datetime

class EcosystemSyncRunRecord(BaseModel):
    run_id: str
    plan_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    lag_records: List[SyncLagRecord] = Field(default_factory=list)

class EcosystemSyncAuditRecord(BaseModel):
    audit_id: str
    run_ref: str
    summary: Dict[str, Any]
    timestamp: datetime

class RoutingPolicyRecord(BaseModel):
    policy_id: str
    strategy: str

class RouteSelectionConstraintRecord(BaseModel):
    constraint_id: str
    require_freshness: bool

class RouteFallbackPolicyRecord(BaseModel):
    fallback_id: str
    allow_stale: bool

class RouteVisibilityPolicyRecord(BaseModel):
    visibility_id: str
    hide_quarantined: bool

class RoutingCacheRecord(BaseModel):
    cache_id: str
    query_family: str
    best_current_candidates: List[str]
    safe_subset_protocol_hints: List[str]
    freshness_state: str
    required_caveats: List[str]
    invalidated_candidates: List[str]
    quarantine_only_candidates: List[str]
    fallback_candidates: List[str]

class CachedRoutingEntryRecord(BaseModel):
    entry_id: str
    candidate_ref: str

class RoutingInvalidationRecord(BaseModel):
    invalidation_id: str
    reason: str

class FallbackRouteRecord(BaseModel):
    fallback_id: str
    candidate_ref: str

class SubscriptionQuarantineRecord(BaseModel):
    quarantine_id: str
    subscription_id: str
    reason: str
    timestamp: datetime

class SourceTrustDowngradeRecord(BaseModel):
    downgrade_id: str
    source_ref: str
    old_trust: float
    new_trust: float

class SyncFailureClusterRecord(BaseModel):
    cluster_id: str
    failures: int

class QuarantineRecoveryRecord(BaseModel):
    recovery_id: str
    quarantine_id: str
    timestamp: datetime
