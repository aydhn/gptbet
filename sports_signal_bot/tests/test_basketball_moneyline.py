import pytest

from sports_signal_bot.probabilistic.basketball.contracts import \
    BasketballDistributionConfig
from sports_signal_bot.probabilistic.basketball.distribution import \
    BasketballDistributionCore
from sports_signal_bot.probabilistic.basketball.markets import \
    BasketballMarketExtractor


def test_moneyline_probability_extraction():
    config = BasketballDistributionConfig()
    core = BasketballDistributionCore(config)
    extractor = BasketballMarketExtractor(core)

    # Exact pick'em
    ml = extractor.extract_moneyline(expected_margin_home=0.0, margin_std=10.0)
    assert ml["home_win"] == 0.5
    assert ml["away_win"] == 0.5

    # Home favored
    ml = extractor.extract_moneyline(expected_margin_home=5.0, margin_std=10.0)
    assert ml["home_win"] > 0.5
    assert ml["away_win"] < 0.5
    assert pytest.approx(ml["home_win"] + ml["away_win"]) == 1.0
