import pytest

from sports_signal_bot.ratings.draw_probability import calculate_1x2_probabilities


def test_draw_probability_heuristic_normalization():
    # Teams are exactly equal (0.5 vs 0.5 expected score)
    p_h, p_d, p_a = calculate_1x2_probabilities(0.5, 0.5, method="heuristic")

    assert p_d == 0.3  # Max draw probability
    assert p_h == 0.35  # (1 - 0.3) / 2
    assert p_a == 0.35
    assert round(p_h + p_d + p_a, 5) == 1.0


def test_draw_probability_heuristic_decay():
    # Home heavily favored
    p_h, p_d, p_a = calculate_1x2_probabilities(0.9, 0.1, method="heuristic")

    assert p_d < 0.1  # Draw prob drops significantly
    assert p_h > p_a
    assert round(p_h + p_d + p_a, 5) == 1.0


def test_draw_probability_none():
    p_h, p_d, p_a = calculate_1x2_probabilities(0.6, 0.4, method="none")
    assert p_d == 0.0
    assert p_h == 0.6
    assert p_a == 0.4
