import pytest
import pandas as pd
from sports_signal_bot.evaluation.pairwise import compute_pairwise_comparison

def test_compute_pairwise_comparison():
    df = pd.DataFrame({
        "event_id": ["e1", "e2", "e1", "e2"],
        "source_name": ["A", "A", "B", "B"],
        "true_label": ["home_win", "away_win", "home_win", "away_win"],
        "predicted_class": ["home_win", "away_win", "away_win", "home_win"],
        # Provide probas in alphabetical order of labels ("away_win", "home_win") to please sklearn
        # or use the appropriate columns. Let's just fix the test to match lexicographical order.
        "prob_away_win": [0.4, 0.6, 0.6, 0.4],
        "prob_home_win": [0.6, 0.4, 0.4, 0.6]
    })

    result = compute_pairwise_comparison(
        df, "A", "B",
        proba_cols=["prob_away_win", "prob_home_win"],
        labels=["away_win", "home_win"]
    )

    assert result is not None
    assert result.common_event_count == 2
    assert result.better_on_common_universe == "A"  # A gets it right, B gets it wrong
