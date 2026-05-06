from sports_signal_bot.operational_hardening.disaster_recovery import build_disaster_recovery_rehearsal

def test_build_disaster_recovery_rehearsal():
    rehearsal = build_disaster_recovery_rehearsal("archive_restore_rehearsal")
    assert rehearsal.rehearsal_family == "archive_restore_rehearsal"
    assert rehearsal.rehearsal_status == "recovery_rehearsed_honestly"
