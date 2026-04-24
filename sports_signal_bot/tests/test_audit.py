import pytest
from datetime import datetime, timedelta
from sports_signal_bot.audit.leakage import detect_post_event_snapshot_leakage
from sports_signal_bot.benchmark.bookmaker_implied import decimal_odds_to_implied_prob, normalize_overround

def test_detect_leakage():
    event_start = datetime(2024, 3, 1, 15, 0, 0)
    pre_match_ts = event_start - timedelta(hours=1)
    post_match_ts = event_start + timedelta(hours=1)

    audit_pass = detect_post_event_snapshot_leakage(event_start, pre_match_ts, "1", "1x2")
    assert audit_pass.audit_status == "pass"

    audit_fail = detect_post_event_snapshot_leakage(event_start, post_match_ts, "1", "1x2")
    assert audit_fail.audit_status == "fail"

def test_implied_prob():
    assert decimal_odds_to_implied_prob(2.0) == 0.5
    assert decimal_odds_to_implied_prob(0.5) == 0.0 # Error case fallback

def test_normalize_overround():
    probs = {"home": 0.5, "away": 0.6} # Overround
    norm = normalize_overround(probs)
    assert abs(sum(norm.values()) - 1.0) < 0.0001
    assert norm["home"] < 0.5
