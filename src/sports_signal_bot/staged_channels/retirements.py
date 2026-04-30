from typing import List
from sports_signal_bot.staged_channels.contracts import RolloutDecisionType, RolloutDecisionRecord

def detect_retirement_conditions(metrics: dict) -> bool:
    # simple mock: retire if 'error_rate' > 0.5
    return metrics.get("error_rate", 0.0) > 0.5

def summarize_retirement_reason(candidate_id: str, metrics: dict) -> str:
    if detect_retirement_conditions(metrics):
        return f"Candidate {candidate_id} retired due to high error rate."
    return ""
