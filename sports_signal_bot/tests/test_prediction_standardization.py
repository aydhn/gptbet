from sports_signal_bot.ensemble.contracts import StandardizedPredictionRecord
from sports_signal_bot.ensemble.standardize import standardize_prediction

def test_standardize_prediction():
    record = standardize_prediction(
        event_id="e1",
        sport="football",
        market_type="1x2",
        source_family="ml_raw",
        source_name="logistic_regression",
        class_labels=["1", "X", "2"],
        probabilities={"1": 0.5, "X": 0.3, "2": 0.2},
        predicted_class="1"
    )

    assert isinstance(record, StandardizedPredictionRecord)
    assert record.event_id == "e1"
    assert record.sport == "football"
    assert record.market_type == "1x2"
    assert record.source_family == "ml_raw"
    assert record.source_name == "logistic_regression"
    assert record.class_labels == ["1", "X", "2"]
    assert record.probabilities == {"1": 0.5, "X": 0.3, "2": 0.2}
    assert record.predicted_class == "1"
    assert record.is_calibrated is False
