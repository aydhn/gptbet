from src.sports_signal_bot.geo_quorum_hardening.active_passive import build_active_passive_rehearsal

def test_build_active_passive_rehearsal_healthy():
    inputs = {
        "passive_stale": False,
        "unmeasured_readiness": False,
        "explicit_rollback_path": True
    }
    record = build_active_passive_rehearsal(inputs)
    assert record.rehearsal_status == "rehearsal_honest"

def test_build_active_passive_rehearsal_blocked():
    inputs = {
        "passive_stale": True,
        "unmeasured_readiness": False,
        "explicit_rollback_path": True
    }
    record = build_active_passive_rehearsal(inputs)
    assert record.rehearsal_status == "rehearsal_blocked"
