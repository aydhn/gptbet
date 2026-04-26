from typing import Any, Dict, List


def compute_regime_adjustment(
    regime_assignments: List[Dict[str, Any]], policies: Dict[str, Any]
) -> float:
    """Computes an adjustment based on assigned regimes."""

    if not regime_assignments:
        return 0.0

    adjustment = 0.0

    # We look through the regimes and apply policy-defined boosts/penalties
    for assignment in regime_assignments:
        family = assignment.get("regime_family")
        label = assignment.get("regime_label")

        if not family or not label:
            continue

        family_policies = policies.get(family, {})
        label_adjustment = family_policies.get(label, 0.0)

        adjustment += label_adjustment

    # Bound the adjustment so regime doesn't completely dominate the score
    max_boost = policies.get("max_boost", 0.2)
    max_penalty = policies.get("max_penalty", -0.3)

    return max(min(adjustment, max_boost), max_penalty)
