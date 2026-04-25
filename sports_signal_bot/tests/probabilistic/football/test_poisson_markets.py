import numpy as np
import pytest

from sports_signal_bot.probabilistic.football import (GoalEnvironmentConfig,
                                                      GoalLambdaEstimate,
                                                      MarketExtractor,
                                                      PoissonScoreMatrix)


def setup_matrix(home_lambda: float, away_lambda: float) -> PoissonScoreMatrix:
    estimate = GoalLambdaEstimate(
        event_id="test",
        home_lambda=home_lambda,
        away_lambda=away_lambda,
        expected_total_goals=home_lambda + away_lambda,
        expected_goal_diff=home_lambda - away_lambda,
        model_name="test",
    )
    config = GoalEnvironmentConfig(max_goals_cutoff=10)
    return PoissonScoreMatrix(estimate, config)


def test_extract_1x2():
    # Strong home favorite
    matrix = setup_matrix(2.5, 0.5)
    probs = MarketExtractor.extract_1x2(matrix)

    assert probs["home_win"] > 0.7
    assert probs["away_win"] < 0.15
    assert np.isclose(sum(probs.values()), 1.0)


def test_extract_over_under():
    # Total goals = 3.0, Over 2.5 should be favored
    matrix = setup_matrix(2.0, 1.0)
    probs = MarketExtractor.extract_over_under(matrix, 2.5)

    assert probs["over"] > 0.5
    assert probs["under"] < 0.5
    assert np.isclose(probs["over"] + probs["under"], 1.0)


def test_extract_btts():
    # Both scoring high
    matrix = setup_matrix(2.0, 2.0)
    probs = MarketExtractor.extract_btts(matrix)

    # Prob that home scores > 0 is 1 - e^-2 = 0.86
    # Indep prob that both score > 0 is ~ 0.74
    assert probs["yes"] > 0.7
    assert np.isclose(probs["yes"] + probs["no"], 1.0)


def test_extract_expected_metrics():
    matrix = setup_matrix(1.5, 1.0)
    metrics = MarketExtractor.extract_expected_metrics(matrix)

    # Because of the 10 goal cutoff and re-normalization, the expected goals will be slightly shifted
    # but extremely close to the input lambdas
    assert np.isclose(metrics["expected_home_goals"], 1.5, atol=0.01)
    assert np.isclose(metrics["expected_away_goals"], 1.0, atol=0.01)
