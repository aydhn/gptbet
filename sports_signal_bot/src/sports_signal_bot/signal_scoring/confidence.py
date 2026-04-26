import math
from typing import Dict, List, Optional


def compute_entropy(probabilities: Dict[str, float]) -> float:
    """Computes Shannon entropy for a probability distribution."""
    if not probabilities:
        return 0.0

    entropy = 0.0
    for prob in probabilities.values():
        if prob > 0:
            entropy -= prob * math.log2(prob)

    return entropy


def compute_top_class_gap(probabilities: Dict[str, float]) -> float:
    """Computes the difference between top class and second class probability."""
    if not probabilities or len(probabilities) < 2:
        return 0.0

    sorted_probs = sorted(probabilities.values(), reverse=True)
    return sorted_probs[0] - sorted_probs[1]


def compute_probability_flatness(probabilities: Dict[str, float]) -> float:
    """Measures how flat the distribution is relative to max entropy.
    1.0 means perfectly flat (equal probs), 0.0 means completely sharp (one class=1.0).
    """
    if not probabilities or len(probabilities) < 2:
        return 0.0

    n_classes = len(probabilities)
    max_entropy = math.log2(n_classes)

    if max_entropy == 0:
        return 0.0

    entropy = compute_entropy(probabilities)
    return entropy / max_entropy


def compute_probability_sharpness(probabilities: Dict[str, float]) -> float:
    """Inverse of flatness."""
    return 1.0 - compute_probability_flatness(probabilities)


def compute_confidence_score(
    max_probability: float,
    top_class_gap: float,
    entropy: float,
    max_possible_entropy: float = 1.585,  # e.g., for 3 classes
) -> float:
    """Computes a unified confidence score."""

    # Simple heuristic: heavily weight the final probability and the gap,
    # with a penalty for high entropy.

    sharpness = (
        1.0 - (entropy / max_possible_entropy) if max_possible_entropy > 0 else 0.0
    )
    sharpness = max(0.0, sharpness)

    # 50% from raw probability, 30% from the gap to the next best, 20% from overall sharpness
    score = (max_probability * 0.5) + (top_class_gap * 0.3) + (sharpness * 0.2)
    return score
