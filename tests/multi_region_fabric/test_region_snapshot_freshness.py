from sports_signal_bot.multi_region_fabric.snapshots import build_region_snapshot, validate_snapshot_freshness_for_transfer

def test_build_region_snapshot():
    snap = build_region_snapshot("us-east")
    assert validate_snapshot_freshness_for_transfer(snap)
