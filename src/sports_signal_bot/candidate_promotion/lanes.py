from .contracts import CandidateLane, CandidateReleaseRecord
from ..simulation.contracts import RiskLevel

def assign_lane(candidate: CandidateReleaseRecord, gate_burden: str, simulation_confidence: str) -> CandidateLane:
    """
    Assigns a candidate lane based on risk, scope, simulation confidence, gate burden and support.
    FAST lane requires narrow scope, low/medium risk, strong support, clean simulation, and light gate burden.
    """
    is_narrow = len(candidate.scope) <= 1
    low_risk = candidate.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM]
    strong_support = candidate.support_strength >= 0.8
    clean_sim = simulation_confidence in ["high", "very_high"]
    light_gates = gate_burden in ["low", "none"]

    if is_narrow and low_risk and strong_support and clean_sim and light_gates:
        return CandidateLane.FAST_SAFE_CANDIDATE_LANE

    if candidate.risk_level == RiskLevel.CRITICAL or gate_burden == "high":
        return CandidateLane.HIGH_RISK_REVIEW_LANE

    return CandidateLane.STANDARD_CANDIDATE_LANE
