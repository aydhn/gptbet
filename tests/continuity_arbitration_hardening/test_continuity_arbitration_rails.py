from src.sports_signal_bot.continuity_arbitration_hardening.contracts import ArbitrationRailEvidenceRecord
from src.sports_signal_bot.continuity_arbitration_hardening.arbitration_rails import build_continuity_arbitration_rail

def test_build_continuity_arbitration_rail_fresh():
    evidence = [ArbitrationRailEvidenceRecord(evidence_id="1", is_fresh=True, evidence_type="test")]
    rail = build_continuity_arbitration_rail("test_rail", evidence)
    assert rail.rail_status == "rail_verified"
    assert len(rail.warnings) == 0

def test_build_continuity_arbitration_rail_stale():
    evidence = [ArbitrationRailEvidenceRecord(evidence_id="1", is_fresh=False, evidence_type="test")]
    rail = build_continuity_arbitration_rail("test_rail", evidence)
    assert rail.rail_status == "rail_caveated"
    assert "Stale evidence detected" in rail.warnings[0]
