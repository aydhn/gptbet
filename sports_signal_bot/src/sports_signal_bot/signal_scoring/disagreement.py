from typing import Any, Dict


def compute_disagreement_penalty(
    source_disagreement_diagnostics: Dict[str, Any],
    disagreement_thresholds: Dict[str, float],
) -> float:
    """Computes a penalty derived from source disagreement."""

    if not source_disagreement_diagnostics:
        return 0.0

    source_variance = source_disagreement_diagnostics.get("source_variance", 0.0)
    top_class_disagreement = source_disagreement_diagnostics.get(
        "top_class_disagreement", False
    )

    penalty = 0.0

    # Variance penalty
    high_variance = disagreement_thresholds.get("high_variance", 0.05)
    medium_variance = disagreement_thresholds.get("medium_variance", 0.02)

    if source_variance >= high_variance:
        penalty += 0.25
    elif source_variance >= medium_variance:
        penalty += 0.1

    # Top class disagreement penalty
    if top_class_disagreement:
        penalty += 0.15

    return min(penalty, 1.0)
