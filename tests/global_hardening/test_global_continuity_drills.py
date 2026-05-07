from sports_signal_bot.global_hardening.contracts import GlobalContinuityDrillRecord, ContinuityResidueRecord
from sports_signal_bot.global_hardening.continuity_drills import build_global_continuity_drill, record_global_continuity_residue, summarize_global_continuity_drill

def test_drill_residue():
    drill = build_global_continuity_drill("d1", "global_quorum_loss_drill")
    residue = ContinuityResidueRecord(residue_id="r1", description="unresolved")
    record_global_continuity_residue(drill, residue)
    summary = summarize_global_continuity_drill(drill)

    assert drill.drill_status == "continuity_rehearsed_with_caveats"
