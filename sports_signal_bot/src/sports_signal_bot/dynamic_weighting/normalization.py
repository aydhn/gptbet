from typing import List, Dict
import numpy as np

def apply_weight_caps_and_floors(
    weights: List[float],
    min_floor: float = 0.0,
    max_cap: float = 1.0
) -> List[float]:
    return [max(min_floor, min(max_cap, w)) for w in weights]

def normalize_weights(
    weights: List[float],
    temperature: float = 1.0,
    min_floor: float = 0.0,
    max_cap: float = 1.0
) -> List[float]:
    if not weights:
        return []

    sum_w = sum(weights)
    if sum_w == 0:
        # Fallback to equal weights if all zeros
        return [1.0 / len(weights)] * len(weights)

    # Apply temperature
    if temperature != 1.0 and temperature > 0:
        powered = [pow(w, 1.0/temperature) for w in weights]
        sum_powered = sum(powered)
        if sum_powered > 0:
            weights = [w / sum_powered for w in powered]

    # Normalize
    sum_w = sum(weights)
    normalized = [w / sum_w for w in weights]

    # Cap and floor
    bounded = apply_weight_caps_and_floors(normalized, min_floor, max_cap)

    # Re-normalize after cap/floor
    sum_bounded = sum(bounded)
    if sum_bounded > 0:
        return [w / sum_bounded for w in bounded]

    return [1.0 / len(weights)] * len(weights)

def explain_weighting_decision(source_name: str, final_weight: float, components: 'WeightComponentRecord') -> str:
    parts = []
    parts.append(f"{source_name}: Final={final_weight:.3f}")
    parts.append(f"Trust={components.trust_score:.2f}")
    if components.regime_fit_score > 0:
        parts.append(f"Regime={components.regime_fit_score:.2f}")
    if components.disagreement_penalty < 0:
        parts.append(f"Disag.={components.disagreement_penalty:.2f}")
    if components.recency_penalty < 0:
        parts.append(f"Stale={components.recency_penalty:.2f}")

    return " | ".join(parts)
