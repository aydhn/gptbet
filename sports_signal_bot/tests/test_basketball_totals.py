import pytest
from sports_signal_bot.probabilistic.basketball.contracts import BasketballDistributionConfig
from sports_signal_bot.probabilistic.basketball.distribution import BasketballDistributionCore
from sports_signal_bot.probabilistic.basketball.markets import BasketballMarketExtractor

def test_totals_over_under_complementarity():
    config = BasketballDistributionConfig()
    core = BasketballDistributionCore(config)
    extractor = BasketballMarketExtractor(core)

    # Expected total is 220
    totals = extractor.extract_totals(expected_total=220.0, total_std=10.0, lines=[220.0, 210.5, 230.5])

    # Exactly on line
    assert totals["total_220_0"]["over"] == 0.5
    assert totals["total_220_0"]["under"] == 0.5

    # Lower line -> over favored
    assert totals["total_210_5"]["over"] > 0.5
    assert totals["total_210_5"]["under"] < 0.5
    assert pytest.approx(totals["total_210_5"]["over"] + totals["total_210_5"]["under"]) == 1.0

    # Higher line -> under favored
    assert totals["total_230_5"]["under"] > 0.5
    assert totals["total_230_5"]["over"] < 0.5
    assert pytest.approx(totals["total_230_5"]["over"] + totals["total_230_5"]["under"]) == 1.0
