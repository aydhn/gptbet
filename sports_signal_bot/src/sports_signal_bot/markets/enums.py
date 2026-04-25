from enum import Enum


class TargetType(str, Enum):
    MULTICLASS_CLASSIFICATION = "multiclass_classification"
    BINARY_CLASSIFICATION = "binary_classification"
    NUMERIC_REGRESSION = "numeric_regression"
    ORDINAL = "ordinal"


class LabelValidityStatus(str, Enum):
    VALID = "valid"
    VOID = "void"
    INVALID = "invalid"
    PENDING = "pending"
    UNSUPPORTED = "unsupported"


# Extending the core MarketType if it doesn't already have these.
# But we should rely on extending or keeping our own enums clean.
class ExtendedMarketType(str, Enum):
    # Football
    FOOTBALL_1X2 = "football_1x2"
    FOOTBALL_DOUBLE_CHANCE = "football_double_chance"
    FOOTBALL_DRAW_NO_BET = "football_draw_no_bet"
    FOOTBALL_OVER_UNDER = "football_over_under"
    FOOTBALL_BTTS = "football_btts"
    FOOTBALL_HOME_OVER_UNDER = "football_home_over_under"
    FOOTBALL_AWAY_OVER_UNDER = "football_away_over_under"
    FOOTBALL_ASIAN_HANDICAP = "football_asian_handicap"
    FOOTBALL_CORRECT_SCORE = "football_correct_score"

    # Basketball
    BASKETBALL_MATCH_WINNER = "basketball_match_winner"  # moneyline
    BASKETBALL_HANDICAP = "basketball_handicap"  # spread
    BASKETBALL_TOTAL_POINTS = "basketball_total_points"
    BASKETBALL_TEAM_TOTALS = "basketball_team_totals"
    BASKETBALL_QUARTER_HALF = "basketball_quarter_half"
