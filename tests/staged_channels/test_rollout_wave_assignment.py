from sports_signal_bot.staged_channels.waves import build_rollout_wave, validate_wave_coherence

def test_wave_assignment():
    wave = build_rollout_wave(["c1", "c2"], "shadow", {"max": 5})
    assert validate_wave_coherence(wave) is True
    assert wave.target_channel == "shadow"

    empty_wave = build_rollout_wave([], "shadow", {})
    assert validate_wave_coherence(empty_wave) is False
