from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from datetime import datetime, timezone

class ConvergenceInputRecord(BaseModel):
    input_id: str
    source_layer: str
    is_stale: bool = False
    details: Dict[str, str] = Field(default_factory=dict)

class ConvergenceDimensionRecord(BaseModel):
    dimension_id: str
    dimension_type: str
    details: Dict[str, str] = Field(default_factory=dict)

class ConvergenceBlockerRecord(BaseModel):
    blocker_id: str
    severity: str
    description: str
    resolved: bool = False
    hidden: bool = False

class ConvergenceCaveatRecord(BaseModel):
    caveat_id: str
    description: str
    impact: str

class ConvergenceResidueRecord(BaseModel):
    residue_id: str
    description: str
    hidden: bool = False

class ConvergenceDecisionRecord(BaseModel):
    decision_id: str
    outcome: str
    rationale: str

class ConvergenceReplayRecord(BaseModel):
    replay_id: str
    replayable: bool
    details: Dict[str, str] = Field(default_factory=dict)

class FinalHardeningConvergenceRecord(BaseModel):
    final_convergence_id: str
    convergence_family: Literal[
        "final_readiness_convergence",
        "proof_and_replay_convergence",
        "visibility_and_sovereignty_convergence",
        "operator_and_recovery_convergence",
        "archive_and_lineage_convergence",
        "release_gate_convergence",
        "composite_final_convergence"
    ]
    input_refs: List[ConvergenceInputRecord] = Field(default_factory=list)
    dimension_refs: List[ConvergenceDimensionRecord] = Field(default_factory=list)
    blocker_refs: List[ConvergenceBlockerRecord] = Field(default_factory=list)
    caveat_refs: List[ConvergenceCaveatRecord] = Field(default_factory=list)
    residue_refs: List[ConvergenceResidueRecord] = Field(default_factory=list)
    decision_refs: List[ConvergenceDecisionRecord] = Field(default_factory=list)
    replay_refs: List[ConvergenceReplayRecord] = Field(default_factory=list)
    convergence_status: Literal[
        "convergence_verified",
        "convergence_caveated",
        "convergence_review_only",
        "convergence_gapped",
        "convergence_blocked",
        "convergence_overclaimed"
    ]
    warnings: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class FinalHardeningConvergenceWarningRecord(BaseModel):
    warning_id: str
    message: str

class FinalHardeningConvergenceHealthRecord(BaseModel):
    health_status: str
    metrics: Dict[str, int] = Field(default_factory=dict)

class FinalHardeningConvergenceManifestRecord(BaseModel):
    manifest_id: str
    version: str
    convergence_refs: List[str] = Field(default_factory=list)

# Dimension Models
class ConvergenceFreshnessRecord(BaseModel):
    freshness_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_stale: bool = False

class ConvergenceLineageRecord(BaseModel):
    lineage_id: str
    source_refs: List[str] = Field(default_factory=list)

class ConvergenceGapRecord(BaseModel):
    gap_id: str
    description: str

class ConvergenceRollbackRecord(BaseModel):
    rollback_id: str
    explicit: bool = False

class ConvergenceHealthMarkerRecord(BaseModel):
    marker_id: str
    status: str

class ConvergencePrecedenceRecord(BaseModel):
    precedence_id: str
    level: int

# Baseline Models
class BaselineScopeRecord(BaseModel):
    scope_id: str
    scope_type: str

class BaselineInputRecord(BaseModel):
    input_id: str
    description: str

class BaselineHashRecord(BaseModel):
    hash_id: str
    hash_value: str

class BaselineFreshnessRecord(BaseModel):
    freshness_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_stale: bool = False

class BaselineDriftRecord(BaseModel):
    drift_id: str
    description: str
    hidden: bool = False

class BaselineExceptionRecord(BaseModel):
    exception_id: str
    description: str

class BaselineResidueRecord(BaseModel):
    residue_id: str
    description: str

class FrozenBaselineRecord(BaseModel):
    frozen_baseline_id: str
    baseline_family: Literal[
        "final_validation_baseline",
        "release_gating_baseline",
        "operator_proof_baseline",
        "replay_closure_baseline",
        "visibility_ledger_baseline",
        "scheduler_truth_baseline",
        "composite_frozen_baseline"
    ]
    scope_refs: List[BaselineScopeRecord] = Field(default_factory=list)
    input_refs: List[BaselineInputRecord] = Field(default_factory=list)
    hash_refs: List[BaselineHashRecord] = Field(default_factory=list)
    freshness_refs: List[BaselineFreshnessRecord] = Field(default_factory=list)
    drift_refs: List[BaselineDriftRecord] = Field(default_factory=list)
    residue_refs: List[BaselineResidueRecord] = Field(default_factory=list)
    baseline_status: Literal[
        "baseline_verified",
        "baseline_caveated",
        "baseline_review_only",
        "baseline_gapped",
        "baseline_blocked",
        "baseline_overclaimed"
    ]
    warnings: List[str] = Field(default_factory=list)

class FrozenBaselineHealthRecord(BaseModel):
    health_status: str

class FrozenBaselineManifestRecord(BaseModel):
    manifest_id: str
    baseline_refs: List[str] = Field(default_factory=list)

class FrozenBaselineWarningRecord(BaseModel):
    warning_id: str
    message: str

# Scope Models
class BaselineOwnerRecord(BaseModel):
    owner_id: str

class BaselineGapRecord(BaseModel):
    gap_id: str

class BaselineRollbackRecord(BaseModel):
    rollback_id: str

class BaselineReplayRecord(BaseModel):
    replay_id: str

class BaselineHealthMarkerRecord(BaseModel):
    marker_id: str

class BaselineApplicabilityRecord(BaseModel):
    applicability_id: str
    hidden: bool = False

# Review Surface Models
class ReviewSurfaceSectionRecord(BaseModel):
    section_id: str
    section_type: str

class ReviewSurfaceEvidenceRecord(BaseModel):
    evidence_id: str

class ReviewSurfaceBlockerRecord(BaseModel):
    blocker_id: str
    hidden: bool = False

class ReviewSurfaceResidueRecord(BaseModel):
    residue_id: str
    hidden: bool = False

class ReviewSurfaceGapRecord(BaseModel):
    gap_id: str
    hidden: bool = False

class ReviewSurfaceDecisionRecord(BaseModel):
    decision_id: str

class ReviewSurfaceContinuityRecord(BaseModel):
    continuity_id: str

class ProductionReadinessReviewSurfaceRecord(BaseModel):
    readiness_review_surface_id: str
    surface_family: Literal[
        "operator_readiness_review_surface",
        "release_readiness_review_surface",
        "visibility_readiness_review_surface",
        "archive_and_replay_review_surface",
        "no_safe_visibility_review_surface",
        "sovereignty_visibility_review_surface",
        "composite_production_readiness_review_surface"
    ]
    section_refs: List[ReviewSurfaceSectionRecord] = Field(default_factory=list)
    evidence_refs: List[ReviewSurfaceEvidenceRecord] = Field(default_factory=list)
    blocker_refs: List[ReviewSurfaceBlockerRecord] = Field(default_factory=list)
    residue_refs: List[ReviewSurfaceResidueRecord] = Field(default_factory=list)
    gap_refs: List[ReviewSurfaceGapRecord] = Field(default_factory=list)
    decision_refs: List[ReviewSurfaceDecisionRecord] = Field(default_factory=list)
    continuity_refs: List[ReviewSurfaceContinuityRecord] = Field(default_factory=list)
    surface_status: Literal[
        "surface_verified",
        "surface_caveated",
        "surface_review_only",
        "surface_gapped",
        "surface_blocked",
        "surface_overclaimed"
    ]
    warnings: List[str] = Field(default_factory=list)

class ProductionReadinessReviewHealthRecord(BaseModel):
    health_status: str

class ProductionReadinessReviewManifestRecord(BaseModel):
    manifest_id: str

class ProductionReadinessReviewWarningRecord(BaseModel):
    warning_id: str
    message: str

# Section Models
class ReviewSurfaceOwnerRecord(BaseModel):
    owner_id: str

class ReviewSurfaceFreshnessRecord(BaseModel):
    freshness_id: str
    is_stale: bool = False

class ReviewSurfaceMismatchRecord(BaseModel):
    mismatch_id: str
    hidden: bool = False

class ReviewSurfaceDriftRecord(BaseModel):
    drift_id: str

class ReviewSurfaceHealthMarkerRecord(BaseModel):
    marker_id: str

class ReviewSurfaceAcknowledgementRecord(BaseModel):
    ack_id: str
    explicit: bool = False

# Acceptance Pack Models
class AcceptancePackSectionRecord(BaseModel):
    section_id: str
    section_type: str

class AcceptancePackEvidenceRecord(BaseModel):
    evidence_id: str
    replayable: bool = False

class AcceptancePackReplayRecord(BaseModel):
    replay_id: str

class AcceptancePackBlockerRecord(BaseModel):
    blocker_id: str
    hidden: bool = False

class AcceptancePackResidueRecord(BaseModel):
    residue_id: str
    hidden: bool = False

class AcceptancePackGapRecord(BaseModel):
    gap_id: str
    hidden: bool = False

class AcceptancePackDecisionRecord(BaseModel):
    decision_id: str

class TerminalAcceptancePackRecord(BaseModel):
    terminal_acceptance_pack_id: str
    pack_family: Literal[
        "final_readiness_acceptance_pack",
        "operator_acceptance_pack",
        "visibility_acceptance_pack",
        "archive_replay_acceptance_pack",
        "release_gate_acceptance_pack",
        "no_safe_visibility_acceptance_pack",
        "composite_terminal_acceptance_pack"
    ]
    section_refs: List[AcceptancePackSectionRecord] = Field(default_factory=list)
    evidence_refs: List[AcceptancePackEvidenceRecord] = Field(default_factory=list)
    replay_refs: List[AcceptancePackReplayRecord] = Field(default_factory=list)
    blocker_refs: List[AcceptancePackBlockerRecord] = Field(default_factory=list)
    residue_refs: List[AcceptancePackResidueRecord] = Field(default_factory=list)
    gap_refs: List[AcceptancePackGapRecord] = Field(default_factory=list)
    decision_refs: List[AcceptancePackDecisionRecord] = Field(default_factory=list)
    pack_status: Literal[
        "pack_verified",
        "pack_caveated",
        "pack_review_only",
        "pack_gapped",
        "pack_blocked",
        "pack_overclaimed"
    ]
    warnings: List[str] = Field(default_factory=list)

class TerminalAcceptancePackHealthRecord(BaseModel):
    health_status: str

class TerminalAcceptancePackManifestRecord(BaseModel):
    manifest_id: str

class TerminalAcceptancePackWarningRecord(BaseModel):
    warning_id: str
    message: str

# Acceptance Section Models
class AcceptancePackOwnerRecord(BaseModel):
    owner_id: str

class AcceptancePackFreshnessRecord(BaseModel):
    freshness_id: str
    is_stale: bool = False

class AcceptancePackMismatchRecord(BaseModel):
    mismatch_id: str
    hidden: bool = False

class AcceptancePackDriftRecord(BaseModel):
    drift_id: str

class AcceptancePackHealthMarkerRecord(BaseModel):
    marker_id: str

class AcceptancePackAcknowledgementRecord(BaseModel):
    ack_id: str
    explicit: bool = False

# Budget Models
class ConvergenceBudgetRecord(BaseModel):
    budget_id: str

class FrozenBaselineBudgetRecord(BaseModel):
    budget_id: str

class ReviewSurfaceBudgetRecord(BaseModel):
    budget_id: str

class TerminalAcceptanceBudgetRecord(BaseModel):
    budget_id: str

class BudgetConsumptionRecord(BaseModel):
    consumption_id: str

class BudgetBreachRecord(BaseModel):
    breach_id: str

class FinalConvergenceBudgetHealthRecord(BaseModel):
    health_status: str

class FinalConvergenceBudgetManifestRecord(BaseModel):
    manifest_id: str

class FinalConvergenceBudgetWarningRecord(BaseModel):
    warning_id: str
