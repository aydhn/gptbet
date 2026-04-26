from typing import Dict, Any


def compute_data_quality_penalty(
    data_quality_summaries: Dict[str, Any],
    thresholds: Dict[str, float]
) -> float:
    """Computes a penalty based on missing features and sparse history."""

    if not data_quality_summaries:
        return 0.0

    penalty = 0.0

    missing_ratio = data_quality_summaries.get("missing_feature_ratio", 0.0)
    sparse_history = data_quality_summaries.get("sparse_history", False)
    alias_uncertainty = data_quality_summaries.get("alias_uncertainty", False)

    # Missing feature ratio penalty
    high_missing = thresholds.get("high_missing_ratio", 0.2)
    medium_missing = thresholds.get("medium_missing_ratio", 0.1)

    if missing_ratio >= high_missing:
        penalty += 0.3
    elif missing_ratio >= medium_missing:
        penalty += 0.1

    # Boolean penalties
    if sparse_history:
        penalty += 0.2

    if alias_uncertainty:
        penalty += 0.1

    return min(penalty, 1.0)
