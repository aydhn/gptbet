from sports_signal_bot.endurance_hardening.visibility_matrix import build_long_run_visibility_matrix, summarize_visibility_matrix

def test_build_long_run_visibility_matrix():
    matrix = build_long_run_visibility_matrix()
    res = summarize_visibility_matrix(matrix)
    assert res["status"] == "healthy"
