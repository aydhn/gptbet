import pytest
import pandas as pd
from pathlib import Path
from sports_signal_bot.evaluation.loader import load_evaluation_dataframe, extract_probability_columns

def test_extract_probability_columns():
    df = pd.DataFrame({
        "event_id": [1],
        "prob_home_win": [0.5],
        "prob_draw": [0.3],
        "prob_away_win": [0.2]
    })

    cols = extract_probability_columns(df, ["home_win", "draw", "away_win"])
    assert len(cols) == 3
    assert "prob_home_win" in cols

def test_load_evaluation_dataframe_empty():
    df = load_evaluation_dataframe([])
    assert df.empty
