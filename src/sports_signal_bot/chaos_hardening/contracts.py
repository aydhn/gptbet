from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# ----------------- CHAOS PROBES -----------------

class ChaosFaultRecord(BaseModel):
    fault_type: str
    severity: str
    target_component: str

class ChaosInjectionPointRecord(BaseModel):
    point_id: str
    location: str
    fault: ChaosFaultRecord

class ChaosObservationRecord(BaseModel):
    observation_id: str
    surface: str
    degraded: bool
    caveat_preserved: bool
    no_safe_visible: bool

class ChaosOutcomeRecord(BaseModel):
    status: str
    details: str

class ChaosResidueRecord(BaseModel):
    residue_id: str
    family: str
    resolved: bool

class ChaosHealthRecord(BaseModel):
    is_healthy: bool
    score: int

class ChaosManifestRecord(BaseModel):
    manifest_id: str
    description: str

class ChaosWarningRecord(BaseModel):
    warning_id: str
    severity: str
    message: str

class ChaosScenarioRecord(BaseModel):
    scenario_id: str
    family: str
    description: str

class ChaosProbeRunRecord(BaseModel):
    chaos_probe_run_id: str
    run_family: str
    scenario_refs: List[str]
    injected_fault_refs: List[str]
    seed_ref: str
    environment_hash: str
    observed_effect_refs: List[str]
    outcome_status: str
    residue_refs: List[str]
    warnings: List[ChaosWarningRecord]

# ----------------- FAULT INJECTION -----------------

class FaultTargetRecord(BaseModel):
    target_id: str
    family: str

class FaultSeverityRecord(BaseModel):
    severity: str

class FaultRecoveryExpectationRecord(BaseModel):
    expectation_id: str
    description: str

class FaultWindowRecord(BaseModel):
    start_time: str
    end_time: str

class FaultInjectionEventRecord(BaseModel):
    event_id: str
    fault_type: str
    target: FaultTargetRecord

class FaultInjectionHealthRecord(BaseModel):
    is_healthy: bool

class FaultInjectionManifestRecord(BaseModel):
    manifest_id: str

class FaultInjectionWarningRecord(BaseModel):
    warning_id: str
    message: str

class FaultInjectionPlanRecord(BaseModel):
    plan_id: str
    events: List[FaultInjectionEventRecord]

# ----------------- DEGRADATION REHEARSALS -----------------

class RehearsalStageRecord(BaseModel):
    stage_id: str
    description: str

class RehearsalFallbackRecord(BaseModel):
    fallback_id: str
    is_stale: bool

class RehearsalDegradationPathRecord(BaseModel):
    path_id: str
    is_hidden: bool

class RehearsalDecisionRecord(BaseModel):
    decision_id: str
    status: str

class RehearsalResidueRecord(BaseModel):
    residue_id: str
    is_visible: bool

class RehearsalHealthRecord(BaseModel):
    is_healthy: bool

class RehearsalManifestRecord(BaseModel):
    manifest_id: str

class RehearsalWarningRecord(BaseModel):
    warning_id: str
    message: str

class DegradationRehearsalRecord(BaseModel):
    rehearsal_id: str
    rehearsal_family: str
    stage_refs: List[str]
    fallback_refs: List[str]
    degradation_path_refs: List[str]
    residue_refs: List[str]
    outcome_status: str
    warnings: List[RehearsalWarningRecord]

# ----------------- RECOVERY HONESTY VALIDATION -----------------

class RecoveryEvidenceRecord(BaseModel):
    evidence_id: str

class RecoveryResidueRecord(BaseModel):
    residue_id: str

class RecoveryOverclaimRecord(BaseModel):
    overclaim_id: str
    description: str

class RecoveryHonestyDecisionRecord(BaseModel):
    decision_id: str

class RecoveryHonestyHealthRecord(BaseModel):
    is_healthy: bool

class RecoveryHonestyManifestRecord(BaseModel):
    manifest_id: str

class RecoveryHonestyWarningRecord(BaseModel):
    warning_id: str

class RecoveryClaimRecord(BaseModel):
    recovery_claim_id: str
    claim_family: str
    claimed_status: str
    supporting_evidence_refs: List[str]
    residue_refs: List[str]
    contradiction_refs: List[str]
    honesty_status: str
    warnings: List[RecoveryHonestyWarningRecord]

class RecoveryHonestyValidationRecord(BaseModel):
    validation_id: str
    claims: List[RecoveryClaimRecord]

# ----------------- FAILURE VISIBILITY -----------------

class FailureSurfaceRecord(BaseModel):
    surface_id: str

class FailureMarkerRecord(BaseModel):
    marker_id: str

class FailureSuppressionRecord(BaseModel):
    suppression_id: str

class FailureVisibilityHealthRecord(BaseModel):
    is_healthy: bool

class FailureVisibilityManifestRecord(BaseModel):
    manifest_id: str

class FailureVisibilityWarningRecord(BaseModel):
    warning_id: str
    message: str

class FailureVisibilityRecord(BaseModel):
    visibility_id: str
    surfaces: List[str]
    warnings: List[FailureVisibilityWarningRecord]

# ----------------- CHAOS SCHEDULE PERTURBATION -----------------

class PerturbationStepRecord(BaseModel):
    step_id: str

class PerturbationClusterRecord(BaseModel):
    cluster_id: str

class PerturbationReplayRecord(BaseModel):
    replay_id: str

class PerturbationHealthRecord(BaseModel):
    is_healthy: bool

class PerturbationManifestRecord(BaseModel):
    manifest_id: str

class PerturbationWarningRecord(BaseModel):
    warning_id: str

class ChaosScheduleRecord(BaseModel):
    schedule_id: str
    steps: List[PerturbationStepRecord]

# ----------------- FAULT TOLERANCE BUDGETS -----------------

class ToleranceWindowRecord(BaseModel):
    window_id: str

class ErrorBudgetRecord(BaseModel):
    budget_id: str

class RecoveryBudgetRecord(BaseModel):
    budget_id: str

class DegradationBudgetRecord(BaseModel):
    budget_id: str

class BudgetHealthRecord(BaseModel):
    is_healthy: bool

class FaultToleranceManifestRecord(BaseModel):
    manifest_id: str

class FaultToleranceWarningRecord(BaseModel):
    warning_id: str

class FaultToleranceBudgetRecord(BaseModel):
    budget_id: str
    error_budgets: List[ErrorBudgetRecord]
