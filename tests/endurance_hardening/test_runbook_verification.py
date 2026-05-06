from sports_signal_bot.endurance_hardening.runbooks import build_runbook_record

def test_build_runbook_record():
    rb = build_runbook_record("rb_1", "test_family")
    assert rb.runbook_id == "rb_1"
    assert rb.runbook_status == "runbook_blocked"
