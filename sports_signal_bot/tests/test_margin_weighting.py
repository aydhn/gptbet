import pytest
from sports_signal_bot.ratings.margin import get_margin_multiplier

def test_margin_no_margin():
    assert get_margin_multiplier("no_margin", 5, 0) == 1.0

def test_margin_log():
    # log(4) approx 1.38
    m = get_margin_multiplier("log_margin", 3, 0)
    assert m > 1.3 and m < 1.4

def test_margin_capped():
    m1 = get_margin_multiplier("capped_margin", 10, 0, cap=5)
    m2 = get_margin_multiplier("capped_margin", 20, 0, cap=5)
    assert m1 == m2 # capped

def test_margin_football_default():
    assert get_margin_multiplier("football_default", 1, 0) == 1.0
    assert get_margin_multiplier("football_default", 2, 0) == 1.5
    assert get_margin_multiplier("football_default", 3, 0) == 14.0/8.0

def test_margin_basketball_default():
    m1 = get_margin_multiplier("basketball_default", 5, 0)
    m2 = get_margin_multiplier("basketball_default", 15, 0)
    assert m2 > m1 # larger margin = larger mult

    # Cap works
    m_cap = get_margin_multiplier("basketball_default", 40, 0, cap=20)
    m_uncap = get_margin_multiplier("basketball_default", 40, 0, cap=None)
    assert m_uncap > m_cap
