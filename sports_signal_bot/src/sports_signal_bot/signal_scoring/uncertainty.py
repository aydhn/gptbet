from typing import Dict, Any, List

def compute_uncertainty_penalty(
    entropy: float,
    entropy_thresholds: Dict[str, float],
    unstable_source_set: bool = False,
    flat_probability_vector: bool = False
) -> float:
    """Computes penalty based on entropy thresholds and instability flags."""
    penalty = 0.0

    # 1. High entropy penalty
    high_threshold = entropy_thresholds.get("high", 1.5)
    critical_threshold = entropy_thresholds.get("critical", 1.8)

    if entropy >= critical_threshold:
        penalty += 0.3
    elif entropy >= high_threshold:
        penalty += 0.15

    # 2. Flatness penalty
    if flat_probability_vector:
        penalty += 0.1

    # 3. Unstable sources
    if unstable_source_set:
        penalty += 0.2

    return min(penalty, 1.0) # Cap at 1.0
