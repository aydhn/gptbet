from sports_signal_bot.providers.normalization import normalize_provider_field_aliases


def test_fixtures_normalization():
    raw = {"start_time": "2026-01-01", "home": "A", "away": "B"}
    mapping = {"start_time": "kickoff_time", "home": "home_team", "away": "away_team"}
    norm = normalize_provider_field_aliases(raw, mapping)
    assert "kickoff_time" in norm
    assert norm["home_team"] == "A"
