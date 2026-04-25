from enum import Enum


class SportType(str, Enum):
    FOOTBALL = "football"
    BASKETBALL = "basketball"


class LeagueType(str, Enum):
    PREMIER_LEAGUE = "premier_league"
    NBA = "nba"
    # Can be extended
    UNKNOWN = "unknown"


class MarketType(str, Enum):
    MONEYLINE = "moneyline"  # Typically for basketball 1/2
    MATCH_ODDS = "1X2"  # Typically for football 1/X/2
    SPREAD = "spread"
    TOTALS = "totals"
    UNKNOWN = "unknown"
