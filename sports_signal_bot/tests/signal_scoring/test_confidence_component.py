import pytest
import math
from sports_signal_bot.signal_scoring.confidence import (
    compute_entropy, compute_top_class_gap, compute_probability_flatness,
    compute_probability_sharpness, compute_confidence_score
)

def test_compute_entropy():
    # Certain distribution
    assert compute_entropy({"a": 1.0, "b": 0.0}) == 0.0
    # Uniform distribution (2 classes)
    assert compute_entropy({"a": 0.5, "b": 0.5}) == 1.0

def test_compute_top_class_gap():
    assert compute_top_class_gap({"home": 0.6, "draw": 0.3, "away": 0.1}) == 0.3
    assert compute_top_class_gap({"home": 0.4, "draw": 0.4, "away": 0.2}) == 0.0

def test_flatness_and_sharpness():
    probs = {"a": 0.5, "b": 0.5}
    assert compute_probability_flatness(probs) == 1.0
    assert compute_probability_sharpness(probs) == 0.0

    probs = {"a": 1.0, "b": 0.0}
    assert compute_probability_flatness(probs) == 0.0
    assert compute_probability_sharpness(probs) == 1.0

def test_compute_confidence_score():
    score = compute_confidence_score(0.6, 0.3, 0.5, max_possible_entropy=1.585)
    assert round(score, 3) == 0.527
