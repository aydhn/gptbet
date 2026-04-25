from sports_signal_bot.stacker.runner import StackerRunner
from sports_signal_bot.stacker.dataset import MetaDatasetBuilder
from sports_signal_bot.ensemble.contracts import StandardizedPredictionRecord

def test_stacker_runner_logistic():
    config = {
        "model_name": "meta_logistic",
        "enabled_sources": ["model_A", "model_B"],
        "use_only_calibrated_sources": True,
        "include_disagreement_features": True
    }

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
        ),
        StandardizedPredictionRecord(
            event_id="e2", sport="football", market_type="1x2",
            source_family="ml", source_name="model_A",
            class_labels=["home", "draw", "away"],
            probabilities={"home": 0.1, "draw": 0.3, "away": 0.6},
            predicted_class="away",
            is_calibrated=True
        ),
        StandardizedPredictionRecord(
            event_id="e2", sport="football", market_type="1x2",
            source_family="ml", source_name="model_B",
            class_labels=["home", "draw", "away"],
            probabilities={"home": 0.2, "draw": 0.3, "away": 0.5},
            predicted_class="away",
            is_calibrated=True
        )
    ]

    target_labels = {"e1": "home", "e2": "away"}
    class_labels = ["home", "draw", "away"]

    builder = MetaDatasetBuilder(config)
    dataset = builder.build_meta_dataset(preds, target_labels, class_labels, "football", "1x2")

    runner = StackerRunner(config)

    # Test training
    train_result = runner.train(dataset)
    assert train_result["status"] == "success"
    assert "manifest" in train_result

    # Test prediction
    predictions = runner.predict(dataset)
    assert len(predictions) == 2
    assert predictions[0].event_id == "e1"
    assert "home" in predictions[0].final_probabilities
