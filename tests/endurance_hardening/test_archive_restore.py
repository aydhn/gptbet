from sports_signal_bot.endurance_hardening.archive_restore import restore_archived_artifacts
from sports_signal_bot.endurance_hardening.archives import build_archive_snapshot

def test_restore_archived_artifacts():
    snap = build_archive_snapshot("snap_1", "soak_archive_snapshot")
    res = restore_archived_artifacts(snap)
    assert res.restore_id == "restore_snap_1"
    assert res.status == "restored"
