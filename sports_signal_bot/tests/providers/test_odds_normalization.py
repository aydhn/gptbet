from sports_signal_bot.providers.normalization import normalize_provider_field_aliases


def test_odds_normalization():
    raw = {"bookie": "1xBet", "1": 2.5, "2": 3.0}
    mapping = {"bookie": "bookmaker"}
    norm = normalize_provider_field_aliases(raw, mapping)
    assert norm["bookmaker"] == "1xBet"
