import pytest
from sports_signal_bot.candidate_promotion.contracts import CandidateManifest, CandidateReleaseRecord
from sports_signal_bot.simulation.contracts import RiskLevel

def test_candidate_manifest_serialization():
    cand = CandidateReleaseRecord(
        candidate_release_id="c1", suggestion_id="s1", patch_id="p1", tournament_ref="t1",
        target_component_family="threshold", scope={}, risk_level=RiskLevel.LOW, support_strength=0.9, confidence_band="high"
    )
    manifest = CandidateManifest(
        manifest_id="m1",
        candidates=[cand],
        decisions=[],
        readiness=[]
    )
    j = manifest.model_dump_json()
    assert "m1" in j
    assert "c1" in j
