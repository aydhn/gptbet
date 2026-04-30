from sports_signal_bot.staged_channels.retirements import detect_retirement_conditions
from sports_signal_bot.staged_channels.supersession import record_supersession

def test_retirement():
    assert detect_retirement_conditions({"error_rate": 0.6}) is True
    assert detect_retirement_conditions({"error_rate": 0.1}) is False

def test_supersession():
    result = record_supersession("old_c", "new_c")
    assert result["superseded_candidate"] == "old_c"
    assert result["superseding_candidate"] == "new_c"
