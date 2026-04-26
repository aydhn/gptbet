import pytest

from sports_signal_bot.probabilistic.basketball.registry import (
    BASKETBALL_MODEL_REGISTRY,
)


def test_sample_preview_pipeline():
    model = BASKETBALL_MODEL_REGISTRY.get_model("basketball_normal_baseline")

    features = {
        "base_total_points": 210.0,
        "home_advantage_points": 2.5,
        "rating_diff": 5.0,
    }

    records = model.predict("test_event", features)

    assert len(records) > 0

    ml_record = next(r for r in records if r.market_type == "moneyline")
    assert "home_win" in ml_record.predicted_probabilities

    ou_record = next(r for r in records if r.market_type.startswith("total_"))
    assert "over" in ou_record.predicted_probabilities

    spread_record = next(r for r in records if r.market_type.startswith("spread_"))
    assert "home_cover" in spread_record.predicted_probabilities
