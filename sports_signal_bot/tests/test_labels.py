import pytest

from sports_signal_bot.labels.naming import generate_label_name


def test_generate_label_name():
    assert generate_label_name("football_1x2") == "football_1x2"
    assert generate_label_name("football_over_under", 2.5) == "football_ou_2_5"
    assert (
        generate_label_name("basketball_total_points", 220.5)
        == "basketball_total_220_5"
    )
