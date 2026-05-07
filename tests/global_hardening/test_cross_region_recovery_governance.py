from sports_signal_bot.global_hardening.contracts import CrossRegionRecoveryGovernanceRecord, GovernanceGapRecord
from sports_signal_bot.global_hardening.recovery_governance import build_cross_region_recovery_governance, detect_cross_region_governance_gaps

def test_governance_ambiguity():
    gov = build_cross_region_recovery_governance("g1", "regional_recovery_governance")
    gap = GovernanceGapRecord(gap_id="g1", description="ambiguous")
    detect_cross_region_governance_gaps(gov, gap)

    assert gov.governance_status == "governance_gapped"
    assert len(gov.warnings) > 0
