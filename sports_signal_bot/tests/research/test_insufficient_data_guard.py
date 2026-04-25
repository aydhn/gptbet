import datetime

from sports_signal_bot.research.contracts import WindowDefinition
from sports_signal_bot.research.windows import (
    decide_skip_or_degrade, validate_window_data_sufficiency)


def test_data_guard():
    w1 = WindowDefinition(
        period_id=1,
        train_start=datetime.date(2023, 1, 1),
        train_end=datetime.date(2023, 1, 31),
        forward_start=datetime.date(2023, 2, 1),
        forward_end=datetime.date(2023, 2, 10),
    )

    suff = validate_window_data_sufficiency(w1, 10, 0, 10, 100)
    assert suff["is_sufficient"] is False

    dec1 = decide_skip_or_degrade(suff, True)
    assert dec1 == "skip"

    dec2 = decide_skip_or_degrade(suff, False)
    assert dec2 == "proceed_with_warnings"
