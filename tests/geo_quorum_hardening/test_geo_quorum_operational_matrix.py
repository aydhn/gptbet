from src.sports_signal_bot.geo_quorum_hardening.summaries import build_geo_quorum_operational_matrix

def test_build_geo_quorum_operational_matrix():
    matrix = build_geo_quorum_operational_matrix({})
    assert matrix["status"] == "built"
