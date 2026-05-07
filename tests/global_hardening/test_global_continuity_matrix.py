from sports_signal_bot.global_hardening.contracts import RegionalQuorumMeshRecord, PlanetaryCoverageSynthesisRecord, GlobalContinuityDrillRecord, CrossRegionRecoveryGovernanceRecord, GlobalResilienceBudgetsRecord
from sports_signal_bot.global_hardening.integration import build_global_continuity_matrix, summarize_global_continuity_matrix
from sports_signal_bot.global_hardening.quorum_meshes import build_regional_quorum_mesh
from sports_signal_bot.global_hardening.planetary_coverage import build_planetary_coverage_synthesis
from sports_signal_bot.global_hardening.continuity_drills import build_global_continuity_drill
from sports_signal_bot.global_hardening.recovery_governance import build_cross_region_recovery_governance
from sports_signal_bot.global_hardening.budgets import build_global_resilience_budgets

def test_global_continuity_matrix():
    mesh = build_regional_quorum_mesh("m1", "bounded_regional_quorum_mesh")
    cov = build_planetary_coverage_synthesis("s1", "global_follow_the_sun_synthesis")
    drill = build_global_continuity_drill("d1", "global_quorum_loss_drill")
    gov = build_cross_region_recovery_governance("g1", "regional_recovery_governance")
    budgets = build_global_resilience_budgets("b1")

    matrix = build_global_continuity_matrix([mesh], [cov], [drill], [gov], [budgets])
    summary = summarize_global_continuity_matrix(matrix)

    assert summary["mesh_verified_count"] == 1
    assert summary["overall_health"] == "verified"
