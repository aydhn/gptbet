from pathlib import Path

import pytest

from sports_signal_bot.core.constants import MarketType
from sports_signal_bot.data.normalization.markets import (
    implied_prob_from_decimal_odds, normalize_market_name, safe_decimal_odds)
from sports_signal_bot.data.normalization.names import (normalize_league_name,
                                                        normalize_team_name)
from sports_signal_bot.data.resolution.team_aliases import TeamResolver


def test_normalize_team_name():
    assert normalize_team_name(" Man Utd. ") == "Man Utd"
    assert normalize_team_name("L.A. Lakers") == "LA Lakers"


def test_normalize_league_name():
    assert normalize_league_name("Premier League") == "premier_league"
    assert normalize_league_name(" NBA ") == "nba"


def test_normalize_market_name():
    assert normalize_market_name("1X2") == MarketType.MATCH_ODDS
    assert normalize_market_name("moneyline") == MarketType.MONEYLINE
    assert normalize_market_name("spread") == MarketType.SPREAD
    assert normalize_market_name("unknown_market") == MarketType.UNKNOWN


def test_safe_decimal_odds():
    assert safe_decimal_odds("2.5") == 2.5
    assert safe_decimal_odds("invalid") == 0.0


def test_implied_prob_from_decimal_odds():
    assert implied_prob_from_decimal_odds(2.0) == 0.5
    assert implied_prob_from_decimal_odds(0.5) == 0.0


def test_team_resolver(tmp_path):
    import yaml

    alias_file = tmp_path / "aliases.yaml"
    aliases = {
        "football": {"premier_league": {"Manchester United": ["Man Utd", "Man United"]}}
    }
    with open(alias_file, "w") as f:
        yaml.dump(aliases, f)

    resolver = TeamResolver(alias_file)
    assert (
        resolver.resolve_team_name("Man Utd", "football", "premier_league")
        == "Manchester United"
    )
    assert (
        resolver.resolve_team_name("Unknown Team", "football", "premier_league")
        == "Unknown Team"
    )
