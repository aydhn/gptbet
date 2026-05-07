from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime, timezone

class FederationFamily(str, Enum):
    BOUNDED_PLANETARY_MESH_FEDERATION = "bounded_planetary_mesh_federation"
    DEGRADED_PLANETARY_MESH_FEDERATION = "degraded_planetary_mesh_federation"
    ARCHIVE_ASSISTED_MESH_FEDERATION = "archive_assisted_mesh_federation"
    NO_SAFE_VISIBILITY_MESH_FEDERATION = "no_safe_visibility_mesh_federation"
    SOVEREIGNTY_VISIBILITY_MESH_FEDERATION = "sovereignty_visibility_mesh_federation"
    SCHEDULER_VISIBILITY_MESH_FEDERATION = "scheduler_visibility_mesh_federation"
    COMPOSITE_PLANETARY_MESH_FEDERATION = "composite_planetary_mesh_federation"

class FederationStatus(str, Enum):
    FEDERATION_VERIFIED = "federation_verified"
    FEDERATION_CAVEATED = "federation_caveated"
    FEDERATION_REVIEW_ONLY = "federation_review_only"
    FEDERATION_GAPPED = "federation_gapped"
    FEDERATION_BLOCKED = "federation_blocked"
    FEDERATION_OVERCLAIMED = "federation_overclaimed"

@dataclass
class FederatedMeshNodeRecord:
    node_id: str
    region: str
    is_stale: bool = False

@dataclass
class MeshFederationLinkRecord:
    link_id: str
    source_node: str
    target_node: str
    is_stale: bool = False

@dataclass
class MeshFederationAgreementRecord:
    agreement_id: str
    band: str
    caveat_notes: List[str] = field(default_factory=list)

@dataclass
class MeshFederationLagRecord:
    lag_id: str
    lag_ms: int

@dataclass
class MeshFederationCaveatRecord:
    caveat_id: str
    description: str

@dataclass
class MeshFederationContinuityRecord:
    continuity_id: str
    no_safe_visible: bool = True
    sovereignty_note_visible: bool = True

@dataclass
class MeshFederationResidueRecord:
    residue_id: str
    description: str

@dataclass
class PlanetaryMeshFederationHealthRecord:
    is_healthy: bool
    status: FederationStatus
    details: str

@dataclass
class PlanetaryMeshFederationManifestRecord:
    manifest_id: str
    version: str

@dataclass
class PlanetaryMeshFederationWarningRecord:
    warning_id: str
    severity: str
    description: str

@dataclass
class PlanetaryMeshFederationRecord:
    planetary_mesh_federation_id: str
    federation_family: FederationFamily
    member_mesh_refs: List[FederatedMeshNodeRecord] = field(default_factory=list)
    active_link_refs: List[MeshFederationLinkRecord] = field(default_factory=list)
    agreement_refs: List[MeshFederationAgreementRecord] = field(default_factory=list)
    lag_refs: List[MeshFederationLagRecord] = field(default_factory=list)
    continuity_refs: List[MeshFederationContinuityRecord] = field(default_factory=list)
    residue_refs: List[MeshFederationResidueRecord] = field(default_factory=list)
    warnings: List[PlanetaryMeshFederationWarningRecord] = field(default_factory=list)
    federation_status: FederationStatus = FederationStatus.FEDERATION_REVIEW_ONLY

class SuperchainFamily(str, Enum):
    INTERCONTINENTAL_ARCHIVE_SUPERCHAIN = "intercontinental_archive_superchain"
    FOLLOW_THE_SUN_HANDOFF_SUPERCHAIN = "follow_the_sun_handoff_superchain"
    NO_SAFE_VISIBILITY_SUPERCHAIN = "no_safe_visibility_superchain"
    SOVEREIGNTY_VISIBILITY_SUPERCHAIN = "sovereignty_visibility_superchain"
    REVIEW_SURFACE_SUPERCHAIN = "review_surface_superchain"
    SCHEDULER_SUPPORT_SUPERCHAIN = "scheduler_support_superchain"
    COMPOSITE_CORRIDOR_SUPERCHAIN = "composite_corridor_superchain"

class SuperchainStatus(str, Enum):
    SUPERCHAIN_VERIFIED = "superchain_verified"
    SUPERCHAIN_CAVEATED = "superchain_caveated"
    SUPERCHAIN_REVIEW_ONLY = "superchain_review_only"
    SUPERCHAIN_GAPPED = "superchain_gapped"
    SUPERCHAIN_BROKEN = "superchain_broken"
    SUPERCHAIN_OVERCLAIMED = "superchain_overclaimed"

@dataclass
class SuperchainNodeRecord:
    node_id: str

@dataclass
class SuperchainEdgeRecord:
    edge_id: str

@dataclass
class SuperchainSegmentRecord:
    segment_id: str
    is_stale: bool = False

@dataclass
class SuperchainHashRecord:
    hash_id: str
    hash_value: str

@dataclass
class SuperchainLineageRecord:
    lineage_id: str
    preserved: bool = True

@dataclass
class SuperchainReplayRecord:
    replay_id: str
    is_supported: bool = True

@dataclass
class SuperchainRollbackRecord:
    rollback_id: str
    is_ready: bool = True

@dataclass
class SuperchainResidueRecord:
    residue_id: str
    description: str

@dataclass
class CorridorSuperchainHealthRecord:
    is_healthy: bool
    status: SuperchainStatus

@dataclass
class CorridorSuperchainManifestRecord:
    manifest_id: str

@dataclass
class CorridorSuperchainWarningRecord:
    warning_id: str
    description: str

@dataclass
class CorridorSuperchainRecord:
    corridor_superchain_id: str
    superchain_family: SuperchainFamily
    node_refs: List[SuperchainNodeRecord] = field(default_factory=list)
    edge_refs: List[SuperchainEdgeRecord] = field(default_factory=list)
    segment_refs: List[SuperchainSegmentRecord] = field(default_factory=list)
    hash_refs: List[SuperchainHashRecord] = field(default_factory=list)
    lineage_refs: List[SuperchainLineageRecord] = field(default_factory=list)
    replay_refs: List[SuperchainReplayRecord] = field(default_factory=list)
    rollback_refs: List[SuperchainRollbackRecord] = field(default_factory=list)
    residue_refs: List[SuperchainResidueRecord] = field(default_factory=list)
    warnings: List[CorridorSuperchainWarningRecord] = field(default_factory=list)
    superchain_status: SuperchainStatus = SuperchainStatus.SUPERCHAIN_REVIEW_ONLY

class BusFamily(str, Enum):
    PLANETARY_COVERAGE_SCHEDULER_BUS = "planetary_coverage_scheduler_bus"
    NO_SAFE_VISIBILITY_SCHEDULER_BUS = "no_safe_visibility_scheduler_bus"
    SOVEREIGNTY_VISIBILITY_SCHEDULER_BUS = "sovereignty_visibility_scheduler_bus"
    ARCHIVE_RESTORE_SCHEDULER_BUS = "archive_restore_scheduler_bus"
    CONTINUITY_OWNER_SCHEDULER_BUS = "continuity_owner_scheduler_bus"
    EXECUTIVE_VISIBILITY_SCHEDULER_BUS = "executive_visibility_scheduler_bus"
    COMPOSITE_SCHEDULER_BUS = "composite_scheduler_bus"

class BusStatus(str, Enum):
    BUS_VERIFIED = "bus_verified"
    BUS_CAVEATED = "bus_caveated"
    BUS_REVIEW_ONLY = "bus_review_only"
    BUS_GAPPED = "bus_gapped"
    BUS_BLOCKED = "bus_blocked"
    BUS_OVERCLAIMED = "bus_overclaimed"

@dataclass
class SchedulerBusLaneRecord:
    lane_id: str
    is_ownerless: bool = False

@dataclass
class SchedulerBusPacketRecord:
    packet_id: str
    is_stale: bool = False
    has_ack: bool = True

@dataclass
class SchedulerBusEnvelopeRecord:
    envelope_id: str

@dataclass
class SchedulerBusCadenceRecord:
    cadence_id: str
    drift_ms: int = 0

@dataclass
class SchedulerBusGapRecord:
    gap_id: str

@dataclass
class SchedulerBusResidueRecord:
    residue_id: str

@dataclass
class SchedulerBusContinuityRecord:
    continuity_id: str
    no_safe_visible: bool = True
    sovereignty_note_visible: bool = True

@dataclass
class SchedulerBusHealthRecord:
    is_healthy: bool
    status: BusStatus

@dataclass
class SchedulerBusManifestRecord:
    manifest_id: str

@dataclass
class SchedulerBusWarningRecord:
    warning_id: str
    description: str

@dataclass
class SchedulerBusRecord:
    scheduler_bus_id: str
    bus_family: BusFamily
    lane_refs: List[SchedulerBusLaneRecord] = field(default_factory=list)
    packet_refs: List[SchedulerBusPacketRecord] = field(default_factory=list)
    envelope_refs: List[SchedulerBusEnvelopeRecord] = field(default_factory=list)
    cadence_refs: List[SchedulerBusCadenceRecord] = field(default_factory=list)
    gap_refs: List[SchedulerBusGapRecord] = field(default_factory=list)
    residue_refs: List[SchedulerBusResidueRecord] = field(default_factory=list)
    continuity_refs: List[SchedulerBusContinuityRecord] = field(default_factory=list)
    warnings: List[SchedulerBusWarningRecord] = field(default_factory=list)
    bus_status: BusStatus = BusStatus.BUS_REVIEW_ONLY

class OrchestrationFamily(str, Enum):
    WORLDWIDE_FOLLOW_THE_SUN_CADENCE_ORCHESTRATION = "worldwide_follow_the_sun_cadence_orchestration"
    NO_SAFE_VISIBILITY_CADENCE_ORCHESTRATION = "no_safe_visibility_cadence_orchestration"
    SOVEREIGNTY_VISIBILITY_CADENCE_ORCHESTRATION = "sovereignty_visibility_cadence_orchestration"
    ARCHIVE_RESTORE_CADENCE_ORCHESTRATION = "archive_restore_cadence_orchestration"
    CONTINUITY_OWNER_CADENCE_ORCHESTRATION = "continuity_owner_cadence_orchestration"
    EXECUTIVE_VISIBILITY_CADENCE_ORCHESTRATION = "executive_visibility_cadence_orchestration"
    COMPOSITE_GLOBAL_AUDIT_CADENCE_ORCHESTRATION = "composite_global_audit_cadence_orchestration"

class OrchestrationStatus(str, Enum):
    ORCHESTRATION_VERIFIED = "orchestration_verified"
    ORCHESTRATION_CAVEATED = "orchestration_caveated"
    ORCHESTRATION_REVIEW_ONLY = "orchestration_review_only"
    ORCHESTRATION_GAPPED = "orchestration_gapped"
    ORCHESTRATION_BLOCKED = "orchestration_blocked"
    ORCHESTRATION_OVERCLAIMED = "orchestration_overclaimed"

@dataclass
class CadenceWindowRecord:
    window_id: str
    is_stale: bool = False
    has_ack: bool = True

@dataclass
class CadenceZoneRecord:
    zone_id: str

@dataclass
class CadenceOwnerRecord:
    owner_id: str

@dataclass
class CadenceSeamRecord:
    seam_id: str

@dataclass
class CadenceScenarioRecord:
    scenario_id: str

@dataclass
class CadenceGapRecord:
    gap_id: str

@dataclass
class CadenceResidueRecord:
    residue_id: str

@dataclass
class GlobalAuditCadenceHealthRecord:
    is_healthy: bool
    status: OrchestrationStatus

@dataclass
class GlobalAuditCadenceManifestRecord:
    manifest_id: str

@dataclass
class GlobalAuditCadenceWarningRecord:
    warning_id: str
    description: str

@dataclass
class GlobalAuditCadenceOrchestrationRecord:
    global_audit_cadence_orchestration_id: str
    orchestration_family: OrchestrationFamily
    zone_refs: List[CadenceZoneRecord] = field(default_factory=list)
    window_refs: List[CadenceWindowRecord] = field(default_factory=list)
    owner_refs: List[CadenceOwnerRecord] = field(default_factory=list)
    seam_refs: List[CadenceSeamRecord] = field(default_factory=list)
    scenario_refs: List[CadenceScenarioRecord] = field(default_factory=list)
    gap_refs: List[CadenceGapRecord] = field(default_factory=list)
    residue_refs: List[CadenceResidueRecord] = field(default_factory=list)
    warnings: List[GlobalAuditCadenceWarningRecord] = field(default_factory=list)
    orchestration_status: OrchestrationStatus = OrchestrationStatus.ORCHESTRATION_REVIEW_ONLY
