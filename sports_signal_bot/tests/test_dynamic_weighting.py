import pytest

from sports_signal_bot.dynamic_weighting.components import combine_weight_components
from sports_signal_bot.dynamic_weighting.contracts import WeightingPolicyDefinition
from sports_signal_bot.dynamic_weighting.runner import DynamicWeightingRunner
from sports_signal_bot.dynamic_weighting.strategies.dynamic_hybrid import (
    DynamicHybridWeighted,
)
from sports_signal_bot.dynamic_weighting.strategies.trust_weighted import TrustWeighted


def test_trust_weighted_strategy():
    policy = WeightingPolicyDefinition(name="test", description="desc")
    strategy = TrustWeighted(policy, {})

    sources = [
        {"name": "a", "family": "f1", "trust_score": 0.8},
        {"name": "b", "family": "f2", "trust_score": 0.2},
    ]
    context = {"event_id": "1", "sport": "s", "market_type": "m"}

    weights = strategy.compute_weights(sources, context)

    assert len(weights) == 2
    assert weights[0].final_weight > weights[1].final_weight
    assert weights[0].source_name == "a"


def test_dynamic_hybrid_strategy():
    policy = WeightingPolicyDefinition(
        name="test", description="desc", min_weight_floor=0.1, max_weight_cap=0.9
    )
    strategy = DynamicHybridWeighted(policy, {"family_priors": {"default": {}}})

    sources = [
        {
            "name": "a",
            "family": "f1",
            "trust_score": 0.9,
            "regime_fit": 0.9,
            "regime_sample_size": 100,
            "is_calibrated": True,
        },
        {
            "name": "b",
            "family": "f2",
            "trust_score": 0.5,
            "regime_fit": 0.5,
            "regime_sample_size": 20,
            "is_stale": True,
        },
    ]
    context = {"event_id": "1", "sport": "s", "market_type": "m"}

    weights = strategy.compute_weights(sources, context)

    assert len(weights) == 2
    assert weights[0].final_weight > weights[1].final_weight
    assert weights[1].component_scores.recency_penalty < 0  # Stale penalty applied


def test_runner_fallback():
    runner = DynamicWeightingRunner(
        "dynamic_hybrid", {"name": "p", "description": "d"}, {}
    )

    # Only one source
    sources = [{"name": "single", "family": "f", "trust_score": 0.9}]
    context = {"event_id": "1"}

    weights, diagnostics = runner.run(sources, context)

    assert len(weights) == 1
    assert weights[0].final_weight == 1.0
    assert diagnostics.fallback_used == True
