import pytest

from sports_signal_bot.probabilistic.football import (CorrectScoreExtractor,
                                                      GoalEnvironmentConfig,
                                                      GoalLambdaEstimate,
                                                      PoissonScoreMatrix)


def test_correct_score_top_k():
    estimate = GoalLambdaEstimate(
        event_id="test",
        home_lambda=1.2,
        away_lambda=0.8,
        expected_total_goals=2.0,
        expected_goal_diff=0.4,
        model_name="test",
    )
    config = GoalEnvironmentConfig(max_goals_cutoff=10)
    matrix = PoissonScoreMatrix(estimate, config)

    # 1.2 and 0.8 mean 1-1 and 1-0 should be highly probable
    top_scores = CorrectScoreExtractor.get_top_k(matrix, k=3)

    assert len(top_scores) == 3

    # Assert sorted by probability descending
    assert top_scores[0].probability >= top_scores[1].probability
    assert top_scores[1].probability >= top_scores[2].probability

    # Check that probabilities are valid
    for cs in top_scores:
        assert 0.0 <= cs.probability <= 1.0
