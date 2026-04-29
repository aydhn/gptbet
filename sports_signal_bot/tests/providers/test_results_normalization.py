from sports_signal_bot.providers.normalization import normalize_provider_field_aliases


def test_results_normalization():
    raw = {"h_score": 1, "a_score": 2}
    mapping = {"h_score": "home_score", "a_score": "away_score"}
    norm = normalize_provider_field_aliases(raw, mapping)
    assert norm["home_score"] == 1
    assert norm["away_score"] == 2
