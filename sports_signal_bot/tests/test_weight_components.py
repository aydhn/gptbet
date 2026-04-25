import pytest
from sports_signal_bot.dynamic_weighting.components import (
    compute_base_prior, compute_trust_weight_component,
    compute_regime_weight_component, compute_disagreement_component,
    compute_recency_component, combine_weight_components
)
from sports_signal_bot.dynamic_weighting.normalization import normalize_weights, apply_weight_caps_and_floors
from sports_signal_bot.dynamic_weighting.contracts import WeightingPolicyDefinition

def test_base_prior():
    config = {
        "football": {"ml_calibrated": 1.2},
        "default": {"benchmark": 1.0}
    }
    assert compute_base_prior("ml_calibrated", "football", config) == 1.2
    assert compute_base_prior("benchmark", "basketball", config) == 1.0

def test_trust_component():
    assert compute_trust_weight_component(0.8) == 0.8
    assert compute_trust_weight_component(0.8, damping=0.5) == 0.4

def test_regime_component():
    # Large sample size, damping effect is small
    val1 = compute_regime_weight_component(0.9, 100, damping_factor=10.0)
    assert val1 > 0.8
    # Small sample size, damping effect is large
    val2 = compute_regime_weight_component(0.9, 5, damping_factor=10.0)
    assert val2 < val1
    assert val2 == 0.0 # because (1.0 - 10/5) < 0

def test_disagreement_component():
    # Not enough peers -> 0
    assert compute_disagreement_component(0.9, [0.8, 0.9], min_peers=3) == 0.0
    # Mild disagreement -> 0
    assert compute_disagreement_component(0.5, [0.45, 0.55, 0.5], penalty_weight=1.0) == 0.0
    # High disagreement -> penalty
    penalty = compute_disagreement_component(0.9, [0.1, 0.2, 0.15], penalty_weight=1.0)
    assert penalty < 0.0

def test_recency_component():
    assert compute_recency_component(False) == 0.0
    assert compute_recency_component(True, penalty_weight=0.5) == -0.5

def test_combine_components():
    policy = WeightingPolicyDefinition(name="test", description="desc")
    comp = combine_weight_components(0.8, 0.5, -0.2, -0.1, 1.0, 1.0, 0.1, policy)
    assert comp.combined_score > 0
    assert comp.trust_score == 0.8
    assert comp.disagreement_penalty == -0.2

def test_normalize_weights():
    weights = [2.0, 1.0, 1.0]
    norm = normalize_weights(weights)
    assert norm == [0.5, 0.25, 0.25]

    # Floor test
    weights2 = [0.9, 0.05, 0.05]
    norm2 = normalize_weights(weights2, min_floor=0.1, max_cap=0.8)
    assert all(w >= 0.1 for w in norm2)
    assert all(w <= 0.8 for w in norm2)
    assert abs(sum(norm2) - 1.0) < 1e-6
