from sports_signal_bot.ensemble.contracts import StandardizedPredictionRecord, EnsembleInputRecord
from sports_signal_bot.ensemble.strategies.best_source_fallback import BestSourceFallbackEnsembler

def test_best_source_fallback():
    preds = [
        StandardizedPredictionRecord(
            event_id="e1", sport="football", market_type="1x2", source_family="f1", source_name="s1",
            class_labels=["1", "X", "2"], probabilities={"1": 0.4, "X": 0.3, "2": 0.3}, predicted_class="1"
        ),
        StandardizedPredictionRecord(
            event_id="e1", sport="football", market_type="1x2", source_family="f2", source_name="s2",
            class_labels=["1", "X", "2"], probabilities={"1": 0.6, "X": 0.2, "2": 0.2}, predicted_class="1"
        )
    ]
    input_rec = EnsembleInputRecord(event_id="e1", sport="football", market_type="1x2", predictions=preds)

    config = {
        "source_priority": ["s2", "s1"]
    }

    ensembler = BestSourceFallbackEnsembler(config=config)
    output = ensembler.combine(input_rec)

    assert output.status == "success"
    assert output.diagnostics.num_sources_used == 1
    assert output.component_sources[0].source_name == "s2"
    assert "s1" in output.diagnostics.excluded_sources
