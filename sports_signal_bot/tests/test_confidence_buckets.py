import pandas as pd
import pytest

from sports_signal_bot.evaluation.confidence import build_confidence_buckets


def test_build_confidence_buckets():
    df = pd.DataFrame(
        {
            "true_label": [1, 0, 1, 0],
            "predicted_class": [1, 1, 1, 0],
            "prob_0": [0.1, 0.4, 0.4, 0.9],
            "prob_1": [0.9, 0.6, 0.6, 0.1],
        }
    )

    buckets = build_confidence_buckets(
        df, proba_cols=["prob_0", "prob_1"], labels=[0, 1]
    )

    assert len(buckets) > 0
    # The [0.9-1.0) bucket should have 2 items (prob_1=0.9, prob_0=0.9)
    high_conf = next((b for b in buckets if b.bucket_max >= 0.9 and b.count > 0), None)
    assert high_conf is not None
    assert high_conf.count == 2
    assert high_conf.accuracy == 1.0  # 1 is correct (1), 0 is correct (0)
