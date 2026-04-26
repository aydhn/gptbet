import math
from typing import Optional, Tuple


def validate_decimal_odds(odds: Optional[float]) -> bool:
    if odds is None:
        return False
    if math.isnan(odds) or math.isinf(odds):
        return False
    if odds <= 1.0:
        return False
    return True


def fallback_missing_selection_odds(
    market_odds_dict: dict, selected_side: str
) -> Optional[float]:
    """Attempts to find a proxy or fallback if the selected side's odds are missing."""
    if not market_odds_dict:
        return None

    # If other sides have odds, we might be able to imply it (very rough proxy, usually skip is better)
    # For now, just return None.
    return None


def resolve_decision_odds(
    market_odds_dict: dict,
    selected_side: str,
    implied_odds: Optional[float] = None,
    missing_policy: str = "skip",
) -> Tuple[Optional[float], str]:
    """
    Resolves the decimal odds for the given decision.
    Returns (decimal_odds, warning_message).
    """
    if market_odds_dict and selected_side in market_odds_dict:
        odds = market_odds_dict[selected_side]
        if validate_decimal_odds(odds):
            return odds, ""

    # Try fallback to implied_odds if available
    if implied_odds is not None and implied_odds > 0:
        odds = 1.0 / implied_odds
        if validate_decimal_odds(odds):
            return odds, "Using implied probability as proxy for missing odds"

    # Fallback policy
    if missing_policy == "fallback":
        fallback_odds = fallback_missing_selection_odds(market_odds_dict, selected_side)
        if validate_decimal_odds(fallback_odds):
            return fallback_odds, "Used fallback proxy for missing odds"

    return None, "Missing valid decimal odds"


def map_selection_to_odds(
    event_data: dict, market_type: str, selected_side: str
) -> Optional[float]:
    """Map a selection to decimal odds from the raw event data if possible."""
    # Placeholder for actual odds mapping logic from event data
    # In a real system, this would extract from the canonical schema
    return None
