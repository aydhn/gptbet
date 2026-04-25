import pytest
import pandas as pd
from pathlib import Path
import tempfile
from sports_signal_bot.evaluation.runner import EvaluationRunner
from sports_signal_bot.evaluation.registry import EvaluationRegistry

def test_evaluation_runner():
    # Setup mock data
    df = pd.DataFrame({
        "event_id": ["e1", "e2", "e1", "e2"],
        "sport": ["football", "football", "football", "football"],
        "market_type": ["1x2", "1x2", "1x2", "1x2"],
        "source_name": ["A", "A", "B", "B"],
        "source_family": ["ml", "ml", "benchmark", "benchmark"],
        "true_label": ["home_win", "away_win", "home_win", "away_win"],
        "predicted_class": ["home_win", "away_win", "away_win", "home_win"],
        "prob_home_win": [0.6, 0.4, 0.4, 0.6],
        "prob_draw": [0.2, 0.2, 0.2, 0.2],
        "prob_away_win": [0.2, 0.4, 0.4, 0.2],
        "prediction_status": ["valid", "valid", "valid", "valid"]
    })

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        data_path = tmp_path / "mock_data.csv"
        df.to_csv(data_path, index=False)

        registry = EvaluationRegistry()
        registry.register_source("A", "ml", data_path)
        registry.register_source("B", "benchmark", data_path)

        config = {
            "same_sample_only": True,
            "primary_metric": "log_loss",
            "secondary_metrics": ["brier"],
            "include_pairwise_comparisons": True
        }

        runner = EvaluationRunner(registry, tmp_path / "runs", config)
        manifest = runner.run("football", "1x2", ["home_win", "draw", "away_win"])

        assert manifest is not None
        assert manifest.sport == "football"
        assert manifest.market_type == "1x2"
        assert len(manifest.sources_evaluated) == 2
        assert manifest.common_universe_size == 2

        # Check files exist
        assert Path(manifest.leaderboard_path).exists()
        assert Path(manifest.comparison_table_path).exists()
