import pytest

from sports_signal_bot.probabilistic.football import (GoalEnvironmentConfig,
                                                      GoalLambdaBuilder,
                                                      LambdaBuildContext)


def test_lambda_builder_basic():
    ctx = LambdaBuildContext(event_id="test1", run_id="r1")
    builder = GoalLambdaBuilder()

    # Even strength, standard baseline
    features = {
        "league_total_goal_baseline": 2.5,
        "home_rating_proxy": 1500.0,
        "away_rating_proxy": 1500.0,
        "home_advantage": 0.2,
    }

    estimate = builder.build(ctx, features)

    # Base share is 0.5. Base team exp is 1.25.
    # Home raw = 1.25 * 1.0 + 0.2 = 1.45
    # Away raw = 1.25 * 1.0 = 1.25
    assert estimate.home_lambda == 1.45
    assert estimate.away_lambda == 1.25
    assert len(estimate.warnings) == 0


def test_lambda_builder_clipping():
    # Test min limit
    config = GoalEnvironmentConfig(lambda_min=0.5)
    ctx = LambdaBuildContext(event_id="test1", run_id="r1", config=config)
    builder = GoalLambdaBuilder()

    # Insanely weak team
    features = {
        "league_total_goal_baseline": 2.5,
        "home_rating_proxy": 500.0,
        "away_rating_proxy": 3000.0,
        "home_advantage": 0.0,
    }

    estimate = builder.build(ctx, features)

    # Should clip to minimum
    assert estimate.home_lambda == 0.5
    assert any("clipped" in w for w in estimate.warnings)


def test_lambda_builder_leakage_guard():
    ctx = LambdaBuildContext(event_id="test1", run_id="r1")
    builder = GoalLambdaBuilder()

    features = {
        "league_total_goal_baseline": 2.5,
        "home_rating_proxy": 1500.0,
        "away_rating_proxy": 1500.0,
        "final_home_score": 2.0,  # LEAKAGE!
    }

    estimate = builder.build(ctx, features)

    # Estimate should still run, but with a severe warning
    assert len(estimate.warnings) > 0
    assert any("LEAKAGE" in w for w in estimate.warnings)
