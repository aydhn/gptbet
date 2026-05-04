from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class OverlayMeshWarningRecord(BaseModel):
    warning_type: str
    description: str

class OverlayMeshCaveatRecord(BaseModel):
    caveat_id: str
    caveat_description: str
    caveat_source: str

class OverlayMeshConstraintRecord(BaseModel):
    constraint_id: str
    constraint_type: str
    details: Dict[str, Any]

class OverlayMeshCurrentnessRecord(BaseModel):
    currentness_state: str
    last_updated: datetime
    expiration: datetime

class OverlayMeshHealthRecord(BaseModel):
    status: str
    details: Dict[str, str]

class OverlayMeshManifestRecord(BaseModel):
    manifest_id: str
    created_at: datetime
    content: Dict[str, Any]

class OverlayMeshNodeRecord(BaseModel):
    node_id: str
    node_family: str
    supported_scopes: List[str]
    warnings: List[OverlayMeshWarningRecord] = Field(default_factory=list)

class OverlayMeshEdgeRecord(BaseModel):
    edge_id: str
    source_node_ref: str
    target_node_ref: str
    supported_exchange_scopes: List[str]
    supported_projection_families: List[str]
    currentness_state: OverlayMeshCurrentnessRecord
    caveat_policy_ref: str
    sovereignty_constraints: List[OverlayMeshConstraintRecord]
    edge_status: str
    warnings: List[OverlayMeshWarningRecord] = Field(default_factory=list)

class OverlayMeshPathRecord(BaseModel):
    path_id: str
    node_sequence: List[str]
    edge_sequence: List[str]
    path_caveats: List[OverlayMeshCaveatRecord]
    path_status: str

class OverlayExchangeMeshRecord(BaseModel):
    overlay_mesh_id: str
    mesh_family: str
    node_refs: List[str]
    edge_refs: List[str]
    propagation_policy_ref: str
    currentness_policy_ref: str
    degradation_policy_ref: str
    health_status: OverlayMeshHealthRecord
    warnings: List[OverlayMeshWarningRecord] = Field(default_factory=list)

class PropagationDimensionRecord(BaseModel):
    dimension_name: str
    dimension_value: Any

class PropagationDecayRecord(BaseModel):
    decay_reason: str
    decay_amount: float

class PropagationReplaySupportRecord(BaseModel):
    support_id: str
    support_ref: str

class PropagationVisibilityDecisionRecord(BaseModel):
    visibility_status: str
    reasons: List[str]

class OverlayMeshPropagationRecord(BaseModel):
    propagation_id: str
    source_overlay_ref: str
    propagation_path: OverlayMeshPathRecord
    projected_dimensions: List[PropagationDimensionRecord]
    preserved_caveats: List[OverlayMeshCaveatRecord]
    currentness_decay: PropagationDecayRecord
    replay_support_refs: List[PropagationReplaySupportRecord]
    downgrade_reasons: List[str]
    target_visibility_result: PropagationVisibilityDecisionRecord

class RouteGovernanceWarningRecord(BaseModel):
    warning_type: str
    description: str

class RouteGovernanceConstraintRecord(BaseModel):
    constraint_id: str
    constraint_type: str

class TierDowngradeRecord(BaseModel):
    downgrade_reason: str
    details: str

class TierBlockingReasonRecord(BaseModel):
    blocking_reason: str
    details: str

class GovernanceTierPolicyRecord(BaseModel):
    policy_id: str
    rules: Dict[str, Any]

class RouteGovernanceManifestRecord(BaseModel):
    manifest_id: str
    created_at: datetime
    content: Dict[str, Any]

class TierPrecedenceRecord(BaseModel):
    precedence_rule_id: str
    precedence_order: List[str]

class RouteGovernanceTierRecord(BaseModel):
    tier_id: str
    tier_family: str
    tier_scope: str
    policy_ref: str
    precedence_rank: int
    downgrade_rules: List[TierDowngradeRecord]
    block_rules: List[TierBlockingReasonRecord]
    visibility_profile: str
    warnings: List[RouteGovernanceWarningRecord] = Field(default_factory=list)

class MultiTierRouteGovernanceRecord(BaseModel):
    governance_id: str
    tier_refs: List[str]
    tier_precedence_rules: TierPrecedenceRecord
    supported_route_classes: List[str]
    bounded_scope_rules: Dict[str, Any]
    sovereignty_override_rules: Dict[str, Any]
    health_status: OverlayMeshHealthRecord
    warnings: List[RouteGovernanceWarningRecord] = Field(default_factory=list)

class RouteTierDecisionRecord(BaseModel):
    decision_id: str
    route_ref: str
    tier_ref: str
    decision_type: str
    reasons: List[str]

class ConsortiumWarningRecord(BaseModel):
    warning_type: str
    description: str

class ConsortiumProvenanceRecord(BaseModel):
    provenance_source: str
    provenance_confidence: float

class ConsortiumCorroborationRecord(BaseModel):
    corroboration_band: str
    corroborating_sources: List[str]

class ConsortiumSignalFreshnessBandRecord(BaseModel):
    band_name: str
    description: str

class ConsortiumSignalApplicabilityRecord(BaseModel):
    applicable_scopes: List[str]

class ConsortiumSignalConflictRecord(BaseModel):
    conflict_id: str
    description: str

class ConsortiumSignalProjectionRecord(BaseModel):
    projection_target: str
    projection_value: float

class ConsortiumSignalRecord(BaseModel):
    signal_id: str
    source_member: str
    source_baseline_ref: str
    signal_family: str
    freshness_band: ConsortiumSignalFreshnessBandRecord
    provenance_confidence: ConsortiumProvenanceRecord
    corroboration_band: ConsortiumCorroborationRecord
    caveat_density: float
    suppression_state: str
    projection_targets: List[ConsortiumSignalProjectionRecord]

class ConsortiumMemberRecord(BaseModel):
    member_id: str
    member_family: str

class ConsortiumLayerDecisionRecord(BaseModel):
    decision_id: str
    decision_type: str
    reasons: List[str]

class ConsortiumHealthRecord(BaseModel):
    status: str
    details: Dict[str, str]

class ConsortiumManifestRecord(BaseModel):
    manifest_id: str
    created_at: datetime
    content: Dict[str, Any]

class ConsortiumLayerRecord(BaseModel):
    layer_id: str
    layer_family: str
    member_refs: List[str]
    supported_signal_families: List[str]
    freshness_policy_ref: str
    corroboration_thresholds: Dict[str, float]
    suppression_policy_ref: str
    layer_status: str
    warnings: List[ConsortiumWarningRecord] = Field(default_factory=list)

class BenchmarkSignalConsortiumRecord(BaseModel):
    consortium_id: str
    consortium_family: str
    layer_refs: List[str]
    member_refs: List[str]
    active_signal_refs: List[str]
    provenance_rules: Dict[str, Any]
    corroboration_rules: Dict[str, Any]
    suppression_rules: Dict[str, Any]
    health_status: ConsortiumHealthRecord
    warnings: List[ConsortiumWarningRecord] = Field(default_factory=list)

class BaselineRegistryWarningRecord(BaseModel):
    warning_type: str
    description: str

class BaselineRegistryVersionRecord(BaseModel):
    version_id: str
    timestamp: datetime

class BaselineRegistryApplicabilityRecord(BaseModel):
    applicability_scopes: List[str]

class BaselineRegistrySupersessionRecord(BaseModel):
    supersession_reason: str
    successor_ref: Optional[str] = None

class BaselineRegistryValidationRecord(BaseModel):
    validation_id: str
    validation_status: str

class BaselineRegistryHealthRecord(BaseModel):
    status: str
    details: Dict[str, str]

class BaselineRegistryManifestRecord(BaseModel):
    manifest_id: str
    created_at: datetime
    content: Dict[str, Any]

class BaselineRegistryCurrentPointerRecord(BaseModel):
    pointer_id: str
    baseline_entry_ref: str

class BaselineRegistryEntryRecord(BaseModel):
    baseline_registry_entry_id: str
    baseline_ref: str
    baseline_family: str
    version_ref: BaselineRegistryVersionRecord
    currentness_state: str
    applicability_scope: BaselineRegistryApplicabilityRecord
    validity_window: Dict[str, datetime]
    supersession_state: BaselineRegistrySupersessionRecord
    warnings: List[BaselineRegistryWarningRecord] = Field(default_factory=list)

class SovereignResilienceBaselineRegistryRecord(BaseModel):
    baseline_registry_id: str
    registry_family: str
    registered_baseline_refs: List[str]
    current_pointer_refs: List[str]
    applicability_refs: List[str]
    validation_refs: List[str]
    supersession_refs: List[str]
    health_status: BaselineRegistryHealthRecord
    warnings: List[BaselineRegistryWarningRecord] = Field(default_factory=list)

class ControllerTierCapRecord(BaseModel):
    cap_id: str
    tier_ref: str
    cap_reason: str

class ControllerConsortiumActionRecord(BaseModel):
    action_id: str
    consortium_ref: str
    action_type: str

class ControllerBaselineRegistryActionRecord(BaseModel):
    action_id: str
    registry_ref: str
    action_type: str

class ControllerRecoveryPathRecord(BaseModel):
    recovery_id: str
    path_details: str
