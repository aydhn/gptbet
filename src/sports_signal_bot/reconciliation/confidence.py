
from typing import List
from sports_signal_bot.reconciliation.contracts import FieldConflictRecord

def compute_field_confidence(conflicts: List[FieldConflictRecord]) -> float:
    if not conflicts:
        return 1.0

    severity_weights = {"low": 0.1, "medium": 0.3, "high": 0.6, "critical": 0.9}
    penalty = sum(severity_weights.get(c.severity, 0.5) for c in conflicts)

    return max(0.0, 1.0 - penalty)

def compute_group_confidence(field_confidences: List[float]) -> float:
    if not field_confidences: return 1.0
    return sum(field_confidences) / len(field_confidences)

def classify_confidence_band(score: float, has_dispute: bool = False) -> str:
    if has_dispute: return "disputed"
    if score >= 0.8: return "high_confidence"
    if score >= 0.5: return "medium_confidence"
    return "low_confidence"

def explain_confidence_score(score: float) -> str:
    return f"Score {score:.2f} based on conflict penalties"
