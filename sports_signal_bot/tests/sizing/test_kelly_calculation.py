import pytest
from sports_signal_bot.sizing.kelly import compute_full_kelly_fraction, compute_fractional_kelly, explain_kelly_estimate

def test_full_kelly_standard():
    odds = 2.0  # +100, b = 1
    prob = 0.55 # 55% win rate, 5% edge
    # Kelly = (b*p - q) / b = (1*0.55 - 0.45)/1 = 0.1
    assert compute_full_kelly_fraction(odds, prob) == pytest.approx(0.1)

def test_full_kelly_negative_edge():
    odds = 2.0
    prob = 0.45 # negative edge
    assert compute_full_kelly_fraction(odds, prob) <= 0.0

def test_fractional_kelly():
    odds = 2.0
    prob = 0.55
    full = compute_full_kelly_fraction(odds, prob) # 0.1
    quarter = compute_fractional_kelly(full, 0.25)
    assert quarter == pytest.approx(0.025)

def test_explain_kelly():
    odds = 2.0
    prob = 0.55
    res = explain_kelly_estimate(odds, prob, 0.5)
    assert res.b == 1.0
    assert res.p == 0.55
    assert res.full_kelly_fraction == pytest.approx(0.1)
    assert res.fractional_kelly_fraction == pytest.approx(0.05)
    assert len(res.warnings) == 0

def test_invalid_odds():
    assert compute_full_kelly_fraction(0.5, 0.6) == 0.0
    assert compute_full_kelly_fraction(1.0, 0.6) == 0.0
