from sports_signal_bot.endurance_hardening.archives import build_archive_snapshot

def test_build_archive_snapshot():
    snap = build_archive_snapshot("snap_1", "soak_archive_snapshot")
    assert snap.archive_snapshot_id == "snap_1"
    assert snap.completeness_status == "incomplete"
