import os
from datetime import datetime, timezone

import pytest

import sports_signal_bot.calibration  # Ensure registered
from sports_signal_bot.calibration.runner import CalibrationRunner
from sports_signal_bot.training.contracts import ValidationPredictionRecord


def test_calibration_runner():
    # Setup mock data
    records = [
        ValidationPredictionRecord(
            event_id=f"e{i}",
            sport="football",
            market_type="ou_2_5",
            label_name="football_ou_2_5",
            true_class_index=i % 2,
            predicted_class=1,
            predicted_probabilities={"0": 0.3, "1": 0.7},
            model_name="test",
            fold_id="fold1",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
        )
        for i in range(10)
    ]

    config = {
        "sport": "football",
        "market_type": "ou_2_5",
        "label_name": "football_ou_2_5",
        "method": "binary_identity",
        "class_labels": ["0", "1"],
    }

    runner = CalibrationRunner(config)
    result = runner.run(records)

    assert result["status"] == "success"
    assert os.path.exists(result["output_dir"])
    assert os.path.exists(os.path.join(result["output_dir"], "manifest.json"))
    assert os.path.exists(
        os.path.join(result["output_dir"], "calibrated_predictions.jsonl")
    )
