import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class BusStatus(str, Enum):
    BUS_VERIFIED = "bus_verified"
    BUS_CAVEATED = "bus_caveated"
    BUS_REVIEW_ONLY = "bus_review_only"
    BUS_GAPPED = "bus_gapped"
    BUS_BLOCKED = "bus_blocked"
    BUS_OVERCLAIMED = "bus_overclaimed"

class PlanetaryCoverageBusRecord(BaseModel):
    planetary_coverage_bus_id: str
    bus_family: str
    lane_refs: List[str]
    packet_refs: List[str]
    envelope_refs: List[str]
    lag_refs: List[str]
    continuity_refs: List[str]
    residue_refs: List[str]
    bus_status: BusStatus
    warnings: List[str]

class CoverageBusLaneRecord(BaseModel):
    lane_id: str
    lane_family: str
    sources: List[str]
    targets: List[str]
    status: str

class CoverageBusPacketRecord(BaseModel):
    packet_id: str
    content_hash: str
    freshness_note: Optional[str] = None
    no_safe_notes: List[str] = Field(default_factory=list)
    sovereignty_notes: List[str] = Field(default_factory=list)
    lag_ms: int = 0

class CoverageBusEnvelopeRecord(BaseModel):
    envelope_id: str
    packet_ids: List[str]
    freshness_note: Optional[str] = None

class CoverageBusLagRecord(BaseModel):
    lag_id: str
    packet_id: str
    lag_ms: int

class CoverageBusCaveatRecord(BaseModel):
    caveat_id: str
    description: str
    severity: str

class CoverageBusContinuityRecord(BaseModel):
    continuity_id: str
    description: str
    is_preserved: bool

class CoverageBusResidueRecord(BaseModel):
    residue_id: str
    description: str
    severity: str

class PlanetaryCoverageBusHealthRecord(BaseModel):
    bus_id: str
    status: BusStatus
    is_healthy: bool

class PlanetaryCoverageBusManifestRecord(BaseModel):
    manifest_id: str
    bus_ids: List[str]
    timestamp: datetime.datetime

class PlanetaryCoverageBusWarningRecord(BaseModel):
    warning_id: str
    message: str

class CoverageBusSourceRecord(BaseModel):
    source_id: str

class CoverageBusTargetRecord(BaseModel):
    target_id: str

class CoverageBusOwnerRecord(BaseModel):
    owner_id: str

class CoverageBusAckRecord(BaseModel):
    ack_id: str
    timestamp: datetime.datetime

class CoverageBusGapRecord(BaseModel):
    gap_id: str
    description: str

class CoverageBusRollbackRecord(BaseModel):
    rollback_id: str
    path: str

class CoverageBusHealthMarkerRecord(BaseModel):
    marker_id: str
    is_healthy: bool

class ArchiveStatus(str, Enum):
    ARCHIVE_VERIFIED = "archive_verified"
    ARCHIVE_CAVEATED = "archive_caveated"
    ARCHIVE_REVIEW_ONLY = "archive_review_only"
    ARCHIVE_GAPPED = "archive_gapped"
    ARCHIVE_BLOCKED = "archive_blocked"
    ARCHIVE_OVERCLAIMED = "archive_overclaimed"

class IntercontinentalHandoffArchiveRecord(BaseModel):
    intercontinental_handoff_archive_id: str
    archive_family: str
    entry_refs: List[str]
    segment_refs: List[str]
    owner_refs: List[str]
    ack_refs: List[str]
    freshness_refs: List[str]
    residue_refs: List[str]
    replay_refs: List[str]
    archive_status: ArchiveStatus
    warnings: List[str]

class HandoffArchiveEntryRecord(BaseModel):
    entry_id: str
    timestamp: datetime.datetime
    content_hash: str

class HandoffArchiveSegmentRecord(BaseModel):
    segment_id: str

class HandoffArchiveOwnerRecord(BaseModel):
    owner_id: str

class HandoffArchiveAckRecord(BaseModel):
    ack_id: str

class HandoffArchiveFreshnessRecord(BaseModel):
    freshness_id: str

class HandoffArchiveResidueRecord(BaseModel):
    residue_id: str
    description: str

class HandoffArchiveReplayRecord(BaseModel):
    replay_id: str
    status: str
    preserved_caveats: List[str] = Field(default_factory=list)
    preserved_no_safe: List[str] = Field(default_factory=list)
    preserved_sovereignty: List[str] = Field(default_factory=list)

class HandoffArchiveHealthRecord(BaseModel):
    archive_id: str
    is_healthy: bool

class HandoffArchiveManifestRecord(BaseModel):
    manifest_id: str
    timestamp: datetime.datetime

class HandoffArchiveWarningRecord(BaseModel):
    warning_id: str
    message: str

class HandoffArchiveWindowRecord(BaseModel):
    window_id: str

class HandoffArchiveMismatchRecord(BaseModel):
    mismatch_id: str
    description: str

class HandoffArchiveContinuityRecord(BaseModel):
    continuity_id: str

class HandoffArchiveGapRecord(BaseModel):
    gap_id: str

class HandoffArchiveHashRecord(BaseModel):
    hash_id: str

class HandoffArchiveHealthMarkerRecord(BaseModel):
    marker_id: str

class CorridorStatus(str, Enum):
    CORRIDOR_VERIFIED = "corridor_verified"
    CORRIDOR_CAVEATED = "corridor_caveated"
    CORRIDOR_REVIEW_ONLY = "corridor_review_only"
    CORRIDOR_GAPPED = "corridor_gapped"
    CORRIDOR_BLOCKED = "corridor_blocked"
    CORRIDOR_OVERCLAIMED = "corridor_overclaimed"

class QuorumFederationCorridorRecord(BaseModel):
    quorum_federation_corridor_id: str
    corridor_family: str
    node_refs: List[str]
    edge_refs: List[str]
    segment_refs: List[str]
    agreement_refs: List[str]
    lag_refs: List[str]
    residue_refs: List[str]
    corridor_status: CorridorStatus
    warnings: List[str]

class CorridorNodeRecord(BaseModel):
    node_id: str

class CorridorEdgeRecord(BaseModel):
    edge_id: str

class CorridorSegmentRecord(BaseModel):
    segment_id: str

class CorridorAgreementRecord(BaseModel):
    agreement_id: str
    level: str

class CorridorLagRecord(BaseModel):
    lag_id: str
    lag_ms: int

class CorridorCaveatRecord(BaseModel):
    caveat_id: str

class CorridorResidueRecord(BaseModel):
    residue_id: str

class CorridorHealthRecord(BaseModel):
    corridor_id: str

class QuorumFederationCorridorManifestRecord(BaseModel):
    manifest_id: str

class QuorumFederationCorridorWarningRecord(BaseModel):
    warning_id: str

class CorridorOwnerRecord(BaseModel):
    owner_id: str

class CorridorFallbackRecord(BaseModel):
    fallback_id: str

class CorridorRollbackRecord(BaseModel):
    rollback_id: str

class CorridorGapRecord(BaseModel):
    gap_id: str

class CorridorAsymmetryRecord(BaseModel):
    asymmetry_id: str
    severity: str

class CorridorHealthMarkerRecord(BaseModel):
    marker_id: str

class SimulationStatus(str, Enum):
    SIMULATION_VERIFIED = "simulation_verified"
    SIMULATION_CAVEATED = "simulation_caveated"
    SIMULATION_REVIEW_ONLY = "simulation_review_only"
    SIMULATION_GAPPED = "simulation_gapped"
    SIMULATION_BLOCKED = "simulation_blocked"
    SIMULATION_OVERCLAIMED = "simulation_overclaimed"

class WorldwideAuditCalendarSimulationRecord(BaseModel):
    worldwide_audit_calendar_simulation_id: str
    simulation_family: str
    zone_refs: List[str]
    window_refs: List[str]
    owner_refs: List[str]
    seam_refs: List[str]
    scenario_refs: List[str]
    gap_refs: List[str]
    residue_refs: List[str]
    simulation_status: SimulationStatus
    warnings: List[str]

class AuditCalendarZoneRecord(BaseModel):
    zone_id: str

class AuditCalendarWindowRecord(BaseModel):
    window_id: str

class AuditCalendarOwnerRecord(BaseModel):
    owner_id: str

class AuditCalendarSeamRecord(BaseModel):
    seam_id: str

class AuditCalendarScenarioRecord(BaseModel):
    scenario_id: str

class AuditCalendarGapRecord(BaseModel):
    gap_id: str

class AuditCalendarResidueRecord(BaseModel):
    residue_id: str

class WorldwideAuditCalendarHealthRecord(BaseModel):
    simulation_id: str

class WorldwideAuditCalendarManifestRecord(BaseModel):
    manifest_id: str

class WorldwideAuditCalendarWarningRecord(BaseModel):
    warning_id: str

class AuditCalendarHandoffRecord(BaseModel):
    handoff_id: str

class AuditCalendarAckRecord(BaseModel):
    ack_id: str

class AuditCalendarReachabilityRecord(BaseModel):
    reachability_id: str

class AuditCalendarMismatchRecord(BaseModel):
    mismatch_id: str

class AuditCalendarContinuityRecord(BaseModel):
    continuity_id: str

class AuditCalendarHealthMarkerRecord(BaseModel):
    marker_id: str

class CoverageBusBudgetRecord(BaseModel):
    budget_id: str

class HandoffArchiveBudgetRecord(BaseModel):
    budget_id: str

class CorridorBudgetRecord(BaseModel):
    budget_id: str

class AuditSimulationBudgetRecord(BaseModel):
    budget_id: str

class BudgetConsumptionRecord(BaseModel):
    consumption_id: str

class BudgetBreachRecord(BaseModel):
    breach_id: str

class PlanetaryTransportBudgetHealthRecord(BaseModel):
    health_id: str

class PlanetaryTransportBudgetManifestRecord(BaseModel):
    manifest_id: str

class PlanetaryTransportBudgetWarningRecord(BaseModel):
    warning_id: str

class PlanetaryTransportMatrixRow(BaseModel):
    row_id: str
    owner_visible: bool
    freshness_note_visible: bool
    no_safe_visible: bool
    sovereignty_note_visible: bool
    residue_visible: bool
    degraded_lane_visible: bool
    replayability_preserved: bool
    archive_continuity_preserved: bool
    rollback_explicit: bool
    seam_explicit: bool
    lag_visibility_explicit: bool
    agreement_boundedness_explicit: bool
    audit_handoff_explicit: bool

class PlanetaryTransportMatrix(BaseModel):
    matrix_id: str
    rows: List[PlanetaryTransportMatrixRow]
