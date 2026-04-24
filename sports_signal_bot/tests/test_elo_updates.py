import pytest
from sports_signal_bot.ratings.elo import EloRatingEngine
from sports_signal_bot.ratings.contracts import RatingConfig

def test_elo_basic_expected_outcome():
    config = RatingConfig(k_factor=20.0, home_advantage=0.0)
    engine = EloRatingEngine(config)

    # Equal ratings
    exp_h, exp_a = engine.calculate_expected_outcome(1500.0, 1500.0)
    assert exp_h == 0.5
    assert exp_a == 0.5

    # Home has huge advantage
    exp_h, exp_a = engine.calculate_expected_outcome(1900.0, 1500.0)
    assert exp_h > 0.9
    assert exp_a < 0.1

def test_elo_basic_updates():
    config = RatingConfig(k_factor=20.0, home_advantage=0.0)
    engine = EloRatingEngine(config)

    # Home wins
    h_delta, a_delta = engine.calculate_rating_updates(1500.0, 1500.0, 2.0, 1.0)
    assert h_delta == 10.0 # 20 * (1 - 0.5)
    assert a_delta == -10.0

    # Draw
    h_delta, a_delta = engine.calculate_rating_updates(1500.0, 1500.0, 1.0, 1.0)
    assert h_delta == 0.0 # 20 * (0.5 - 0.5)
    assert a_delta == 0.0

    # Away wins
    h_delta, a_delta = engine.calculate_rating_updates(1500.0, 1500.0, 0.0, 2.0)
    assert h_delta == -10.0
    assert a_delta == 10.0

def test_elo_home_advantage():
    config = RatingConfig(k_factor=20.0, home_advantage=100.0)
    engine = EloRatingEngine(config)

    exp_h, exp_a = engine.calculate_expected_outcome(1500.0, 1500.0)
    assert exp_h > 0.5 # Home should be favored because of 100pt advantage

    exp_h_neutral, exp_a_neutral = engine.calculate_expected_outcome(1500.0, 1500.0, is_neutral=True)
    assert exp_h_neutral == 0.5 # Neutral cancels advantage

def test_elo_draw_update():
    # In a game where home is much stronger, a draw penalizes home
    config = RatingConfig(k_factor=20.0, home_advantage=0.0)
    engine = EloRatingEngine(config)

    h_delta, a_delta = engine.calculate_rating_updates(1900.0, 1500.0, 1.0, 1.0)
    assert h_delta < 0.0
    assert a_delta > 0.0
