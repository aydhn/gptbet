from src.sports_signal_bot.geo_quorum_hardening.quorum_drills import build_regional_quorum_drill

def test_build_regional_quorum_drill_healthy():
    inputs = {
        "explicit_evidence": True,
        "stale_member_present": False,
        "unresolved_residue": False
    }
    record = build_regional_quorum_drill(inputs)
    assert record.quorum_status == "quorum_verified"

def test_build_regional_quorum_drill_caveated():
    inputs = {
        "explicit_evidence": False,
        "stale_member_present": False,
        "unresolved_residue": False
    }
    record = build_regional_quorum_drill(inputs)
    assert record.quorum_status == "quorum_caveated"
