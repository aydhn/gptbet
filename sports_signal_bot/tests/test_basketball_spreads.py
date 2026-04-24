import pytest
from sports_signal_bot.probabilistic.basketball.contracts import BasketballDistributionConfig
from sports_signal_bot.probabilistic.basketball.distribution import BasketballDistributionCore
from sports_signal_bot.probabilistic.basketball.markets import BasketballMarketExtractor

def test_spread_probability_direction():
    config = BasketballDistributionConfig()
    core = BasketballDistributionCore(config)
    extractor = BasketballMarketExtractor(core)

    # Expected margin = 5.0 (Home favored by 5)
    # Line = -5.0 (Pick'em against spread)
    spreads = extractor.extract_spreads(expected_margin_home=5.0, margin_std=10.0, lines=[-5.0])

    assert spreads["spread_m5_0"]["home_cover"] == 0.5
    assert spreads["spread_m5_0"]["away_cover"] == 0.5

    # Line = -3.5 (Home expected to win by more, so should cover often)
    spreads = extractor.extract_spreads(expected_margin_home=5.0, margin_std=10.0, lines=[-3.5])
    assert spreads["spread_m3_5"]["home_cover"] > 0.5
    assert spreads["spread_m3_5"]["away_cover"] < 0.5

    # Line = +3.5 (Home favored heavily, away getting points)
    spreads = extractor.extract_spreads(expected_margin_home=-5.0, margin_std=10.0, lines=[3.5])
    # Expected margin is -5 (Away favored by 5). Line gives Home +3.5. Away easily covers.
    assert spreads["spread_3_5"]["away_cover"] > 0.5
    assert spreads["spread_3_5"]["home_cover"] < 0.5
