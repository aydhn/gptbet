from sports_signal_bot.handoff.contracts import HandoffCandidateRecord, ReadinessBand

def test_handoff_candidate_record_creation():
    record = HandoffCandidateRecord(
        handoff_candidate_id="c_1",
        candidate_release_id="r_1",
        target_component_family="nba_spread",
        current_channel="live_like_safe_channel",
        current_stage="live_like_safe_verified"
    )
    assert record.target_component_family == "nba_spread"
    assert record.readiness_band == ReadinessBand.WARN
