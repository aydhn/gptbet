from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ==============================================================================
# Planetary Coverage Calendar Contracts
# ==============================================================================

class CoverageCalendarZoneRecord(BaseModel):
    zone_id: str
    owner: str

class CoverageCalendarWindowRecord(BaseModel):
    window_id: str
    family: str
    is_stale: bool = False

class CoverageCalendarOwnerRecord(BaseModel):
    owner_id: str
    contact: str

class CoverageCalendarSeamRecord(BaseModel):
    seam_id: str
    is_gapped: bool = False

class CoverageCalendarGapRecord(BaseModel):
    gap_id: str
    description: str

class CoverageCalendarReachabilityRecord(BaseModel):
    reachability_id: str
    is_reachable: bool = True
    is_acknowledged: bool = True

class CoverageCalendarResidueRecord(BaseModel):
    residue_id: str
    description: str

class PlanetaryCoverageCalendarWarningRecord(BaseModel):
    warning_id: str
    message: str

class PlanetaryCoverageCalendarRecord(BaseModel):
    planetary_coverage_calendar_id: str
    calendar_family: str
    zone_refs: List[CoverageCalendarZoneRecord] = Field(default_factory=list)
    window_refs: List[CoverageCalendarWindowRecord] = Field(default_factory=list)
    owner_refs: List[CoverageCalendarOwnerRecord] = Field(default_factory=list)
    seam_refs: List[CoverageCalendarSeamRecord] = Field(default_factory=list)
    gap_refs: List[CoverageCalendarGapRecord] = Field(default_factory=list)
    reachability_refs: List[CoverageCalendarReachabilityRecord] = Field(default_factory=list)
    residue_refs: List[CoverageCalendarResidueRecord] = Field(default_factory=list)
    calendar_status: str
    warnings: List[PlanetaryCoverageCalendarWarningRecord] = Field(default_factory=list)

class PlanetaryCoverageCalendarHealthRecord(BaseModel):
    calendar_ref: str
    is_healthy: bool
    status: str

class PlanetaryCoverageCalendarManifestRecord(BaseModel):
    manifest_id: str
    calendars: List[PlanetaryCoverageCalendarRecord] = Field(default_factory=list)

# Calendar Shifts & Handoffs
class CalendarShiftRecord(BaseModel):
    shift_id: str
    owner: str

class CalendarHandoffRecord(BaseModel):
    handoff_id: str
    from_owner: str
    to_owner: str

class CalendarAckRecord(BaseModel):
    ack_id: str
    is_acknowledged: bool

class CalendarContinuityRecord(BaseModel):
    continuity_id: str
    preserves_no_safe: bool = True
    preserves_sovereignty: bool = True

class CalendarMismatchRecord(BaseModel):
    mismatch_id: str
    details: str

class CalendarLagRecord(BaseModel):
    lag_id: str
    duration_hours: float

class CalendarHealthMarkerRecord(BaseModel):
    marker_id: str
    status: str


# ==============================================================================
# Intercontinental Recovery Lane Contracts
# ==============================================================================

class RecoveryLaneSourceRecord(BaseModel):
    source_id: str
    is_fresh: bool

class RecoveryLaneTargetRecord(BaseModel):
    target_id: str
    is_ready: bool

class RecoveryLaneStageRecord(BaseModel):
    stage_id: str
    family: str

class RecoveryLaneCheckpointRecord(BaseModel):
    checkpoint_id: str
    family: str

class RecoveryLaneLagRecord(BaseModel):
    lag_id: str
    duration_hours: float

class RecoveryLaneRollbackRecord(BaseModel):
    rollback_id: str
    is_explicit: bool

class RecoveryLaneResidueRecord(BaseModel):
    residue_id: str
    description: str

class IntercontinentalRecoveryWarningRecord(BaseModel):
    warning_id: str
    message: str

class IntercontinentalRecoveryLaneRecord(BaseModel):
    intercontinental_recovery_lane_id: str
    lane_family: str
    source_ref: RecoveryLaneSourceRecord
    target_ref: RecoveryLaneTargetRecord
    stage_refs: List[RecoveryLaneStageRecord] = Field(default_factory=list)
    checkpoint_refs: List[RecoveryLaneCheckpointRecord] = Field(default_factory=list)
    lag_refs: List[RecoveryLaneLagRecord] = Field(default_factory=list)
    rollback_refs: List[RecoveryLaneRollbackRecord] = Field(default_factory=list)
    residue_refs: List[RecoveryLaneResidueRecord] = Field(default_factory=list)
    lane_status: str
    warnings: List[IntercontinentalRecoveryWarningRecord] = Field(default_factory=list)

class IntercontinentalRecoveryHealthRecord(BaseModel):
    lane_ref: str
    is_healthy: bool
    status: str

class IntercontinentalRecoveryManifestRecord(BaseModel):
    manifest_id: str
    lanes: List[IntercontinentalRecoveryLaneRecord] = Field(default_factory=list)

# Lane Stages & Dependencies
class RecoveryLaneDependencyRecord(BaseModel):
    dependency_id: str

class RecoveryLaneGapRecord(BaseModel):
    gap_id: str

class RecoveryLaneDriftRecord(BaseModel):
    drift_id: str

class RecoveryLaneVisibilityRecord(BaseModel):
    visibility_id: str

class RecoveryLaneContinuityRecord(BaseModel):
    continuity_id: str
    preserves_no_safe: bool = True
    preserves_sovereignty: bool = True

class RecoveryLaneHealthMarkerRecord(BaseModel):
    marker_id: str


# ==============================================================================
# Global Quorum Federation Contracts
# ==============================================================================

class FederatedQuorumNodeRecord(BaseModel):
    node_id: str
    is_stale: bool = False

class QuorumFederationLinkRecord(BaseModel):
    link_id: str

class QuorumFederationAgreementRecord(BaseModel):
    agreement_id: str
    agreement_band: str

class QuorumFederationCurrentnessRecord(BaseModel):
    currentness_id: str
    is_current: bool

class QuorumFederationCaveatRecord(BaseModel):
    caveat_id: str
    description: str

class QuorumFederationContinuityRecord(BaseModel):
    continuity_id: str
    preserves_no_safe: bool = True
    preserves_sovereignty: bool = True

class QuorumFederationResidueRecord(BaseModel):
    residue_id: str

class GlobalQuorumFederationWarningRecord(BaseModel):
    warning_id: str
    message: str

class GlobalQuorumFederationRecord(BaseModel):
    global_quorum_federation_id: str
    federation_family: str
    member_quorum_refs: List[FederatedQuorumNodeRecord] = Field(default_factory=list)
    active_link_refs: List[QuorumFederationLinkRecord] = Field(default_factory=list)
    agreement_refs: List[QuorumFederationAgreementRecord] = Field(default_factory=list)
    currentness_refs: List[QuorumFederationCurrentnessRecord] = Field(default_factory=list)
    continuity_refs: List[QuorumFederationContinuityRecord] = Field(default_factory=list)
    residue_refs: List[QuorumFederationResidueRecord] = Field(default_factory=list)
    federation_status: str
    warnings: List[GlobalQuorumFederationWarningRecord] = Field(default_factory=list)

class GlobalQuorumFederationHealthRecord(BaseModel):
    federation_ref: str
    is_healthy: bool
    status: str

class GlobalQuorumFederationManifestRecord(BaseModel):
    manifest_id: str
    federations: List[GlobalQuorumFederationRecord] = Field(default_factory=list)

# Quorum Federation details
class QuorumFederationLagRecord(BaseModel):
    lag_id: str
    lag_hours: float

class QuorumFederationGapRecord(BaseModel):
    gap_id: str

class QuorumFederationRollbackRecord(BaseModel):
    rollback_id: str

class QuorumFederationHealthMarkerRecord(BaseModel):
    marker_id: str

class QuorumFederationVoteLineageRecord(BaseModel):
    lineage_id: str

class QuorumFederationAsymmetryRecord(BaseModel):
    asymmetry_id: str


# ==============================================================================
# Follow-The-Sun Audit Pack Contracts
# ==============================================================================

class AuditPackWindowRecord(BaseModel):
    window_id: str

class AuditPackHandoffRecord(BaseModel):
    handoff_id: str
    is_replayable: bool = True

class AuditPackOwnerRecord(BaseModel):
    owner_id: str

class AuditPackEvidenceRecord(BaseModel):
    evidence_id: str
    is_stale: bool = False

class AuditPackGapRecord(BaseModel):
    gap_id: str

class AuditPackResidueRecord(BaseModel):
    residue_id: str

class AuditPackDecisionRecord(BaseModel):
    decision_id: str

class FollowTheSunAuditWarningRecord(BaseModel):
    warning_id: str
    message: str

class FollowTheSunAuditPackRecord(BaseModel):
    follow_the_sun_audit_pack_id: str
    audit_family: str
    window_refs: List[AuditPackWindowRecord] = Field(default_factory=list)
    handoff_refs: List[AuditPackHandoffRecord] = Field(default_factory=list)
    owner_refs: List[AuditPackOwnerRecord] = Field(default_factory=list)
    evidence_refs: List[AuditPackEvidenceRecord] = Field(default_factory=list)
    gap_refs: List[AuditPackGapRecord] = Field(default_factory=list)
    residue_refs: List[AuditPackResidueRecord] = Field(default_factory=list)
    decision_refs: List[AuditPackDecisionRecord] = Field(default_factory=list)
    audit_status: str
    warnings: List[FollowTheSunAuditWarningRecord] = Field(default_factory=list)

class FollowTheSunAuditHealthRecord(BaseModel):
    audit_ref: str
    is_healthy: bool
    status: str

class FollowTheSunAuditManifestRecord(BaseModel):
    manifest_id: str
    audits: List[FollowTheSunAuditPackRecord] = Field(default_factory=list)

# Audit Pack Handoff details
class AuditPackShiftRecord(BaseModel):
    shift_id: str

class AuditPackAckRecord(BaseModel):
    ack_id: str
    is_acknowledged: bool

class AuditPackEscalationRecord(BaseModel):
    escalation_id: str
    is_reachable: bool = True

class AuditPackMismatchRecord(BaseModel):
    mismatch_id: str

class AuditPackContinuityRecord(BaseModel):
    continuity_id: str
    preserves_no_safe: bool = True
    preserves_sovereignty: bool = True

class AuditPackHealthMarkerRecord(BaseModel):
    marker_id: str


# ==============================================================================
# Planetary Resilience Budgets
# ==============================================================================

class PlanetaryCoverageBudgetRecord(BaseModel):
    budget_id: str
    max_seam_gap_hours: float

class IntercontinentalLaneBudgetRecord(BaseModel):
    budget_id: str
    max_lag_hours: float

class QuorumFederationBudgetRecord(BaseModel):
    budget_id: str
    max_asymmetry_score: float

class FollowTheSunAuditBudgetRecord(BaseModel):
    budget_id: str
    max_handoff_lag_hours: float

class BudgetConsumptionRecord(BaseModel):
    consumption_id: str
    amount: float

class BudgetBreachRecord(BaseModel):
    breach_id: str
    description: str

class PlanetaryResilienceBudgetHealthRecord(BaseModel):
    budget_ref: str
    is_healthy: bool

class PlanetaryResilienceBudgetManifestRecord(BaseModel):
    manifest_id: str
    planetary_budgets: List[PlanetaryCoverageBudgetRecord] = Field(default_factory=list)
    lane_budgets: List[IntercontinentalLaneBudgetRecord] = Field(default_factory=list)
    quorum_budgets: List[QuorumFederationBudgetRecord] = Field(default_factory=list)
    audit_budgets: List[FollowTheSunAuditBudgetRecord] = Field(default_factory=list)
    breaches: List[BudgetBreachRecord] = Field(default_factory=list)

class PlanetaryResilienceBudgetWarningRecord(BaseModel):
    warning_id: str
    message: str
