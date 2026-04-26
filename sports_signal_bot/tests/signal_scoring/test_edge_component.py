from sports_signal_bot.signal_scoring.edge import (
    compute_edge, compute_fair_odds, normalize_market_probabilities, extract_market_implied_for_selection
)

def test_extract_market_implied():
    probs = {"home": 0.45, "draw": 0.25, "away": 0.3}
    assert extract_market_implied_for_selection("home", probs) == 0.45
    assert extract_market_implied_for_selection("draw", probs) == 0.25
    assert extract_market_implied_for_selection("unknown", probs) is None

def test_compute_edge():
    assert round(compute_edge(0.55, 0.50), 2) == 0.05
    assert round(compute_edge(0.40, 0.45), 2) == -0.05
    assert compute_edge(0.60, None) == 0.0

def test_compute_fair_odds():
    assert compute_fair_odds(0.5) == 2.0
    assert compute_fair_odds(0.2) == 5.0
    assert compute_fair_odds(0.0) is None

def test_normalize_market_probabilities():
    # 10% overround
    probs = {"home": 0.5, "draw": 0.3, "away": 0.3}
    normalized = normalize_market_probabilities(probs)
    assert sum(normalized.values()) == 1.0
    assert normalized["home"] == 0.5 / 1.1
