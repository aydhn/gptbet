import pytest
from sports_signal_bot.probabilistic.basketball.contracts import BasketballDistributionConfig
from sports_signal_bot.probabilistic.basketball.expected_points import ExpectedPointsBuilder

def test_expected_points_builder_baseline():
    config = BasketballDistributionConfig(base_total_points=220.0, home_advantage_points=4.0)
    builder = ExpectedPointsBuilder()

    # No extra features
    est = builder.build("test", {}, config)

    # Home gets (220/2) + (4/2) = 112
    # Away gets (220/2) - (4/2) = 108
    assert est.expected_home_points == 112.0
    assert est.expected_away_points == 108.0
    assert est.expected_total_points == 220.0
    assert est.expected_margin_home == 4.0

def test_expected_points_with_pace_and_rating():
    config = BasketballDistributionConfig(base_total_points=200.0, home_advantage_points=2.0)
    builder = ExpectedPointsBuilder()

    features = {
        "pace_adjustment": 10.0,  # Adds 5 to each
        "rating_diff": 6.0        # Adds 3 to home, subtracts 3 from away
    }

    est = builder.build("test", features, config)

    # Home: 100 + 1 + 5 + 3 = 109
    # Away: 100 - 1 + 5 - 3 = 101
    assert est.expected_home_points == 109.0
    assert est.expected_away_points == 101.0
    assert est.expected_total_points == 210.0
    assert est.expected_margin_home == 8.0

def test_expected_points_clipping():
    config = BasketballDistributionConfig(base_total_points=200.0, home_advantage_points=0.0)
    builder = ExpectedPointsBuilder()

    # Extreme away favorite
    features = {
        "rating_diff": -300.0
    }

    est = builder.build("test", features, config)

    # Home points should clip to 0
    assert est.expected_home_points == 0.0
    assert "Expected home points clipped" in est.warnings[0]
