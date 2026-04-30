from typing import List, Dict, Any
from .contracts import TournamentCandidateRecord, TournamentGateRequirementRecord, GateBurdenBand
from ..simulation.contracts import RiskLevel

def compute_gate_burden(
    candidate: TournamentCandidateRecord,
    profile_rules: Dict[str, Any]
) -> TournamentGateRequirementRecord:
    """Computes the quality gate burden for a candidate."""

    # Defaults
    burden_band = GateBurdenBand.LOW
    smoke = ["core_api_smoke"]
    regression = []
    scenario = []
    approval_req = False
    canary_req = False
    manual_adj = False

    if candidate.risk_level == RiskLevel.CRITICAL:
        burden_band = GateBurdenBand.VERY_HIGH
        regression = ["full_system_regression"]
        scenario = ["edge_case_chaos", "load_profile"]
        approval_req = True
        canary_req = True
        manual_adj = True
    elif candidate.risk_level == RiskLevel.HIGH:
        burden_band = GateBurdenBand.HIGH
        regression = ["component_regression"]
        scenario = ["boundary_testing"]
        approval_req = True
        canary_req = True
    elif candidate.risk_level == RiskLevel.MEDIUM:
        burden_band = GateBurdenBand.MEDIUM
        regression = ["targeted_regression"]
        approval_req = True

    if candidate.estimated_blast_radius > 0.5:
        canary_req = True
        if burden_band in [GateBurdenBand.LOW, GateBurdenBand.MEDIUM]:
            burden_band = GateBurdenBand.HIGH

    return TournamentGateRequirementRecord(
        candidate_id=candidate.candidate_id,
        burden_band=burden_band,
        required_smoke_suites=smoke,
        required_regression_suites=regression,
        required_scenario_suites=scenario,
        approval_required=approval_req,
        canary_mandatory=canary_req,
        manual_adjudication_follow_up_needed=manual_adj
    )

def summarize_gate_requirements(gate: TournamentGateRequirementRecord) -> str:
    parts = [f"Band: {gate.burden_band.value}"]
    if gate.approval_required: parts.append("Approval Req")
    if gate.canary_mandatory: parts.append("Canary Req")
    return " | ".join(parts)

def penalize_heavy_gate_burden_if_benefit_small(
    gate: TournamentGateRequirementRecord,
    benefit_score: float
) -> float:
    """Calculates a penalty if the gate burden is high but the benefit is small."""
    penalty = 0.0
    if gate.burden_band == GateBurdenBand.VERY_HIGH and benefit_score < 0.5:
        penalty = 10.0
    elif gate.burden_band == GateBurdenBand.HIGH and benefit_score < 0.3:
        penalty = 5.0
    return penalty

def attach_gate_burden_notes(gate: TournamentGateRequirementRecord) -> List[str]:
    notes = []
    if gate.burden_band in [GateBurdenBand.HIGH, GateBurdenBand.VERY_HIGH]:
        notes.append("High operational burden to verify this change.")
    if gate.canary_mandatory:
        notes.append("Must be deployed via canary release.")
    return notes
