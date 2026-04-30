import pytest
from sports_signal_bot.candidate_promotion.bundles import build_candidate_bundle, compute_bundle_risk
from sports_signal_bot.candidate_promotion.contracts import CandidateReleaseRecord
from sports_signal_bot.simulation.contracts import RiskLevel

def test_build_bundle():
    cand1 = CandidateReleaseRecord(
        candidate_release_id="c1", suggestion_id="s1", patch_id="p1", tournament_ref="t1",
        target_component_family="threshold", scope={}, risk_level=RiskLevel.LOW, support_strength=0.9, confidence_band="high"
    )
    cand2 = CandidateReleaseRecord(
        candidate_release_id="c2", suggestion_id="s2", patch_id="p2", tournament_ref="t1",
        target_component_family="threshold", scope={}, risk_level=RiskLevel.MEDIUM, support_strength=0.9, confidence_band="high"
    )
    bundle = build_candidate_bundle([cand1, cand2], "threshold")
    assert len(bundle.included_candidate_ids) == 2
    assert "c1" in bundle.included_candidate_ids

    risk = compute_bundle_risk(bundle, [cand1, cand2])
    assert risk == "medium"
