from sports_signal_bot.endurance_hardening.regressions import detect_long_horizon_regressions

def test_detect_long_horizon_regressions():
    res = detect_long_horizon_regressions()
    assert len(res) == 0
