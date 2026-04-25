import pandas as pd
import pytest

from sports_signal_bot.evaluation.segments import evaluate_by_segment


def test_evaluate_by_segment():
    df = pd.DataFrame(
        {
            "event_id": [f"e{i}" for i in range(20)],
            "source_family": ["ml"] * 10 + ["benchmark"] * 10,
            "true_label": ["home_win"] * 20,
            "predicted_class": ["home_win"] * 15 + ["away_win"] * 5,
        }
    )

    segments = evaluate_by_segment(df, "source_family", "A", min_rows=5)

    assert len(segments) == 2
    ml_seg = next(s for s in segments if s.segment_value == "ml")
    assert ml_seg.row_count == 10
    assert ml_seg.metrics["accuracy"] == 1.0
