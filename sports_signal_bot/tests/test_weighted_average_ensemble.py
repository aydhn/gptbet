import numpy as np

from sports_signal_bot.ensemble.contracts import (EnsembleInputRecord,
                                                  StandardizedPredictionRecord)
from sports_signal_bot.ensemble.strategies.weighted_average import \
    WeightedAverageEnsembler


def test_weighted_average_combine():
    preds = [
        StandardizedPredictionRecord(
            event_id="e1",
            sport="football",
            market_type="1x2",
            source_family="f1",
            source_name="s1",
            class_labels=["1", "X", "2"],
            probabilities={"1": 0.4, "X": 0.3, "2": 0.3},
            predicted_class="1",
        ),
        StandardizedPredictionRecord(
            event_id="e1",
            sport="football",
            market_type="1x2",
            source_family="f2",
            source_name="s2",
            class_labels=["1", "X", "2"],
            probabilities={"1": 0.6, "X": 0.2, "2": 0.2},
            predicted_class="1",
        ),
    ]
    input_rec = EnsembleInputRecord(
        event_id="e1", sport="football", market_type="1x2", predictions=preds
    )

    config = {"weights": {"s1": 1.0, "s2": 3.0}}

    ensembler = WeightedAverageEnsembler(config=config)
    output = ensembler.combine(input_rec)

    assert output.status == "success"
    # s1 weight = 0.25, s2 weight = 0.75
    # prob 1 = 0.4*0.25 + 0.6*0.75 = 0.1 + 0.45 = 0.55
    assert np.isclose(output.final_probabilities["1"], 0.55)
    assert output.diagnostics.num_sources_used == 2
