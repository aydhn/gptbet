from sports_signal_bot.staged_channels.fleets import build_candidate_fleet, detect_fleet_conflicts

def test_conflict_detection():
    fleet = build_candidate_fleet(["c1", "c2", "c3", "c4", "c5", "c6"], "Test Fleet")
    conflicts = detect_fleet_conflicts(fleet, {})
    assert len(conflicts) > 0
    assert conflicts[0].conflict_type == "capacity_warning"

def test_target_conflict():
    fleet = build_candidate_fleet(["c1", "c2"], "Target Fleet")
    meta = {
        "c1": {"target_family": "odds_processor"},
        "c2": {"target_family": "odds_processor"}
    }
    conflicts = detect_fleet_conflicts(fleet, meta)
    assert len(conflicts) == 1
    assert conflicts[0].conflict_type == "target_conflict"
    assert "c1" in conflicts[0].involved_candidates
    assert "c2" in conflicts[0].involved_candidates
