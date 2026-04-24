from sports_signal_bot.ensemble.contracts import StandardizedPredictionRecord
from sports_signal_bot.ensemble.policies import apply_calibrated_preference_policy

def test_apply_calibrated_preference_policy():
    preds = [
        StandardizedPredictionRecord(
            event_id="e1", sport="f", market_type="m", source_family="f1", source_name="s1",
            class_labels=["A", "B"], probabilities={"A": 0.5, "B": 0.5}, predicted_class="A",
            is_calibrated=False
        ),
        StandardizedPredictionRecord(
            event_id="e1", sport="f", market_type="m", source_family="f1", source_name="s1",
            class_labels=["A", "B"], probabilities={"A": 0.6, "B": 0.4}, predicted_class="A",
            is_calibrated=True
        ),
        StandardizedPredictionRecord(
            event_id="e1", sport="f", market_type="m", source_family="f2", source_name="s2",
            class_labels=["A", "B"], probabilities={"A": 0.3, "B": 0.7}, predicted_class="B",
            is_calibrated=False
        )
    ]

    # prefer calibrated: s1 should be calibrated, s2 should be raw
    res = apply_calibrated_preference_policy(preds, "prefer_calibrated")
    assert len(res) == 2
    for p in res:
        if p.source_name == "s1":
            assert p.is_calibrated is True
        elif p.source_name == "s2":
            assert p.is_calibrated is False

    # calibrated only: only s1 calibrated
    res_cal = apply_calibrated_preference_policy(preds, "calibrated_only")
    assert len(res_cal) == 1
    assert res_cal[0].source_name == "s1"

    # raw only: s1 raw, s2 raw
    res_raw = apply_calibrated_preference_policy(preds, "raw_only")
    assert len(res_raw) == 2
    for p in res_raw:
         assert p.is_calibrated is False
