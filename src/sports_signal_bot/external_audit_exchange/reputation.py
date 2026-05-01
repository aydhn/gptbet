from typing import Dict, List
from .contracts import WitnessReputationRecord, ReputationSignalRecord, ReputationAdjustmentRecord
import datetime
import uuid

def collect_reputation_signals(witness_id: str) -> List[ReputationSignalRecord]:
    return []

def compute_witness_reputation(witness_id: str, signals: List[ReputationSignalRecord]) -> WitnessReputationRecord:
    score = 50.0
    for signal in signals:
        score += signal.value

    score = max(0.0, min(100.0, score))

    band = "adequate"
    if score > 80:
        band = "excellent"
    elif score > 60:
        band = "strong"
    elif score < 30:
        band = "low_trust"

    return WitnessReputationRecord(
        witness_id=witness_id,
        reputation_score=score,
        reputation_band=band,
        freshness="fresh"
    )

def apply_reputation_adjustments(reputation: WitnessReputationRecord, adjustments: List[ReputationAdjustmentRecord]) -> WitnessReputationRecord:
    score = reputation.reputation_score
    for adj in adjustments:
        score += adj.score_delta

    score = max(0.0, min(100.0, score))

    band = "adequate"
    if score > 80:
        band = "excellent"
    elif score > 60:
        band = "strong"
    elif score < 30:
        band = "low_trust"

    reputation.reputation_score = score
    reputation.reputation_band = band
    reputation.last_updated_at = datetime.datetime.utcnow()
    return reputation

def explain_reputation_score(reputation: WitnessReputationRecord) -> str:
    return f"Witness {reputation.witness_id} has score {reputation.reputation_score} ({reputation.reputation_band})"

def detect_reputation_instability(reputation: WitnessReputationRecord) -> bool:
    return len(reputation.downgrade_flags) > 3
