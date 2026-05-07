import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Planetary Bus Mesh Contracts
# ---------------------------------------------------------

class MeshStatus(str, Enum):
    MESH_VERIFIED = "mesh_verified"
    MESH_CAVEATED = "mesh_caveated"
    MESH_REVIEW_ONLY = "mesh_review_only"
    MESH_GAPPED = "mesh_gapped"
    MESH_BLOCKED = "mesh_blocked"
    MESH_OVERCLAIMED = "mesh_overclaimed"

class PlanetaryBusMeshRecord(BaseModel):
    planetary_bus_mesh_id: str
    mesh_family: str
    node_refs: List[str]
    edge_refs: List[str]
    path_refs: List[str]
    lag_refs: List[str]
    packet_refs: List[str]
    continuity_refs: List[str]
    residue_refs: List[str]
    mesh_status: MeshStatus
    warnings: List[str]

class BusMeshNodeRecord(BaseModel):
    node_id: str
    node_family: str
    owner: str

class BusMeshEdgeRecord(BaseModel):
    edge_id: str
    edge_status: str
    source_node: str
    target_node: str

class BusMeshPathRecord(BaseModel):
    path_id: str
    edge_refs: List[str]

class BusMeshLagRecord(BaseModel):
    lag_id: str
    duration_ms: int

class BusMeshPacketRecord(BaseModel):
    packet_id: str
    freshness: str

class BusMeshContinuityRecord(BaseModel):
    continuity_id: str
    preserves_no_safe: bool
    preserves_sovereignty: bool

class BusMeshResidueRecord(BaseModel):
    residue_id: str
    resolved: bool

class PlanetaryBusMeshHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    release_blockers: List[str]

class PlanetaryBusMeshManifestRecord(BaseModel):
    manifest_id: str
    mesh_count: int

class PlanetaryBusMeshWarningRecord(BaseModel):
    warning_id: str
    message: str


# ---------------------------------------------------------
# Node / Edge Model
# ---------------------------------------------------------

class BusMeshFreshnessRecord(BaseModel):
    freshness_id: str
    is_stale: bool

class BusMeshOwnerRecord(BaseModel):
    owner_id: str
    owner_name: str

class BusMeshGapRecord(BaseModel):
    gap_id: str
    gap_type: str

class BusMeshFallbackRecord(BaseModel):
    fallback_id: str

class BusMeshRollbackRecord(BaseModel):
    rollback_id: str

class BusMeshHealthMarkerRecord(BaseModel):
    marker_id: str


# ---------------------------------------------------------
# Archive Corridor Chain Contracts
# ---------------------------------------------------------

class ChainStatus(str, Enum):
    CHAIN_VERIFIED = "chain_verified"
    CHAIN_CAVEATED = "chain_caveated"
    CHAIN_REVIEW_ONLY = "chain_review_only"
    CHAIN_GAPPED = "chain_gapped"
    CHAIN_BROKEN = "chain_broken"
    CHAIN_OVERCLAIMED = "chain_overclaimed"

class ArchiveCorridorChainRecord(BaseModel):
    archive_corridor_chain_id: str
    chain_family: str
    node_refs: List[str]
    edge_refs: List[str]
    segment_refs: List[str]
    hash_refs: List[str]
    lineage_refs: List[str]
    replay_refs: List[str]
    residue_refs: List[str]
    chain_status: ChainStatus
    warnings: List[str]

class CorridorChainNodeRecord(BaseModel):
    node_id: str

class CorridorChainEdgeRecord(BaseModel):
    edge_id: str

class CorridorChainSegmentRecord(BaseModel):
    segment_id: str
    segment_family: str

class CorridorChainHashRecord(BaseModel):
    hash_id: str
    is_verified: bool

class CorridorChainLineageRecord(BaseModel):
    lineage_id: str
    is_broken: bool

class CorridorChainReplayRecord(BaseModel):
    replay_id: str
    is_supported: bool

class CorridorChainResidueRecord(BaseModel):
    residue_id: str

class ArchiveCorridorChainHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool

class ArchiveCorridorChainManifestRecord(BaseModel):
    manifest_id: str

class ArchiveCorridorChainWarningRecord(BaseModel):
    warning_id: str


# ---------------------------------------------------------
# Corridor Chain Segment / Replay Model
# ---------------------------------------------------------

class CorridorChainOwnerRecord(BaseModel):
    owner_id: str

class CorridorChainGapRecord(BaseModel):
    gap_id: str

class CorridorChainDriftRecord(BaseModel):
    drift_id: str

class CorridorChainMismatchRecord(BaseModel):
    mismatch_id: str

class CorridorChainCheckpointRecord(BaseModel):
    checkpoint_id: str
    checkpoint_family: str

class CorridorChainHealthMarkerRecord(BaseModel):
    marker_id: str


# ---------------------------------------------------------
# Audit Simulation Federation Contracts
# ---------------------------------------------------------

class FederationStatus(str, Enum):
    FEDERATION_VERIFIED = "federation_verified"
    FEDERATION_CAVEATED = "federation_caveated"
    FEDERATION_REVIEW_ONLY = "federation_review_only"
    FEDERATION_GAPPED = "federation_gapped"
    FEDERATION_BLOCKED = "federation_blocked"
    FEDERATION_OVERCLAIMED = "federation_overclaimed"

class AuditSimulationFederationRecord(BaseModel):
    audit_simulation_federation_id: str
    federation_family: str
    member_simulation_refs: List[str]
    link_refs: List[str]
    agreement_refs: List[str]
    continuity_refs: List[str]
    residue_refs: List[str]
    asymmetry_refs: List[str]
    federation_status: FederationStatus
    warnings: List[str]

class FederatedSimulationNodeRecord(BaseModel):
    node_id: str

class SimulationFederationLinkRecord(BaseModel):
    link_id: str

class SimulationFederationAgreementRecord(BaseModel):
    agreement_id: str
    band: str

class SimulationFederationCaveatRecord(BaseModel):
    caveat_id: str

class SimulationFederationContinuityRecord(BaseModel):
    continuity_id: str

class SimulationFederationResidueRecord(BaseModel):
    residue_id: str

class SimulationFederationAsymmetryRecord(BaseModel):
    asymmetry_id: str
    is_hidden: bool

class AuditSimulationFederationHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool

class AuditSimulationFederationManifestRecord(BaseModel):
    manifest_id: str

class AuditSimulationFederationWarningRecord(BaseModel):
    warning_id: str

# ---------------------------------------------------------
# Link / Asymmetry Model
# ---------------------------------------------------------

class SimulationFederationLagRecord(BaseModel):
    lag_id: str

class SimulationFederationGapRecord(BaseModel):
    gap_id: str

class SimulationFederationRollbackRecord(BaseModel):
    rollback_id: str

class SimulationFederationHealthMarkerRecord(BaseModel):
    marker_id: str

class SimulationFederationReplayRecord(BaseModel):
    replay_id: str

class SimulationFederationDriftRecord(BaseModel):
    drift_id: str


# ---------------------------------------------------------
# Global Continuity Scheduler Audit Contracts
# ---------------------------------------------------------

class AuditStatus(str, Enum):
    SCHEDULER_VERIFIED = "scheduler_verified"
    SCHEDULER_CAVEATED = "scheduler_caveated"
    SCHEDULER_REVIEW_ONLY = "scheduler_review_only"
    SCHEDULER_GAPPED = "scheduler_gapped"
    SCHEDULER_BLOCKED = "scheduler_blocked"
    SCHEDULER_OVERCLAIMED = "scheduler_overclaimed"

class GlobalContinuitySchedulerAuditRecord(BaseModel):
    global_continuity_scheduler_audit_id: str
    audit_family: str
    zone_refs: List[str]
    window_refs: List[str]
    owner_refs: List[str]
    seam_refs: List[str]
    cadence_refs: List[str]
    gap_refs: List[str]
    residue_refs: List[str]
    audit_status: AuditStatus
    warnings: List[str]

class SchedulerWindowRecord(BaseModel):
    window_id: str
    window_family: str

class SchedulerZoneRecord(BaseModel):
    zone_id: str

class SchedulerOwnerRecord(BaseModel):
    owner_id: str

class SchedulerSeamRecord(BaseModel):
    seam_id: str

class SchedulerCadenceRecord(BaseModel):
    cadence_id: str

class SchedulerGapRecord(BaseModel):
    gap_id: str

class SchedulerResidueRecord(BaseModel):
    residue_id: str

class GlobalSchedulerAuditHealthRecord(BaseModel):
    health_id: str

class GlobalSchedulerAuditManifestRecord(BaseModel):
    manifest_id: str

class GlobalSchedulerAuditWarningRecord(BaseModel):
    warning_id: str

# ---------------------------------------------------------
# Window / Cadence Model
# ---------------------------------------------------------

class SchedulerHandoffRecord(BaseModel):
    handoff_id: str

class SchedulerAckRecord(BaseModel):
    ack_id: str
    is_missing: bool

class SchedulerReachabilityRecord(BaseModel):
    reachability_id: str

class SchedulerMismatchRecord(BaseModel):
    mismatch_id: str

class SchedulerContinuityRecord(BaseModel):
    continuity_id: str

class SchedulerDriftRecord(BaseModel):
    drift_id: str

class SchedulerHealthMarkerRecord(BaseModel):
    marker_id: str


# ---------------------------------------------------------
# Global Continuity Scheduler Budgets
# ---------------------------------------------------------

class BusMeshBudgetRecord(BaseModel):
    budget_id: str

class CorridorChainBudgetRecord(BaseModel):
    budget_id: str

class SimulationFederationBudgetRecord(BaseModel):
    budget_id: str

class SchedulerAuditBudgetRecord(BaseModel):
    budget_id: str

class BudgetConsumptionRecord(BaseModel):
    consumption_id: str

class BudgetBreachRecord(BaseModel):
    breach_id: str

class GlobalSchedulerBudgetHealthRecord(BaseModel):
    health_id: str

class GlobalSchedulerBudgetManifestRecord(BaseModel):
    manifest_id: str

class GlobalSchedulerBudgetWarningRecord(BaseModel):
    warning_id: str
