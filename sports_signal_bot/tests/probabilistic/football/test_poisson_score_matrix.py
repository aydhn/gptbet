import pytest
import numpy as np
from sports_signal_bot.probabilistic.football import (
    GoalLambdaEstimate, GoalEnvironmentConfig, PoissonScoreMatrix
)

def test_score_matrix_generation_and_normalization():
    estimate = GoalLambdaEstimate(
        event_id="test1", home_lambda=1.5, away_lambda=1.0,
        expected_total_goals=2.5, expected_goal_diff=0.5, model_name="test"
    )
    config = GoalEnvironmentConfig(max_goals_cutoff=10, renormalize_truncated_mass=True)

    matrix = PoissonScoreMatrix(estimate, config)

    # 1. The matrix should be sum to 1.0 (or very close)
    assert np.isclose(np.sum(matrix.matrix), 1.0)

    # 2. Extract probability of 0-0 manually and compare
    # P(0-0) = e^-1.5 * e^-1.0 = e^-2.5
    expected_0_0 = np.exp(-2.5)

    # Because of renormalization, it will be slightly higher, but very close since cutoff is 10
    actual_0_0 = matrix.get_probability(0, 0)
    assert np.isclose(actual_0_0, expected_0_0, atol=1e-3)

    # 3. Truncated mass should be tracked
    assert matrix.record.truncated_mass > 0.0
    assert matrix.record.truncated_mass < 0.01 # Should be tiny for cutoff 10 and lambdas < 2

def test_score_matrix_high_cutoff_warning():
    estimate = GoalLambdaEstimate(
        event_id="test2", home_lambda=8.0, away_lambda=7.0, # Huge lambdas
        expected_total_goals=15.0, expected_goal_diff=1.0, model_name="test"
    )
    config = GoalEnvironmentConfig(max_goals_cutoff=5) # Unreasonably low cutoff

    matrix = PoissonScoreMatrix(estimate, config)

    # Should have a warning about truncated mass
    assert len(matrix.record.warnings) > 0
    assert any("truncated mass warning" in w for w in matrix.record.warnings)
