import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from sports_signal_bot.training.contracts import FoldManifest
from sports_signal_bot.training.manifests import generate_manifest


def test_generate_manifest(tmp_path):
    output_file = tmp_path / "manifest.json"

    fold1 = FoldManifest(
        fold_id="holdout_1",
        train_start="2024-01-01",
        train_end="2024-01-02",
        valid_start="2024-01-03",
        valid_end="2024-01-04",
        train_rows=100,
        valid_rows=20,
        metrics={"log_loss": 0.69},
    )

    manifest = generate_manifest(
        run_id="test_run_123",
        sport="test_sport",
        market_type="test_market",
        label_name="test_label",
        model_name="logistic",
        split_strategy="holdout",
        total_train_rows=100,
        total_valid_rows=20,
        feature_count=10,
        feature_list_path="/fake/path",
        model_artifact_path="/fake/path2",
        metrics_summary={"log_loss": 0.69},
        fold_manifests=[fold1],
        warnings=[],
        seed=42,
        config_snapshot={"some_key": "some_val"},
        started_at_utc="2024-01-01T00:00:00Z",
        output_path=str(output_file),
    )

    assert manifest.run_id == "test_run_123"
    assert manifest.sport == "test_sport"
    assert len(manifest.fold_manifests) == 1

    assert output_file.exists()

    with open(output_file, "r") as f:
        data = json.load(f)
        assert data["run_id"] == "test_run_123"
        assert data["model_name"] == "logistic"
