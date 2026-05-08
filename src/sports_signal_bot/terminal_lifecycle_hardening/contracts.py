from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum

class BundleFamily(str, Enum):
    final_platform_closure_bundle = "final_platform_closure_bundle"
    maintenance_transition_closure_bundle = "maintenance_transition_closure_bundle"
    operator_handoff_closure_bundle = "operator_handoff_closure_bundle"
    visibility_and_sovereignty_closure_bundle = "visibility_and_sovereignty_closure_bundle"
    archive_and_replay_closure_bundle = "archive_and_replay_closure_bundle"
    deprecation_transition_closure_bundle = "deprecation_transition_closure_bundle"
    composite_terminal_closure_bundle = "composite_terminal_closure_bundle"

class BundleStatus(str, Enum):
    bundle_verified = "bundle_verified"
    bundle_caveated = "bundle_caveated"
    bundle_review_only = "bundle_review_only"
    bundle_gapped = "bundle_gapped"
    bundle_blocked = "bundle_blocked"
    bundle_overclaimed = "bundle_overclaimed"

class SectionFamily(str, Enum):
    blocker_summary_section = "blocker_summary_section"
    residue_summary_section = "residue_summary_section"
    frozen_surface_section = "frozen_surface_section"
    deprecation_section = "deprecation_section"
    no_safe_visibility_section = "no_safe_visibility_section"
    sovereignty_visibility_section = "sovereignty_visibility_section"
    replay_and_archive_section = "replay_and_archive_section"
    maintenance_boundary_section = "maintenance_boundary_section"
    stewardship_owner_section = "stewardship_owner_section"
    terminal_summary_section = "terminal_summary_section"

class MapFamily(str, Enum):
    runtime_surface_deprecation_map = "runtime_surface_deprecation_map"
    review_surface_deprecation_map = "review_surface_deprecation_map"
    archive_transition_deprecation_map = "archive_transition_deprecation_map"
    replay_transition_deprecation_map = "replay_transition_deprecation_map"
    operator_workflow_deprecation_map = "operator_workflow_deprecation_map"
    visibility_surface_deprecation_map = "visibility_surface_deprecation_map"
    composite_deprecation_map = "composite_deprecation_map"

class MapStatus(str, Enum):
    map_verified = "map_verified"
    map_caveated = "map_caveated"
    map_review_only = "map_review_only"
    map_gapped = "map_gapped"
    map_blocked = "map_blocked"
    map_overclaimed = "map_overclaimed"

class StateFamily(str, Enum):
    active_supported = "active_supported"
    active_caveated = "active_caveated"
    frozen_supported = "frozen_supported"
    frozen_review_only = "frozen_review_only"
    deprecated_with_replacement = "deprecated_with_replacement"
    deprecated_archive_only = "deprecated_archive_only"
    deprecated_blocked = "deprecated_blocked"
    sunset_complete = "sunset_complete"

class ModeFamily(str, Enum):
    bounded_runtime_maintenance_mode = "bounded_runtime_maintenance_mode"
    archive_first_maintenance_mode = "archive_first_maintenance_mode"
    review_surface_maintenance_mode = "review_surface_maintenance_mode"
    visibility_preservation_maintenance_mode = "visibility_preservation_maintenance_mode"
    stewardship_transition_maintenance_mode = "stewardship_transition_maintenance_mode"
    frozen_baseline_maintenance_mode = "frozen_baseline_maintenance_mode"
    composite_maintenance_mode = "composite_maintenance_mode"

class ModeStatus(str, Enum):
    mode_verified = "mode_verified"
    mode_caveated = "mode_caveated"
    mode_review_only = "mode_review_only"
    mode_gapped = "mode_gapped"
    mode_blocked = "mode_blocked"
    mode_overclaimed = "mode_overclaimed"

class BoundaryFamily(str, Enum):
    runtime_boundary = "runtime_boundary"
    archive_boundary = "archive_boundary"
    replay_boundary = "replay_boundary"
    review_boundary = "review_boundary"
    no_safe_visibility_boundary = "no_safe_visibility_boundary"
    sovereignty_visibility_boundary = "sovereignty_visibility_boundary"
    operator_boundary = "operator_boundary"
    stewardship_boundary = "stewardship_boundary"

class PackFamily(str, Enum):
    runtime_stewardship_pack = "runtime_stewardship_pack"
    archive_stewardship_pack = "archive_stewardship_pack"
    replay_stewardship_pack = "replay_stewardship_pack"
    visibility_stewardship_pack = "visibility_stewardship_pack"
    no_safe_visibility_stewardship_pack = "no_safe_visibility_stewardship_pack"
    sovereignty_visibility_stewardship_pack = "sovereignty_visibility_stewardship_pack"
    composite_long_horizon_stewardship_pack = "composite_long_horizon_stewardship_pack"

class PackStatus(str, Enum):
    pack_verified = "pack_verified"
    pack_caveated = "pack_caveated"
    pack_review_only = "pack_review_only"
    pack_gapped = "pack_gapped"
    pack_blocked = "pack_blocked"
    pack_overclaimed = "pack_overclaimed"

class OwnerFamily(str, Enum):
    runtime_owner = "runtime_owner"
    archive_owner = "archive_owner"
    replay_owner = "replay_owner"
    visibility_owner = "visibility_owner"
    no_safe_owner = "no_safe_owner"
    sovereignty_owner = "sovereignty_owner"
    operator_owner = "operator_owner"
    executive_visibility_owner = "executive_visibility_owner"

class ClosureBundleSectionRecord(BaseModel):
    section_id: str
    section_family: SectionFamily
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureBundleEvidenceRecord(BaseModel):
    evidence_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureBundleBlockerRecord(BaseModel):
    blocker_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureBundleResidueRecord(BaseModel):
    residue_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureBundleGapRecord(BaseModel):
    gap_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureBundleReplayRecord(BaseModel):
    replay_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureBundleDecisionRecord(BaseModel):
    decision_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureBundleHealthRecord(BaseModel):
    health_id: str
    status: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureBundleWarningRecord(BaseModel):
    warning_id: str
    message: str

class ClosureBundleManifestRecord(BaseModel):
    manifest_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureBundleRecord(BaseModel):
    closure_bundle_id: str
    bundle_family: BundleFamily
    section_refs: List[ClosureBundleSectionRecord] = Field(default_factory=list)
    evidence_refs: List[ClosureBundleEvidenceRecord] = Field(default_factory=list)
    blocker_refs: List[ClosureBundleBlockerRecord] = Field(default_factory=list)
    residue_refs: List[ClosureBundleResidueRecord] = Field(default_factory=list)
    gap_refs: List[ClosureBundleGapRecord] = Field(default_factory=list)
    replay_refs: List[ClosureBundleReplayRecord] = Field(default_factory=list)
    decision_refs: List[ClosureBundleDecisionRecord] = Field(default_factory=list)
    bundle_status: BundleStatus
    warnings: List[ClosureBundleWarningRecord] = Field(default_factory=list)

class ClosureSectionOwnerRecord(BaseModel):
    owner_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureSectionFreshnessRecord(BaseModel):
    freshness_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureSectionMismatchRecord(BaseModel):
    mismatch_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureSectionDriftRecord(BaseModel):
    drift_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureSectionRollbackRecord(BaseModel):
    rollback_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureSectionHealthMarkerRecord(BaseModel):
    marker_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationSurfaceRecord(BaseModel):
    surface_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationStateRecord(BaseModel):
    state_id: str
    state_family: StateFamily
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationWindowRecord(BaseModel):
    window_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationReplacementRecord(BaseModel):
    replacement_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationResidueRecord(BaseModel):
    residue_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationGapRecord(BaseModel):
    gap_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationHealthRecord(BaseModel):
    health_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationMapManifestRecord(BaseModel):
    manifest_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationMapWarningRecord(BaseModel):
    warning_id: str
    message: str

class DeprecationMapRecord(BaseModel):
    deprecation_map_id: str
    map_family: MapFamily
    surface_refs: List[DeprecationSurfaceRecord] = Field(default_factory=list)
    state_refs: List[DeprecationStateRecord] = Field(default_factory=list)
    window_refs: List[DeprecationWindowRecord] = Field(default_factory=list)
    replacement_refs: List[DeprecationReplacementRecord] = Field(default_factory=list)
    residue_refs: List[DeprecationResidueRecord] = Field(default_factory=list)
    gap_refs: List[DeprecationGapRecord] = Field(default_factory=list)
    map_status: MapStatus
    warnings: List[DeprecationMapWarningRecord] = Field(default_factory=list)

class DeprecationOwnerRecord(BaseModel):
    owner_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationFreshnessRecord(BaseModel):
    freshness_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationFallbackRecord(BaseModel):
    fallback_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationRollbackRecord(BaseModel):
    rollback_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationApplicabilityRecord(BaseModel):
    applicability_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationHealthMarkerRecord(BaseModel):
    marker_id: str
    details: Dict[str, Any] = Field(default_factory=dict)


class MaintenanceBoundaryRecord(BaseModel):
    boundary_id: str
    boundary_family: BoundaryFamily
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceSurfaceRecord(BaseModel):
    surface_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceCadenceRecord(BaseModel):
    cadence_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceConstraintRecord(BaseModel):
    constraint_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceResidueRecord(BaseModel):
    residue_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceGapRecord(BaseModel):
    gap_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceDecisionRecord(BaseModel):
    decision_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceModeHealthRecord(BaseModel):
    health_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceModeManifestRecord(BaseModel):
    manifest_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceModeWarningRecord(BaseModel):
    warning_id: str
    message: str

class MaintenanceModeRecord(BaseModel):
    maintenance_mode_id: str
    mode_family: ModeFamily
    boundary_refs: List[MaintenanceBoundaryRecord] = Field(default_factory=list)
    surface_refs: List[MaintenanceSurfaceRecord] = Field(default_factory=list)
    cadence_refs: List[MaintenanceCadenceRecord] = Field(default_factory=list)
    constraint_refs: List[MaintenanceConstraintRecord] = Field(default_factory=list)
    residue_refs: List[MaintenanceResidueRecord] = Field(default_factory=list)
    gap_refs: List[MaintenanceGapRecord] = Field(default_factory=list)
    decision_refs: List[MaintenanceDecisionRecord] = Field(default_factory=list)
    mode_status: ModeStatus
    warnings: List[MaintenanceModeWarningRecord] = Field(default_factory=list)


class MaintenanceOwnerRecord(BaseModel):
    owner_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceFreshnessRecord(BaseModel):
    freshness_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceDriftRecord(BaseModel):
    drift_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceRollbackRecord(BaseModel):
    rollback_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceReplayRecord(BaseModel):
    replay_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceHealthMarkerRecord(BaseModel):
    marker_id: str
    details: Dict[str, Any] = Field(default_factory=dict)


class StewardshipOwnerRecord(BaseModel):
    owner_id: str
    owner_family: OwnerFamily
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipScopeRecord(BaseModel):
    scope_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipCadenceRecord(BaseModel):
    cadence_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipEscalationRecord(BaseModel):
    escalation_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipArchiveResponsibilityRecord(BaseModel):
    responsibility_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipResidueRecord(BaseModel):
    residue_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipGapRecord(BaseModel):
    gap_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class LongHorizonStewardshipHealthRecord(BaseModel):
    health_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class LongHorizonStewardshipManifestRecord(BaseModel):
    manifest_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class LongHorizonStewardshipWarningRecord(BaseModel):
    warning_id: str
    message: str

class LongHorizonStewardshipPackRecord(BaseModel):
    stewardship_pack_id: str
    pack_family: PackFamily
    owner_refs: List[StewardshipOwnerRecord] = Field(default_factory=list)
    scope_refs: List[StewardshipScopeRecord] = Field(default_factory=list)
    cadence_refs: List[StewardshipCadenceRecord] = Field(default_factory=list)
    escalation_refs: List[StewardshipEscalationRecord] = Field(default_factory=list)
    archive_responsibility_refs: List[StewardshipArchiveResponsibilityRecord] = Field(default_factory=list)
    residue_refs: List[StewardshipResidueRecord] = Field(default_factory=list)
    gap_refs: List[StewardshipGapRecord] = Field(default_factory=list)
    pack_status: PackStatus
    warnings: List[LongHorizonStewardshipWarningRecord] = Field(default_factory=list)

class StewardshipCoverageRecord(BaseModel):
    coverage_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipAckRecord(BaseModel):
    ack_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipReachabilityRecord(BaseModel):
    reachability_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipMismatchRecord(BaseModel):
    mismatch_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipContinuityRecord(BaseModel):
    continuity_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipHealthMarkerRecord(BaseModel):
    marker_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ClosureBundleBudgetRecord(BaseModel):
    budget_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class DeprecationBudgetRecord(BaseModel):
    budget_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class MaintenanceModeBudgetRecord(BaseModel):
    budget_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class StewardshipBudgetRecord(BaseModel):
    budget_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class BudgetConsumptionRecord(BaseModel):
    consumption_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class BudgetBreachRecord(BaseModel):
    breach_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class TerminalLifecycleBudgetHealthRecord(BaseModel):
    health_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class TerminalLifecycleBudgetManifestRecord(BaseModel):
    manifest_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class TerminalLifecycleBudgetWarningRecord(BaseModel):
    warning_id: str
    message: str

class LifecycleMatrixRow(BaseModel):
    surface_id: str
    owner_visible: bool = False
    freshness_note_visible: bool = False
    no_safe_visible: bool = False
    sovereignty_note_visible: bool = False
    residue_visible: bool = False
    degraded_lane_visible: bool = False
    replayability_preserved: bool = False
    lineage_preserved: bool = False
    rollback_explicit: bool = False
    deprecation_state_explicit: bool = False
    maintenance_boundary_explicit: bool = False
    stewardship_cadence_explicit: bool = False
    acceptance_carry_forward_explicit: bool = False
