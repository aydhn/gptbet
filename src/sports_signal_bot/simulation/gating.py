from typing import List
from .contracts import SimulationRecommendationRecord, CandidatePatchRecord

def derive_required_quality_gates(patch: CandidatePatchRecord) -> List[str]:
    # Mock lookup
    gate_map = {
        "provider_priority": ["regression", "provider_smoke"],
        "threshold_band": ["policy_scenario", "bankroll_proxy"],
        "source_penalty": ["regression", "quality_proxy"]
    }
    return gate_map.get(patch.target_component_family, ["regression"])

def attach_gate_requirements_to_recommendation(rec: SimulationRecommendationRecord, gates: List[str]) -> SimulationRecommendationRecord:
    rec.required_gates.extend(gates)
    return rec
