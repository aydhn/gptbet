from sports_signal_bot.signal_scoring.data_quality import \
    compute_data_quality_penalty
from sports_signal_bot.signal_scoring.disagreement import \
    compute_disagreement_penalty
from sports_signal_bot.signal_scoring.source_health import \
    compute_source_health_penalty
from sports_signal_bot.signal_scoring.uncertainty import \
    compute_uncertainty_penalty


def test_uncertainty_penalty():
    thresholds = {"high": 1.5, "critical": 1.8}
    assert compute_uncertainty_penalty(1.0, thresholds) == 0.0
    assert compute_uncertainty_penalty(1.6, thresholds) == 0.15
    assert compute_uncertainty_penalty(1.9, thresholds) == 0.3
    assert (
        compute_uncertainty_penalty(1.6, thresholds, flat_probability_vector=True)
        == 0.25
    )
    assert (
        compute_uncertainty_penalty(1.6, thresholds, unstable_source_set=True) == 0.35
    )


def test_disagreement_penalty():
    thresholds = {"high_variance": 0.05, "medium_variance": 0.02}
    assert compute_disagreement_penalty({"source_variance": 0.01}, thresholds) == 0.0
    assert compute_disagreement_penalty({"source_variance": 0.03}, thresholds) == 0.1
    assert compute_disagreement_penalty({"source_variance": 0.06}, thresholds) == 0.25
    assert (
        compute_disagreement_penalty(
            {"source_variance": 0.06, "top_class_disagreement": True}, thresholds
        )
        == 0.4
    )


def test_data_quality_penalty():
    thresholds = {"high_missing_ratio": 0.2, "medium_missing_ratio": 0.1}
    assert (
        compute_data_quality_penalty({"missing_feature_ratio": 0.05}, thresholds) == 0.0
    )
    assert (
        compute_data_quality_penalty({"missing_feature_ratio": 0.15}, thresholds) == 0.1
    )
    assert (
        compute_data_quality_penalty({"missing_feature_ratio": 0.25}, thresholds) == 0.3
    )
    assert (
        compute_data_quality_penalty(
            {"missing_feature_ratio": 0.25, "sparse_history": True}, thresholds
        )
        == 0.5
    )


def test_source_health_penalty():
    thresholds = {"high_stale_ratio": 0.2}
    assert (
        compute_source_health_penalty({"stale_components_ratio": 0.1}, thresholds)
        == 0.0
    )
    assert (
        compute_source_health_penalty({"stale_components_ratio": 0.25}, thresholds)
        == 0.2
    )
    assert (
        compute_source_health_penalty(
            {"stale_components_ratio": 0.25, "weak_trust_dominance": True}, thresholds
        )
        == 0.35
    )
