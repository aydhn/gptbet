from sports_signal_bot.verifier_portal.readiness import compute_verifier_experience_readiness, score_portal_maturity

def test_compute_verifier_experience_readiness():
    components = {"c1": True, "c2": True}
    assert compute_verifier_experience_readiness(components) == "public_style_verification_experience_ready"

    components = {"c1": True, "c2": False}
    assert compute_verifier_experience_readiness(components) == "verifier_portal_ready"

    components = {"c1": False, "c2": False}
    assert compute_verifier_experience_readiness(components) == "internal_preview_only"

def test_score_portal_maturity():
    components = {"c1": True, "c2": True}
    assert score_portal_maturity(components) == 100

    components = {"c1": True, "c2": False}
    assert score_portal_maturity(components) == 50
