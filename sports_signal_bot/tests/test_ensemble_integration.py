import pytest

from sports_signal_bot.ensemble.contracts import (
    EnsembleInputRecord,
    StandardizedPredictionRecord,
)
from sports_signal_bot.ensemble.runner import EnsembleRunner


def test_dynamic_weighted_average_ensembler():
    config = {
        "strategy": "dynamic_weighted_average",
        "strategy_config": {"dynamic_weights": {"s1": 0.8, "s2": 0.2}},
    }

    runner = EnsembleRunner(config)

    # We simulate that the dynamic weighting runner attached metadata weights
    pred1 = StandardizedPredictionRecord(
        event_id="e1",
        sport="s",
        market_type="m",
        source_name="s1",
        source_family="f1",
        class_labels=["A", "B"],
        probabilities={"A": 0.9, "B": 0.1},
        predicted_class="A",
        metadata={"dynamic_weight": 0.7},
    )

    pred2 = StandardizedPredictionRecord(
        event_id="e1",
        sport="s",
        market_type="m",
        source_name="s2",
        source_family="f2",
        class_labels=["A", "B"],
        probabilities={"A": 0.2, "B": 0.8},
        predicted_class="B",
        metadata={"dynamic_weight": 0.3},
    )

    input_rec = EnsembleInputRecord(
        event_id="e1", sport="s", market_type="m", predictions=[pred1, pred2]
    )

    res = runner.run([input_rec])

    assert res["status"] == "success"
    outputs = res["outputs"]
    assert len(outputs) == 1
    out = outputs[0]

    # Check probabilities: (0.9*0.7 + 0.2*0.3) for A = 0.63 + 0.06 = 0.69
    assert abs(out.final_probabilities["A"] - 0.69) < 1e-5
    assert out.final_predicted_class == "A"


def test_dynamic_weighted_fallback_to_config():
    config = {
        "strategy": "dynamic_weighted_average",
        "strategy_config": {"dynamic_weights": {"s1": 0.9, "s2": 0.1}},
    }

    runner = EnsembleRunner(config)

    pred1 = StandardizedPredictionRecord(
        event_id="e1",
        sport="s",
        market_type="m",
        source_name="s1",
        source_family="f1",
        class_labels=["A", "B"],
        probabilities={"A": 1.0, "B": 0.0},
        predicted_class="A",
    )

    pred2 = StandardizedPredictionRecord(
        event_id="e1",
        sport="s",
        market_type="m",
        source_name="s2",
        source_family="f2",
        class_labels=["A", "B"],
        probabilities={"A": 0.0, "B": 1.0},
        predicted_class="B",
    )

    input_rec = EnsembleInputRecord(
        event_id="e1", sport="s", market_type="m", predictions=[pred1, pred2]
    )

    res = runner.run([input_rec])
    outputs = res["outputs"]
    out = outputs[0]

    # Weights should fall back to 0.9 and 0.1
    assert abs(out.final_probabilities["A"] - 0.9) < 1e-5
    assert out.final_predicted_class == "A"
