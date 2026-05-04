from sports_signal_bot.ecosystem_resilience.overlays import build_federation_trust_overlay

def test_federated_currentness_effects():
    overlay = build_federation_trust_overlay(
        overlay_id="o1",
        overlay_family="federated",
        target_scope_ref="scope1",
        source_registry_refs=[],
        source_hub_refs=[],
        dimension_scores={"currentness": 1.0}, # Base score is 1.0, minus penalty 0.5 = 0.5. Since it is > 0.4, band should be fragile when is_stale is True
        sovereignty_deny=False,
        is_stale=True
    )
    assert overlay.final_overlay_band == "fragile"
