
from typing import Dict
from sports_signal_bot.reconciliation.contracts import SourceObservationRecord

def compute_source_trust_for_family(obs: SourceObservationRecord) -> float:
    base_trust = obs.provider_quality_score
    if obs.provider_health_status == "degraded":
        base_trust *= 0.8
    elif obs.provider_health_status == "down":
        base_trust *= 0.1
    return min(1.0, max(0.0, base_trust))

def adjust_trust_by_health(trust: float, health: str) -> float:
    return trust

def adjust_trust_by_freshness(trust: float, freshness_gap: float) -> float:
    return trust

def adjust_trust_by_dispute_history(trust: float, history_score: float) -> float:
    return trust

def explain_source_trust(obs: SourceObservationRecord) -> str:
    return "Calculated from quality and health"
