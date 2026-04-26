from typing import Dict, Any

def compute_source_health_penalty(
    source_selection_diagnostics: Dict[str, Any],
    thresholds: Dict[str, float]
) -> float:
    """Computes a penalty based on stale components and weak source dominance."""

    if not source_selection_diagnostics:
        return 0.0

    penalty = 0.0

    stale_ratio = source_selection_diagnostics.get("stale_components_ratio", 0.0)
    weak_trust_dominance = source_selection_diagnostics.get("weak_trust_dominance", False)
    fallback_heavy = source_selection_diagnostics.get("fallback_heavy_selection", False)

    # Stale components penalty
    high_stale = thresholds.get("high_stale_ratio", 0.2)

    if stale_ratio >= high_stale:
        penalty += 0.2

    if weak_trust_dominance:
        penalty += 0.15

    if fallback_heavy:
        penalty += 0.25

    return min(penalty, 1.0)
