from sports_signal_bot.global_hardening.contracts import PlanetaryCoverageSynthesisRecord, CoverageGapRecord
from sports_signal_bot.global_hardening.planetary_coverage import build_planetary_coverage_synthesis, verify_planetary_coverage_handoff

def test_planetary_coverage_gap():
    synthesis = build_planetary_coverage_synthesis("s1", "global_follow_the_sun_synthesis")
    gap = CoverageGapRecord(gap_id="g1", duration_minutes=30)
    verify_planetary_coverage_handoff(synthesis, gap)

    assert synthesis.synthesis_status == "coverage_gapped"
    assert len(synthesis.warnings) > 0
