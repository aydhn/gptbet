"""
Data structures (Contracts) for Hardening.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class DeterminismRunRecord:
    determinism_run_id: str
    run_family: str
    source_command_ref: str
    config_hash: str
    input_hash: str
    environment_hash: str
    seed_ref: str
    clock_ref: str
    output_hashes: Dict[str, str]
    parity_status: str
    warnings: List[str] = field(default_factory=list)

@dataclass
class RegressionCaseRecord:
    regression_case_id: str
    case_family: str
    fixture_ref: str
    expected_golden_ref: str
    actual_output_ref: str
    diff_ref: str
    tolerance_ref: str
    result_status: str
    warnings: List[str] = field(default_factory=list)

@dataclass
class SafetyInvariantRecord:
    invariant_id: str
    family: str
    severity: str
    description: str

@dataclass
class SafetyValidationRunRecord:
    validation_run_id: str
    target_module: str
    checked_invariants: List[str]
    violations: List['SafetyViolationRecord']
    status: str

@dataclass
class SafetyViolationRecord:
    invariant_id: str
    severity: str
    context: Dict[str, Any]
    details: str

@dataclass
class CrossModuleInvariantMatrixRecord:
    matrix_id: str
    modules: List[str]
    pair_validations: Dict[str, Dict[str, str]]
    overall_health: str

@dataclass
class ReplayParityRunRecord:
    replay_run_id: str
    fixture_ref: str
    parity_status: str
    diff_ref: Optional[str] = None
    warnings: List[str] = field(default_factory=list)

@dataclass
class ArtifactReproducibilityRecord:
    artifact_id: str
    artifact_type: str
    reproducibility_status: str
    mismatch_details: Optional[str] = None

@dataclass
class FlakinessCaseRecord:
    flakiness_case_id: str
    target_command: str
    run_count: int
    inconsistent_outputs: bool
    cluster_refs: List[str]
    is_safety_preserving: bool

@dataclass
class HardeningManifestRecord:
    manifest_id: str
    timestamp: str
    determinism_runs: List[DeterminismRunRecord]
    regression_cases: List[RegressionCaseRecord]
    safety_validations: List[SafetyValidationRunRecord]
    replay_parity_runs: List[ReplayParityRunRecord]
    artifact_reproducibility: List[ArtifactReproducibilityRecord]
    flakiness_cases: List[FlakinessCaseRecord]
    release_blockers: List[str]
    overall_health: str
