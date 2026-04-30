from sports_signal_bot.handoff.reporting import generate_handoff_summary

def test_generate_handoff_summary():
    results = [
        {"decision": "approve_handoff"},
        {"decision": "hold_for_more_evidence"},
        {"decision": "reject_handoff"},
        {"decision": "kill_candidate_before_handoff"}
    ]
    summary = generate_handoff_summary(results)
    assert summary.total_candidates_evaluated == 4
    assert summary.approve_count == 1
    assert summary.hold_count == 1
    assert summary.reject_count == 1
    assert summary.kill_count == 1
