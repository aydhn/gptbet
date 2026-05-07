from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QuorumMeshNodeRecord(BaseModel):
    node_id: str
    node_family: str
    region: str
    status: str

class QuorumMeshEdgeRecord(BaseModel):
    edge_id: str
    source_node_id: str
    target_node_id: str
    edge_status: str
    lag_ms: int

class QuorumMeshPathRecord(BaseModel):
    path_id: str
    nodes: List[str]
    edges: List[str]
    path_status: str

class QuorumMeshLagRecord(BaseModel):
    lag_id: str
    lag_ms: int
    context: str

class QuorumMeshVoteRecord(BaseModel):
    vote_id: str
    voter_node_id: str
    target_node_id: str
    vote_weight: int
    caveats: List[str]

class QuorumMeshContinuityRecord(BaseModel):
    continuity_id: str
    continuity_status: str
    caveats: List[str]

class QuorumMeshResidueRecord(BaseModel):
    residue_id: str
    description: str

class QuorumMeshHealthRecord(BaseModel):
    health_id: str
    status: str
    issues: List[str]

class RegionalQuorumMeshWarningRecord(BaseModel):
    warning_id: str
    message: str

class RegionalQuorumMeshRecord(BaseModel):
    regional_quorum_mesh_id: str
    mesh_family: str
    node_refs: List[QuorumMeshNodeRecord] = Field(default_factory=list)
    edge_refs: List[QuorumMeshEdgeRecord] = Field(default_factory=list)
    path_refs: List[QuorumMeshPathRecord] = Field(default_factory=list)
    lag_refs: List[QuorumMeshLagRecord] = Field(default_factory=list)
    vote_refs: List[QuorumMeshVoteRecord] = Field(default_factory=list)
    continuity_refs: List[QuorumMeshContinuityRecord] = Field(default_factory=list)
    residue_refs: List[QuorumMeshResidueRecord] = Field(default_factory=list)
    mesh_status: str
    warnings: List[RegionalQuorumMeshWarningRecord] = Field(default_factory=list)

class RegionalQuorumMeshManifestRecord(BaseModel):
    manifest_id: str
    mesh_refs: List[RegionalQuorumMeshRecord]

# Planetary Coverage
class CoverageZoneRecord(BaseModel):
    zone_id: str
    name: str

class CoverageWindowRecord(BaseModel):
    window_id: str
    start_time: str
    end_time: str

class CoverageOwnerRecord(BaseModel):
    owner_id: str
    role: str

class CoverageSeamRecord(BaseModel):
    seam_id: str
    status: str

class CoverageOverlapRecord(BaseModel):
    overlap_id: str
    duration_minutes: int

class CoverageGapRecord(BaseModel):
    gap_id: str
    duration_minutes: int

class CoverageReachabilityRecord(BaseModel):
    reachability_id: str
    status: str

class PlanetaryCoverageWarningRecord(BaseModel):
    warning_id: str
    message: str

class PlanetaryCoverageHealthRecord(BaseModel):
    health_id: str
    status: str

class PlanetaryCoverageSynthesisRecord(BaseModel):
    planetary_coverage_synthesis_id: str
    synthesis_family: str
    zone_refs: List[CoverageZoneRecord] = Field(default_factory=list)
    window_refs: List[CoverageWindowRecord] = Field(default_factory=list)
    owner_refs: List[CoverageOwnerRecord] = Field(default_factory=list)
    seam_refs: List[CoverageSeamRecord] = Field(default_factory=list)
    overlap_refs: List[CoverageOverlapRecord] = Field(default_factory=list)
    gap_refs: List[CoverageGapRecord] = Field(default_factory=list)
    reachability_refs: List[CoverageReachabilityRecord] = Field(default_factory=list)
    synthesis_status: str
    warnings: List[PlanetaryCoverageWarningRecord] = Field(default_factory=list)

class PlanetaryCoverageManifestRecord(BaseModel):
    manifest_id: str
    synthesis_refs: List[PlanetaryCoverageSynthesisRecord]

# Global Drill
class ContinuityRegionRecord(BaseModel):
    region_id: str

class ContinuityScenarioRecord(BaseModel):
    scenario_id: str
    description: str

class ContinuityPhaseRecord(BaseModel):
    phase_id: str
    phase_family: str

class ContinuityCheckpointRecord(BaseModel):
    checkpoint_id: str
    checkpoint_family: str

class ContinuityDecisionRecord(BaseModel):
    decision_id: str
    outcome: str

class ContinuityGapRecord(BaseModel):
    gap_id: str
    description: str

class ContinuityResidueRecord(BaseModel):
    residue_id: str
    description: str

class GlobalContinuityWarningRecord(BaseModel):
    warning_id: str
    message: str

class GlobalContinuityHealthRecord(BaseModel):
    health_id: str
    status: str

class GlobalContinuityDrillRecord(BaseModel):
    global_continuity_drill_id: str
    drill_family: str
    region_refs: List[ContinuityRegionRecord] = Field(default_factory=list)
    scenario_refs: List[ContinuityScenarioRecord] = Field(default_factory=list)
    phase_refs: List[ContinuityPhaseRecord] = Field(default_factory=list)
    checkpoint_refs: List[ContinuityCheckpointRecord] = Field(default_factory=list)
    decision_refs: List[ContinuityDecisionRecord] = Field(default_factory=list)
    gap_refs: List[ContinuityGapRecord] = Field(default_factory=list)
    residue_refs: List[ContinuityResidueRecord] = Field(default_factory=list)
    drill_status: str
    warnings: List[GlobalContinuityWarningRecord] = Field(default_factory=list)

class GlobalContinuityManifestRecord(BaseModel):
    manifest_id: str
    drill_refs: List[GlobalContinuityDrillRecord]

# Governance
class GovernanceRegionRoleRecord(BaseModel):
    role_id: str
    role_family: str

class GovernanceDecisionWindowRecord(BaseModel):
    window_id: str
    start_time: str
    end_time: str

class GovernanceApprovalRecord(BaseModel):
    approval_id: str
    status: str

class GovernanceFallbackRecord(BaseModel):
    fallback_id: str
    status: str

class GovernanceGapRecord(BaseModel):
    gap_id: str
    description: str

class GovernanceResidueRecord(BaseModel):
    residue_id: str
    description: str

class GovernanceContinuityRecord(BaseModel):
    continuity_id: str
    status: str

class CrossRegionGovernanceWarningRecord(BaseModel):
    warning_id: str
    message: str

class CrossRegionGovernanceHealthRecord(BaseModel):
    health_id: str
    status: str

class CrossRegionRecoveryGovernanceRecord(BaseModel):
    cross_region_recovery_governance_id: str
    governance_family: str
    region_role_refs: List[GovernanceRegionRoleRecord] = Field(default_factory=list)
    decision_window_refs: List[GovernanceDecisionWindowRecord] = Field(default_factory=list)
    approval_refs: List[GovernanceApprovalRecord] = Field(default_factory=list)
    fallback_refs: List[GovernanceFallbackRecord] = Field(default_factory=list)
    gap_refs: List[GovernanceGapRecord] = Field(default_factory=list)
    residue_refs: List[GovernanceResidueRecord] = Field(default_factory=list)
    continuity_refs: List[GovernanceContinuityRecord] = Field(default_factory=list)
    governance_status: str
    warnings: List[CrossRegionGovernanceWarningRecord] = Field(default_factory=list)

class CrossRegionGovernanceManifestRecord(BaseModel):
    manifest_id: str
    governance_refs: List[CrossRegionRecoveryGovernanceRecord]

# Budgets
class GlobalQuorumBudgetRecord(BaseModel):
    budget_id: str
    limit: int

class CoverageBudgetRecord(BaseModel):
    budget_id: str
    limit: int

class GlobalContinuityBudgetRecord(BaseModel):
    budget_id: str
    limit: int

class GovernanceApprovalBudgetRecord(BaseModel):
    budget_id: str
    limit: int

class BudgetConsumptionRecord(BaseModel):
    consumption_id: str
    amount: int

class BudgetBreachRecord(BaseModel):
    breach_id: str
    description: str

class GlobalResilienceBudgetWarningRecord(BaseModel):
    warning_id: str
    message: str

class GlobalResilienceBudgetHealthRecord(BaseModel):
    health_id: str
    status: str

class GlobalResilienceBudgetsRecord(BaseModel):
    budgets_id: str
    quorum_budgets: List[GlobalQuorumBudgetRecord] = Field(default_factory=list)
    coverage_budgets: List[CoverageBudgetRecord] = Field(default_factory=list)
    continuity_budgets: List[GlobalContinuityBudgetRecord] = Field(default_factory=list)
    governance_budgets: List[GovernanceApprovalBudgetRecord] = Field(default_factory=list)
    consumptions: List[BudgetConsumptionRecord] = Field(default_factory=list)
    breaches: List[BudgetBreachRecord] = Field(default_factory=list)
    warnings: List[GlobalResilienceBudgetWarningRecord] = Field(default_factory=list)

class GlobalResilienceBudgetManifestRecord(BaseModel):
    manifest_id: str
    budgets_refs: List[GlobalResilienceBudgetsRecord]
