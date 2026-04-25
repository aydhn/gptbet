from sports_signal_bot.research.stability import (detect_performance_drop,
                                                  summarize_period_deltas)


def test_deltas():
    prev = {"log_loss": 0.6, "accuracy": 0.55}
    curr = {"log_loss": 0.65, "accuracy": 0.50}

    deltas = summarize_period_deltas(prev, curr)

    assert abs(deltas["log_loss"] - 0.05) < 1e-5
    assert abs(deltas["accuracy"] - (-0.05)) < 1e-5

    assert detect_performance_drop(deltas, "log_loss", 0.04) is True
    assert detect_performance_drop(deltas, "accuracy", 0.04) is True
    assert detect_performance_drop(deltas, "log_loss", 0.1) is False
