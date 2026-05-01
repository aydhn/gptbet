from src.sports_signal_bot.public_verification_gateway.readiness import compute_public_gateway_readiness

def test_readiness_scoring():
    # 0 entries -> internal_only
    summary = compute_public_gateway_readiness("g1", [], 0, {})
    assert summary.readiness_score == "internal_only"

    # Good metrics -> ready
    summary = compute_public_gateway_readiness("g1", ["e1"], 0, {"malformed_intake_rate": 0.05})
    assert summary.readiness_score == "public_style_gateway_ready"
