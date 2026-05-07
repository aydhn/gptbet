from src.sports_signal_bot.supermesh_hardening.observatory_replays import replay_handoff_observatory, diff_handoff_observatory_replay
from src.sports_signal_bot.supermesh_hardening.contracts import HandoffObservatoryReplayRecord

def test_stale_replay_fails():
    replay = HandoffObservatoryReplayRecord(replay_id="r1", is_stale=True)
    assert not replay_handoff_observatory(replay)
    diffs = diff_handoff_observatory_replay(replay)
    assert "Stale replay" in diffs

def test_missing_no_safe_fails():
    replay = HandoffObservatoryReplayRecord(replay_id="r1", no_safe_preserved=False)
    assert not replay_handoff_observatory(replay)
    diffs = diff_handoff_observatory_replay(replay)
    assert "No-safe visibility lost in replay" in diffs

def test_missing_sovereignty_fails():
    replay = HandoffObservatoryReplayRecord(replay_id="r1", sovereignty_preserved=False)
    assert not replay_handoff_observatory(replay)
    diffs = diff_handoff_observatory_replay(replay)
    assert "Sovereignty visibility lost in replay" in diffs
