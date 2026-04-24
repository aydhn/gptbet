from typing import Dict, List
import numpy as np

def normalize_source_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """Normalizes a dictionary of weights so they sum to 1.0."""
    total = sum(weights.values())
    if total <= 0:
        # Fallback to uniform if weights are invalid or sum to 0
        n = len(weights)
        if n == 0:
             return {}
        return {k: 1.0 / n for k in weights}

    return {k: v / total for k, v in weights.items()}

def derive_source_weight(validation_log_loss: float = None,
                         brier_score: float = None,
                         is_calibrated: bool = False,
                         min_weight: float = 0.01) -> float:
    """Derives a simple reliability weight."""
    weight = 1.0

    if validation_log_loss is not None:
         # simple inverse log loss, bounded to avoid div by zero
         weight = 1.0 / max(validation_log_loss, 0.01)
    elif brier_score is not None:
         weight = 1.0 / max(brier_score, 0.01)

    if is_calibrated:
         weight *= 1.2 # slight bump for calibrated sources

    return max(weight, min_weight)
