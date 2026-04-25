from sports_signal_bot.core.constants import MarketType


def normalize_market_name(name: str) -> MarketType:
    if not name:
        return MarketType.UNKNOWN

    name = name.strip().lower()

    if name in ["1x2", "match_odds", "match odds"]:
        return MarketType.MATCH_ODDS
    elif name in ["moneyline", "ml"]:
        return MarketType.MONEYLINE
    elif name in ["spread", "handicap", "ah"]:
        return MarketType.SPREAD
    elif name in ["totals", "over/under", "ou"]:
        return MarketType.TOTALS

    return MarketType.UNKNOWN


def safe_decimal_odds(odds_str: str) -> float:
    try:
        odds = float(odds_str)
        return odds
    except (ValueError, TypeError):
        return 0.0


def implied_prob_from_decimal_odds(odds: float) -> float:
    if odds <= 1.0:
        return 0.0
    return 1.0 / odds
