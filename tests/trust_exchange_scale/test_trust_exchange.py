from sports_signal_bot.trust_exchange_scale.integration import run_trust_exchange_scale_pass

def test_trust_exchange_scale_pass():
    result = run_trust_exchange_scale_pass()
    assert result["overall_health"] in ["healthy", "caution", "degraded"]
    assert "overlay_exchange_packet" in result
    assert "scaled_mesh" in result
    assert "signal_ecosystem" in result
    assert "baselines" in result
    assert "controller_actions" in result

    # Check specifics
    assert result["scaled_mesh"]["health_status"] in ["healthy", "degraded"]
    assert len(result["signal_ecosystem"]["suppression_refs"]) == 1 # one stale signal
    assert any(b["baseline_status"] == "drifted" for b in result["baselines"])
