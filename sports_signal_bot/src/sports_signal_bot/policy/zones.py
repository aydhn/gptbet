from typing import Any, Dict


def determine_band(
    value: float, bands_config: Dict[str, float], reverse: bool = False
) -> str:
    """Determine the band a value falls into based on config."""
    if not bands_config:
        return "unknown"

    sorted_bands = sorted(bands_config.items(), key=lambda x: x[1], reverse=reverse)

    if not reverse:
        # e.g., low: 0.1, medium: 0.3, high: 0.5 (for scores where higher is better)
        # However, for score_bands in config, it's rejected: 0.2, no_bet: 0.4...
        for name, threshold in sorted_bands:
            if value < threshold:
                return name
        return sorted_bands[-1][0] if sorted_bands else "unknown"
    else:
        # e.g., for uncertainty where lower is better
        for name, threshold in sorted_bands:
            if value > threshold:
                return name
        return sorted_bands[-1][0] if sorted_bands else "unknown"


def get_score_band(score: float, config: Dict[str, Any]) -> str:
    bands = config.get("score_bands", {})
    if not bands:
        return "unknown"

    if score < bands.get("rejected", 0.2):
        return "rejected"
    if score < bands.get("no_bet", 0.4):
        return "no_bet"
    if score < bands.get("watchlist", 0.6):
        return "watchlist"
    if score < bands.get("candidate", 0.8):
        return "candidate"
    return "approved"


def get_edge_band(edge: float, config: Dict[str, Any]) -> str:
    bands = config.get("edge_bands", {})
    if not bands:
        return "unknown"

    if edge < bands.get("low", 0.01):
        return "none"
    if edge < bands.get("medium", 0.03):
        return "low"
    if edge < bands.get("high", 0.05):
        return "medium"
    return "high"
