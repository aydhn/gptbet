from sports_signal_bot.sovereign_corridors.translations import replay_border_translation, detect_translation_drift

def test_replay_and_drift():
    replay = replay_border_translation({})
    assert replay.outcome == "replay_matched"

    drift = detect_translation_drift({"rule": "A"}, {"rule": "B"})
    assert drift is True

    no_drift = detect_translation_drift({"rule": "A"}, {"rule": "A"})
    assert no_drift is False
