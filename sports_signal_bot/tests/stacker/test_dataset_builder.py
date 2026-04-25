from sports_signal_bot.stacker.dataset import MetaDatasetBuilder
from sports_signal_bot.ensemble.contracts import StandardizedPredictionRecord
from sports_signal_bot.stacker.contracts import MetaTrainingDataset

def test_meta_dataset_builder():
    config = {
        "enabled_sources": ["model_A", "model_B"],
        "use_only_calibrated_sources": True,
        "include_disagreement_features": True
    }
    builder = MetaDatasetBuilder(config)

    # Mock data
    preds = [
        StandardizedPredictionRecord(
            event_id="e1", sport="football", market_type="1x2",
            source_family="ml", source_name="model_A",
            class_labels=["home", "draw", "away"],
            probabilities={"home": 0.5, "draw": 0.3, "away": 0.2},
            predicted_class="home",
            is_calibrated=True
        ),
        StandardizedPredictionRecord(
            event_id="e1", sport="football", market_type="1x2",
            source_family="ml", source_name="model_B",
            class_labels=["home", "draw", "away"],
            probabilities={"home": 0.4, "draw": 0.4, "away": 0.2},
            predicted_class="home",
            is_calibrated=True
        )
    ]

    target_labels = {"e1": "home"}
    class_labels = ["home", "draw", "away"]

    dataset = builder.build_meta_dataset(
        preds, target_labels, class_labels, "football", "1x2"
    )

    assert isinstance(dataset, MetaTrainingDataset)
    assert len(dataset.records) == 1

    record = dataset.records[0]
    assert record.target_class_name == "home"
    assert record.target_class_index == 0
    assert "model_A_prob_home" in record.source_probabilities
    assert "model_B_prob_home" in record.source_probabilities
    assert "std_prob_home" in record.agreement_features
    assert "model_A_max_prob" in record.confidence_features
