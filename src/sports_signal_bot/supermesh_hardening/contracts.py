from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ==============================================================================
# FEDERATION BUS SUPERMESH CONTRACTS
# ==============================================================================

class SupermeshNodeRecord(BaseModel):
    node_id: str
    node_family: str
    is_ownerless: bool = False
    is_critical: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)

class SupermeshEdgeRecord(BaseModel):
    edge_id: str
    edge_status: str
    from_node: str
    to_node: str
    is_stale: bool = False
    is_fallback: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)

class SupermeshPathRecord(BaseModel):
    path_id: str
    edge_refs: List[str] = Field(default_factory=list)
    has_lagged_edges: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)

class SupermeshLagRecord(BaseModel):
    lag_id: str
    target_ref: str
    lag_amount: float
    details: Dict[str, Any] = Field(default_factory=dict)

class SupermeshCaveatRecord(BaseModel):
    caveat_id: str
    target_ref: str
    description: str

class SupermeshResidueRecord(BaseModel):
    residue_id: str
    description: str
    severity: str

class SupermeshAgreementRecord(BaseModel):
    agreement_id: str
    path_refs: List[str] = Field(default_factory=list)

class FederationBusSupermeshWarningRecord(BaseModel):
    warning_id: str
    description: str
    severity: str

class FederationBusSupermeshRecord(BaseModel):
    federation_bus_supermesh_id: str
    supermesh_family: str
    node_refs: List[str] = Field(default_factory=list)
    edge_refs: List[str] = Field(default_factory=list)
    path_refs: List[str] = Field(default_factory=list)
    agreement_refs: List[str] = Field(default_factory=list)
    lag_refs: List[str] = Field(default_factory=list)
    residue_refs: List[str] = Field(default_factory=list)
    supermesh_status: str
    warnings: List[str] = Field(default_factory=list)
    no_safe_visible: bool = True
    sovereignty_visible: bool = True

class FederationBusSupermeshHealthRecord(BaseModel):
    readiness_score: float
    status: str
    blockers: List[str] = Field(default_factory=list)

class FederationBusSupermeshManifestRecord(BaseModel):
    supermeshes: List[FederationBusSupermeshRecord] = Field(default_factory=list)
    health: FederationBusSupermeshHealthRecord

# ==============================================================================
# SCHEDULER CADENCE FABRIC CONTRACTS
# ==============================================================================

class CadenceFabricLaneRecord(BaseModel):
    lane_id: str
    lane_family: str
    is_ownerless: bool = False
    is_critical: bool = False

class CadenceFabricPacketRecord(BaseModel):
    packet_id: str
    lane_ref: str
    is_stale: bool = False
    details: Dict[str, Any] = Field(default_factory=dict)

class CadenceFabricWindowRecord(BaseModel):
    window_id: str
    packet_refs: List[str] = Field(default_factory=list)

class CadenceFabricDriftRecord(BaseModel):
    drift_id: str
    target_ref: str
    drift_amount: float
    is_hidden: bool = False

class CadenceFabricReachabilityRecord(BaseModel):
    reachability_id: str
    target_ref: str
    is_reachable: bool = True

class CadenceFabricResidueRecord(BaseModel):
    residue_id: str
    description: str

class CadenceFabricContinuityRecord(BaseModel):
    continuity_id: str
    description: str

class SchedulerCadenceFabricWarningRecord(BaseModel):
    warning_id: str
    description: str
    severity: str

class SchedulerCadenceFabricRecord(BaseModel):
    scheduler_cadence_fabric_id: str
    fabric_family: str
    lane_refs: List[str] = Field(default_factory=list)
    packet_refs: List[str] = Field(default_factory=list)
    window_refs: List[str] = Field(default_factory=list)
    drift_refs: List[str] = Field(default_factory=list)
    reachability_refs: List[str] = Field(default_factory=list)
    residue_refs: List[str] = Field(default_factory=list)
    continuity_refs: List[str] = Field(default_factory=list)
    fabric_status: str
    warnings: List[str] = Field(default_factory=list)
    no_safe_visible: bool = True
    sovereignty_visible: bool = True

class SchedulerCadenceFabricHealthRecord(BaseModel):
    status: str
    blockers: List[str] = Field(default_factory=list)

class SchedulerCadenceFabricManifestRecord(BaseModel):
    fabrics: List[SchedulerCadenceFabricRecord] = Field(default_factory=list)
    health: SchedulerCadenceFabricHealthRecord

# ==============================================================================
# GLOBAL AUDIT PULSE LANE CONTRACTS
# ==============================================================================

class AuditPulseRecord(BaseModel):
    pulse_id: str
    pulse_family: str
    is_stale: bool = False

class AuditPulseWindowRecord(BaseModel):
    window_id: str
    pulse_refs: List[str] = Field(default_factory=list)

class AuditPulseDeliveryRecord(BaseModel):
    delivery_id: str
    pulse_ref: str
    has_ack: bool = True

class AuditPulseMissRecord(BaseModel):
    miss_id: str
    pulse_ref: str
    is_hidden: bool = False

class AuditPulseGapRecord(BaseModel):
    gap_id: str
    description: str

class AuditPulseResidueRecord(BaseModel):
    residue_id: str
    description: str

class AuditPulseContinuityRecord(BaseModel):
    continuity_id: str
    description: str

class GlobalAuditPulseLaneWarningRecord(BaseModel):
    warning_id: str
    description: str
    severity: str

class GlobalAuditPulseLaneRecord(BaseModel):
    global_audit_pulse_lane_id: str
    lane_family: str
    pulse_refs: List[str] = Field(default_factory=list)
    window_refs: List[str] = Field(default_factory=list)
    delivery_refs: List[str] = Field(default_factory=list)
    miss_refs: List[str] = Field(default_factory=list)
    gap_refs: List[str] = Field(default_factory=list)
    residue_refs: List[str] = Field(default_factory=list)
    continuity_refs: List[str] = Field(default_factory=list)
    lane_status: str
    warnings: List[str] = Field(default_factory=list)
    no_safe_visible: bool = True
    sovereignty_visible: bool = True

class GlobalAuditPulseLaneHealthRecord(BaseModel):
    status: str
    blockers: List[str] = Field(default_factory=list)

class GlobalAuditPulseLaneManifestRecord(BaseModel):
    lanes: List[GlobalAuditPulseLaneRecord] = Field(default_factory=list)
    health: GlobalAuditPulseLaneHealthRecord

# ==============================================================================
# PLANETARY HANDOFF OBSERVATORY CONTRACTS
# ==============================================================================

class HandoffObservatoryWindowRecord(BaseModel):
    window_id: str
    window_family: str
    is_ownerless: bool = False

class HandoffObservatoryOwnerRecord(BaseModel):
    owner_id: str
    description: str

class HandoffObservatorySeamRecord(BaseModel):
    seam_id: str
    description: str

class HandoffObservatoryAckRecord(BaseModel):
    ack_id: str
    target_ref: str

class HandoffObservatoryGapRecord(BaseModel):
    gap_id: str
    is_hidden: bool = False

class HandoffObservatoryResidueRecord(BaseModel):
    residue_id: str
    description: str

class HandoffObservatoryReplayRecord(BaseModel):
    replay_id: str
    is_stale: bool = False
    no_safe_preserved: bool = True
    sovereignty_preserved: bool = True
    mismatch_hidden: bool = False

class PlanetaryHandoffObservatoryWarningRecord(BaseModel):
    warning_id: str
    description: str
    severity: str

class PlanetaryHandoffObservatoryRecord(BaseModel):
    planetary_handoff_observatory_id: str
    observatory_family: str
    window_refs: List[str] = Field(default_factory=list)
    owner_refs: List[str] = Field(default_factory=list)
    seam_refs: List[str] = Field(default_factory=list)
    ack_refs: List[str] = Field(default_factory=list)
    gap_refs: List[str] = Field(default_factory=list)
    residue_refs: List[str] = Field(default_factory=list)
    replay_refs: List[str] = Field(default_factory=list)
    observatory_status: str
    warnings: List[str] = Field(default_factory=list)

class PlanetaryHandoffObservatoryHealthRecord(BaseModel):
    status: str
    blockers: List[str] = Field(default_factory=list)

class PlanetaryHandoffObservatoryManifestRecord(BaseModel):
    observatories: List[PlanetaryHandoffObservatoryRecord] = Field(default_factory=list)
    health: PlanetaryHandoffObservatoryHealthRecord

# ==============================================================================
# MATRIX AND BUDGET CONTRACTS
# ==============================================================================

class SupermeshBudgetRecord(BaseModel):
    budget_id: str
    description: str

class CadenceFabricBudgetRecord(BaseModel):
    budget_id: str
    description: str

class AuditPulseBudgetRecord(BaseModel):
    budget_id: str
    description: str

class HandoffObservatoryBudgetRecord(BaseModel):
    budget_id: str
    description: str

class BudgetConsumptionRecord(BaseModel):
    consumption_id: str
    budget_ref: str
    amount: float

class BudgetBreachRecord(BaseModel):
    breach_id: str
    budget_ref: str
    no_safe_loss: bool = False
    sovereignty_loss: bool = False

class SupermeshFabricBudgetHealthRecord(BaseModel):
    status: str
    blockers: List[str] = Field(default_factory=list)

class SupermeshFabricBudgetManifestRecord(BaseModel):
    supermesh_budgets: List[SupermeshBudgetRecord] = Field(default_factory=list)
    fabric_budgets: List[CadenceFabricBudgetRecord] = Field(default_factory=list)
    pulse_budgets: List[AuditPulseBudgetRecord] = Field(default_factory=list)
    observatory_budgets: List[HandoffObservatoryBudgetRecord] = Field(default_factory=list)
    consumptions: List[BudgetConsumptionRecord] = Field(default_factory=list)
    breaches: List[BudgetBreachRecord] = Field(default_factory=list)
    health: SupermeshFabricBudgetHealthRecord

class SupermeshFabricWarningRecord(BaseModel):
    warning_id: str
    description: str
