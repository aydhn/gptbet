from sports_signal_bot.ensemble.contracts import (
    EnsembleInputRecord,
    StandardizedPredictionRecord,
)
from sports_signal_bot.ensemble.strategies.rule_based_hybrid import (
    RuleBasedHybridEnsembler,
)


def test_rule_based_hybrid():
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
        )
    ]
    input_rec = EnsembleInputRecord(
        event_id="e1", sport="football", market_type="1x2", predictions=preds
    )

    config = {
        "rules": {"football_1x2": "best_source_fallback"},
        "default_strategy": "simple_average",
        "source_priority": ["s1"],
    }

    ensembler = RuleBasedHybridEnsembler(config=config)
    output = ensembler.combine(input_rec)

    assert output.status == "success"
    assert "best_source_fallback" in output.ensemble_name
