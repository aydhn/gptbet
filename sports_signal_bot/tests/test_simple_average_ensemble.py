import numpy as np

from sports_signal_bot.ensemble.contracts import (EnsembleInputRecord,
                                                  StandardizedPredictionRecord)
from sports_signal_bot.ensemble.strategies.simple_average import \
    SimpleAverageEnsembler


def test_simple_average_combine():
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

    ensembler = SimpleAverageEnsembler()
    output = ensembler.combine(input_rec)

    assert output.status == "success"
    assert output.final_predicted_class == "1"
    assert np.isclose(output.final_probabilities["1"], 0.5)
    assert np.isclose(output.final_probabilities["X"], 0.25)
    assert np.isclose(output.final_probabilities["2"], 0.25)
    assert output.diagnostics.num_sources_used == 2
