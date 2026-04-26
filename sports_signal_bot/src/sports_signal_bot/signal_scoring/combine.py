from typing import Dict, Any, Optional

from .contracts import SignalComponentRecord

def combine_signal_components(
    components: SignalComponentRecord,
    weights: Dict[str, float]
) -> float:
    """Combine signal components into a single raw score."""

    score = 0.0

    # Positive components
    score += components.edge_estimate * weights.get("edge_weight", 1.0)
    score += components.confidence_score * weights.get("confidence_weight", 1.0)

    # Penalties
    score -= components.uncertainty_penalty * weights.get("uncertainty_penalty_weight", 1.0)
    score -= components.disagreement_penalty * weights.get("disagreement_penalty_weight", 1.0)
    score -= components.data_quality_penalty * weights.get("data_quality_penalty_weight", 1.0)
    score -= components.source_health_penalty * weights.get("source_health_penalty_weight", 1.0)

    # Regime adjustment
    score += components.regime_adjustment * weights.get("regime_adjustment_weight", 1.0)

    return score

def normalize_signal_score(
    raw_score: float,
    mode: str = "0_to_100",
    min_expected: float = -2.0,
    max_expected: float = 3.0
) -> float:
    """Normalize the raw signal score to a standard range."""

    # Clamp the raw score
    clamped = max(min(raw_score, max_expected), min_expected)

    # Normalize to 0-1
    normalized = (clamped - min_expected) / (max_expected - min_expected)

    if mode == "0_to_100":
        return normalized * 100.0
    elif mode == "0_to_1":
        return normalized

    return raw_score
