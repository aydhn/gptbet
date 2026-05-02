from sports_signal_bot.assurance_exchange.quarantine import quarantine_assurance_packet, decide_quarantine_release

def test_quarantine_paths():
    q = quarantine_assurance_packet("q_1", "p_1", "reason")
    assert q.status == "active"

    assert decide_quarantine_release(q, False) is False
    assert decide_quarantine_release(q, True) is True
    assert q.status == "released"
