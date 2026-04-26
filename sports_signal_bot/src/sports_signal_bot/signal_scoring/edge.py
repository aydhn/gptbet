from typing import Dict, Optional, Tuple


def extract_market_implied_for_selection(
    selection: str, market_implied_probabilities: Dict[str, float]
) -> Optional[float]:
    """Extracts implied probability for a specific selection safely."""
    return market_implied_probabilities.get(selection)


def compute_edge(
    final_probability: float, market_implied_probability: Optional[float]
) -> float:
    """Computes edge if market probability is available."""
    if market_implied_probability is None or market_implied_probability <= 0:
        return 0.0
    return final_probability - market_implied_probability


def compute_fair_odds(probability: float) -> Optional[float]:
    """Computes fair odds from probability."""
    if probability <= 0.0:
        return None
    return 1.0 / probability


def normalize_market_probabilities(market_probs: Dict[str, float]) -> Dict[str, float]:
    """Normalizes market probabilities to remove overround."""
    total = sum(market_probs.values())
    if total <= 0:
        return market_probs

    return {k: v / total for k, v in market_probs.items()}
