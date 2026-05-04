from sports_signal_bot.ecosystem_resilience.overlays import build_federation_trust_overlay

def test_build_federation_trust_overlay():
    overlay = build_federation_trust_overlay(
        overlay_id="o1",
        overlay_family="federated_registry_trust_overlay",
        target_scope_ref="scope1",
        source_registry_refs=["reg1"],
        source_hub_refs=["hub1"],
        dimension_scores={"currentness_integrity": 0.9, "attestation_validity_coverage": 0.85},
        sovereignty_deny=False,
        is_stale=False
    )
    assert overlay.final_overlay_score == 0.875
    assert overlay.final_overlay_band == "strong_bounded_signal"

def test_build_overlay_with_sovereignty_deny():
    overlay = build_federation_trust_overlay(
        overlay_id="o2",
        overlay_family="federated_registry_trust_overlay",
        target_scope_ref="scope2",
        source_registry_refs=["reg2"],
        source_hub_refs=["hub2"],
        dimension_scores={"currentness_integrity": 0.9},
        sovereignty_deny=True,
        is_stale=False
    )
    assert overlay.final_overlay_score == 0.0
    assert overlay.final_overlay_band == "highly_fragile"
