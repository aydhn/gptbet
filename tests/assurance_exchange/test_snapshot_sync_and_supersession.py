from sports_signal_bot.assurance_exchange.sync import build_registry_snapshot, compare_snapshots_for_drift

def test_snapshot_drift():
    s1 = build_registry_snapshot("s1", "r1", "man", ["a"])
    s2 = build_registry_snapshot("s2", "r1", "man", ["a", "b"])

    drift = compare_snapshots_for_drift(s1, s2)
    assert len(drift) > 0
